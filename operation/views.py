from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from operation.models import UseToSearch
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from WebScraper.WebSearch import GoogleSearch
from WebScraper.WebPageScraper import WebPageScraper
from models import Keyword, Operator, Webpage, Tokens
from SSlib.tokens import Tokenizer
from django.db import IntegrityError
from _mysql import NULL


def userlogin(request):
    'display login page'
#     if len(error_message) is not 0:
#         error = error_message
#     else:
#         error = None
    return render(request, 'operation/login.html',)

def process_login(request):
    'process the login form'
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('operation:dashboard',))
        else:
            url = reverse('login',)# kwargs={'error_message':'Invalid login'})
            return HttpResponseRedirect(url)
    else:
        url = reverse('login',)# kwargs={'error_message':'Invalid login'})
        return HttpResponseRedirect(url)

def process_logout(request):
    'log the user out my application'
    logout(request)
    return HttpResponseRedirect(reverse('login',))

@login_required(login_url="/")
def dashboard(request):
    'function to go to home page'
    return render(request, 'operation/dashboard/dashboard.html',)

@login_required(login_url="/")
def keywords(request):
    'display keywords page summary'
    kwords = Keyword.objects.all().order_by('create_time').reverse()
    paginator = Paginator(kwords, 10)
    page = request.GET.get('page')
    try:
        kwords = paginator.page(page)
    except PageNotAnInteger:
        kwords = paginator.page(1)
    except EmptyPage:
        kwords = paginator.page(paginator.num_pages)
    return render_to_response('operation/keywords/keywords.html', {'keywords':kwords})

@login_required(login_url="/")
def add_new_keyword(request):
    'display form to add new keyword'
    return render(request, 'operation/keywords/add_new_keyword.html',)

@login_required(login_url="/")
def process_add_new_keyword(request):
    'saving submitted keyword'
    Keyword.objects.create(words=request.POST['words'],
                           search_area=request.POST['search_area'],
                           create_time=timezone.now(),
                           user=request.user)
    return HttpResponseRedirect(reverse('operation:keywords'))

@login_required(login_url="/")
def tokens(request):
    'display page to view tokens from web pages'
    template = 'operation/tokens/tokens.html'
    token = Tokens.objects.all()
    paginator = Paginator(token, 10)
    page = request.GET.get('page')
    try:
        token = paginator.page(page)
    except PageNotAnInteger:
        token = paginator.page(1)
    except EmptyPage:
        token = paginator.page(paginator.num_pages)
    return render_to_response(template, {'tokens':token})
    #return render(request, template,{'tokens':token})

@login_required(login_url="/")
def view_all_tokens(request):
    'display all tokens in database'
    template = 'operation/tokens/tokens.html'
    token = Keyword.objects.all()
    return render(request, template,{'keyword':token})

@login_required(login_url="/")
def manual_search_webpages(request, keyword_id):
    'view to handle manual search by operator'
    try:
        keyword = Keyword.objects.get(id=keyword_id)
        if keyword.search_area == 'webpage':
            searching = GoogleSearch(keyword.words)
        searching.startSearch(maxPage=2)
        for result in searching.searchResult:
            try:
                web = Webpage.objects.create(url=result)
                UseToSearch.objects.create(keyword=keyword, webpage=web)
            except IntegrityError:
                web = Webpage.objects.get(url=result)
                UseToSearch.objects.create(webpage=web, keyword=keyword)
    except ObjectDoesNotExist:
        token = Tokens.objects.get(id=keyword_id)
        searching = GoogleSearch(token.sentence)
        searching.startSearch(maxPage=2)
        for result in searching.searchResult:
            try:
                web = Webpage.objects.create(url=result)
                UseToSearch.objects.create(token=token, webpage=web)
            except IntegrityError:
                web = Webpage.objects.get(url=result)
                UseToSearch.objects.create(webpage=web, token=token)
    return HttpResponseRedirect(reverse('operation:webpages',))

@login_required(login_url="/")
def manual_search_result(request):
    'display search result from manual search'
    webs = Webpage.objects.all()
    template = 'operation/tokens/manual_search_result.html'
    return render(request, template, {'webs':webs})

@login_required(login_url="/")
def fetch_html_source(request, web_id):
    "fetch the web's html source"
    web = Webpage.objects.get(id=web_id)
    if len(web.htmlPage) is 0:
        page_scraper = WebPageScraper(web.url)
        web.htmlPage = page_scraper.request
        web.save()
        token = Tokenizer(page_scraper.getTextBody())
        for item in token.sentence_tokens():
            try:
                tkn = Tokens.objects.create(sentence=item)
                tkn.webpages.add(web)
                tkn.save()
            except IntegrityError:
                tkn = Tokens.objects.get(sentence=item)
                tkn.webpages.add(web)
                tkn.save()
    url = reverse('operation:view_web_detail',kwargs={'web_id':web.id},)
    return HttpResponseRedirect(url)

