from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger
import tldextract

from .models import ExtendHomepage, Sequence, StringParameter
from website_management.models import Homepage, Webpage
from .analyzer_lib import string_analyst, add_list_url_to_webpage
from .analyzer_lib import add_url_to_webpage, add_scam_url_website
from webscraper.pagescraper import PageScraper
from .forms import AddScamWebsiteForm, AddSequenceForm


def add_sequence(request):
    'view to display and process form add new parameter sequence'
    if request.method == 'POST':
        form = AddSequenceForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data['sentence'].lower()
            definitive = form.cleaned_data['definitive']
            StringParameter.objects.create(sentence=sentence.strip(),
                                           definitive=definitive)
            return redirect('website_analyzer:view_sequence')
    else:
        form = AddSequenceForm()
    return render(request, 'website_analyzer/add_sequence.html',
                  {'form': form})

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
    # if this is a POST request, the form data is processed
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = AddScamWebsiteForm(request.POST)
        
        # check the form is valid or not
        if form.is_valid():
            # start saving scam homepage url to database
            add_scam_url_website(form.cleaned_data['url'])
            return redirect('website_analyzer:view_websites')
    else:
        form = AddScamWebsiteForm()
    return render(request, 'website_analyzer/add_scam_website.html',
                  {'form': form})


def view_websites(request):
    "display scam website"
    websites = Homepage.objects.all()
    context = {'websites': []}
    for hp in websites:
        try:
            exthp = ExtendHomepage.objects.get(homepage=hp)
            context['websites'].append({'id': hp.id,
                                        'name': hp.name,
                                        'scam': exthp.scam,
                                        'inspection': exthp.inspected,
                                        'report': exthp.reported,
                                        'access': exthp.access,
                                        'web_count': hp.webpage_set.all().count(),
                                        'date_added': hp.date_added,
                                        'domain': hp.domain.name})
        except ExtendHomepage.DoesNotExist:
            context['websites'].append({'id': hp.id,
                                        'name': hp.name,
                                        'scam': 'n/a',
                                        'inspection': 'n/a',
                                        'report': 'n/a',
                                        'access': 'n/a',
                                        'web_count': hp.webpage_set.all().count(),
                                        'date_added': hp.date_added,
                                        'domain': hp.domain.name})
    paginator = Paginator(context['websites'], 10)
    page = request.GET.get('page')
    try:
        context['websites'] = paginator.page(page)
    except PageNotAnInteger:
        context['websites'] = paginator.page(1)
    except EmptyPage:
        context['websites'] = paginator.page(paginator.num_pages)
    return render(request, 'website_analyzer/view_websites.html', context)


def view_sequence(request):
    "display sequence parameter used for analyze website"
    parameters = StringParameter.objects.all()
    context = {'parameters': []}
    for parameter in parameters:
        context['parameters'].append({'sentence': parameter.sentence,
                                     'date_added': parameter.date_added,
                                     'definitive': parameter.definitive})
    paginator = Paginator(context['parameters'], 10)
    page = request.GET.get('page')
    try:
        context['parameters'] = paginator.page(page)
    except PageNotAnInteger:
        context['parameters'] = paginator.page(1)
    except EmptyPage:
        context['parameters'] = paginator.page(paginator.num_pages)
    return render(request, 'website_analyzer/view_sequences.html', context)
