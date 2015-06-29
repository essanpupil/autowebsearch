from django.forms import ModelForm, URLInput
from django import forms

from .models import Client, Website


class AddClientForm(ModelForm):
    "input new client"
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address') 


class AddClientHomepageForm(ModelForm):
    "input client's homepage"
    class Meta:
        model = Website
        fields = ['homepage', 'event']
        widgets = {
            'homepage': URLInput(),
        }
