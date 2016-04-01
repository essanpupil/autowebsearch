"functional tes module"
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse


class FunctionalTest(StaticLiveServerTestCase):
    "testing wesite from browser point of view."
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def test_homepage(self):
        "this the homepage for first visitor."
        self.browser.get('http://localhost:8000')
        self.assertIn('Welcome to ScamSearcher Project', self.browser.title)
