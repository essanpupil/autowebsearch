from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Client, Event, Operator, Website
from .form import AddClientForm, AddClientHomepageForm, DeleteClientHomepageForm
from .administrative_lib import save_client, save_client_homepage
from website_management.management_lib import add_url_to_webpage
from website_management.models import Webpage


@login_required
def admin_dashboard(request):
    "Display summary administrative info"
    context = {}
    users = User.objects.all()
    clients = Client.objects.all().order_by('date_start')
    context['clients'] = {'count': clients.count(),
                          'last_added': [],}
    for client in clients[:5]:
        client_data = {'id': client.id,
                       'name': client.name,}
        context['clients']['last_added'].append(client_data)
    events = Event.objects.all()
    return render(request, 'administrative/dashboard.html', context)


@login_required
def add_client(request):
    'Display add client form'
    # if this is a POST request, the data should be processed
    if request.method == 'POST':
        # create form instance and populate with data from the request
        form = AddClientForm(request.POST)
        # check the form is valid or not
        if form.is_valid():
            # start saving new client to database
            save_client(name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'])
            return redirect('administrative:view_client')
    else:
        form = AddClientForm()
    return render(request,
                  'administrative/add_client.html',
                  {'form':form})


@login_required
def view_client(request):
    'Display all client'
    clients = Client.objects.all().order_by('date_start').reverse()
    context = {'clients': []}
    for item in clients:
        client_data = {'id': item.id,
                       'name': item.name,
                       'email': item.email,
                       'phone': item.phone,
                       'status': '',
                      # 'date_start': item.date_start,
                      # 'date_end': item.date_end,
                       'address': item.address}
        if item.date_end == None:
            client_data['status'] = 'Active'
        else:
            client_data['status'] = 'Deleted'
        context['clients'].append(client_data)
    paginator = Paginator(context['clients'], 10)
    page = request.GET.get('page')
    try:
        context['clients'] = paginator.page(page)
    except PageNotAnInteger:
        context['clients'] = paginator.page(1)
    except EmptyPage:
        context['clients'] = paginator.page(paginator.num_pages)
    return render(request,
                  'administrative/view_client.html', context)
        

@login_required
def detail_client(request, client_id):
    "Display detail client's data"
    client = get_object_or_404(Client, id=client_id)
    client_data = {'id': client.id,
                   'name': client.name,
                   'email': client.email,
                   'phone': client.phone,
                   'date_start': client.date_start,
                   'date_end': client.date_end,
                   'status': '',
                   'websites': [],
                   'address': client.address,}
    if client_data['date_end'] == None:
        client_data['status'] = 'Active'
    else:
        client_data['status'] = 'Deleted'
    websites = Website.objects.filter(client=client)
    for website in websites:
        client_data['websites'].append({'url': website.homepage.name,
                                        'id_homepage': website.homepage.id,
                                        'id_website': website.id})
    return render(request, 'administrative/detail_client.html',
                  {'client': client_data})


@login_required
def add_homepage(request, client_id):
    "Display add client's homepage form"
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = AddClientHomepageForm(request.POST)
        if form.is_valid():
            add_url_to_webpage(form.cleaned_data['url'])
            webpage = Webpage.objects.get(url=form.cleaned_data['url'])
            Website.objects.create(client=form.cleaned_data['client'],
                homepage=webpage.homepage,
                event=form.cleaned_data['event'])
            return redirect('administrative:detail_client', client_id=client_id)
    else:
        form = AddClientHomepageForm(initial={'client':client, 'event':None})
    return render(request,
                  'administrative/add_homepage.html',
                  {'form':form,
                   'client': {'id': client.id,
                              'name': client.name}
                  })


#@login_required
class WebsiteDelete(DeleteView):
    "delete client's website"
    model = Website
    success_url = reverse_lazy('administrative:delete_client_website_success')
    template_name = 'administrative/delete_client_website.html'


def delete_homepage_success(request):
    "display delete success"
    return render(request, 'administrative/delete_client_website_success.html')

def edit_client(request):
    'Display edit client form'
    pass


def delete_client(request, client_id):
    'Display delete client confirmation'
    pass


def add_operator(request):
    'Display add operator form'
    pass


def view_operator(request):
    'Display all operator form'
    pass


def edit_operator(request):
    'display edit operator form'
    pass


def delete_operator(request):
    'display delete operator confirmation'
    pass


def add_user(request):
    'display add user form'
    pass


def edit_user(request):
    "display edit operator form"
    pass


def view_user(request):
    "display all operator"
    pass


def delete_user(request):
    "display delete operator confirmation"
    pass


def add_event(request):
    "display add event form"
    pass


def delete_event(request):
    "display delete event confirmation"
    pass


def view_event(request):
    "display all event"
    pass


def edit_event(request):
    "display edit event form"
    pass
