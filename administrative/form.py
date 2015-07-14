from django.forms import ModelForm, URLInput, HiddenInput
from django.core import validators
from django import forms
from django.contrib.auth.models import User

from .models import Client, Website, Event, Operator


class AddClientForm(ModelForm):
    "input new client"
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address') 


class AddOperatorForm(ModelForm):
    "input new operator"
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput)
    class Meta:
        model = Operator
        fields = ('username',
                  'password',
                  'password_again',
                  'first_name',
                  'last_name',
                  'email',
                  'client',)
        widgets = {'client': HiddenInput(),}

class AddClientHomepageForm(ModelForm):
    "input client's homepage"
    url =  forms.URLField(validators=[validators.URLValidator])
    class Meta:
        model = Website
        fields = ['url', 'event', 'client']
        widgets = {
            'client': HiddenInput(),
        }


class DeleteEventForm(forms.Form):
    "input new client"
    deactive = forms.BooleanField()


class DeleteClientForm(forms.Form):
    "input new client"
    deactive = forms.BooleanField()


class AddEventForm(ModelForm):
    "save event for specific client"
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {'client': HiddenInput(),}
