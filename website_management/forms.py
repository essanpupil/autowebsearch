from django.forms import ModelForm

from .models import Webpage


class AddWebpageForm(ModelForm):
    "input new webpage url"
    class Meta:
        model = Webpage
        fields = ['url']
