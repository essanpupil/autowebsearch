"functional tes module"
from selenium.webdriver.common.by import By

from django.contrib.auth.models import User

from functional_tests.base import BaseFunctionalTest


class LoggedInUserTest(BaseFunctionalTest):
    "testing wesite from browser point of view for logged in user"

    def test_login_user(self):
        "test user login"
        user = User(username='anderson')
        user.set_password('thejourneybegins')
        user.save()
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
