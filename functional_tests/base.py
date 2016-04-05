"functional test module"
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class BaseFunctionalTest(StaticLiveServerTestCase):
    "testing wesite from browser point of view."
    def setUp(self):
        "setup browser selenium"
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        "closing browser after test."
        self.browser.refresh()
        self.browser.quit()
