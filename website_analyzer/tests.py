import datetime

from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from .models import ExtendDomain, ExtendHomepage, ExtendWebpage, Token, Pieces
from .models import Sequence, StringParameter
from .analyzer_lib import string_analyst, add_url_to_webpage
from .analyzer_lib import add_list_url_to_webpage
from website_management.models import Homepage, Domain, Webpage
from webscraper.pagescraper import PageScraper


def analye_website_setup():
    "prepare data for AnalyzeWebsiteViewTest"
    dom = Domain.objects.create(name='pupil.com')
    hp = Homepage.objects.create(name='www.pupil.com', domain=dom)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    web0 = Webpage.objects.create(url='http://www.pupil.com/', homepage=hp)
    ExtendWebpage.objects.create(webpage=web0,
                                 text_body="""
                                           This is a homepage.
                                           Contain common post.
                                           this is a dummy test page.
                                           """)
    web0.save()
    web1 = Webpage.objects.create(url='http://www.pupil.com/scam', homepage=hp)
    ExtendWebpage.objects.create(webpage=web1,
                                 text_body="""
                                           This is the obviously scam webpage.
                                           From this webpage,
                                           we can safely assume
                                           that all webpage from this homepage
                                           is a scam. this is scam.
                                           """)
    web1.save()
    web2 = Webpage.objects.create(url='http://www.pupil.com/two', homepage=hp)
    ExtendWebpage.objects.create(webpage=web2,
                                 text_body="""
                                           This is also part of scam homepage.
                                           But, this page is not
                                           the definitive page.
                                           """)
    web2.save()
    StringParameter.objects.create(name='this is scam', level="1")


class ExtendDomainModelTest(TestCase):
    "Testing custom save() & clean() in model ExtendHomepage"
    def setUp(self):
        hp = Homepage.objects.create(name='www.pupil.com')
        ext = ExtendHomepage.objects.create(homepage=hp)
        ext.save()

    def test_extendhomepage_scam_value_none(self):
        ext1 = ExtendHomepage.objects.get(homepage__name='www.pupil.com')
        ext1.save()
        self.assertEqual(ext1.scam, None)
        self.assertEqual(ext1.whitelist, None)

    def test_extendhomepage_known_scam(self):
        ext2 = ExtendHomepage.objects.get(homepage__name='www.pupil.com')
        ext2.scam = True
        ext2.save()
        self.assertEqual(ext2.whitelist, False)

    def test_extendhomepage_scam_whitelist_same_value(self):
        ext3 = ExtendHomepage.objects.get(homepage__name='www.pupil.com')
        ext3.scam = True
        ext3.whitelist = True
        self.assertRaises(ValidationError, ext3.save())


