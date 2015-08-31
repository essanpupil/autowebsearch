from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from django import forms

from .models import Webpage, Query


class AddWebpageForm(ModelForm):
    """input new webpage url"""
    class Meta:
        model = Webpage
        fields = ['url']
        labels = {'url': _('Alamat halaman web'),}


class SearchWebpageForm(forms.Form):
    """form to manually search webpage"""
    keyword = forms.CharField(label='Kata kunci pencarian', max_length=255)
    page = forms.IntegerField(label='Jumlah halaman hasil pencarian', initial=1)


class AddNewKeywordForm(ModelForm):
    "Form to add new search keyword, which is saved in model Query"
    class Meta:
        model = Query
        fields = ['keywords']
        labels = {'keywords': _('Kata kunci pencarian')}
