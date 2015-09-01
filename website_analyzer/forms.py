from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from website_management.models import Webpage, Homepage
from .models import StringParameter, ExtendHomepage, ExtendDomain


class AddScamWebsiteForm(ModelForm):
    """add known scam website to database"""
    class Meta:  # lint:ok
        model = Webpage
        fields = ['url']
        labels = {'url': _('Alamat halaman web'),}


class AddSequenceForm(ModelForm):
    """Add new sequence to database"""
    class Meta:  # lint:ok
        model = StringParameter
        fields = ['sentence', 'definitive','target_analyze']
        labels = {'sentence': _('Parameter analisa'),
                  'definitive': _('Apakah definitif'),
                  'target_analyze': _('Target analisa'),
                 }


class EditAnalystForm(ModelForm):
    "Form to edit analyst data of website"
    date_added = ''
    def __init__(self, *args, **kwargs):
        super(EditAnalystForm, self).__init__(*args, **kwargs)
    class Meta:
        model = ExtendHomepage
        exclude = ['homepage']


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
