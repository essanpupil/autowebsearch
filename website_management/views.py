"""views module to manage website data."""
import tldextract
from pygoogling.googling import GoogleSearch

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from website_management.models import Webpage, Domain, Homepage, Search, Query
from website_management.forms import AddWebpageForm, SearchWebpageForm, \
                                     AddNewKeywordForm
from website_management.management_lib import add_list_url_to_webpage, \
                                              add_url_to_webpage
from webscraper.pagescraper import PageScraper

from website_analyzer.models import ExtendWebpage
from website_analyzer.analyzer_lib import fill_text_body


def website_dashboard(request):
    """display info summary about saved webpages, homepage, & domain"""
    webs = Webpage.objects.all()
    homepages = Homepage.objects.all()
    domains = Domain.objects.all()
    context = {'web_count': webs.count(),
               'hp_count': homepages.count(),
               'dom_count': domains.count(),
               'newest_5_web': [],
               'newest_5_dom': [],
               'newest_5_hp': []}
    for webage in webs.order_by('id').reverse()[0:5]:
        context['newest_5_web'].append({'url': webage.url, 'id': webage.id})
    for homepage in homepages.order_by('id').reverse()[0:5]:
        context['newest_5_hp'].append(
            {'name': homepage.name, 'id': homepage.id})
    for domain in domains.order_by('id').reverse()[0:5]:
        context['newest_5_dom'].append({'name': domain.name, 'id': domain.id})
    return render(request, 'website_management/dashboard.html', context)


def webpage_detail(request, web_id):
    """display detail info of selected webpage"""
    webpage = get_object_or_404(Webpage, id=web_id)
    web_data = {'url': webpage.url,
                'hp': '',
                'idhp': '',
                'iddom': '',
                'dom': '',
                'added': webpage.date_added,
                'status': webpage.last_response,
                'last_check': webpage.last_response_check,
                'html_page': bool(webpage.html_page),
                'text_body': '',
                'id': webpage.id, }
    if webpage.html_page is None:
        extw, _ = ExtendWebpage.objects.get_or_create(webpage=webpage)
        fill_text_body(extw)
        web_data['text_body'] = extw.text_body
    else:
        web_data['text_body'] = None
    if webpage.homepage is None:
        web_data['hp'] = None
        web_data['idhp'] = None
        web_data['iddom'] = None
        web_data['dom'] = None
    else:
        web_data['hp'] = webpage.homepage.name
        web_data['idhp'] = webpage.homepage.id
        web_data['iddom'] = webpage.homepage.domain.id
        web_data['dom'] = webpage.homepage.domain.name
    return render(request,
                  'website_management/web_detail.html',
                  {'web': web_data})


@login_required
def fetch_html_page(request, web_id):
    """downloading html source code of webpage"""
    webpage = get_object_or_404(Webpage, id=web_id)
    ext = tldextract.extract(webpage.url)
    domain, _ = Domain.objects.get_or_create(name=".".join(ext[1:]))
    homepage, _ = Homepage.objects.get_or_create(name=".".join(ext),
                                                 domain=domain)
    webpage.homepage = homepage
    webpage.save()
    page_scraper = PageScraper()
    page_scraper.fetch_webpage(webpage.url)
    webpage.html_page = page_scraper.html
    webpage.save()
    return redirect('website_management:webpage_detail', web_id=webpage.id)


@login_required
def get_domain_homepage(request, web_id):
    """extract domain and homepage from webpage's url"""
    webpage = get_object_or_404(Webpage, id=web_id)
    ext = tldextract.extract(webpage.url)
    domain, _ = Domain.objects.get_or_create(name=".".join(ext[1:]))
    homepage, _ = Homepage.objects.get_or_create(name=".".join(ext),
                                                 domain=domain)
    webpage.homepage = homepage
    webpage.save()
    return redirect('website_management:webpage_detail', web_id=webpage.id)


def homepage_detail(request, hp_id):
    "display detail info of selected homepage"
    homepage = get_object_or_404(Homepage, id=hp_id)
    context = {
        'hpname': homepage.name,
        'hpid': homepage.id,
        'hpadded': homepage.date_added,
        'hpdomain': homepage.domain.name,
        'iddom': homepage.domain.id,
        'hpweb': []
    }
    for item in homepage.webpage_set.all():
        context['hpweb'].append({'url': item.url, 'id': item.id})
    return render(request, 'website_management/homepage_detail.html', context)


