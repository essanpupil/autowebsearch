"""views module for website_analyzer app."""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from website_management.models import Homepage, Webpage, Domain
from website_analyzer.models import ExtendHomepage, StringParameter, \
                                    StringAnalysist, ExtendDomain
from website_analyzer.analyzer_lib import string_analyst, \
                                          add_list_url_to_webpage, \
                                          add_scam_url_website, \
                                          string_analysist, crawl_website
from website_analyzer.forms import AddScamWebsiteForm, AddSequenceForm, \
                                   EditAnalystForm, EditAnalystDomainForm, \
                                   SearchForm
from webscraper.pagescraper import PageScraper


@login_required
def add_sequence(request):
    """view to display and process form add new parameter sequence"""
    if request.user.is_staff:
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
    else:
        return redirect('website_analyzer:analyst_dashboard')


@login_required
def analyze_website(request, hp_id):
    """Display page to analyze website,
    the last analysist result is displayed"""
    homepage = get_object_or_404(Homepage, id=hp_id)
    my_webpage = homepage.webpage_set.all()
    ExtendHomepage.objects.get_or_create(homepage=homepage)
    context = {'name': homepage.name,
               'id': homepage.id,
               'domain': homepage.domain.name,
               'domain_id': homepage.domain.id,
               'date_added': homepage.date_added,
               'scam': homepage.extendhomepage.scam,
               'inspection': homepage.extendhomepage.inspected,
               'report': homepage.extendhomepage.reported,
               'access': homepage.extendhomepage.access,
               'whitelist': homepage.extendhomepage.whitelist,
               'full_crawl': homepage.extendhomepage.full_crawled,
               'times_analyzed': homepage.extendhomepage.times_analyzed,
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
                        hp_id=website.id)
    else:
        form = EditAnalystForm()
    context = {'form': form,
               'homepage': {}}
    context['homepage'] = {'id': website.id,
                           'name': website.name,
                           'date_added': website.date_added,
                           'scam_status': website.extendhomepage.scam,
                           'inspected': website.extendhomepage.inspected,
                           'reported': website.extendhomepage.reported,
                           'access': website.extendhomepage.access,
                           'whitelist': website.extendhomepage.whitelist}
    return render(request, 'website_analyzer/edit_analyst.html', context)


