import requests
from urlparse import urlparse
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize


class PageScraper:
    """Default class to scrape for random webpage"""
    def __init__(self):
        self.url = None
        self.html = None
        self.response = None
        self.redirect_url = None

    def fetch_webpage(self, url):
        """start fetching webpage"""
        self.url = url
        req = requests.get(self.url)
        self.html = req.text

    def get_text_body(self, html=None):
        """
        method to remove javascript and css from html body and return only
        text body inside a list
        """
        if html is None:
            self.soup = BeautifulSoup(self.html)
        else:
            self.soup = BeautifulSoup(html)
        [x.extract() for x in self.soup.find_all('script')]
        [x.extract() for x in self.soup.find_all('style')]
        page_text = self.soup.body.get_text()
        linedPageText = page_text.splitlines()
        line2 = []
        for line in linedPageText:
            line_a = line.strip()
            line_b = line_a.lower()
            if len(line) != 0:
                line2.append(line_b.encode('ascii', 'ignore'))
        return "\n".join(line2)

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
            soup = BeautifulSoup(html)
        else:
            soup = BeautifulSoup(self.html)
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

#todo: make class for specific free web domain hosting
