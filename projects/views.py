from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewProjectForm, NewClientForm, ProjectAddressForm, ProjectContactInfoForm
from django.contrib.auth.decorators import login_required
from .models import Client
from .models import Project, ProjectAdress, ProjectContactInfo
from documents.models import ProjectDocument
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


def project_details(request, project_id):
    # Get project
    project = Project.objects.get(id=project_id)

    # Get project details
    try:
        address = ProjectAdress.objects.get(project=project)
    except ProjectAdress.DoesNotExist:
        address = None

    try:
        project_doc = ProjectDocument.objects.get(project=project)
    except ProjectDocument.DoesNotExist:
        project_doc = None

    try:
        contact_info = ProjectContactInfo.objects.get(project=project)
    except ProjectContactInfo.DoesNotExist:
        contact_info = None

    context = {
        'project': project,
        'address': address,
        'project_doc': project_doc,
        'contact_info': contact_info
    }
    return render(request, 'projects/project_details.html', context)
    
# Construction site address
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


def client_details(request, client_id):
    # Get client
    client = Client.objects.get(id=client_id)
    client_fields = client._meta.get_fields()

    # Create a dict
    values = {}

    for field in client_fields:
        field_name = field.name
        if field_name != 'id':
            try:
                values[field.verbose_name] = getattr(client, field_name)
            except AttributeError:
                pass
            

    context = {
        'values': values
    }
    print(values)
    return render(request, 'projects/client_details.html', context)



def add_project_contact_info(request, project_id):
    if request.method == "GET":
        project = Project.objects.get(id=project_id)
        context = {
            'form': ProjectContactInfoForm(initial={'project': project})
        }
        return render(request, 'projects/add_project_contact_info.html', context)

    # If form is submitted
    elif request.method == "POST":
        project = Project.objects.get(id=project_id)
        form = ProjectContactInfoForm(request.POST, initial={
            'project': project
        })
        if form.is_valid():
            # Check if client already exists in db
            project = Project.objects.get(id=project_id)
            object_count = len(ProjectContactInfo.objects.filter(project=project))
            # If no
            if object_count == 0:
                form.save()
                return HttpResponseRedirect('/projekti/' + str(project_id) + '/')
            # If yes
            else:
                context = {
                    'form': ProjectContactInfoForm,
                    'client_exists': True
                }
                return render(request, 'projects/add_client.html', context)


