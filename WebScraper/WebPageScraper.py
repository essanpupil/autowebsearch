'''
Created on Jan 5, 2015

@author: pupil
'''
import requests
from bs4 import BeautifulSoup

class WebPageScraper:
    'Default class to scrape for random webpage'
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        self.soup = BeautifulSoup(self.request.text)

    def getTextBody(self):
        'method to remove javascript and css from html body and return only text body inside a list'
        [x.extract() for x in self.soup.find_all('script')]
        [x.extract() for x in self.soup.find_all('style')]
        pageText = self.soup.body.get_text()
        linedPageText = pageText.splitlines()
        line2 = []
        for line in linedPageText:
            if len(line) != 0:
                line2.append(line)
        return line2

#todo: make class for specific free web domain hosting