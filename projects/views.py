from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewProjectForm, NewClientForm, ProjectAddressForm, ProjectContactInfoForm
from workers.forms import AssignedToProjectForm
from django.contrib.auth.decorators import login_required
from .models import Client
from .models import Project, ProjectAdress, ProjectContactInfo
from workers.models import AssignedToProject
from documents.models import ProjectDocument, ProjectContract
from documents.models import DocumentTemplate
from django.db.models import Q


@login_required
def project_overview(request):
    all_projects = Project.objects.all()
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
    return render(request, 'projects/project_details.html', context)


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


# View for assigning workers to projects
@login_required
def project_assign_worker(request, project_id):
    project = Project.objects.get(id=project_id)
    context = {
        'project': project
    }
    if request.method == 'GET':
        form = AssignedToProjectForm(initial={'project': project})
        context['form'] = form
        return render(request, 'projects/project_assign_worker.html', context)

    elif request.method == 'POST':
        form = AssignedToProjectForm(request.POST, initial={'project': project})
        context['form'] = form

        if form.is_valid():
            # Store date variables
            project_start = project.project_start_date
            project_end = project.project_end_date
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Check if dates fit with project start and end
            if dates_are_valid(project_start, project_end, start_date, end_date):
                
                # Check if worker is available
                worker = form.cleaned_data['worker']
                if worker_is_available(project_start, project_end, start_date, end_date, worker):
                    form.save()
                    return HttpResponseRedirect('/projekti/' + str(project.id) + '/delavci/')

                else:
                    context['worker_not_available'] = True
                    return render(request, 'projects/project_assign_worker.html', context)
            else:
                context['date_error'] = True
                return render(request, 'projects/project_assign_worker.html', context)
        else:
            context['form_not_valid'] = True
            return render(request, 'projects/project_assign_worker.html', context)


# Function to determine if the dates to assign a worker to a project
# match the start and end dates of a project. 
def dates_are_valid(project_start, project_end, start_date, end_date):
    # Print dates
    print('psd: {}, ped: {}, sd: {}, ed: {}'. format(project_start, project_end, start_date, end_date))
    
    # start_date and end_date must be between project_start and project_end
    if project_start <= start_date <= project_end:
        if project_start <= end_date <= project_end:
            return True

    return False


# Function to check if worker is available
def worker_is_available(project_start, project_end, start_date, end_date, worker):
    already_assigned = AssignedToProject.objects.filter(worker=worker)
    
    # If there is no previously stored project for this worker
    # He is automatically available
    if len(already_assigned) < 1:
        return True

    # Comapre previous assignments to determine
    # If he is available at chosen dates
    else:
        for shift in already_assigned:
            shift_start = shift.start_date
            shift_end = shift.end_date

            if shift_start <= start_date <= shift_end:
                return False
            else:
                if shift_start <= end_date <= shift_end:
                    return False
                else:
                    if shift_start > start_date and shift_end < end_date:
                        return False

        return True


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


