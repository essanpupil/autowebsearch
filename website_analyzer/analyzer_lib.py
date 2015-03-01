from bs4 import BeautifulSoup
import tldextract

from django.db import IntegrityError, transaction
from website_management.models import Homepage, Webpage, Domain
from .models import ExtendHomepage, StringParameter, StringAnalysist
from .models import ExtendWebpage


def string_analyst(hp_id):
    "function to do string analyst to homepage"
    hp = Homepage.objects.get(id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    params = StringParameter.objects.all()
    for web in hp.webpage_set.all():
        for param in params:
            if param.name in web.extendwebpage.text_body:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=True)
                if param.level == "1":
                    exthp.scam=True
                    exthp.save()
            else:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=False)


def add_url_to_webpage(url):
    "add url and its component to database"
    ext = tldextract.extract(url)
    dom, crtd = Domain.objects.get_or_create(name = ext.registered_domain)
    hp, crtd2 = Homepage.objects.get_or_create(name = '.'.join(ext),
                                               domain = dom)
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
            ExtendWebpage.objects.create(webpage=web)
    except IntegrityError:
        raise IntegrityError


def add_list_url_to_webpage(urls):
    "add list url and their components to database"
    for url in urls:
        try:
            add_url_to_webpage(url)
        except IntegrityError:
            continue
