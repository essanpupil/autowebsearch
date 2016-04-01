"Testing module for website_management app."
from django.core.urlresolvers import resolve
from django.test import TestCase

from website_management.views import website_dashboard


class HomePageTest(TestCase):
    "testing homepage from website_management app."
    def test_root_url_resolves_to_welcome_views(self):
        "resolve homepage url"
        found = resolve('/')
        self.assertEqual(found.func, website_dashboard)
