'''
Created on Jan 5, 2015

@author: pupil
'''
import requests
from bs4 import BeautifulSoup

class PageScraper:
    'Default class to scrape for random webpage'
    def __init__(self):
        self.url = None
        self.html = None

    def fetch_webpage(self, url):
        'start fetching webpage'
        self.url = url
        req = requests.get(self.url)
        self.html = req.text

    def getTextBody(self, html=None):
        'method to remove javascript and css from html body and return only text body inside a list'
        if html == None:
            self.soup = BeautifulSoup(self.html)
        else:
            self.soup = BeautifulSoup(html)
        [x.extract() for x in self.soup.find_all('script')]
        [x.extract() for x in self.soup.find_all('style')]
        pageText = self.soup.body.get_text()
        linedPageText = pageText.splitlines()
        line2 = []
        for line in linedPageText:
            if len(line) != 0:
                line2.append(line.encode('ascii', 'ignore'))
        return "\n".join(line2)

#todo: make class for specific free web domain hosting