"Testing module for website_management app."
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase, Client

from website_management.views import website_dashboard


class HomePageTest(TestCase):
    "testing homepage from website_management app."
    def test_root_url_resolves_to_welcome_views(self):
        "resolve homepage url"
        found = resolve('/')
        self.assertEqual(found.func, website_dashboard)


class HomePageResponseTest(TestCase):
    "testing homepage using http request"
    def setUp(self):
        "define default test client"
        self.client = Client()

    def test_request_homepage(self):
        "test requesting homepage"
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website_management/dashboard.html')
        self.assertIn('homepage_count', response.context)
        self.assertIn('newest_5_homepage', response.context)
