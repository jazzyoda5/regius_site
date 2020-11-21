from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
        error = True
        return render(request, 'accounts/main.html', { 'error': error })


def submit_logout(request):
    user = request.user
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def add_user_page(request):
    return render(request, 'accounts/add_user.html', {'add_user_page': True})
