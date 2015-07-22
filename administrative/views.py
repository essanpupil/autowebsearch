from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Client, Event, Operator, Website
from .form import AddClientForm, AddClientHomepageForm, DeleteClientForm, \
                  AddEventForm, DeleteEventForm, AddOperatorForm, \
                  AddUserForm#,# EditUserForm
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
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
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



@login_required
def add_operator(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = AddOperatorForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passwd = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            client = form.cleaned_data['client']
            user = User.objects.create_user(username=uname,
                                            password=passwd,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,)
            operator = Operator.objects.create(client=client,
                                               user=user,)
            return redirect('administrative:view_operator', client.id)
    else:
        form = AddOperatorForm(initial={'client': client,})
    return render(request,
                  'administrative/add_operator.html',
                  {'form': form,
                   'client': {'id': client.id,
                              'name': client.name}})


def view_operator(request, client_id):
    'Display all operator form'
    client = get_object_or_404(Client, id=client_id)
    operators = Operator.objects.filter(client=client)
    context = {'operators': [],
               'client': {'id': client.id,
                          'name': client.name}}
    for operator in operators:
        operator_data = {'username': operator.user.get_username(),
                         'id': operator.id,
                         'fullname': operator.user.get_full_name(),
                         'email': operator.user.email,
                         'status': '',
                         'time_start': operator.date_start,
                         'time_end': operator.date_end}
        if operator.user.is_active:
            operator_data['status'] = 'Active'
        else:
            operator_data['status'] = 'Not Active'

        context['operators'].append(operator_data)
    paginator = Paginator(context['operators'], 10)
    page = request.GET.get('page')
    try:
        context['operators'] = paginator.page(page)
    except PageNotAnInteger:
        context['operators'] = paginator.page(1)
    except EmptyPage:
        context['operators'] = paginator.page(paginator.num_pages)
    return render(request, 'administrative/view_operator.html', context)


@login_required
def edit_operator(request, operator_id):
    "display edit operator form"
    operator = Operator.objects.get(id=operator_id)
    context = {'operator': {}, 'client': {}}
    context['client'] = {'id': operator.client.id,
                         'name': operator.client.name}
    context['operator'] = {'id': operator.id,
                           'username': operator.user.get_username(),
                           'first_name': operator.user.first_name,
                           'last_name': operator.user.last_name,
                           'email': operator.user.email,}
    return render(request, 'administrative/edit_operator.html', context)


@login_required
def edit_operator_process(request):
    operator = Operator.objects.get(id=request.POST['operator_id'])
    op_user = operator.user
    op_user.first_name = request.POST['first_name']
    op_user.last_name = request.POST['last_name']
    op_user.email = request.POST['email']
    op_user.save()
    return redirect('administrative:view_operator', operator.client.id)
#class EditOperator(UpdateView):
#    'Display edit client form'
#    model = Operator
#    fields = ['event']
#    template_name_suffix = '_edit_form'
#    
#    def get_context_data(self, **kwargs):
#        # call the base implementation first to get a context
#        context = super(EditOperator, self).get_context_data(**kwargs)
#        # add in a queryset of other context
#        context['client'] = {'id': self.object.client.id,
#                             'name': self.object.client.name,}
#        return context
#
#    def get_success_url(self, **kwargs):
#        success_url = reverse_lazy('administrative:view_operator', args=[self.object.client.id])
#        return success_url


def delete_operator(request, operator_id):
    'display delete operator confirmation'
    operator = Operator.objects.get(id=operator_id)
    context = {'operator': {}, 'client': {}}
    context['client'] = {'id': operator.client.id,
                         'name': operator.client.name}
    context['operator'] = {'id': operator.id,
                           'username': operator.user.get_username(),
                           'date_end': operator.date_end,}
    return render(request, 'administrative/delete_operator.html', context)


def delete_operator_process(request):
    "processing delete client (saving date_end)"
    operator = get_object_or_404(Operator, id=request.POST['id_operator'])
    if request.POST['status'] == "nonactive":
        operator.date_end = timezone.now()
        op_usr = operator.user
        op_usr.is_active = False
        op_usr.save()
        operator.save()
    elif request.POST['status'] == "active":
        operator.date_end = None
        op_usr.is_active = True
        op_usr.save()
        operator.save()
    else:
        pass
    return redirect('administrative:view_operator', operator.client.id)


def add_user(request):
    'display add user form'
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                       username = form.cleaned_data['username'],
                       password = form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.is_staff = True
            user.save()
            return redirect('administrative:view_user')
    else:
        form = AddUserForm()
    context = {'form': form,}
    return render(request, 'administrative/add_user.html', context)
    

class EditUser(UpdateView):
    model = User
    fields = ['is_staff', 'is_superuser']
    template_name = 'administrative/user_update_form.html'
    success_url = reverse_lazy('administrative:view_user')
#def edit_user(request, user_id):
#    "display edit operator form"
#    user = User.objects.get(id=user_id)
#    if request.method == 'POST':
#        form = EditUserForm(request.POST)
#        if form.is_valid():
#            return redirect('administrative/view_user.html')
#    else:
#        form = EditUserForm()
#    context = {'form': form,}
#    return render(request, 'administrative/edit_user.html', context)
class DeleteUser(UpdateView):
    model = User
    fields = ['is_active']
    template_name = 'administrative/user_update_form.html'
    success_url = reverse_lazy('administrative:view_user')


def view_user(request):
    "display all operator"
    users = User.objects.filter(operator=None).order_by('id').reverse()
    context = {'users': [],}
    for user in users:
        user_data = {'id': user.id,
                     'username': user.get_username(),
                     'fullname': user.get_full_name(),
                     'email': user.email,
                     'staff': user.is_staff,
                     'superuser': user.is_superuser,
                     'status': '',}
        if user.is_active:
            user_data['status'] = 'Active'
        else:
            user_data['status'] = 'Not Active'
        context['users'].append(user_data)
    paginator = Paginator(context['users'], 10)
    page = request.GET.get('page')
    try:
        context['users'] = paginator.page(page)
    except PageNotAnInteger:
        context['users'] = paginator.page(1)
    except EmptyPage:
        context['users'] = paginator.page(paginator.num_pages)
    return render(request, 'administrative/view_user.html', context)


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

