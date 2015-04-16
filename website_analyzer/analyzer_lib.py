import tldextract

from django.db import IntegrityError, transaction
from website_management.models import Homepage, Webpage, Domain
from .models import ExtendHomepage, StringParameter, StringAnalysist
from .models import ExtendWebpage, ExtendDomain

from webscraper.pagescraper import PageScraper

def string_analyst(hp_id):
    """function to do string analyst to homepage"""
    hp = Homepage.objects.get(id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    params = StringParameter.objects.all()
    for web in hp.webpage_set.all():
        for param in params:
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


def add_url_to_webpage(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    try:
        with transaction.atomic():
            dom, crtd = Domain.objects.get_or_create(name=ext.registered_domain)
            ExtendDomain.objects.create(domain=dom)
    except:
        pass
    try:
        with transaction.atomic():
            hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                                       domain=dom)
            ExtendHomepage.objects.create(homepage=hp)
    except:
        pass
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
            ExtendWebpage.objects.create(webpage=web)
    except IntegrityError:
        raise IntegrityError


def add_scam_url_website(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    dom, crtd = Domain.objects.get_or_create(name=ext.registered_domain)
    ExtendDomain.objects.create(domain=dom)
    hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                               domain=dom)
    ExtendHomepage.objects.create(homepage=hp)
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
            ExtendWebpage.objects.create(webpage=web)
            exthp = ExtendHomepage.objects.get(homepage=hp)
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
