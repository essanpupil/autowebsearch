from django.forms import ModelForm, URLInput, HiddenInput, PasswordInput
from django.core import validators
from django import forms
from django.contrib.auth.models import User

from .models import Client, Website, Event, Operator, ClientKeyword


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


class AddClientKeywordForm(ModelForm):
    "input client's keyword"
    keywords =  forms.CharField()
    class Meta:
        model = ClientKeyword
        fields = ['keywords', 'client']
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


class AddUserForm(ModelForm):
    "Add new user"
    password_again = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        'custom clean to match password & password_again field'
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_again']:
            self._errors['password'] = ["Password do not match"]
            del form_data['password']
        return form_data
    class Meta:
        model = User
        fields = ('username', 'password', 'password_again', 'first_name', 
                  'last_name', 'email')
        widgets = {'password': PasswordInput(),}


#class EditUserForm(ModelForm):
