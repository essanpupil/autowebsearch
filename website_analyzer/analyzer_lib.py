"""helper module for website analyzer app."""
import logging

import tldextract

from django.utils import timezone
from django.db import IntegrityError, transaction

from website_management.models import Website, Webpage, Domain
from website_analyzer.models import ExtendWebsite, StringParameter, \
                                    StringAnalysist, ExtendWebpage, \
                                    ExtendDomain
from webscraper.pagescraper import PageScraper


def string_analyst(hp_id):
    """function to do string analyst to homepage"""
    website = Website.objects.get(id=hp_id)
    exthp, _ = ExtendWebsite.objects.get_or_create(homepage=website)
    params = StringParameter.objects.all()
    for web in website.webpage_set.all():
        if web.extendwebpage.text_body is None:
            page = PageScraper()
            page.fetch_webpage(web.url)
            web.html_page = page.html
            extw = web.extendwebpage
            extw.text_body = page.get_text_body()
            extw.save()
            web.save()

        for param in params:
            param.times_used += 1
            param.save(update_fields=['times_used'])
            if param.sentence in web.extendwebpage.text_body:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=True)
                if param.definitive:
                    exthp.scam = True
                    exthp.save()
            else:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=False)
    exthp.times_analyzed += 1
    exthp.save()


def add_url_to_webpage(url):
    """add url and its component to database"""
    logging.basicConfig(level=logging.WARN)
    extract = tldextract.TLDExtract(
        cache_file='/home/skripsi/tldextractcache/tldextract.cache')
    ext = extract(url)
    try:
        with transaction.atomic():
            domain, _ = Domain.objects.get_or_create(
                name=ext.registered_domain)
            ExtendDomain.objects.create(domain=domain)
    except:
        pass
    try:
        with transaction.atomic():
            website, _ = Website.objects.get_or_create(name='.'.join(ext),
                                                       domain=domain)
            ExtendWebsite.objects.create(homepage=website)
    except:
        website, _ = Website.objects.get_or_create(name='.'.join(ext),
                                                   domain=domain)
    try:
        with transaction.atomic():
            if len(url) > 255:
                truncate_url = url[0:255]
                webpage = Webpage.objects.create(url=truncate_url,
                                                 full_url=url,
                                                 homepage=website)
                ExtendWebpage.objects.create(webpage=webpage)
            else:
                webpage = Webpage.objects.create(url=url,
                                                 full_url=url,
                                                 homepage=website)
                ExtendWebpage.objects.create(webpage=webpage)
    except IntegrityError:
        raise IntegrityError


def add_scam_url_website(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    domain, _ = Domain.objects.get_or_create(name=ext.registered_domain)
    ExtendDomain.objects.create(domain=domain)
    website, _ = Website.objects.get_or_create(name='.'.join(ext),
                                               domain=domain)
    ExtendWebsite.objects.create(homepage=website)
    try:
        with transaction.atomic():
            webpage = Webpage.objects.create(url=url, homepage=website)
            ExtendWebpage.objects.create(webpage=webpage)
            exthp = ExtendWebsite.objects.get(homepage=website)
            exthp.scam = True
            exthp.save()
    except IntegrityError:
        raise IntegrityError


def add_list_url_to_webpage(urls):
    """add list url and their components to database"""
    for url in urls:
        try:
            add_url_to_webpage(url)
        except IntegrityError:
            continue


def fill_text_body(extw):
    "Function to fill text_body of an ExtendWebpage object"
    page = PageScraper()
    text = page.get_text_body(html=extw.webpage.html_page)
    extw.text_body = text
    extw.save()


def string_analysist(homepage):
    """function to doing string analysist on to website/homepage model object.
    required website_management.models.Homepage as argument"""
    hari_ini = timezone.now()
    parameters = StringParameter.objects.filter(target_analyze='text_body')
    webpages = homepage.webpage_set.all()
    for parameter in parameters:
        for webpage in webpages:
            newest_string_analysist = StringAnalysist.objects.filter(
                webpage=webpage,
                parameter=parameter).order_by('time').reverse()
            if newest_string_analysist.count() == 0:
                extw, _ = ExtendWebpage.objects.get_or_create(webpage=webpage)
                if extw.text_body is None:
                    continue
                if parameter.sentence in extw.text_body:
                    StringAnalysist.objects.create(webpage=webpage,
                                                   parameter=parameter,
                                                   find=True)
                else:
                    StringAnalysist.objects.create(webpage=webpage,
                                                   parameter=parameter,
                                                   find=False)
            else:
                if (hari_ini - newest_string_analysist[0].time).days == 0:
                    continue
                else:
                    extw, _ = ExtendWebpage.objects.get_or_create(
                        webpage=webpage)
                    if parameter.sentence in extw.text_body:
                        StringAnalysist.objects.create(webpage=webpage,
                                                       parameter=parameter,
                                                       find=True)
                    else:
                        StringAnalysist.objects.create(webpage=webpage,
                                                       parameter=parameter,
                                                       find=False)
            continue
        continue
    string_analysist_result = StringAnalysist.objects.filter(
        find=True, webpage__in=homepage.webpage_set.all())
    if string_analysist_result.filter(parameter__definitive=True).count() > 0:
        exthp = homepage.extendhomepage
        exthp.scam = True
        exthp.save()


def crawl_website(homepage):
    """function to fetch html code and url of a website, start from available
    webpages in the database. The only accepted argument in Homepage object."""
    try:
        add_url_to_webpage("http://"+homepage.name)
    except:
        pass
    page = PageScraper()
    page.fetch_webpage("http://"+homepage.name)
    webpage = Webpage.objects.get(url="http://"+homepage.name)
    webpage.html_page = page.html
    extw, _ = ExtendWebpage.objects.get_or_create(
        webpage=webpage)
    extw.text_body = page.get_text_body()
    extw.save(update_fields=['text_body'])
    webpage.save(update_fields=['html_page'])
    keep_crawling = True
    while keep_crawling:
        ext_hp = ExtendWebsite.objects.get(
            homepage=homepage).only('full_crawled')
        ext_hp.full_crawled += 1
        ext_hp.save(update_fields=['full_crawled'])
        for webpage in homepage.webpage_set.all():
            page = PageScraper()
            page.fetch_webpage(webpage.url)
            webpage.html_page = page.html
            extw, _ = ExtendWebpage.objects.get_or_create(webpage=webpage)
            extw.text_body = page.get_text_body()
            extw.save(update_fields=['text_body'])
            webpage.save(update_fields=['html_page'])
            add_list_url_to_webpage(page.ideal_urls())
        if not homepage.webpage_set.filter(html_page__isnull=True).exists():
            break
        keep_crawling = False