def domain_detail(request, dom_id):
    """display detail info of selected domain"""
    domain = get_object_or_404(Domain, id=dom_id)
    context = {'domname': domain.name,
               'domid': domain.id,
               'domadded': domain.date_added,
               'domhp': []}
    for item in domain.homepage_set.all():
        context['domhp'].append({'name': item.name, 'id': item.id})
    return render(request, 'website_management/domain_detail.html', context)


@login_required
def add_new_webpage(request):
    """Display form to add new webpage"""
    # if this is a POST request, we should process the form data
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = AddWebpageForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # start saving new webpage url
            add_url_to_webpage(form.cleaned_data['url'])
            return redirect('website_management:view_all_webpages')
    else:
        form = AddWebpageForm()
    return render(request,
                  'website_management/add_new_webpage.html',
                  {'form': form})


def view_all_webpages(request):
    """display all webpage"""
    webs = Webpage.objects.all().order_by('id').reverse()
    context = {'webs': []}
    for item in webs:
        context['webs'].append({
            'url': item.url,
            'date_added': item.date_added,
            'last_response': item.last_response,
            'last_response_check': item.last_response_check,
            'id': item.id})
    paginator = Paginator(context['webs'], 10)
    page = request.GET.get('page')
    try:
        context['webs'] = paginator.page(page)
    except PageNotAnInteger:
        context['webs'] = paginator.page(1)
    except EmptyPage:
        context['webs'] = paginator.page(paginator.num_pages)
    return render(request,
                  'website_management/view_all_webpages.html', context)


def view_all_homepages(request):
    """display all webpage"""
    homes = Homepage.objects.all().order_by('id').reverse()
    context = {'homes': []}
    for item in homes:
        context['homes'].append({
            'name': item.name,
            'date_added': item.date_added,
            'domain': item.domain.name,
            'id': item.id})
    paginator = Paginator(context['homes'], 10)
    page = request.GET.get('page')
    try:
        context['homes'] = paginator.page(page)
    except PageNotAnInteger:
        context['homes'] = paginator.page(1)
    except EmptyPage:
        context['homes'] = paginator.page(paginator.num_pages)
    return render(request,
                  'website_management/view_all_homepages.html', context)


def view_all_domains(request):
    """display all domain"""
    doms = Domain.objects.all()
    context = {'doms': []}
    for item in doms:
        context['doms'].append({'name': item.name,
                                'date_added': item.date_added,
                                'id': item.id})
    return render(request,
                  'website_management/view_all_domains.html', context)


@login_required
def search_webpage(request):
    """display text input to start searching website in internet"""
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = SearchWebpageForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # start saving new webpage url
            search = GoogleSearch(form.cleaned_data['keyword'])
            query_object = Query.objects.get_or_create(
                keywords=form.cleaned_data['keyword'],
                times_used=1
            )
            search.start_search(max_page=form.cleaned_data['page'])
            add_list_url_to_webpage(search.search_result)
            for url in search.search_result:
                webpage = Webpage.objects.get(url=url)
                query_object = Query.objects.get(
                    keywords=form.cleaned_data['keyword'])
                Search.objects.create(webpage=webpage, query=query_object)
            return redirect('website_management:view_all_webpages')
    else:
        form = SearchWebpageForm()
    return render(request,
                  'website_management/search_webpage.html',
                  {'form': form})


@login_required
def add_new_keyword(request):
    """Display form to add new webpage"""
    if request.method == 'POST':
        form = AddNewKeywordForm(request.POST)
        if form.is_valid():
            Query.objects.create(keywords=form.cleaned_data['keywords'])
            return redirect('website_management:view_all_keywords')
    else:
        form = AddNewKeywordForm()
    return render(request,
                  'website_management/add_new_keyword.html',
                  {'form': form})


def view_all_keywords(request):
    """display all keywords"""
    queries = Query.objects.all().order_by('id').reverse()
    context = {'queries': []}
    for item in queries:
        context['queries'].append({'keyword': item.keywords,
                                   'date_added': item.date_added,
                                   'times_used': item.times_used,
                                   'id': item.id})
    return render(request,
                  'website_management/view_all_keywords.html', context)


def view_search_result(request):
    "display all search result, times, & keyword"
    searches = Search.objects.all().order_by('search_time').reverse()
    context = {'search_results': []}
    for search in searches:
        search_data = {'keywords': search.query,
                       'webpage': search.webpage,
                       'search_time': search.search_time}
        context['search_results'].append(search_data)
    return render(request, 'website_management/view_search_result.html',
                  context)
