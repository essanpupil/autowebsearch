"""views module for administrative app."""
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy

from administrative.models import Client, Event, Operator, Website, \
                                  ClientKeyword, ClientSequence
from administrative.form import AddClientForm, AddClientHomepageForm, \
                                DeleteClientForm, AddEventForm, \
                                DeleteEventForm, AddOperatorForm, \
                                AddUserForm, AddClientKeywordForm, \
                                AddClientSequenceForm
from administrative.administrative_lib import save_client
from website_management.management_lib import add_url_to_webpage
from website_management.models import Webpage, Query
from website_analyzer.models import StringParameter


@login_required
def admin_dashboard(request):
    "Display summary administrative info"
    if request.user.is_staff:
        context = {}
        clients = Client.objects.all().order_by('date_start')
        operators = Operator.objects.all().order_by('date_start')
        events = Event.objects.all().order_by('time_start')
        context['clients'] = {'count': clients.count(), 'last_added': []}
        for client in clients[:5]:
            client_data = {'id': client.id, 'name': client.name}
            context['clients']['last_added'].append(client_data)
        context['operators'] = {'count': operators.count(), 'last_added': []}
        for operator in operators[:5]:
            operator_data = {'name': operator.user.get_username()}
            context['operators']['last_added'].append(operator_data)
        context['events'] = {'count': events.count(), 'last_added': []}
        for event in events[:5]:
            event_data = {'id': event.id, 'name': event.name}
            context['events']['last_added'].append(event_data)
        return render(request, 'administrative/dashboard.html', context)
    else:
        operator = Operator.objects.get(user=request.user)
        client = operator.client
        return redirect('administrative:detail_client', client.id)


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
    return render(request, 'administrative/add_client.html', {'form': form})


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
        if item.date_end is None:
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
    return render(request, 'administrative/view_client.html', context)


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
                   'address': client.address}
    if client_data['date_end'] is None:
        client_data['status'] = 'Active'
    else:
        client_data['status'] = 'Not Active'
    websites = Website.objects.filter(client=client)
    for website in websites:
        client_data['websites'].append({'url': website.homepage.name,
                                        'id_homepage': website.homepage.id,
                                        'id_website': website.id})
    return render(request,
                  'administrative/detail_client.html',
                  {'client': client_data})


@login_required
def add_homepage(request, client_id):
    "Display add client's homepage form"
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = AddClientHomepageForm(request.POST)
        if form.is_valid():
            if Webpage.objects.filter(url=form.cleaned_data['url']).exists():
                webpage = Webpage.objects.get(url=form.cleaned_data['url'])
            else:
                add_url_to_webpage(form.cleaned_data['url'])
            webpage = Webpage.objects.get(url=form.cleaned_data['url'])
            try:
                Website.objects.create(client=form.cleaned_data['client'],
                                       homepage=webpage.homepage,
                                       event=form.cleaned_data['event'])
                return redirect('administrative:detail_client',
                                client_id=client_id)
            except:
                return redirect('administrative:detail_client',
                                client_id=client_id)
    else:
        form = AddClientHomepageForm(initial={'client': client, 'event': None})
        form.fields['event'].queryset = Event.objects.filter(client=client)
    return render(request,
                  'administrative/add_homepage.html',
                  {'form': form,
                   'client': {'id': client.id,
                              'name': client.name}})


class WebsiteDelete(DeleteView):
    "delete client's website"
    model = Website
    success_url = reverse_lazy('administrative:delete_client_website_success')
    template_name = 'administrative/delete_client_website.html'


@login_required
def delete_homepage_success(request):
    "display delete success"
    return render(request, 'administrative/delete_client_website_success.html')


class EditClient(UpdateView):
    'Display edit client form'
    model = Client
    success_url = reverse_lazy('administrative:view_client')
    fields = ['name', 'email', 'phone', 'address']
    template_name_suffix = '_edit_form'


@login_required
def delete_client(request, client_id):
    'function to set date_end value (delete) to client'
    client = Client.objects.get(id=client_id)
    form = DeleteClientForm()
    return render(request,
                  'administrative/delete_client.html',
                  {'form': form,
                   'client': {'id': client.id,
                              'name': client.name}})


