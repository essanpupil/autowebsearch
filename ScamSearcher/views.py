from django.contrib.auth import authenticate, login as auth_login, \
                                logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

@login_required(login_url='login')
def welcome(request):
    "display welcome page"
    return render(request, "welcome.html")


def login(request):
    "display login form"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('welcome')
                else:
                    return redirect('logout')
            else:
                return redirect('logout')
    else:
        form = LoginForm()
    return render(request,
                  'login.html',
                  {'form':form,})


def logout(request):
    "log user out"
    auth_logout(request)
    return redirect('login')
