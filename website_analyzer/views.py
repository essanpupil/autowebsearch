from django.shortcuts import render, get_object_or_404, redirect
import tldextract

from .models import ExtendHomepage, Sequence
from website_management.models import Homepage, Webpage
from .analyzer_lib import string_analyst, add_list_url_to_webpage
from .analyzer_lib import add_url_to_webpage
from webscraper.pagescraper import PageScraper


def analyze_website(request, hp_id):
    "Display page to analyze website, the last analysist result is displayed"
    hp = get_object_or_404(Homepage, id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    context = {'name': hp.name,
               'domain': hp.domain.name,
               'date_added': hp.date_added,
               'scam': hp.extendhomepage.scam,
               'inspection': hp.extendhomepage.inspected,
               'report': hp.extendhomepage.reported,
               'access': hp.extendhomepage.access,
               'whitelist': hp.extendhomepage.whitelist,
               'webpages': [],
               'params': []}
    for web in hp.webpage_set.all():
        context['webpages'].append({'id': web.id, 'url':web.url})
    return render(request, 'website_analyzer/analyze_website.html', context)

def start_analyze(request, hp_id):
    "execute analyze process"
    string_analyst(hp_id)
    return redirect('website_analyzer:analyze_website', hp_id= hp_id)


def analyst_dashboard(request):
    "Display summary info of analyzed website."
    exthp = ExtendHomepage.objects.all()
    context = {'scam_count': exthp.filter(scam=True).count(),
               'whitelist_count': exthp.filter(whitelist=True).count(),
               'hp_count': exthp.count()}
    return render(request, 'website_analyzer/dashboard.html', context)


def display_pages(request, hp_id):
    "Display webpages of current homepage"
    pass


def display_analyst(request, hp_id):
    "Display analysist data of current homepage"
    pass


def edit_analyst(request, hp_id):
    "Display edit form of analyst data for current homepage"
    pass


def view_tokens(requesst, web_id):
    "Display tokens of current webpage"
    pass


def extract_links(request, web_id):
    "extract links from the current webpage. filter ideal links only"
    web = get_object_or_404(Webpage, id=web_id)
    ps = PageScraper()
    links = ps.ideal_urls(web.html_page)
    add_list_url_to_webpage(links)
    return redirect('website_management:view_all_webpages')


def add_scam_website(request):
    "manually add website known as scam"
    pass


def view_websites(request):
    "display scam website"
    pass


def view_sequence(request):
    "display sequence parameter used for analyze website"
    pass
