from django.forms import ModelForm
from django import forms

from .models import Webpage


class AddWebpageForm(ModelForm):
    "input new webpage url"
    class Meta:
        model = Webpage
        fields = ['url']

class SearchWebpageForm(forms.Form):
    "form to manually search webpage"
    keyword = forms.CharField(label='keyword')
    page = forms.IntegerField(label='page', initial=1)
