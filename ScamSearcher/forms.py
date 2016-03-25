"""forms module for main ScamSearcher project."""
from django import forms


class LoginForm(forms.Form):
    """Generate login forms."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
