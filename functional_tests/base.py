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

    def check_for_cell_in_table(self, id_table, row_text):
        table = self.browser.find_element_by_id(id_table)
        cells = table.find_elements_by_tag_name('td')
        self.assertIn(row_text, [cell.text for cell in cells])
