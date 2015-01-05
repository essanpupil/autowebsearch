'''
Created on Jan 2, 2015

@author: pupil
'''
import unittest
from WebScraper import WebSearch


class Test(unittest.TestCase):


    def setUp(self):
        self.googleSearch = WebSearch.GoogleSearch

    def zeroArgumentGoogleSearch(self):
        self.googleSearch()
        self.assertEqual(len(self.googleSearch.searchResult), 0)

    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()