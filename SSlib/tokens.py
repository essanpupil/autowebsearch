'''
Created on Jan 17, 2015

@author: pupil
'''
#from WebScraper.WebPageScraper import WebPageScraper
from nltk.tokenize import sent_tokenize

#page = WebPageScraper("http://bri-1.weebly.com/info-pemenang.html")
class Tokenizer():
    'class to manage tokens spesific for ScamSearcher project'
    def __init__(self, text):
        self.text = text

    def sentence_tokens(self):
        'tokenize the text list from scraped webpage per sentece. Return list of sentence tokens'
        token_list = []
        for linestr in self.text.splitlines():
            sent_tokenize_list = sent_tokenize(linestr)
            for tokn in sent_tokenize_list:
                tokn = tokn.lower()
                tokn = tokn.strip()
                token_list.append(str(tokn).encode('ascii', 'ignore'))
        return token_list