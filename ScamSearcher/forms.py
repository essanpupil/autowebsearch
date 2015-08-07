from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
