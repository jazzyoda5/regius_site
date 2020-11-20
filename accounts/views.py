from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


def login_page(request):
    return render(request, 'accounts/main.html')


def submit_login(request):
    username = request.POST['login-username']
    password = request.POST['login-password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/overview/')

    else:
        return HttpResponseRedirect('/')
