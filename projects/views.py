from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewProjectForm, NewClientForm
from django.contrib.auth.decorators import login_required
from .models import Project


@login_required
def project_overview(request):
    all_projects = Project.objects.all()
    context = {
        'projects': all_projects
    }
    return render(request, 'projects/projects_overview.html', context)


@login_required
def add_project(request):
    if request.method == "GET":
        context = {
            'form': NewProjectForm
        }
        return render(request, 'projects/add_project.html', context)

    elif request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/')
        return HttpResponse('No')


@login_required
def add_client(request):
    if request.method == "GET":
        context = {
            'form': NewClientForm
        }
        return render(request, 'projects/add_client.html', context)

    elif request.method == "POST":
        form = NewClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/')
        return HttpResponse('No')
