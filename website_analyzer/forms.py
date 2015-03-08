from django.forms import ModelForm
from django import forms

from website_management.models import Webpage
from .models import StringParameter


class AddScamWebsiteForm(ModelForm):
    "add known scam website to database"
    class Meta:
        model = Webpage
        fields = ['url']


class AddSequenceForm(ModelForm):
    "Add new sequence to database"
    class Meta:
        model = StringParameter
        fields = ['sentence', 'definitive']
