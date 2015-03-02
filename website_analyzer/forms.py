from django.forms import ModelForm
from django import forms

from website_management.models import Webpage


class AddScamWebsiteForm(ModelForm):
    "add known scam website to database"
    class Meta:
        model = Webpage
        fields = ['url']
