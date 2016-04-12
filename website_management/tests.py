"Testing module for website_management app."
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase, Client

from website_management.views import website_dashboard
from website_management.models import Website


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

    def test_request_view_all_websites_empty_data(self):
        "Check response for view all websites"
        response = self.client.get(
            reverse('website_management:view_all_homepages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'website_management/view_all_homepages.html')

    def test_request_view_all_websites_filled_data(self):
        "Check response for view all websites"
        Website.objects.create(name='undianmkios.blogspot.com')
        response = self.client.get(
            reverse('website_management:view_all_homepages'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('homes', response.context)
        self.assertTemplateUsed(
            response, 'website_management/view_all_homepages.html')

    def test_request_view_all_keywords(self):
        "Check response for view all keywords"
        response = self.client.get(
            reverse('website_management:view_all_keywords'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'website_management/view_all_keywords.html')