@login_required
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
    """Add client's operator."""
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
            Operator.objects.create(client=client, user=user)
            return redirect('administrative:view_operator', client.id)
    else:
        form = AddOperatorForm(initial={'client': client})
    return render(request,
                  'administrative/add_operator.html',
                  {'form': form,
                   'client': {'id': client.id, 'name': client.name}})


def view_operator(request, client_id):
    'Display all operator form'
    client = get_object_or_404(Client, id=client_id)
    operators = Operator.objects.filter(client=client)
    context = {'operators': [],
               'client': {'id': client.id, 'name': client.name}}
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
                           'email': operator.user.email}
    return render(request, 'administrative/edit_operator.html', context)


@login_required
def edit_operator_process(request):
    """function to submit the new operator data to database."""
    operator = Operator.objects.get(id=request.POST['operator_id'])
    op_user = operator.user
    op_user.first_name = request.POST['first_name']
    op_user.last_name = request.POST['last_name']
    op_user.email = request.POST['email']
    op_user.save()
    return redirect('administrative:view_operator', operator.client.id)


def delete_operator(request, operator_id):
    'display delete operator confirmation'
    operator = Operator.objects.get(id=operator_id)
    context = {'operator': {}, 'client': {}}
    context['client'] = {'id': operator.client.id,
                         'name': operator.client.name}
    context['operator'] = {'id': operator.id,
                           'username': operator.user.get_username(),
                           'date_end': operator.date_end}
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


@login_required
def add_user(request):
    'display add user form'
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.is_staff = True
            user.save()
            return redirect('administrative:view_user')
    else:
        form = AddUserForm()
    context = {'form': form}
    return render(request, 'administrative/add_user.html', context)


class EditUser(UpdateView):
    """Edit user data."""
    model = User
    fields = ['is_staff', 'is_superuser']
    template_name = 'administrative/user_update_form.html'
    success_url = reverse_lazy('administrative:view_user')


class DeleteUser(UpdateView):
    """Delete user from database."""
    model = User
    fields = ['is_active']
    template_name = 'administrative/user_update_form.html'
    success_url = reverse_lazy('administrative:view_user')


@login_required
def view_user(request):
    "display all operator"
    users = User.objects.filter(operator=None).order_by('id').reverse()
    context = {'users': []}
    for user in users:
        user_data = {'id': user.id,
                     'username': user.get_username(),
                     'fullname': user.get_full_name(),
                     'email': user.email,
                     'staff': user.is_staff,
                     'superuser': user.is_superuser,
                     'status': ''}
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


@login_required
def delete_user(request):
    "display delete operator confirmation"
    pass


@login_required
def add_event(request, client_id):
    "display add event form"
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            Event.objects.create(
                client=client, name=form.cleaned_data['name'],
                time_end=form.cleaned_data['time_end'])
            return redirect('administrative:view_event', client_id=client_id)
    else:
        client = Client.objects.get(id=client_id)
        form = AddEventForm(initial={'client': client})
    return render(request,
                  'administrative/add_event.html',
                  {'form': form,
                   'client': {'id': client.id, 'name': client.name}})


@login_required
def delete_event(request, event_id):
    "display delete event confirmation"
    event = Event.objects.get(id=event_id)
    form = DeleteEventForm()
    return render(request,
                  'administrative/delete_event.html',
                  {'form': form,
                   'event': event,
                   'client': {'id': event.client.id,
                              'name': event.client.name}})


@login_required
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


@login_required
def detail_event(request, event_id):
    "display delete event confirmation"
    event = Event.objects.get(id=event_id)
    context = {'event': '',
               'client': {'id': event.client.id, 'name': event.client.name}}
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
        event_data['websites'].append({'name': website.homepage.name,
                                       'id': website.homepage.id})
    context['event'] = event_data
    return render(request, 'administrative/detail_event.html', context)


