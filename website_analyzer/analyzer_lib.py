import tldextract
import logging
import time
import timeout_decorator

from django.utils import timezone
from django.db import IntegrityError, transaction
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from website_management.models import Homepage, Webpage, Domain
from .models import ExtendHomepage, StringParameter, StringAnalysist, \
                    ExtendWebpage, ExtendDomain, Token, Pieces
from administrative.models import SentEmail

from webscraper.pagescraper import PageScraper


def string_analyst(hp_id):
    """function to do string analyst to homepage"""
    hp = Homepage.objects.get(id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    params = StringParameter.objects.filter(target_analyze='text_body')
    for web in hp.webpage_set.all():
        if web.extendwebpage.text_body == None:
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
            hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                                       domain=dom)
    try:
        with transaction.atomic():
            if len(url) > 255:
                truncate_url = url[0:255]
                web = Webpage.objects.create(url=truncate_url,
                                             full_url=url,
                                             homepage=hp)
                ExtendWebpage.objects.create(webpage=web)
            else:
                web = Webpage.objects.create(url=url,
                                             full_url=url,
                                             homepage=hp)
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
                extw, created = ExtendWebpage.objects.get_or_create(
                        webpage=webpage)
                if extw.text_body == None:
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
                    extw, created = ExtendWebpage.objects.get_or_create(
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
            find=True, 
            webpage__in=homepage.webpage_set.all())
    if string_analysist_result.filter(parameter__definitive=True).count() > 0:
        exthp = homepage.extendhomepage
        exthp.scam=True
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
    extw, created = ExtendWebpage.objects.get_or_create(
            webpage=webpage)
    extw.text_body = page.get_text_body()
    extw.save(update_fields=['text_body'])
    webpage.save(update_fields=['html_page'])
    keep_crawling = True
    homepages_nogif = homepage.webpage_set.exclude(url__endswith='.gif')
    homepages_nojpg = homepages_nogif.exclude(url__iendswith='.jpg')
    homepages_nopng = homepages_nojpg.exclude(url__endswith='.png')
    while keep_crawling:
        for webpage in homepages_nopng:
            page = PageScraper()
            page.fetch_webpage(webpage.url)
            webpage.html_page = page.html
            extw, created = ExtendWebpage.objects.get_or_create(
                    webpage=webpage)
            extw.text_body = page.get_text_body()
            extw.save(update_fields=['text_body'])
            webpage.save(update_fields=['html_page'])
            add_list_url_to_webpage(page.ideal_urls())
        if not homepage.webpage_set.filter(html_page__isnull=True).exists():
            break
        keep_crawling = False
    exhp,created = ExtendHomepage.objects.get_or_create(homepage=homepage)
    exhp.full_crawled += 1
    exhp.save(update_fields=['full_crawled'])


def send_email_website_analyze(homepage, operator_recipients):
    "Send website analyze to recipient list"
    subject_mail = "ScamSearcher scam notification"
    for operator in operator_recipients:
        params = StringAnalysist.objects.filter(
                webpage__in=homepage.webpage_set.all(),
                find=True).distinct('parameter')
        list_params = []
        for item in params:
            list_params.append({'parameter':item.parameter.sentence,})
        send_mail(subject_mail,
                  get_template('website_analyzer/send_email_notification.txt'
                      ).render(
                          Context({'name': homepage.name,
                                   'domain': homepage.domain,
                                   'scam': homepage.extendhomepage.scam,
                                   'params': list_params,})),
                  'support@scamsearcher.com',
                  [operator.user.email,],
                  fail_silently=False)
        SentEmail.objects.create(recipient=operator.user, homepage=homepage)


def webpage_word_tokenizer(webpage_id):
    "execute word tokenizer onto webpage's html code"
    webpage = Webpage.objects.only('html_page').get(id=webpage_id)
    pagescraper = PageScraper()
    number = 0
    for word in pagescraper.word_tokens(html=webpage.html_page):
        token,created = Token.objects.get_or_create(name=word)
        pieces = Pieces.objects.create(webpage=webpage,
                                       token=token,
                                       number=number)
        number += 1
