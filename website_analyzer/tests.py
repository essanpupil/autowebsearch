import datetime

from django.test import TestCase, TransactionTestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from .models import ExtendHomepage, ExtendWebpage, ExtendDomain
from .models import StringParameter
from .analyzer_lib import string_analyst, add_url_to_webpage
from .analyzer_lib import add_list_url_to_webpage
from website_management.models import Homepage, Domain, Webpage


TIME_NOW = datetime.datetime.now()


def analye_website_setup():
    """prepare data for AnalyzeWebsiteViewTest"""
    domain = Domain.objects.create(name='pupil.com')
    homepage = Homepage.objects.create(name='www.pupil.com', domain=domain)
    web0 = Webpage.objects.create(url='http://www.pupil.com/',
                                  homepage=homepage)
    ExtendWebpage.objects.create(webpage=web0,
                                 text_body="""
                                           This is a homepage.
                                           Contain common post.
                                           this is a dummy test page.
                                           """)
    web0.save()
    web1 = Webpage.objects.create(url='http://www.pupil.com/scam',
                                  homepage=homepage)
    ExtendWebpage.objects.create(webpage=web1,
                                 text_body="""
                                           This is the obviously scam webpage.
                                           From this webpage,
                                           we can safely assume
                                           that all webpage from this homepage
                                           is a scam. this is scam.
                                           """)
    web1.save()
    web2 = Webpage.objects.create(url='http://www.pupil.com/two',
                                  homepage=homepage)
    ExtendWebpage.objects.create(webpage=web2,
                                 text_body="""
                                           This is also part of scam homepage.
                                           But, this page is not
                                           the definitive page.
                                           """)
    web2.save()
    StringParameter.objects.create(sentence='this is scam', definitive=True)


def view_all_website_setup():
    """prepare data for test view all website"""
    urls = ['http://www.ppl.com/profile/',
            'http://www.ppl.com/setting/',
            'http://www.pupil.com/profile/',
            'http://www.pupil.com/profile/',
            'http://www.essanpupil.com/profile/']
    add_list_url_to_webpage(urls)


class AddScamWebsiteTestCase(WebTest):
    "testing adding known scam websites"
    def test_access_input_page(self):
        "testing the response of webpage that should display the input form"
        resp = self.app.get(reverse('website_analyzer:add_scam_website'))
        self.assertEqual(resp.status_code, 200)

        # fill the form input with url of website's homepage, then submit it
        form = resp.form
        form['url'] = 'http://www.pupil.com'
        submit_form = form.submit().follow()

        # check the new homepage url in the view_webpage
        self.assertIn('www.pupil.com', submit_form.content)


class ViewAllWebsiteTestCase(TestCase):
    "testing view: view all website in database"
    def test_view_for_empty_database_view_all_websites_testcase(self):
        """test all context throwed from view when the database is empty"""
        resp = self.client.get(reverse('website_analyzer:view_websites'))
        self.assertEqual(resp.status_code, 200)

        # display notification of empty website data
        self.assertIn('Website database is empty', resp.content)

    def test_view_for_filled_database_view_all_website_testcase(self):
        """test all context throwed from view when the database is filled"""
        view_all_website_setup()
        resp = self.client.get(reverse('website_analyzer:view_websites'))
        self.assertEqual(resp.status_code, 200)
        # based-on setup method, we should have 3 websites
        self.assertEqual(len(resp.context['websites']), 3)
        # testing dictionary key for each list item of website
        self.assertIn('name', list(resp.context['websites'][0].keys()))
        self.assertIn('scam', list(resp.context['websites'][0].keys()))
        self.assertIn('inspection', list(resp.context['websites'][0].keys()))
        self.assertIn('report', list(resp.context['websites'][0].keys()))
        self.assertIn('access', list(resp.context['websites'][0].keys()))
        self.assertIn('web_count', list(resp.context['websites'][0].keys()))
        self.assertIn('date_added', list(resp.context['websites'][0].keys()))
        self.assertIn('domain', list(resp.context['websites'][0].keys()))
        self.assertIn('id', list(resp.context['websites'][0].keys()))

    def test_rendered_html_view_all_websites(self):
        """testing the rendered template variable"""
        view_all_website_setup()
        resp = self.client.get(reverse('website_analyzer:view_websites'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'www.pupil.com', 1)
        self.assertContains(resp, 'www.ppl.com', 1)
        self.assertContains(resp, 'www.essanpupil.com', 1)


class ExtendDomainModelTest(TestCase):
    """Testing custom save() & clean() in model ExtendHomepage"""

    def setUp(self):
        "setup dummy homepage"
        homepage = Homepage.objects.create(name='www.pupil.com')
        ext = ExtendHomepage.objects.create(homepage=homepage)
        ext.save()

    def test_extendhomepage_scam_value_none(self):
        "testing custom save() in ExtendHomepage model"
        ext1 = ExtendHomepage.objects.get(homepage__name='www.pupil.com')
        ext1.save()
        self.assertEqual(ext1.scam, None)
        self.assertEqual(ext1.whitelist, None)

    def test_extendhomepage_known_scam(self):
        "testing custom save() in ExtendHomepage model"
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
    """test analyst dashboard view"""

    def setUp(self):
        "setup dummy dashboard data"
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
        """test the context rendered from view"""
        web = Homepage.objects.all().count()
        exhp = ExtendHomepage.objects.all().count()
        resp = self.client.get(reverse('website_analyzer:analyst_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(web, 6)
        self.assertEqual(exhp, 6)
        self.assertTrue('hp_count' in list(resp.context.keys()))
        self.assertEqual(resp.context['hp_count'], 6)
        self.assertTrue('scam_count' in list(resp.context.keys()))
        self.assertEqual(resp.context['scam_count'], 1)
        self.assertTrue('whitelist_count' in list(resp.context.keys()))
        self.assertEqual(resp.context['whitelist_count'], 4)


class AnalyzeWebsiteViewTest(TestCase):
    "Testing view analyze website"
    def test_view_website_does_not_exist(self):
        "test passed context from view to template"
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       kwargs={'hp_id': 40}))
        self.assertEqual(resp.status_code, 404)

    def test_view_website_exist_not_yet_analyzed(self):
        """context should contains: homepage name,
        webpages (id & url) from this homepage, any matching string parameter,
        scam, report, access, whitelist, date added & domain name"""
        analye_website_setup()
        homepage = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       args=[homepage.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['name'], 'www.pupil.com')
        self.assertEqual(resp.context['scam'], None)
        self.assertEqual(resp.context['report'], False)
        self.assertEqual(resp.context['whitelist'], None)
        self.assertEqual(resp.context['date_added'], TIME_NOW.date())
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
        homepage = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:analyze_website',
                                       kwargs={'hp_id': homepage.id}))
        self.assertEqual(resp.status_code, 200)
        # pupil.com will appear in: domain, homepage + 3 webpages
        self.assertContains(resp, 'pupil.com', 5)
        # True will appear for access
        # self.assertContains(resp, 'True', 1)
        # make sure crawling url is the correct homepage id
        href = "/website_analyzer/crawl_website/%s/" % (homepage.id)
        self.assertContains(resp, href, 1)
        # make sure edit analyst data is the correct homepage id
        href = "/website_analyzer/edit_analyst/%s/" % (homepage.id)
        self.assertContains(resp, href, 1)


