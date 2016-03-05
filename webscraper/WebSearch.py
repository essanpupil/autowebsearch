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
        self.is_final_page = False
        self.search_result = []
        self.max_page = None
        self.current_page = None
        self.page_request = None

    def start_search(self, max_page=1):
        """method to start searching and parse the url link result to self.searchResult"""
        self.current_page = 1
        self.max_page = max_page
        for page in range(1, self.max_page + 1):
            self.fetch_page(self.current_page)
            self.current_page = page

    def next_page(self, page=1):
        """method the set the url next page of google search result,
        return the start number of the next page"""
        self.current_page += page
        self.fetch_page(self.current_page)

    def fetch_page(self, page=1):
        """method to download the html text of current page result"""
        start_number = (page - 1) * 10
        self.page_request = requests.get("http://google.com/search",
                                        params={'query': self.query,
                                                'start': start_number})
        soup = BeautifulSoup(self.page_request.text, "html5lib")
        results = soup.find_all('a', class_=False)
        href_ls = []
        for target in results:
            if ((target.get('href').find("/url?q") == 0) and not (
                    target.get('href').find("/url?q=http://webcache.googleusercontent.com") == 0) and not (
                    target.get('href').find("/url?q=/settings/") == 0)):
                href_ls.append(target.get('href')[target.get('href').find("http"):target.get('href').find("&sa")])
        for href in results:
            if href.get_text() == "repeat the search with the omitted results included":
                self.is_final_page = True
            else:
                pass
        for href in href_ls:
            self.search_result.append(href)
