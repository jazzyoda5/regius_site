from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import (NewProjectForm, 
NewClientForm, 
ProjectAddressForm, 
ProjectContactInfoForm,
NewAnexForm)
from workers.forms import AssignedToProjectForm
from django.contrib.auth.decorators import login_required
from .models import Client
from .models import (Project, 
ProjectAdress, 
ProjectContactInfo,
ProjectAnex)
from workers.models import AssignedToProject
from documents.models import (ProjectDocument, 
ProjectContract,
DocumentTemplate,
ProjectAnexDoc)
from django.db.models import Q


@login_required
def project_overview(request):
    all_projects = Project.objects.all().order_by('pub_date')[:15]
    context = {
        'projects': all_projects
    }
    return render(request, 'projects/projects_overview.html', context)


def project_overview_search(request):
    q = request.GET.get('q')
    projects = Project.objects.filter(
        Q(project_name__icontains=q) | Q(client__name__icontains=q)
    )
    context = {
        'projects': projects
    }
    return render(request, 'projects/projects_overview.html', context)



@ login_required
def add_project(request):
    if request.method == "GET":
        context={
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
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.delete()
    return HttpResponseRedirect('/projekti/')


@login_required
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
        contract_doc = ProjectContract.objects.get(project=project)
    except ProjectContract.DoesNotExist:
        contract_doc = None
        
    try:
        contact_info = ProjectContactInfo.objects.get(project=project)
    except ProjectContactInfo.DoesNotExist:
        contact_info = None

    context = {
        'project': project,
        'address': address,
        'project_doc': project_doc,
        'contract_doc': contract_doc,
        'contact_info': contact_info,
    }

    try:
        anex_data = ProjectAnex.objects.filter(project=project)
        anex_end_date = project.project_end_date
        value = project.contract_value
        for anex in anex_data:
            if anex.end > anex_end_date:
                anex_end_date = anex.end
            value += anex.value
        context['contract_value'] = value
        context['anex_end_date'] = anex_end_date

    except ProjectAnex.DoesNotExist:
        anex_data = None
        context['contract_value'] = project.contract_value

    # Find end date if anexes exist

    return render(request, 'projects/project_details.html', context)


@login_required
def edit_project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "GET":
        context = {
            'form': NewProjectForm(instance=project),
            'title': project.project_name,
        }
        return render(request, 'projects/edit_project_details.html', context)

    elif request.method == "POST":
        form = NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/' + str(project.id))


@login_required
def project_details_workers(request, project_id):
    project = Project.objects.get(id=project_id)

    # Get context
    try:
        workers_on_project = AssignedToProject.objects.filter(project=project).order_by('start_date')
    except AssignedToProject.DoesNotExist:
        workers_on_project = None

    context = {
        'project': project,
        'workers_on_project': workers_on_project
    }
    return render(request, 'projects/project_details_workers.html', context)


@login_required
def project_details_documents(request, project_id):
    project = Project.objects.get(id=project_id)

    # Context
    try:
        project_doc = ProjectDocument.objects.get(project=project)
    except ProjectDocument.DoesNotExist:
        project_doc = None

    try:
        contract_doc = ProjectContract.objects.get(project=project)
    except ProjectContract.DoesNotExist:
        contract_doc = None

    context = {
        'project': project,
        'project_doc': project_doc,
        'contract_doc': contract_doc
    }

    # Check if there is already data about anex extension created
    # Then check if the document is also already created
    # There can be more than one anex doc so all of them have to be displayed

    # Get all anex_data objects
    anex_data = ProjectAnex.objects.filter(project=project)
    context['anex_data'] = anex_data

    # For each of anex_data obj check, if documents were created
    # And create a dictionary with all of them
    # Where dict key is the id of ProjectAnexDoc object
    anex_docs = {}
    docs = ProjectAnexDoc.objects.filter(project=project)

    for anex in anex_data:
        try:
            doc = ProjectAnexDoc.objects.get(anex_data=anex)
            setattr(anex, 'doc', doc)
        except ProjectAnexDoc.DoesNotExist:
            pass

    



    return render(request, 'projects/project_details_documents.html', context)

# Construction site address
@login_required
def add_project_address(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "GET":
        context = {
            'form': ProjectAddressForm(initial={'project': project}),
            'title': 'Naslov Gradbišča',
            'last_page': False
        }
        return render(request, 'projects/edit_project_details.html', context)

    elif request.method == "POST":
        form = ProjectAddressForm(request.POST, initial={'project': project})
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/projekti/' + str(project.id))


@login_required
def edit_project_address(request, project_id):
    project_address = ProjectAdress.objects.get(project=project_id)
    if request.method == "GET":
        context = {
            'form': ProjectAddressForm(instance=project_address),
            'title': 'Naslov Gradbišča',
            'last_page': False
        }
        return render(request, 'projects/edit_project_details.html', context)

    elif request.method == "POST":
        form = ProjectAddressForm(request.POST, instance=project_address)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/projekti/' + str(project_id))


@login_required
def add_client(request):
    template = 'projects/add_client.html'
    if request.method == "GET":
        context = {
            'form': NewClientForm
        }
        return render(request, template, context)

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
                return render(request, template, context)


@login_required
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
    
    # Projects with this client
    projects = Project.objects.filter(client=client)

    context = {
        'values': values,
        'client': client,
        'projects': projects
    }
    print(values)
    return render(request, 'projects/client_details.html', context)


@login_required
def edit_client_details(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == "GET":
        context = {
            'form': NewClientForm(instance=client),
        }
        return render(request, 'projects/edit_client_details.html', context)

    elif request.method == "POST":
        form = NewClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/stranka/' + str(client.id) + '/')


@login_required
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


@login_required
def edit_project_contact_info(request, project_id):
    contact_info = ProjectContactInfo.objects.get(project=project_id)
    if request.method == "GET":
        context = {
            'form': ProjectContactInfoForm(instance=contact_info),
        }
        return render(request, 'projects/edit_client_details.html', context)

    elif request.method == "POST":
        form = ProjectContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projekti/' + str(project_id) + '/')


@login_required
def add_anex(request, project_id):
    project = Project.objects.get(id=project_id)
    template = 'projects/add_anex.html'

    # Check if there is already previous anex docs created so that 
    # We can assign a number to this anex doc
    anex_docs = ProjectAnex.objects.filter(project=project)
    anex_num = int(len(anex_docs)) + 1

    # Calculate end date to help user fill out the form
    end_date = project.project_end_date
    if len(anex_docs) >= 1:
        for anex in anex_docs:
            if anex.end > end_date:
                end_date = anex.end

    if request.method == 'GET':

        context = {
            'form': NewAnexForm(initial={'project': project, 'anex_num': anex_num}),
            'project': project,
            'end_date': end_date
        }
        return render(request, template, context)

    elif request.method == 'POST':
        form = NewAnexForm(request.POST, initial={'project': project, 'anex_num': anex_num})
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            # Check if inputed dates are after the end of project stated on the contract
            if correct_dates(start, end, end_date):
                form.save()
                return HttpResponseRedirect('/projekti/' + str(project_id) + '/dokumenti/')

            context = {
                'form': form,
                'project': project,
                'incorrect_dates': True
            }
            return render(request, template, context)

        context = {
                'form': form,
                'project': project,
                'form_not_valid': True
            }
        return render(request, template, context)


def correct_dates(start, end, end_date):
    project_end = end_date
    if start > project_end and end > project_end:
        return True
    else:
        return False


def delete_anex(request, project_id, anex_id):
    anex_obj = ProjectAnex.objects.get(project=project_id, id=anex_id)
    anex_obj.delete()
    return HttpResponseRedirect('/projekti/' + str(project_id) + '/dokumenti/')


