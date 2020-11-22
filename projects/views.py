from django.shortcuts import render
from .forms import NewProjectForm

def project_overview(request):
    context = {
        'form': NewProjectForm
    }
    return render(request, 'projects/add_project.html', context)