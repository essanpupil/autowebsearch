from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .models import ExtendDomain, ExtendHomepage, ExtendWebpage


class AnalystDashboardViewTest(WebTest):
    "test analyst dashboard view"
    def setUp(self):
        ppl = Homepage.objects.create(name="www.pupil.com")
        fcb = Homepage.objects.create(name="www.facebook.com")
        dtk = Homepage.objects.create(name="www.detik.com")
        kmp = Homepage.objects.create(name="www.kompas.com")
        twt = Homepage.objects.create(name="www.twitter.com")
        Homepage.objects.create(name="www.republika.co.id")
        ExtendHomepage(homepage=ppl, scam=False, whitelist=True)
        ExtendHomepage(homepage=fcb, scam=False, whitelist=True)
        ExtendHomepage(homepage=dtk, scam=True, whitelist=False)
        ExtendHomepage(homepage=kmp, scam=False, whitelist=True)
        ExtendHomepage(homepage=twt, scam=False, whitelist=True)

    def test_dashboard_view(self):
        "test the context rendered from view"
        resp = self.client.get(reverse('website_analyzer:analyst_dashboard'))
        self.assertEqual(resp.status_code, 200)
        
