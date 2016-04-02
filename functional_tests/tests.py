"functional tes module"
from selenium import webdriver
from selenium.webdriver.common.by import By

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


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

    def test_view_all_websites(self):
        "click link to view all websites"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.assertIn('View all websites', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h4').text
        self.assertIn('View all websites', header_text)

    def test_table_websites_content(self):
        "does the websites data table loaded?"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.assertIn('View all websites', self.browser.title)
        table_websites = self.browser.find_element(By.ID, 'table_websites')
        self.assertTrue(table_websites)
