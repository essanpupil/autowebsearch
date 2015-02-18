from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from .models import ExtendDomain, ExtendHomepage, ExtendWebpage
from website_management.models import Homepage


class ExtendDomainModelTest(TestCase):
    "Testing custom save() & clean() in model ExtendHomepage"
    def setUp(self):
        hp = Homepage.objects.create(name='www.pupil.com')
        ext = ExtendHomepage.objects.create(homepage=hp)
        ext.save()

    def test_extendhomepage_scam_value_None(self):
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
        #self.assertTrue('newest_5_scam' in resp.context)
        #self.assertTrue('newest_5_whitelist' in resp.context)

    #~ def test_rendered_template_dashboard_view(self):
        #~ resp = self.client.get(reverse('website_analyzer:analyst_dashboard'))
        #~ self.assertContains(resp, 'www.pupil.com', count=1, html=True)
        #~ self.assertContains(resp, 'www.facebook.com', count=1, html=True)
        #~ self.assertContains(resp, 'www.detik.com', count=1, html=True)
        #~ self.assertContains(resp, 'www.kompas.com', count=1, html=True)
        #~ self.assertContains(resp, 'www.twitter.com', count=1, html=True)
        #~ self.asertNotContains(resp, 'www.republika.co.id', html=True)
