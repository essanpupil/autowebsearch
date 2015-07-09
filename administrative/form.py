from django.forms import ModelForm, URLInput, HiddenInput
from django.core import validators
from django import forms

from .models import Client, Website, Event


class AddClientForm(ModelForm):
    "input new client"
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address') 


class AddClientHomepageForm(ModelForm):
    "input client's homepage"
    url =  forms.URLField(validators=[validators.URLValidator])
    class Meta:
        model = Website
        fields = ['url', 'event', 'client']
        widgets = {
            'client': HiddenInput(),
        }


class DeleteClientForm(forms.Form):
    "input new client"
    deactive = forms.BooleanField()


class AddEventForm(ModelForm):
    "save event for specific client"
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {'client': HiddenInput(),}