class StartAnalyzeTestCase(TestCase):
    """Test analyst proces execution"""

    def test_view_start_analyze_website_find_sequence(self):
        "Test passed context from view to template"
        analye_website_setup()
        homepage = Homepage.objects.get(name='www.pupil.com')
        resp = self.client.get(reverse('website_analyzer:start_analyze',
                                       kwargs={'hp_id': homepage.id}))
        self.assertEqual(resp.status_code, 302)
        string_analyst(homepage.id)
        self.assertEqual(homepage.extendhomepage.scam, True)
        self.assertEqual(homepage.extendhomepage.whitelist, False)


class ExtractLinksTestCase(TransactionTestCase):
    "Test extract links from webpage"
    def setUp(self):
        "setup dummy webpage"
        add_url_to_webpage('http://www.pupil.com/scam')
        webpage = Webpage.objects.get(url='http://www.pupil.com/scam')
        webpage.html_page = """
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
        webpage.save()

    def test_view_extract_url(self):
        """does the view realy save url inside webpage to database?"""
        webpage = Webpage.objects.get(url='http://www.pupil.com/scam')
        resp = self.client.get(reverse('website_analyzer:extract_links',
                                       args=[webpage.id]))
        self.assertEqual(resp.status_code, 302)
        webs = Webpage.objects.all()
        homepage = Homepage.objects.all()
        domain = Domain.objects.all()
        self.assertEqual(webs.filter(url='http://www.ppl.com/prof').count(),
                         1)
        self.assertEqual(webs.filter(url='https://www.ppl.com/prof').count(),
                         1)
        self.assertEqual(homepage.filter(name='www.ppl.com').count(), 1)
        self.assertEqual(domain.filter(name='ppl.com').count(), 1)


class AddStringParameterTestCase(WebTest):
    """test for insert string parameter to database"""

    def test_add_sequence(self):
        "Testing submit form add sequence"
        resp = self.app.get(reverse('website_analyzer:add_sequence'))
        self.assertEqual(resp.status_code, 200)
        form = resp.form

        # search form input
        form['sentence'] = 'this is a scam'
        submit_form = form.submit().follow()

        # check the new homepage url in the view_sequence
        self.assertIn('this is a scam', submit_form.content)


class ViewStringParameterTestCase(TestCase):
    """test to display all string parameter"""

    def setUp(self):
        """preparing data to test view_string_parameter"""
        StringParameter.objects.create(sentence='This is a scam',
                                       definitive=True)
        StringParameter.objects.create(sentence='scam warning',
                                       definitive=False)

    def test_context_view_empty_view_string_parameter(self):
        """test passed context when database empty"""
        resp = self.client.get(reverse('website_analyzer:view_sequence'))
        self.assertEqual(resp.status_code, 200)  # response test
        self.assertEqual(len(resp.context['parameters']), 0)

    def test_rendered_template_view_string_parameter(self):
        """test rendered html source for empty database"""
        resp = self.client.get(reverse('website_analyzer:view_sequence'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'String Parameter database is empty',
                            count=1)

    def test_context_view_non_empty_database_view_sequence(self):
        """test passed context when the database is not empty"""
        resp = self.client.get(reverse('website_analyzer:view_sequence'))
        self.assertEqual(resp.status_code, 200)  # response test
        self.assertEqual(len(resp.context['parameters']), 2)
        self.assertIn('sentence', list(resp.context['parameters'][0].keys()))
        self.assertIn('definitive', list(resp.context['parameters'][0].keys()))
        self.assertIn('date_added', list(resp.context['parameters'][0].keys()))
        self.assertEqual(resp.context['parameters'][0]['date_added'],
                         TIME_NOW.date())
        self.assertContains(resp, 'This is a scam', count=1)
        self.assertContains(resp, 'scam warning', count=1)


class EditAnalystDataTestCase(WebTest):
    """Testing the edit_analyst view"""
    def setUp(self):  # lint:ok
        domain = Domain.objects.create(name='pupil.com')
        ExtendDomain.objects.create(domain=domain)
        homepage = Homepage.objects.create(name='www.pupil.com', domain=domain)
        ExtendHomepage.objects.create(homepage=homepage)
        web0 = Webpage.objects.create(url='http://www.pupil.com/',
                                      homepage=homepage)
        ExtendWebpage.objects.create(webpage=web0,
                                     text_body="""
                                               This is a homepage.
                                               Contain common post.
                                               this is a dummy test page.
                                               """)
        web0.save()
        web1 = Webpage.objects.create(url='http://www.pupil.com/scam',
                                      homepage=homepage)
        ExtendWebpage.objects.create(webpage=web1,
                                     text_body="""
                                         This is the obviously scam webpage.
                                         From this webpage,
                                         we can safely assume
                                         that all webpage from this homepage
                                         is a scam. this is scam.
                                         """)
        web1.save()
        web2 = Webpage.objects.create(url='http://www.pupil.com/two',
                                      homepage=homepage)
        ExtendWebpage.objects.create(webpage=web2,
                                     text_body="""
                                         This is also part of scam homepage.
                                         But, this page is not
                                         the definitive page.
                                         """)
        web2.save()
        StringParameter.objects.create(sentence='this is scam',
                                       definitive=True)

    def test_website_does_not_exist(self):
        """test when user request for domain id that does not exist in
        database"""
        resp = self.client.get(reverse('website_analyzer:edit_analyst',
                                       args=[4000]))
        self.assertEqual(resp.status_code, 404)

    def test_view_edit_analyst(self):
        """test passed context for view: edit_analyst"""
        homepage = Homepage.objects.get(name='www.pupil.com')
        resp = self.app.get(reverse('website_analyzer:edit_analyst',
                                    kwargs={'homepage_id': homepage.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('homepage', resp.context.keys())
        self.assertIn('form', resp.context.keys())
        self.assertIn('id', resp.context['homepage'])
        self.assertIn('scam_status', resp.context['homepage'])
        self.assertIn('inspected', resp.context['homepage'])
        self.assertIn('reported', resp.context['homepage'])
        self.assertIn('access', resp.context['homepage'])
        self.assertIn('whitelist', resp.context['homepage'])
        self.assertEqual(resp.context['homepage']['id'], homepage.id)
        self.assertEqual(resp.context['homepage']['scam_status'],
                         homepage.extendhomepage.scam)
        self.assertEqual(resp.context['homepage']['name'],
                         homepage.name)
        self.assertEqual(resp.context['homepage']['inspected'],
                         homepage.extendhomepage.inspected)
        self.assertEqual(resp.context['homepage']['reported'],
                         homepage.extendhomepage.reported)
        self.assertEqual(resp.context['homepage']['access'],
                         homepage.extendhomepage.access)
        self.assertEqual(resp.context['homepage']['whitelist'],
                         homepage.extendhomepage.whitelist)

    def test_rendered_html_edit_analyst_form(self):
        "testing the rendered webpage of edit analyst form"
        homepage = Homepage.objects.get(name='www.pupil.com')
        resp = self.app.get(reverse('website_analyzer:edit_analyst',
                                    args=[homepage.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('scam', resp.context['form'].fields)
        self.assertIn('form', resp.context.keys())
        self.assertIn('inspected', resp.context['form'].fields)
        self.assertIn('reported', resp.context['form'].fields)
        self.assertIn('access', resp.context['form'].fields)
        self.assertIn('whitelist', resp.context['form'].fields)

    def test_submit_edit_analyst_form(self):
        "testing when the edit form is submitted"
        website = Homepage.objects.get(name='www.pupil.com')
        resp = self.app.get(reverse('website_analyzer:edit_analyst',
                                    args=[website.id]))
        self.assertEqual(resp.status_code, 200)
        form = resp.form
        form['scam'] = 'True'
        form['inspected'] = 'Inspected'
        form['reported'] = 'Reported'
