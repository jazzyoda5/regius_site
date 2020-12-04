from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateWorkerForm, WorkerInfoForm
import json


def workers_overview(request):
    context = {
        'workers': Worker.objects.all()
    }
    return render(request, 'workers/workers_overview.html', context)


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
    
    # Get data for assignedprojects chart
    # And convert it to json strings
    data = [[]]
    assigned_projects = AssignedToProject.objects.filter(worker=worker)
    for project in assigned_projects:
        print('start: {}, end: {}'.format(project.start_date, project.end_date))

    context = {
        'worker': worker,
        'worker_info': worker_info,
    }
    print(worker_info)
    return render(request, 'workers/worker_details.html', context)


class CreateWorker(CreateView):
    template_name = 'workers/create_worker.html'
    form_class = CreateWorkerForm
    model = Worker

    def get_success_url(self):
        return reverse('worker_details', args=(self.object.id,))


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



def delete_worker(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    worker.delete()
    return HttpResponseRedirect('/delavci/')
