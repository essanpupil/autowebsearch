"functional tes module"
from selenium.webdriver.common.by import By

from functional_tests.base import BaseFunctionalTest


class AnonymouseUserTest(BaseFunctionalTest):
    "testing wesite from browser point of view for anonymouse user"
    def test_homepage(self):
        "this the homepage for first visitor."
        self.assertIn('Welcome to ScamSearcher Project', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('SCAM SEARCHER', header_text)

    def test_view_all_websites(self):
        "click link to view all websites"
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.assertIn('View all websites', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('View all websites', header_text)

    def test_table_websites_content(self):
        "does the websites data table loaded?"
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.assertIn('View all websites', self.browser.title)
        table_websites = self.browser.find_element(By.ID, 'table_websites')
        self.assertTrue(table_websites)

    def test_view_all_keywords(self):
        "click link to view all keywords"
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.assertIn('View all keywords', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('View all keywords', header_text)

    def test_table_keywords_content(self):
        "does the keywords data table loaded?"
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.assertIn('View all keywords', self.browser.title)
        table_websites = self.browser.find_element(By.ID, 'table_keywords')
        self.assertTrue(table_websites)

    def test_click_login(self):
        "does the login page works?"
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        self.assertIn('Please login', self.browser.title)
