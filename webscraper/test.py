""""testing module for web scraper package."""
import unittest

from webscraper.pagescraper import PageScraper


class ExtractUrlTestCase(unittest.TestCase):
    """Test link extraction"""
    def setUp(self):
        self.html = """
                    <html>
                    <head><title>Dummy url extract html</title></head>
                    <body>
                    <a href="http://www.pupil.com/profile">www.pupil.com</a>
                    <a href="https://www.pupil.com/profile">www.pupil.com</a>
                    <a href="/profile">www.pupil.com</a>
                    <a href="profile">www.pupil.com</a>
                    </body>
                    </html>
                    """

    def test_extract_ideal_link(self):
        "Testing url extractor to get the full path good url, not the relative url."
        pagescraper = PageScraper()
        ideal = ['http://www.pupil.com/profile',
                 'https://www.pupil.com/profile']
        ideal.sort()
        self.assertEqual(pagescraper.ideal_urls(self.html), ideal)

if __name__ == 'main':
    unittest.main()
