'''
Created on Jan 2, 2015

@author: pupil
'''
from WebSearch import GoogleSearch
from WebPageScraper import WebPageScraper

# keyword = "pemenang indosat poin plus plus"
# googling = GoogleSearch(keyword)
# googling.startSearch()
# print len(googling.searchResult)
# for hasil in googling.searchResult:
#     print hasil
page = WebPageScraper("http://bri-1.weebly.com/info-pemenang.html")
for linestr in page.getTextBody():
    print linestr



# import unittest
# from WebScraper import WebSearch
#
#
# class Test(unittest.TestCase):
#
#
#     def setUp(self):
#         self.googleSearch = WebSearch.GoogleSearch
#
#     def zeroArgumentGoogleSearch(self):
#         self.googleSearch()
#         self.assertEqual(len(self.googleSearch.searchResult), 0)
#
#     def tearDown(self):
#         pass
#
#
#     def testName(self):
#         pass
#
#
# if __name__ == "__main__":
#     #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()