"functional tes module"
from selenium import webdriver
from selenium.webdriver.common.by import By

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User


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
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('View all websites', header_text)

    def test_table_websites_content(self):
        "does the websites data table loaded?"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.assertIn('View all websites', self.browser.title)
        table_websites = self.browser.find_element(By.ID, 'table_websites')
        self.assertTrue(table_websites)

    def test_view_all_keywords(self):
        "click link to view all keywords"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.assertIn('View all keywords', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('View all keywords', header_text)

    def test_table_keywords_content(self):
        "does the keywords data table loaded?"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.assertIn('View all keywords', self.browser.title)
        table_websites = self.browser.find_element(By.ID, 'table_keywords')
        self.assertTrue(table_websites)

    def test_click_login(self):
        "does the login page works?"
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        self.assertIn('Please login', self.browser.title)

    def test_login_user(self):
        "test user login"
        user = User(username='anderson')
        user.set_password('thejourneybegins')
        user.save()
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys(user.username)
        password.send_keys("thejourneybegins")
        self.browser.find_element_by_tag_name('form').submit()
        # If this assertion fail, the login submition is failed
        self.assertIn(
            "Welcome to ScamSearcher Project {0}".format(user.username),
            self.browser.title)
