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


#class DeleteClientHomepageForm(forms.Form):
#    "input client's homepage"
#    homepage = forms.ModelChoiceField(queryset=None)
#    #client_id = forms.IntegerField()
#    def __init__(self, client, *args, **kwargs):
#        super(DeleteClientHomepageForm, self).__init__(*args, **kwargs)
#        self.fields['homepage'].queryset = Website.objects.filter(
#                                               client=client)
#
#
#class EditClientForm(ModelForm):
#    "form with initial data to edit client's data"
#
