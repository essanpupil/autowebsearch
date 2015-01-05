'''
Created on Jan 5, 2015

@author: pupil
'''
import requests
from bs4 import BeautifulSoup

url = "http://sudutpandangpupil.blogspot.com"
page = requests.get(url)
soup = BeautifulSoup(page.text)
[x.extract() for x in soup.find_all('script')]
[x.extract() for x in soup.find_all('style')]
pageText = soup.body.get_text()
linedPageText = pageText.splitlines()
line2 = ""
for line in linedPageText:
    if len(line) == 0:
        pass
    else:
        line2 = line2 + line + "\n"