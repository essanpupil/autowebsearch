"functional tes module"
from selenium.webdriver.common.by import By

from functional_tests.base import BaseFunctionalTest
from website_analyzer.models import SearchKeywords
from website_management.models import Website, Domain


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
        blogspot = Domain.objects.create(name='blogspot.com')
        wordpress = Domain.objects.create(name='wordpress.com')
        jigdo = Domain.objects.create(name='jigdo.com')
        Website.objects.bulk_create([
            Website(name="undianbri.blogspot.com", domain=blogspot),
            Website(name="undiantelkomsel.wordpress.com", domain=wordpress),
            Website(name="undianindosat.jigdo.com", domain=jigdo)
        ])
        self.browser.find_element(By.LINK_TEXT, 'View all websites').click()
        self.check_for_cell_in_table('table_websites',
                                     'undianbri.blogspot.com')
        self.check_for_cell_in_table('table_websites',
                                     'undiantelkomsel.wordpress.com')
        self.check_for_cell_in_table('table_websites',
                                     'undianindosat.jigdo.com')

    def test_view_all_keywords(self):
        "click link to view all keywords"
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.assertIn('View all keywords', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('View all keywords', header_text)

    def test_table_keywords_content(self):
        "does the keywords data table loaded?"
        SearchKeywords.objects.bulk_create([
            SearchKeywords(keywords='Pemenang undian palsu'),
            SearchKeywords(keywords='Hubungi nomor ini'),
            SearchKeywords(keywords='Ikuti petunjuk kami'),
        ])
        self.browser.find_element(By.LINK_TEXT, 'View all keywords').click()
        self.check_for_cell_in_table('table_keywords', 'Pemenang undian palsu')
        self.check_for_cell_in_table('table_keywords', 'Hubungi nomor ini')
        self.check_for_cell_in_table('table_keywords', 'Ikuti petunjuk kami')

    def test_click_login(self):
        "does the login page works?"
        self.browser.find_element(By.LINK_TEXT, 'Login').click()
        self.assertIn('Please login', self.browser.title)