@login_required
def extract_links(request, web_id):
    """extract links from the current webpage. filter ideal links only"""
    webpage = get_object_or_404(Webpage, id=web_id)
    page_scraper = PageScraper()
    links = page_scraper.ideal_urls(webpage.html_page)
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
    form = SearchForm(request.GET)
    if form.is_valid():
        websites = Homepage.objects.filter(
            name__contains=form.cleaned_data['search']).values_list(
                'id', flat=True).order_by('id').reverse()
    else:
        websites = Homepage.objects.only(
            'id').all().values_list('id', flat=True).order_by('id').reverse()
    context = {'websites': websites, 'divided_websites': []}
    paginator = Paginator(context['websites'], 20)
    page = request.GET.get('page')
    try:
        context['pagebase'] = paginator.page(page)
    except PageNotAnInteger:
        context['pagebase'] = paginator.page(1)
    except EmptyPage:
        context['pagebase'] = paginator.page(paginator.num_pages)
    divided_websites = Homepage.objects.filter(
        id__in=context['pagebase'].object_list)
    context['searchbase'] = "Website name"
    if form.is_valid():
        for homepage in divided_websites.filter(
                name__contains=form.cleaned_data['search']):
            try:
                exthp = ExtendHomepage.objects.get(homepage=homepage)
                context['divided_websites'].append(
                    {'id': homepage.id,
                     'name': homepage.name,
                     'date_added': homepage.date_added,
                     'scam': exthp.scam,
                     'times_analyzed': exthp.times_analyzed,
                     'full_crawled': exthp.full_crawled,
                     'whitelist': exthp.whitelist,
                     'inspection': exthp.inspected,
                     'report': exthp.reported,
                     'access': exthp.access,
                     'web_count': homepage.webpage_set.all().count(),
                     'matched_sequence': {'min': 0, 'max': 0}})
            except ExtendHomepage.DoesNotExist:
                context['divided_websites'].append(
                    {'id': homepage.id,
                     'name': homepage.name,
                     'date_added': homepage.date_added,
                     'whitelist': 'n/a',
                     'scam': 'n/a',
                     'inspection': 'n/a',
                     'report': 'n/a',
                     'access': 'n/a',
                     'web_count': homepage.webpage_set.all().count(),
                     'matched_sequence': {'min': 0, 'max': 0}})
    else:
        for homepage in divided_websites:
            try:
                exthp = ExtendHomepage.objects.get(homepage=homepage)
                context['divided_websites'].append(
                    {'id': homepage.id,
                     'name': homepage.name,
                     'date_added': homepage.date_added,
                     'scam': exthp.scam,
                     'times_analyzed': exthp.times_analyzed,
                     'full_crawled': exthp.full_crawled,
                     'whitelist': exthp.whitelist,
                     'inspection': exthp.inspected,
                     'report': exthp.reported,
                     'access': exthp.access,
                     'web_count': homepage.webpage_set.all().count(),
                     'matched_sequence': {'min': 0, 'max': 0}})
            except ExtendHomepage.DoesNotExist:
                context['divided_websites'].append(
                    {'id': homepage.id,
                     'name': homepage.name,
                     'date_added': homepage.date_added,
                     'whitelist': 'n/a',
                     'scam': 'n/a',
                     'inspection': 'n/a',
                     'report': 'n/a',
                     'access': 'n/a',
                     'web_count': homepage.webpage_set.all().count(),
                     'matched_sequence': {'min': 0, 'max': 0}})
    context['form'] = SearchForm()
    return render(request, 'website_analyzer/view_websites.html', context)


@login_required
def view_sequence(request):
    """display sequence parameter used for analyze website"""
    parameters = StringParameter.objects.all().order_by('date_added')
    context = {'parameters': []}
    for parameter in parameters.reverse():
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


@login_required
def view_analyst_result(request):
    "display analyst result"
    analyst_results = StringAnalysist.objects.only('id').values_list(
        'id', flat=True).order_by('id').reverse()
    context = {}
    context['analyst_results'] = analyst_results
    context['filtered_results'] = []
    paginator = Paginator(context['analyst_results'], 20)
    page = request.GET.get('page')
    try:
        context['analyst_results'] = paginator.page(page)
    except PageNotAnInteger:
        context['analyst_results'] = paginator.page(1)
    except EmptyPage:
        context['analyst_results'] = paginator.page(paginator.num_pages)
    analyst_websites = StringAnalysist.objects.filter(
        id__in=context['analyst_results'].object_list)
    for result in analyst_websites:
        result_data = {'webpage': {'url': result.webpage.url,
                                   'id': result.webpage.id,
                                   'homepage_id': result.webpage.homepage.id},
                       'analyze_time': result.time,
                       'string_parameter': result.parameter,
                       'find': result.find}
        context['filtered_results'].append(result_data)
    return render(request,
                  'website_analyzer/view_analyst_result.html',
                  context)


