from django.shortcuts import render

from .models import ExtendHomepage


def analyze_website(request):
    "Display page to analyze website, the last analysist result is displayed"
    return render(request, 'website_analyzer/analyze_website.html')


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
    pass


def add_scam_website(request):
    "manually add website known as scam"
    pass


def view_scam_website(request):
    "display scam website"
    pass


def view_sequence(request):
    "display sequence parameter used for analyze website"
    pass
