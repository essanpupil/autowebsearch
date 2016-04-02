"functional tes module"
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse


class FunctionalTest(StaticLiveServerTestCase):
    "testing wesite from browser point of view."
    def setUp(self):
        "setup browser selenium"
        self.browser = webdriver.Chrome()

    def tearDown(self):
        "closing browser after test."
        self.browser.refresh()
        self.browser.quit()

    def test_homepage(self):
        "this the homepage for first visitor."
        self.browser.get(self.live_server_url)
        self.assertIn('Welcome to ScamSearcher Project', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('SCAM SEARCHER', header_text)
