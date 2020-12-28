from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateWorkerForm, WorkerInfoForm, AssignedToProjectForm
import json
from .models import AssignedToProject
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import ProjectAnex
from datetime import date, timedelta


def test(request):
    atp1 = AssignedToProject.objects.get(id=1)
    start_date = atp1.start_date
    end_date = atp1.end_date
    return HttpResponse(start_date + 1)

@login_required
def workers_overview(request):
    context = {
        'workers': Worker.objects.all()
    }
    return render(request, 'workers/workers_overview.html', context)


# On search submit
def workers_overview_search(request):
    q = request.GET.get('q')
    workers = Worker.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(company__icontains=q)
    )
    context = {
        'workers': workers
    }
    return render(request, 'workers/workers_overview.html', context)



@login_required
def worker_details(request, worker_id):
    worker = Worker.objects.get(id=worker_id)

    # Try to get worker info
    try:
        worker_info = WorkerInfo.objects.get(worker=worker)
        worker_info_fields = worker_info._meta.get_fields()

        # Create a dict
        values = {}

        for field in worker_info_fields:
            field_name = field.name
            if field_name != 'id':
                try:
                    values[field.verbose_name] = getattr(worker_info, field_name)
                except AttributeError:
                    pass

        worker_info = values


    except WorkerInfo.DoesNotExist:
        worker_info = None
        worker_info_fields = None
    
    context = {
        'worker': worker,
        'worker_info': worker_info,
    }
    print(worker_info)
    return render(request, 'workers/worker_details.html', context)


@login_required
def get_data(request):
    data = {
        'a': 100,
        'b': 10
    }
    return JsonResponse(data)


class CreateWorker(CreateView):
    template_name = 'workers/create_worker.html'
    form_class = CreateWorkerForm
    model = Worker

    def get_success_url(self):
        return reverse('worker_details', args=(self.object.id,))


@login_required
def edit_worker_info(request, worker_id):
    worker = Worker.objects.get(id=worker_id)

    # Check if info about worker already exists
    workerinfolist = WorkerInfo.objects.filter(worker=worker)
    
    if len(workerinfolist) >= 1:
        workerinfo = WorkerInfo.objects.get(worker=worker)
        if request.method == "GET":
            context = {
                'form': WorkerInfoForm(instance=workerinfo),
            }
            return render(request, 'workers/edit_worker_info.html', context)

        elif request.method == "POST":
            form = WorkerInfoForm(request.POST, instance=workerinfo)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/delavci/' + str(worker.id))
    
    elif len(workerinfolist) < 1:
        newworkerinfo = WorkerInfo.create(worker=worker)
        if request.method == "GET":
            context = {
                'form': WorkerInfoForm(instance=newworkerinfo),
            }
            return render(request, 'workers/edit_worker_info.html', context)

        elif request.method == "POST":
            form = WorkerInfoForm(request.POST, instance=newworkerinfo)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/delavci/' + str(worker.id))


@login_required
def delete_worker(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    worker.delete()
    return HttpResponseRedirect('/delavci/')


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

            # Update end date because of anex docs
            # Check if there is already previous anex docs created so that 
            anex_docs = ProjectAnex.objects.filter(project=project)

            # Calculate end date to help user fill out the form
            if len(anex_docs) >= 1:
                for anex in anex_docs:
                    if anex.end > project_end:
                        project_end = anex.end
                        
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


def unassign_worker(request, ass_obj_id):
    # DB object with data about assigning worker to project
    # This is what has to be deleted
    assignment_obj = AssignedToProject.objects.get(id=ass_obj_id)

    project_id = assignment_obj.project.id

    # Delete
    assignment_obj.delete()
    return HttpResponseRedirect('/projekti/' + str(project_id) + '/delavci/')

"""
def update_availability(worker, start_date, end_date):
    # Get availability for the worker
    # If it is the first task he is assigned to create an availability object
    try:
        avail_obj = WorkerAvailability.objects.get(worker=worker)
    except WorkerAvailability.DoesNotExist:
        avail_str = ''
        for i in range(365):
            avail_str += '1'
        avail_obj = WorkerAvailability(worker=worker, availability_str=avail_str)
        avail_obj.save()

    date = date.today()
    num = 0
    for i in avai:
        if date
"""


