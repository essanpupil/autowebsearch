from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def welcome(request):
    "display welcome page"
    return render(request, 'welcome.html')


@login_required
def user_profile(request):
    "display user's profile"
    return render(request, 'profile.html')


@login_required
def password_changed(request):
    "display password successfully chenged"
    return render(request, 'password_changed.html')