class AnalystDashboardViewTest(TestCase):
    "test analyst dashboard view"
    def setUp(self):
        ppl = Homepage.objects.create(name="www.pupil.com")
        fcb = Homepage.objects.create(name="www.facebook.com")
        dtk = Homepage.objects.create(name="www.detik.com")
        kmp = Homepage.objects.create(name="www.kompas.com")
        twt = Homepage.objects.create(name="www.twitter.com")
        rpl = Homepage.objects.create(name="www.republika.co.id")
        ext = ExtendHomepage.objects.create(homepage=ppl, scam=False)
        ext.save()
        ext = ExtendHomepage.objects.create(homepage=fcb, scam=False)
        ext.save()
        ext = ExtendHomepage.objects.create(homepage=dtk, scam=True)
        ext.save()
        ext = ExtendHomepage.objects.create(homepage=kmp, scam=False)
        ext.save()
        ext = ExtendHomepage.objects.create(homepage=twt, scam=False)
        ext.save()
        ext = ExtendHomepage.objects.create(homepage=rpl)
        ext.save()

    def test_dashboard_view(self):
        "test the context rendered from view"
        web = Homepage.objects.all().count()
        exhp = ExtendHomepage.objects.all().count()
        resp = self.client.get(reverse('website_analyzer:analyst_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(web, 6)
        self.assertEqual(exhp, 6)
        self.assertTrue('hp_count' in resp.context.keys())
        self.assertEqual(resp.context['hp_count'], 6)
        self.assertTrue('scam_count' in resp.context.keys())
        self.assertEqual(resp.context['scam_count'], 1)
        self.assertTrue('whitelist_count' in resp.context.keys())
        self.assertEqual(resp.context['whitelist_count'], 4)


class AnalyzeWebsiteViewTest(TestCase):
    def test_view_website_does_not_exist(self):
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       kwargs={'hp_id': 40}))
        self.assertEqual(resp.status_code, 404)

    def test_view_website_exist_not_yet_analyzed(self):
        """context should contains: homepage hame,
        webpages (id & url) from this homepage, any matching string parameter,
        scam, report, access, whitelist, date added & domain name"""
        analye_website_setup()
        now = datetime.datetime.now()
        hp = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       kwargs={'hp_id': hp.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['name'], 'www.pupil.com')
        self.assertEqual(resp.context['scam'], None)
        self.assertEqual(resp.context['report'], None)
        self.assertEqual(resp.context['whitelist'], None)
        self.assertEqual(resp.context['date_added'], now.date())
        self.assertEqual(resp.context['report'], None)
        self.assertEqual(resp.context['inspection'], False)
        self.assertEqual(resp.context['access'], True)
        self.assertEqual(resp.context['domain'], 'pupil.com')
        self.assertEqual(len(resp.context['webpages']), 3)
        self.assertEqual(len(resp.context['params']), 0)

    def test_template_website_exist_not_yet_analyzed(self):
        """rendered template should contains: homepage hame,
        webpages (id & url) from this homepage, any matching string parameter,
        scam, report, access, whitelist, date added & domain name"""
        analye_website_setup()
        now = datetime.datetime.now()
        hp = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       kwargs={'hp_id': hp.id}))
        self.assertEqual(resp.status_code, 200)

        # pupil.com will appear in: domain, homepage + 3 webpages
        self.assertContains(resp, 'pupil.com', 5)

        # None will appear in scam, report, whitelist
        self.assertContains(resp, 'None', 3)
        self.assertContains(resp, now.strftime('%d %b %Y'), 1)

        # False will appear for inspection
        self.assertContains(resp, 'False', 1)

        # True will appear for access
        self.assertContains(resp, 'True', 1)


class StartAnalyzeTestCase(TestCase):
    "Test analyst proces execution"
    def test_view_start_analyze_website_find_sequence(self):
        analye_website_setup()
        hp = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:start_analyze',
                                       kwargs={'hp_id': hp.id}))
        self.assertEqual(resp.status_code, 302)
        string_analyst(hp.id)
        self.assertEqual(hp.extendhomepage.scam, True)
        self.assertEqual(hp.extendhomepage.whitelist, False)


class ExtractLinksTestCase(TestCase):
    def setUp(self):
        add_url_to_webpage('http://www.pupil.com/scam')
        web = Webpage.objects.get(url='http://www.pupil.com/scam')
        web.html_page = """
                        <html>
                        <head><title>Dummy url extract html</title></head>
                        <body>
                        <a href="http://www.ppl.com/prof">www.ppl.com</a>
                        <a href="https://www.ppl.com/prof">www.ppl.com</a>
                        <a href="/profile">www.ppl.com</a>
                        <a href="profile">www.ppl.com</a>
                        </body>
                        </html>
                        """
        web.save()

    def test_view_extract_url(self):
        "does the view realy save url inside webpage to database?"
        web = Webpage.objects.get(url='http://www.pupil.com/scam')
        resp = self.client.get(reverse('website_analyzer:extract_links',
                                       args=[web.id]))
        self.assertEqual(resp.status_code, 302)
        webs = Webpage.objects.all()
        hp = Homepage.objects.all()
        dom = Domain.objects.all()
        self.assertEqual(webs.filter(url='http://www.ppl.com/prof').count(),
                         1)
        self.assertEqual(webs.filter(url='https://www.ppl.com/prof').count(),
                         1)
        self.assertEqual(hp.filter(name='www.ppl.com').count(), 1)
        self.assertEqual(dom.filter(name='ppl.com').count(), 1)
        
