from urllib.parse import urlparse
import unittest

from .google_search import GoogleSearch


class GoogleSearchTestCase(unittest.TestCase):
    def online_testcase(self):
        # this test is intended to not run on every project test.
        # If you want to run the test, you should specifically run this method
        google_search = GoogleSearch('essanpupil')
        google_search.start_search()
        for item in google_search.search_result:
            url = urlparse(item)
            if url.scheme is not None:
                self.assertIn('http', url.scheme)
            else:
                fail('Parsing failed!')
