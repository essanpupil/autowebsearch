from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Client, Event, Operator, Website
from .form import AddClientForm, AddClientHomepageForm, DeleteClientForm, \
                  AddEventForm, DeleteEventForm
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
                       'address': item.address}
        if item.date_end == None:
            client_data['status'] = 'Active'
        else:
            client_data['status'] = 'Not Active'
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
        client_data['status'] = 'Not Active'
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

class EditClient(UpdateView):
    'Display edit client form'
    model = Client
    success_url = reverse_lazy('administrative:view_client')
    fields = ['name', 'email', 'phone', 'address']
    template_name_suffix = '_edit_form'


def delete_client(request, client_id):
    'function to set date_end value (delete) to client'
    client = Client.objects.get(id=client_id)
    form = DeleteClientForm()
    return render(request,
                  'administrative/delete_client.html',
                  {'form':form,
                   'client': {'id': client.id,
                              'name': client.name}
              })


def delete_client_process(request):
    "processing delete client (saving date_end)"
    client = get_object_or_404(Client, id=request.POST['id_client'])
    if request.POST['status'] == "deactive":
        client.date_end = timezone.now()
        client.save()
    elif request.POST['status'] == "active":
        client.date_end = None
        client.save()
    else:
        pass
    return redirect('administrative:detail_client', client.id)



def add_operator(request, client_id):
    'Display add operator form'
    pass


def view_operator(request, client_id):
    'Display all operator form'
    pass


def edit_operator(request, operator_id):
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


def add_event(request, client_id):
    "display add event form"
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            event = Event.objects.create(
                        client=client,
                        name=form.cleaned_data['name'],
                        time_end=form.cleaned_data['time_end'])
            return redirect('administrative:view_event', client_id=client_id)
    else:
        client = Client.objects.get(id=client_id)
        form = AddEventForm(initial={'client': client,})
    return render(request,
                  'administrative/add_event.html',
                  {'form':form,
                   'client': {'id': client.id,
                              'name': client.name}
                  })


def delete_event(request, event_id):
    "display delete event confirmation"
    event = Event.objects.get(id=event_id)
    form = DeleteEventForm()
    return render(request,
                  'administrative/delete_event.html',
                  {'form': form,
                   'event': event,
                   'client': {'id': event.client.id,
                              'name': event.client.name}
                  })


def delete_event_process(request):
    "processing delete event (saving date_end)"
    event = get_object_or_404(Event, id=request.POST['id_event'])
    if request.POST['status'] == "ended":
        event.time_end = timezone.now()
        event.save()
    elif request.POST['status'] == "keepgoing":
        event.time_end = None
        event.save()
    else:
        pass
    return redirect('administrative:detail_event', event.id)


def detail_event(request, event_id):
    "display delete event confirmation"
    event = Event.objects.get(id=event_id)
    context = {'event': '',
               'client': {'id': event.client.id,
                          'name': event.client.name}}
    event_data = {'client': event.client.name,
                  'name': event.name,
                  'time_start': event.time_start,
                  'time_end': event.time_end,
                  'status': '',
                  'websites': []}
    if event.time_end is None:
        event_data['status'] = 'Ongoing'
    else:
        event_data['status'] = 'Ended'
    for website in Website.objects.filter(event=event):
        event_data['website'].append({'name': website.homepage.name,
                                     'id': website.homepage.id,})
    context['event'] = event_data                                     
    return render(request, 'administrative/detail_event.html', context)


def view_event(request, client_id):
    "display all event"
    client = get_object_or_404(Client, id=client_id)
    events = Event.objects.filter(client=client)
    context = {'events': [],
               'client': {'id': client.id,
                          'name': client.name}}
    for event in events:
        event_data = {'name': event.name,
                      'id': event.id,
                      'status': '',
                      'time_start': event.time_start,
                      'time_end': event.time_end}
        if event.time_end == None:
            event_data['status'] = 'Ongoing'
        else:
            event_data['status'] = 'Ended'
        context['events'].append(event_data)
    return render(request, 'administrative/view_event.html', context)


def view_all_event(request):
    "display all event"
    pass


class EditEvent(UpdateView):
    'Display edit event form'
    model = Event
    fields = ['name',]
    template_name_suffix = '_edit_form'
    
    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(EditEvent, self).get_context_data(**kwargs)
        # add in a queryset of other context
        context['client'] = {'id': self.object.client.id,
                             'name': self.object.client.name,}
        return context

    def get_success_url(self, **kwargs):
        success_url = reverse_lazy('administrative:view_event', args=[self.object.client.id])
        return success_url

