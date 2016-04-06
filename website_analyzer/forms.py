"""forms module for website_analyzer app."""
from django.forms import ModelForm
from django import forms

from website_management.models import Webpage
from website_analyzer.models import StringParameter, ExtendWebsite, \
                                    ExtendDomain


class AddScamWebsiteForm(ModelForm):
    """add known scam website to database"""
    class Meta:  # lint:ok
        model = Webpage
        fields = ['url']


class AddSequenceForm(ModelForm):
    """Add new sequence to database"""
    class Meta:  # lint:ok
        model = StringParameter
        fields = ['sentence', 'definitive', 'target_analyze']


class EditAnalystForm(ModelForm):
    "Form to edit analyst data of website"
    date_added = ''

    def __init__(self, *args, **kwargs):
        super(EditAnalystForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExtendWebsite
        exclude = ['website']


class EditAnalystDomainForm(ModelForm):
    "Form to edit analyst data of website"
    date_added = ''

    def __init__(self, *args, **kwargs):
        super(EditAnalystDomainForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExtendDomain
        exclude = ['domain']


class SearchForm(forms.Form):
    "search extendsomain by domain name"
    search = forms.CharField()
