import django
django.setup()
'''
Created on Jan 20, 2015

@author: pupil
'''
from django.apps import apps
apps.get_app_config('operation')
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from WebScraper.WebPageScraper import PageScraper
from operation.models import Webpage

scams = Webpage.objects.filter(scamStatus=True)
# scam = scams[0]
# fetch_scam = PageScraper()
# fetch_scam.fetch_webpage(scam.url)
# scam_page = fetch_scam.getTextBody()
# scam_text = "\n".join(scam_page)
# print scam_text
# print type(scam_text)
for scam in scams:
    scam_page = PageScraper().getTextBody(scam.htmlPage)
    scam_text = "\n".join(scam_page)
    scam_compare = Webpage.objects.filter(scamStatus=True)
    for item in scam_compare:
        item_page = PageScraper().getTextBody(item.htmlPage)
        item_text = "\n".join(item_page)
        if item.url == scam.url:
            continue
        else:
            print "Ratio between"
            print scam.url
            print "and"
            print item.url
            print fuzz.ratio(scam_text, item_text)