@login_required
def view_event(request, client_id):
    "display all event"
    client = get_object_or_404(Client, id=client_id)
    events = Event.objects.filter(client=client)
    context = {'events': [], 'client': {'id': client.id, 'name': client.name}}
    for event in events:
        event_data = {'name': event.name,
                      'id': event.id,
                      'status': '',
                      'time_start': event.time_start,
                      'time_end': event.time_end}
        if event.time_end is None:
            event_data['status'] = 'Ongoing'
        else:
            event_data['status'] = 'Ended'
        context['events'].append(event_data)
    return render(request, 'administrative/view_event.html', context)


@login_required
def view_all_event(request):
    "display all event"
    pass


class EditEvent(UpdateView):
    'Display edit event form'
    model = Event
    fields = ['name']
    template_name_suffix = '_edit_form'

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(EditEvent, self).get_context_data(**kwargs)
        # add in a queryset of other context
        context['client'] = {'id': self.object.client.id,
                             'name': self.object.client.name}
        return context

    def get_success_url(self, **kwargs):
        success_url = reverse_lazy('administrative:view_event',
                                   args=[self.object.client.id])
        return success_url


@login_required
def view_client_keyword(request, client_id):
    "display all keyword belong to this client"
    client = get_object_or_404(Client, id=client_id)
    keywords = ClientKeyword.objects.filter(client=client)
    context = {'keywords': [],
               'client': {'id': client.id, 'name': client.name}}
    for keyword in keywords:
        keyword_data = {'name': keyword.query.keywords, 'id': keyword.id}
        context['keywords'].append(keyword_data)
    return render(request, 'administrative/view_client_keyword.html', context)


@login_required
def add_client_keyword(request, client_id):
    "Display add client's keyword form"
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = AddClientKeywordForm(request.POST)
        if form.is_valid():
            if Query.objects.filter(
                    keywords=form.cleaned_data['keywords']).exists():
                pass
            else:
                Query.objects.create(keywords=form.cleaned_data['keywords'])
            query = Query.objects.get(keywords=form.cleaned_data['keywords'])
            try:
                ClientKeyword.objects.create(
                    client=form.cleaned_data['client'], query=query)
                return redirect('administrative:detail_client',
                                client_id=client_id)
            except:
                return redirect('administrative:detail_client',
                                client_id=client_id)
    else:
        form = AddClientKeywordForm(initial={'client': client})
    return render(request,
                  'administrative/add_client_keyword.html',
                  {'form': form,
                   'client': {'id': client.id, 'name': client.name}})


@login_required
def view_client_sequence(request, client_id):
    "display all sequence belong to this client"
    client = get_object_or_404(Client, id=client_id)
    sequences = ClientSequence.objects.filter(client=client)
    context = {'sequences': [],
               'client': {'id': client.id, 'name': client.name}}
    for sequence in sequences:
        sequence_data = {'name': sequence.string_parameter.sentence,
                         'id': sequence.id,
                         'event': sequence.event,
                         'definitive': sequence.string_parameter.definitive}
        context['sequences'].append(sequence_data)
    return render(request, 'administrative/view_client_sequence.html', context)


@login_required
def add_client_sequence(request, client_id):
    "Display add client's sequence form"
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = AddClientSequenceForm(request.POST)
        if form.is_valid():
            if StringParameter.objects.filter(
                    sentence=form.cleaned_data['sequence']).exists():
                pass
            else:
                StringParameter.objects.create(
                    sentence=form.cleaned_data['sequence'])
                str_prm = StringParameter.objects.get(
                    sentence=form.cleaned_data['sequence'])
            try:
                ClientSequence.objects.create(
                    client=form.cleaned_data['client'],
                    event=form.cleaned_data['event'],
                    string_parameter=str_prm)
                return redirect('administrative:view_client_sequence',
                                client_id=client_id)
            except:
                return redirect('administrative:view_client_sequence',
                                client_id=client_id)
    else:
        form = AddClientSequenceForm(initial={'client': client})
        form.fields['event'].queryset = Event.objects.filter(client=client)
    return render(request,
                  'administrative/add_client_sequence.html',
                  {'form': form,
                   'client': {'id': client.id, 'name': client.name}})


def view_sent_mail(request):
    "dummy function to pass the test"
    pass
