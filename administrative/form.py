from django.forms import ModelForm
from django import forms

from .models import Client


class AddClientForm(ModelForm):
    "input new client"
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address') 
