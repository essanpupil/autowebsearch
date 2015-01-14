from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from WebScraper.WebSearch import GoogleSearch
from WebScraper.WebPageScraper import WebPageScraper
from models import Keyword, Operator, Webpage

def login(request):
    'display login page'
    return render(request, 'operation/login.html',)

def dashboard(request):
    'function to go to home page'
    return render(request, 'operation/dashboard/dashboard.html',)

def tokens(request):
    'display page to view tokens from web pages'
    template = 'operation/tokens/tokens.html'
    token = Keyword.objects.all()
    return render(request, template,{'keyword':token})

def view_all_tokens(request):
    'display all tokens in database'
    template = 'operation/tokens/tokens.html'
    token = Keyword.objects.all()
    return render(request, template,{'keyword':token})

def add_new_token(request):
    'display input form to manualy submit new tokens'
    return render(request, 'operation/tokens/add_new_token.html',)

def process_add_new_token(request):
    'view to process submited form data of new token, no display'
    keyword = request.POST['words']
    if len(keyword) is 0:
        return render(request,
            'operation/tokens/add_new_token.html',
            {'error_message':'You had not write the keyword'}
        )
    else:
        #user = Operator.objects.get(username='testuser')
        words = Keyword(words=keyword)#, operator=user)
        words.save()
        return HttpResponseRedirect(reverse('operation:tokens',))

def manual_search(request, keyword_id):
    'view to handle manual search by operator'
    keyword = Keyword.objects.get(id=keyword_id)
    searching = GoogleSearch(keyword.words)
    searching.startSearch(maxPage=2)
    for result in searching.searchResult:
        web = Webpage.objects.create(url=result)
    return HttpResponseRedirect(reverse('operation:manual_search_result',))
    
def manual_search_result(request):
    'display search result from manual search'
    webs = Webpage.objects.all()
    template = 'operation/tokens/manual_search_result.html'
    return render(request, template, {'webs':webs})

def get_web_source(request, web_id):
    "fetch the web's html source"
    web = Webpage.objects.get(id=web_id)
    page_scraper = WebPageScraper(web.url)
    web.textBody = page_scraper.getTextBody()
    web.htmlBody = page_scraper.request
    web.save()
    url = reverse('operation:web_detail', kwargs={'web_id':web.id})
    return HttpResponseRedirect(url)

def web_detail(request, web_id):
    'display detail info for web id'
    web = Webpage.objects.get(id=web_id)
    template = 'operation/webpages/web_detail.html'
    context = {'web':web}
    return render(request, template, context)
    
    
def webpages(request):
    'display all web pages database'
    return render(request, 'operation/webpages/webpages.html',)

def view_all_webpages(request):
    'display webpages'
    template = 'operation/webpages/webpages.html'
    webpage = Webpage.objects.all()
    urls = []
    for url in webpage:
        urls.append(webpage.url)
    return render(request, template,{'webpage':urls})

def add_new_webpage(request):
    'display input form to manualy submit new tokens'
    return render(request, 'operation/webpages/add_new_webpage.html',)

def process_add_new_webpage(request):
    'view to process submited form data of new token, no display'
    webpage_url = request.POST['url']
    if len(webpage_url) is 0:
        return render(request,
            'operation/webpages/add_new_webpage.html',
            {'error_message':'You had not write the web page url'}
        )
    else:
        webpage = Webpage(url=webpage_url)
        words.save()
        return HttpResponseRedirect(reverse('operation:webpages',))

def settings(requests):
    'display website settings'
    pass