@login_required
def view_analyst_domains(request):
    "display more info about domains"
    form = SearchForm(request.GET)
    if form.is_valid():
        domains = Domain.objects.filter(
            name__contains=form.cleaned_data['search']).values_list(
                'id', flat=True).order_by('id').reverse()
    else:
        domains = Domain.objects.only(
            'id').all().values_list('id', flat=True).order_by('id').reverse()
    context = {'domains': domains, 'divided_domains': []}
    paginator = Paginator(domains, 10)
    page = request.GET.get('page')
    try:
        context['pagebase'] = paginator.page(page)
    except PageNotAnInteger:
        context['pagebase'] = paginator.page(1)
    except EmptyPage:
        context['pagebase'] = paginator.page(paginator.num_pages)
    context['divided_id'] = context['pagebase'].object_list
    divided_domains = Domain.objects.filter(
        id__in=context['pagebase'].object_list).order_by('id').reverse()
    if form.is_valid():
        for dom in divided_domains.filter(
                name__contains=form.cleaned_data['search']):
            try:
                extdom = ExtendDomain.objects.get(domain=dom)
                context['divided_domains'].append(
                    {'id': dom.id,
                     'name': dom.name,
                     'hp_count': dom.homepage_set.all().count(),
                     'whitelist': extdom.whitelist,
                     'free': extdom.free,
                     'date_added': dom.date_added})
            except ExtendDomain.DoesNotExist:
                context['divided_domains'].append(
                    {'id': dom.id,
                     'name': dom.name,
                     'hp_count': dom.homepage_set.all().count(),
                     'whitelist': 'N/A',
                     'free': 'N/A',
                     'date_added': dom.date_added})
    else:
        for dom in divided_domains:
            try:
                extdom = ExtendDomain.objects.get(domain=dom)
                context['divided_domains'].append(
                    {'id': dom.id,
                     'name': dom.name,
                     'hp_count': dom.homepage_set.all().count(),
                     'whitelist': extdom.whitelist,
                     'free': extdom.free,
                     'date_added': dom.date_added})
            except ExtendDomain.DoesNotExist:
                context['divided_domains'].append(
                    {'id': dom.id,
                     'name': dom.name,
                     'hp_count': dom.homepage_set.all().count(),
                     'whitelist': 'N/A',
                     'free': 'N/A',
                     'date_added': dom.date_added})
    context['form'] = SearchForm()
    context['searchbase'] = "Domain"
    return render(request,
                  'website_analyzer/view_analyst_domains.html',
                  context)


@login_required
def edit_analyst_domain(request, dom_id):
    "display form to edit domain data"
    domain = get_object_or_404(Domain, id=dom_id)
    extdom = ExtendDomain.objects.get(domain=domain)
    if request.method == 'POST':
        form = EditAnalystDomainForm(request.POST)
    if form.is_valid():
        extdom.free = form.cleaned_data['free']
        extdom.whitelist = form.cleaned_data['whitelist']
        extdom.save()
        domain_origin = extdom.domain
        my_homepages = domain_origin.homepage_set.all()
        if extdom.whitelist is True:
            for my_hp in my_homepages:
                ext_hp = ExtendHomepage.objects.get(homepage=my_hp)
                ext_hp.whitelist = True
                ext_hp.save()
        domain.save()
        return redirect('website_analyzer:detail_analyst_domain',
                        dom_id=domain.id)
    else:
        form = EditAnalystDomainForm()
    context = {'form': form,
               'id': domain.id,
               'domain': {}}
    context['domain'] = {'id': domain.id,
                         'name': domain.name,
                         'free': domain.extenddomain.free,
                         'whitelist': domain.extenddomain.whitelist}
    return render(request,
                  'website_analyzer/edit_analyst_domain.html',
                  context)


@login_required
def detail_analyst_domain(request, dom_id):
    "display analyst data of a domain"
    domain = get_object_or_404(Domain, id=dom_id)
    my_homepages = domain.homepage_set.all()
    ExtendDomain.objects.get_or_create(domain=domain)
    context = {'name': domain.name,
               'id': domain.id,
               'date_added': domain.date_added,
               'free': domain.extenddomain.free,
               'whitelist': domain.extenddomain.whitelist,
               'homepages': []}
    for homepage in my_homepages:
        context['homepages'].append({'id': homepage.id, 'name': homepage.name})
    return render(request,
                  'website_analyzer/detail_analyst_domain.html',
                  context)
