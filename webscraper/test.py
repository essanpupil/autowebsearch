import unittest

from .pagescraper import PageScraper


class TestNoJavascriptWebpage(unittest.TestCase):
    """perform test for webpage that does not contain javascript"""
    def setUp(self):
        self.nojshtml = """
                   <html>
                   <head><title>Dummy html</title></head>
                   <body>
                       <p>Hello World!</p>
                       <p>
                        Together we will make the world feel better.
                       </p>
                   </body>
                   </html>
                   """

    def test_nojshtml_word_list(self):
        """get text from html without javacript"""
        w = PageScraper()
        text = w.word_tokens(self.nojshtml)
        text.sort()
        self.assertEqual(text, ['!', '.', 'better', 'feel', 'hello',
                                'make', 'the', 'together', 'we',
                                'will', 'world', 'world'])


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
        ps = PageScraper()
        ideal = ['http://www.pupil.com/profile',
                 'https://www.pupil.com/profile']
        ideal.sort()
        self.assertEqual(ps.ideal_urls(self.html), ideal)

if __name__ == 'main':
    unittest.main()
