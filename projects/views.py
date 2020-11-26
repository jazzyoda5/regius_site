from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewProjectForm, NewClientForm, ProjectAddressForm, ProjectContactInfoForm
from django.contrib.auth.decorators import login_required
from .models import Client
from .models import Project, ProjectAdress
from documents.models import DocumentTemplate


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
            'form': NewProjectForm,
            'title': 'Nov Projekt',
            'last_page': False
        }
        return render(request, 'projects/add_project.html', context)

    elif request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/')


@login_required
def add_project_address(request):
    if request.method == "GET":
        context = {
            'form': ProjectAddressForm,
            'title': 'Naslov Gradbišča',
            'last_page': False
        }
        return render(request, 'projects/add_project.html', context)

    elif request.method == "POST":
        form = ProjectAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/')



@login_required
def add_client(request):
    if request.method == "GET":
        context = {
            'form': NewClientForm
        }
        return render(request, 'projects/add_client.html', context)

    # If form is submitted
    elif request.method == "POST":
        form = NewClientForm(request.POST)
        if form.is_valid():
            # Check if client already exists in db
            client_name = form.cleaned_data.get('name')
            client_count = len(Client.objects.filter(name=client_name))
            # If no
            if client_count == 0:
                form.save()
                return HttpResponseRedirect('/projekti/')
            # If yes
            else:
                context = {
                    'form': NewClientForm,
                    'client_exists': True
                }
                return render(request, 'projects/add_client.html', context)


def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    try:
        address = ProjectAdress.objects.get(project=project)
    except ProjectAdress.DoesNotExist:
        address = None
    context = {
        'project': project,
        'address': address,
    }
    return render(request, 'projects/project_details.html', context)
