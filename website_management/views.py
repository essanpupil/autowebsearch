from urlparse import urlparse

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger

from .models import Webpage, Domain, Homepage
from .forms import AddWebpageForm, SearchWebpageForm
from webscraper.pagescraper import PageScraper
from search_extractor.google_search import GoogleSearch


def website_dashboard(request):
    "display info summary about saved webpages, homepage, & domain"
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

def webpage_detail(request, web_id):
    "display detail info of selected webpage"
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
                'id': web.id,}
    if web.homepage == None:
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

def fetch_html_page(request, web_id):
    'downloading html source code of webpage'
    web = Webpage.objects.get(id=web_id)
    if web.html_page is None:
        page_scraper = PageScraper()
        page_scraper.fetch_webpage(web.url)
        web.html_page = page_scraper.html
        web.save()
    return redirect('website_management:webpage_detail', web_id = web.id)
    
def homepage_detail(request, hp_id):
    "display detail info of selected homepage"
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

def domain_detail(request, dom_id):
    "display detail info of selected domain"
    dom = get_object_or_404(Domain, id=dom_id)
    context = {'domname': dom.name,
                'domid': dom.id,
                'domadded': dom.date_added,
                'domhp': []}
    for item in dom.homepage_set.all():
        context['domhp'].append({'name': item.name, 'id': item.id})
    return render(request, 'website_management/domain_detail.html', context)

def add_new_webpage(request):
    "Display form to add new webpage"
    # if this is a POST request, we should process the form data
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = AddWebpageForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # start saving new webpage url
            Webpage.objects.create(url=form.cleaned_data['url'])
            return redirect('website_management:view_all_webpages')
        #~ else:
            #~ return redirect('website_management:add_new_webpage')
    else:
        form = AddWebpageForm()
    return render(request,
                    'website_management/add_new_webpage.html',
                    {'form': form})

def view_all_webpages(request):
    "display all webpage"
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
    "display all webpage"
    homes = Homepage.objects.all()
    context = {'homes': []}
    for item in homes:
        context['homes'].append({
            'name': item.name,
            'date_added': item.date_added,
            'domain': item.domain.name,
            'id': item.id})
    return render(request,
        'website_management/view_all_homepages.html', context)
    
def view_all_domains(request):
    "display all domain"
    doms = Domain.objects.all()
    context = {'doms': []}
    for item in doms:
        context['doms'].append({
            'name': item.name,
            'date_added': item.date_added,
            'id': item.id})
    return render(request,
        'website_management/view_all_domains.html', context)

def search_webpage(request):
    "display text input to start searching website in internet"
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = SearchWebpageForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # start saving new webpage url
            search = GoogleSearch(form.cleaned_data['keyword'])
            search.start_search(max_page=form.cleaned_data['page'])
            for item in search.search_result:
                try:
                    Webpage.objects.create(url=item)
                except IntegrityError:
                    continue
            return redirect('website_management:view_all_webpages')
        #~ else:
            #~ return redirect('website_management:add_new_webpage')
    else:
        form = SearchWebpageForm()
    return render(request,
                    'website_management/search_webpage.html',
                    {'form': form})
