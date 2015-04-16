from django.forms import ModelForm

from website_management.models import Webpage, Homepage
from .models import StringParameter, ExtendHomepage


class AddScamWebsiteForm(ModelForm):

    """add known scam website to database"""
    class Meta:  # lint:ok
        model = Webpage
        fields = ['url']


class AddSequenceForm(ModelForm):

    """Add new sequence to database"""
    class Meta:  # lint:ok
        model = StringParameter
        fields = ['sentence', 'definitive']


class EditAnalystForm(ModelForm):
    "Form to edit analyst data of website"
    date_added = ''
    def __init__(self, *args, **kwargs):
        super(EditAnalystForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ExtendHomepage
	exclude = ['homepage']
