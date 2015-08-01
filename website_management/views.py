import tldextract

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import Webpage, Domain, Homepage, Search, Query
from .forms import AddWebpageForm, SearchWebpageForm, AddNewKeywordForm
from .management_lib import add_list_url_to_webpage, add_url_to_webpage
from webscraper.pagescraper import PageScraper
from search_extractor.google_search import GoogleSearch

from website_analyzer.models import ExtendWebpage
from website_analyzer.analyzer_lib import fill_text_body


@login_required
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
    for web in webs.order_by('id').reverse()[0:5]:
        context['newest_5_web'].append({'url': web.url, 'id': web.id})
    for hp in homepages.order_by('id').reverse()[0:5]:
        context['newest_5_hp'].append({'name': hp.name, 'id': hp.id})
    for dom in domains.order_by('id').reverse()[0:5]:
        context['newest_5_dom'].append({'name': dom.name, 'id': dom.id})
    return render(request, 'website_management/dashboard.html', context)


@login_required
def webpage_detail(request, web_id):
    """display detail info of selected webpage"""
    web = get_object_or_404(Webpage, id=web_id)
    web_data = {'url': web.url,
                'hp': '',
                'idhp': '',
                'iddom': '',
                'dom': '',
                'added': web.date_added,
                'status': web.last_response,
                'last_check': web.last_response_check,
                'html_page': bool(web.html_page),
                'text_body': '',
                'id': web.id, }
    if web.html_page != None:
        page = PageScraper()
        extw, created = ExtendWebpage.objects.get_or_create(webpage=web)
        fill_text_body(extw)
        web_data['text_body'] = extw.text_body
    else:
        web_data['text_body'] = None
    if web.homepage is None:
        web_data['hp'] = None
        web_data['idhp'] = None
        web_data['iddom'] = None
        web_data['dom'] = None
    else:
        web_data['hp'] = web.homepage.name
        web_data['idhp'] = web.homepage.id
        web_data['iddom'] = web.homepage.domain.id
        web_data['dom'] = web.homepage.domain.name
    return render(request,
                  'website_management/web_detail.html',
                  {'web': web_data})


@login_required
def fetch_html_page(request, web_id):
    """downloading html source code of webpage"""
    web = get_object_or_404(Webpage, id=web_id)
    ext = tldextract.extract(web.url)
    dom, created = Domain.objects.get_or_create(name=".".join(ext[1:]))
    hp, created2 = Homepage.objects.get_or_create(name=".".join(ext),
                                                  domain=dom)
    web.homepage = hp
    web.save()
    page_scraper = PageScraper()
    page_scraper.fetch_webpage(web.url)
    web.html_page = page_scraper.html
    web.save()
    return redirect('website_management:webpage_detail', web_id=web.id)


@login_required
def get_domain_homepage(request, web_id):
    """extract domain and homepage from webpage's url"""
    web = get_object_or_404(Webpage, id=web_id)
    ext = tldextract.extract(web.url)
    dom, created = Domain.objects.get_or_create(name=".".join(ext[1:]))
    hp, created2 = Homepage.objects.get_or_create(name=".".join(ext),
                                                  domain=dom)
    web.homepage = hp
    web.save()
    return redirect('website_management:webpage_detail', web_id=web.id)


@login_required
def homepage_detail(request, hp_id):
    """display detail info of selected homepage"""
    hp = get_object_or_404(Homepage, id=hp_id)
    context = {'hpname': hp.name,
               'hpid': hp.id,
               'hpadded': hp.date_added,
               'hpdomain': hp.domain.name,
               'iddom': hp.domain.id,
               'hpweb': []}
    for item in hp.webpage_set.all():
        context['hpweb'].append({'url': item.url, 'id': item.id})
    return render(request, 'website_management/homepage_detail.html', context)


@login_required
def domain_detail(request, dom_id):
    """display detail info of selected domain"""
    dom = get_object_or_404(Domain, id=dom_id)
    context = {'domname': dom.name,
               'domid': dom.id,
               'domadded': dom.date_added,
               'domhp': []}
    for item in dom.homepage_set.all():
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


@login_required
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


@login_required
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


@login_required
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
                                        keywords=form.cleaned_data['keyword'])
            search.start_search(max_page=form.cleaned_data['page'])
            add_list_url_to_webpage(search.search_result)
            for url in search.search_result:
                webpage = Webpage.objects.get(url=url)
                query_object = Query.objects.get(
                                   keywords=form.cleaned_data['keyword'])
                saved_search = Search.objects.create(webpage=webpage,
                                                     query=query_object)
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
            query = Query.objects.create(keywords=form.cleaned_data['keywords'])
            return redirect('website_management:view_all_keywords')
    else:
        form = AddNewKeywordForm()
    return render(request,
                  'website_management/add_new_keyword.html',
                  {'form': form})


@login_required
def view_all_keywords(request):
    """display all keywords"""
    queries = Query.objects.all().order_by('id').reverse()
    context = {'queries': []}
    for item in queries:
        context['queries'].append({'keyword': item.keywords,
                                   'date_added': item.date_added,
                                   'id': item.id})
    return render(request,
                  'website_management/view_all_keywords.html', context)