@login_required(login_url="/")
def view_web_detail(request, web_id):
    'display detail info for web id'
    web = Webpage.objects.get(id=web_id)
    try:
        tokens = Tokens.objects.filter(webpages=web)[:10]
    except ObjectDoesNotExist:
        tokens = []
    template = 'operation/webpages/web_detail.html'
    context = {'web':web, 'tokens':tokens}
    return render(request, template, context)

@login_required(login_url="/")
def process_saving_inspection(request):
    'saving inspection edit'
    web_id = request.POST['web_id']
    web = Webpage.objects.get(id=web_id)
    scam_status = request.POST['scam']
    if scam_status == "True":
        web.scamStatus = True
        web.save()
    else:
        web.scamStatus = False
        web.save()
    report_status = request.POST['report']
    if report_status == "True":
        web.reportStatus = True
        web.save()
    else:
        web.reportStatus = False
        web.save()
    inspect_status = request.POST['inspection']
    if inspect_status == "True":
        web.inspectStatus = True
        web.save()
    else:
        web.inspectStatus = False
        web.save()
    access_status = request.POST['access']
    if access_status == "True":
        web.accessStatus = True
        web.save()
    else:
        web.accessStatus = False
        web.save()
    return HttpResponseRedirect(reverse('operation:view_web_detail', kwargs={'web_id':web_id}))

@login_required(login_url="/")
def report_website(request, web_id):
    'send report to website host'
    pass

@login_required(login_url="/")
def full_webpage_tokens(request, web_id):
    "display all webpage's tokens"
    web = Webpage.objects.get(id=web_id)
    try:
        tokens = Tokens.objects.filter(webpages=web)
    except ObjectDoesNotExist:
        tokens = []
    template = 'operation/webpages/full_webpage_token.html'
    context = {'web':web, 'tokens':tokens}
    return render(request, template, context)

@login_required(login_url="/")
def webpages(request, inspect=all, scam=all, report=all, access=all):
    'display all web pages database'
    webs = Webpage.objects.all().order_by('url').reverse()
    paginator = Paginator(webs, 10)
    page = request.GET.get('page')
    try:
        webs = paginator.page(page)
    except PageNotAnInteger:
        webs = paginator.page(1)
    except EmptyPage:
        webs = paginator.page(paginator.num_pages)
    return render_to_response('operation/webpages/webpages.html', {'webs':webs})

@login_required(login_url="/")
def add_new_webpage(request):
    'display input form to manualy submit new tokens'
    return render(request, 'operation/webpages/add_new_webpage.html',)

@login_required(login_url="/")
def process_add_new_webpage(request):
    'view to process submited form data of new token, no display'
    webpage_url = request.POST['url']
    if len(webpage_url) is 0:
        return render(request,
            'operation/webpages/add_new_webpage.html',
            {'error_message':'You had not write the web page url'}
        )
    else:
        try:
            Webpage.objects.create(url=webpage_url)
        except IntegrityError:
            return render(request,
                          'operation/webpages/add_new_webpage.html',
                          {'error_message':'Webpage already exist'}
                        )
        else:
            return HttpResponseRedirect(reverse('operation:webpages',))

@login_required(login_url="/")
def operator_detail(request):
    "display operator's detail"
    user = User.objects.get(username=request.user)
    try:
        operator = Operator.objects.get(user=user)
    except ObjectDoesNotExist:
        operator = NULL
    template = 'operation/operator/operator.html'
    context = {'operator':operator, 'user':user}
    return render(request, template, context)

@login_required(login_url="/")
def change_password_operator(request):
    'display form operator password change'
    return render(request, 'operation/operator/change_password.html')

@login_required(login_url="/")
def process_change_password_operator(request):
    "saving operator's new password"
    oldpassword = request.POST['oldpassword']
    newpassword1 = request.POST['newpassword1']
    newpassword2 = request.POST['newpassword2']
    user = User.objects.get(username=request.user)
    if (user.check_password(oldpassword)) == False:
        url = reverse('operation:change_password_result', kwargs={'message':'Password change failed Old password is not valid'},)
        return HttpResponseRedirect(url)
    elif newpassword1 != newpassword2:
        url = reverse('operation:change_password_result', kwargs={'message':'Password change failed New password confirmation is not valid'},)
        return HttpResponseRedirect(url)
    elif (user.check_password(oldpassword)) and (newpassword1 == newpassword2):
        user.set_password(newpassword1)
        user.save()
        url = reverse('operation:change_password_result', kwargs={'message':'Password change sucess'},)
        return HttpResponseRedirect(url)
    else:
        url = reverse('operation:change_password_result', kwargs={'message':'Password change failed Operation is not valid'},)
        return HttpResponseRedirect(url)

@login_required(login_url="/")
def change_password_result(request, message):
    'display the result of password change'
    template = 'operation/operator/change_password_result.html'
    context = {'message':message}
    return render(request, template, context)
