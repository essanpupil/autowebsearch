from django.shortcuts import render

from website_management.models import Webpage, Domain, Homepage

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
    pass
    
def homepage_detail(request, hp_id):
    "display detail info of selected homepage"
    pass

def domain_detail(request, dom_id):
    "display detail info of selected domain"
    pass

def add_new_webpage(request):
    "Display form to add new webpage"
    pass

def add_new_homepage(request):
    "Display form to add new homepage"
    pass
    
def add_new_domain(request):
    "Display form to add new domain"
    pass

def view_all_webpage(request):
    "display all webpage"
    pass

def view_all_homepage(request):
    "display all homepage"
    pass
    
def view_all_domain(request):
    "display all domain"
    pass
