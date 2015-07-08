from django.forms import ModelForm, URLInput, HiddenInput
from django.core import validators
from django import forms

from .models import Client, Website


class AddClientForm(ModelForm):
    "input new client"
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'address') 


class AddClientHomepageForm(ModelForm):
    "input client's homepage"
    url =  forms.URLField(validators=[validators.URLValidator])
    class Meta:
        model = Website
        fields = ['url', 'event', 'client']
        widgets = {
            'client': HiddenInput(),
        }


class DeleteClientHomepageForm(forms.Form):
    "input client's homepage"
    homepage = forms.ModelChoiceField(queryset=None)
    #client_id = forms.IntegerField()
    def __init__(self, client, *args, **kwargs):
        super(DeleteClientHomepageForm, self).__init__(*args, **kwargs)
        self.fields['homepage'].queryset = Website.objects.filter(
                                               client=client)
       # self.fields['client_id'].widget = forms.HiddenInput()
       # self.fields['client_id'].initial = client_obj.id
    #class Meta:
    #    model = Website
    #    fields = ['homepage', 'client']
    #    widgets = {
    #        'client': HiddenInput(),
    #    }
