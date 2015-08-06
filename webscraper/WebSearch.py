"""
Created on Jan 2, 2015

@author: pupil
"""
from bs4 import BeautifulSoup
import requests


class GoogleSearch:
    """class dasar untuk berinteraksi dengan google.com"""

    def __init__(self, query):
        self.query = str(query)
        self.query.strip()
        self.query.replace(" ", "+")
        self.isFinalPage = False
        self.searchResult = []

    def start_search(self, maxPage=1):
        """method to start searching and parse the url link result to self.searchResult"""
        self.currentPage = 1
        self.maxPage = maxPage
        for page in range(1, self.maxPage + 1):
            self.fetchPage(self.currentPage)
            self.currentPage = page

    def nextPage(self, page=1):
        """method the set the url next page of google search result,
        return the start number of the next page"""
        self.currentPage += page
        self.fetchPage(self.currentPage)

    def fetchPage(self, page=1):
        """method to download the html text of current page result"""
        startNumber = (page - 1) * 10
        self.pageRequest = requests.get("http://google.com/search", params={'query': self.query, 'start': startNumber})
        soup = BeautifulSoup(self.pageRequest.text, "html5lib")
        results = soup.find_all('a', class_=False)
        href_ls = []
        for target in results:
            if ((target.get('href').find("/url?q") == 0) and not (
                        target.get('href').find("/url?q=http://webcache.googleusercontent.com") == 0) and not (
                        target.get('href').find("/url?q=/settings/") == 0)):
                href_ls.append(target.get('href')[target.get('href').find("http"):target.get('href').find("&sa")])
        for href in results:
            if href.get_text() == "repeat the search with the omitted results included":
                self.isFinalPage = True
            else:
                pass
        for href in href_ls:
            self.searchResult.append(href)
