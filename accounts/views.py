from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout, views, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm)
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.urls import reverse_lazy
from django.views import generic


def login_page(request):
    return render(request, 'accounts/main.html')


def submit_login(request):
    username = request.POST['login-username']
    password = request.POST['login-password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/projekti/')

    else:
        error = True
        return render(request, 'accounts/main.html', {'error': error})


@login_required
def submit_logout(request):
    user = request.user
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def add_user(request):
    user = request.user
    if request.method == "GET":
        context = {
            'user': user,
            'form': SignupForm
        }
        return render(request, 'accounts/add_user.html', context)

    elif request.method == "POST":
        form = SignupForm(request.POST)
        context = {
            'form': SignupForm,
        }
        # User has to be staff to make a new account
        if user.is_staff:

            # Check if form is valid
            if form.is_valid():

                # Get data from the form
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                # Check if user with this email or username already exists
                try:
                    x = User.objects.get(email=email)
                    y = User.objects.get(username=username)
                    context['user_already_exists'] = True
                    return render(request, 'accounts/add_user.html', context)

                # If not, create new user
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password)
                    new_user.first_name = form.cleaned_data['first_name']
                    new_user.last_name = form.cleaned_data['last_name']
                    new_user.save()
                    return HttpResponseRedirect('/overview/')

            # If form isn't valid
            context['invalid_data'] = True
            return render(request, 'accounts/add_user.html', context)
        
        # If user isn't staff
        context['user_not_staff'] = True
        return render(request, 'accounts/add_user.html', context)


@login_required
def settings(request):
    if request.method == "GET":
        context = {
            'user': request.user,
        }
        return render(request, 'accounts/settings.html', context)


class PasswordChange(views.PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'
    success_url = '/accounts/nastavitve/uredi/pregled/'


def EditProfile(request):
    user = request.user
    if request.method == "GET":
        context = {
            'user': user,
            'form': EditProfileForm(instance=user)
        }
        return render(request, 'accounts/edit_profile.html', context)

    elif request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/nastavitve/')
        return HttpResponse('No')
