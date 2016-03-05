from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize


class PageScraper:
    """Default class to scrape for random webpage"""
    def __init__(self):
        self.url = None
        self.html = None
        self.response = None
        self.redirect_url = None
        self.soup = None

    def fetch_webpage(self, url):
        """start fetching webpage"""
        self.url = url
        try:
            req = requests.get(self.url)
            self.html = req.text
        except:
            self.html = "Failed to fetch webpage."

    def get_text_body(self, html=None):
        """
        method to remove javascript and css from html body and return only
        text body inside a list
        """
        if html is None:
            self.soup = BeautifulSoup(self.html, "html5lib")
        else:
            self.soup = BeautifulSoup(html, "html5lib")
        [x.extract() for x in self.soup.find_all('script')]
        [x.extract() for x in self.soup.find_all('style')]
        page_text = self.soup.body.get_text()
        lined_page_text = page_text.splitlines()
        line2 = []
        for line in lined_page_text:
            line_b = line.lower()
            if len(line) != 0:
                line2.append(line_b.encode('ascii', 'ignore'))
        return page_text.lower()

    def word_tokens(self, html=None):
        """return word tokens of webpage"""
        if html is None:
            text = self.get_text_body()
        else:
            text = self.get_text_body(html=html)
        text2 = text.strip()
        text3 = text2.lower()
        return word_tokenize(text3)
    
    def ideal_urls(self, html=None):
        """extract the ideal url inside webpage"""
        if html is not None:
            soup = BeautifulSoup(html, "html5lib")
        else:
            soup = BeautifulSoup(self.html, "html5lib")
        proper_link = []
        for item in soup.find_all('a'):
            try:
                e = urlparse(item.get('href'))
                if (e.scheme == 'http') or (e.scheme == 'https'):
                    proper_link.append(item.get('href'))
                else:
                    continue
            except:
                continue
        proper_link.sort()
        return proper_link

