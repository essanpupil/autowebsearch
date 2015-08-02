from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import ExtendHomepage, StringParameter, StringAnalysist
from website_management.models import Homepage, Webpage
from .analyzer_lib import string_analyst, add_list_url_to_webpage
from .analyzer_lib import add_scam_url_website, string_analysist, crawl_website
from webscraper.pagescraper import PageScraper
from .forms import AddScamWebsiteForm, AddSequenceForm, EditAnalystForm


@login_required
def add_sequence(request):
    """view to display and process form add new parameter sequence"""
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


@login_required
def analyze_website(request, hp_id):
    """Display page to analyze website,
    the last analysist result is displayed"""
    hp = get_object_or_404(Homepage, id=hp_id)
    my_webpage = hp.webpage_set.all()
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    context = {'name': hp.name,
               'id': hp.id,
               'domain': hp.domain.name,
               'date_added': hp.date_added,
               'scam': hp.extendhomepage.scam,
               'inspection': hp.extendhomepage.inspected,
               'report': hp.extendhomepage.reported,
               'access': hp.extendhomepage.access,
               'whitelist': hp.extendhomepage.whitelist,
               'webpages': [],
               'params': []}
    for web in my_webpage:
        context['webpages'].append({'id': web.id, 'url': web.url})
    for item in StringAnalysist.objects.filter(webpage__in=my_webpage,
            find=True):
        temp = {'parameter': '', 'webpage': '', 'find': ''}
        temp['parameter'] = item.parameter.sentence
        temp['webpage'] = item.webpage.url
        temp['find'] = item.find
        temp['time'] = item.time
        context['params'].append(temp)
    return render(request, 'website_analyzer/analyze_website.html', context)


@login_required
def start_analyze(request, hp_id):
    """execute analyze process"""
    string_analyst(hp_id)
    return redirect('website_analyzer:analyze_website', hp_id=hp_id)


@login_required
def analyst_dashboard(request):
    """Display summary info of analyzed website."""
    exthp = ExtendHomepage.objects.all()
    context = {'scam_count': exthp.filter(scam=True).count(),
               'whitelist_count': exthp.filter(whitelist=True).count(),
               'hp_count': exthp.count()}
    return render(request, 'website_analyzer/dashboard.html', context)


@login_required
def display_pages(request, hp_id):
    """Display webpages of current homepage"""
    pass


@login_required
def display_analyst(request, hp_id):
    """Display analysist data of current homepage"""
    pass


@login_required
def edit_analyst(request, homepage_id):
    """Display edit form of analyst data for current homepage"""
    website = get_object_or_404(Homepage, id=homepage_id)
    exth = ExtendHomepage.objects.get(homepage=website)
    if request.method == 'POST':
	form = EditAnalystForm(request.POST)
	if form.is_valid():
            exth.scam = form.cleaned_data['scam']
            exth.inspected = form.cleaned_data['inspected']
            exth.reported = form.cleaned_data['reported']
            exth.access = form.cleaned_data['access']
            exth.whitelist = form.cleaned_data['whitelist']
            exth.save()
            website.save()
            return redirect('website_analyzer:analyze_website',
                            hp_id = website.id)
    else:
        form = EditAnalystForm()
    context = {'form': form,
               'homepage': {},}
    context['homepage'] = {'id': website.id,
                           'name': website.name,
                           'date_added': website.date_added,
                           'scam_status': website.extendhomepage.scam,
                           'inspected': website.extendhomepage.inspected,
                           'reported': website.extendhomepage.reported,
                           'access': website.extendhomepage.access,
                           'whitelist': website.extendhomepage.whitelist,}
    return render(request, 'website_analyzer/edit_analyst.html', context)
    

@login_required
def view_tokens(request, web_id):
    """Display tokens of current webpage"""
    pass


@login_required
def extract_links(request, web_id):
    """extract links from the current webpage. filter ideal links only"""
    web = get_object_or_404(Webpage, id=web_id)
    ps = PageScraper()
    links = ps.ideal_urls(web.html_page)
    add_list_url_to_webpage(links)
    return redirect('website_management:view_all_webpages')


@login_required
def add_scam_website(request):
    """manually add website known as scam"""
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddScamWebsiteForm(request.POST)
            if form.is_valid():
                add_scam_url_website(form.cleaned_data['url'])
                return redirect('website_analyzer:view_websites')
        else:
            form = AddScamWebsiteForm()
        return render(request, 'website_analyzer/add_scam_website.html',
                      {'form': form})
    else:
        return redirect('website_analyzer:analyst_dashboard')


@login_required
def view_websites(request):
    """display scam website"""
    websites = Homepage.objects.all().order_by('date_added').reverse()
    context = {'websites': []}
    for hp in websites:
        try:
            exthp = ExtendHomepage.objects.get(homepage=hp)
            context['websites'].append(
                {'id': hp.id,
                 'name': hp.name,
                 'scam': exthp.scam,
                 'inspection': exthp.inspected,
                 'report': exthp.reported,
                 'access': exthp.access,
                 'web_count': hp.webpage_set.all().count(),
                 'date_added': hp.date_added,})
        except ExtendHomepage.DoesNotExist:
            context['websites'].append(
                {'id': hp.id,
                 'name': hp.name,
                 'scam': 'n/a',
                 'inspection': 'n/a',
                 'report': 'n/a',
                 'access': 'n/a',
                 'web_count': hp.webpage_set.all().count(),
                 'date_added': hp.date_added,})
    paginator = Paginator(context['websites'], 10)
    page = request.GET.get('page')
    try:
        context['websites'] = paginator.page(page)
    except PageNotAnInteger:
        context['websites'] = paginator.page(1)
    except EmptyPage:
        context['websites'] = paginator.page(paginator.num_pages)
    return render(request, 'website_analyzer/view_websites.html', context)


@login_required
def view_sequence(request):
    """display sequence parameter used for analyze website"""
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


@login_required
def crawl_homepage(request, homepage_id):
    "View to extract all links inside a website"
    website = get_object_or_404(Homepage, id=homepage_id)
    crawl_website(website)
    return redirect('website_analyzer:analyze_website', hp_id=website.id)


@login_required
def start_sequence_analysist(request, homepage_id):
    """start executing string parameter analysist on to homepage and then save
    result to StringAnalysist model"""
    homepage = get_object_or_404(Homepage, id=homepage_id)
    string_analysist(homepage)
    return redirect('website_analyzer:analyze_website', hp_id=homepage.id)
