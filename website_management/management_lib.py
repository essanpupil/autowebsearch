from django.db import IntegrityError, transaction
import tldextract
import logging

from .models import Webpage, Homepage, Domain


logging.basicConfig(level=logging.WARN)
extract = tldextract.TLDExtract(
        cache_file='/home/skripsi/tldextractcache/tldextract.cache')

def add_url_to_webpage(url):
    """add url and its component to database"""
    ext = extract(url)
    dom, crtd = Domain.objects.get_or_create(name=ext.registered_domain)
    hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                               domain=dom)
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
    except IntegrityError:
        raise IntegrityError


def add_list_url_to_webpage(urls):
    """add list url and their components to database"""
    for url in urls:
        try:
            add_url_to_webpage(url)
        except IntegrityError:
            continue
