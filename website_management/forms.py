from django.forms import ModelForm
from django import forms

from .models import Webpage, Query


class AddWebpageForm(ModelForm):
    """input new webpage url"""
    class Meta:
        model = Webpage
        fields = ['url']


class SearchWebpageForm(forms.Form):
    """form to manually search webpage"""
    keyword = forms.CharField(label='keyword', max_length=255)
    page = forms.IntegerField(label='page', initial=1)


class AddNewKeywordForm(ModelForm):
    "Form to add new search keyword, which is saved in model Query"
    class Meta:
        model = Query
        fields = ['keywords']
