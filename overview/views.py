from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import Project
from django.http import JsonResponse


@login_required
def overview_page(request):
    # Get all current projects
    projects = Project.objects.filter(status='V teku')
    labels = []
    start_dates = []
    end_dates = []
    for project in projects:
        labels.append(project.project_name)
        start_dates.append(project.project_start_date)
        end_dates.append(project.project_end_date)
    print(projects)
    context = {
        'username': request.user,
        'labels': labels,
        'start_dates': start_dates,
        'end_dates': end_dates
    }
    return render(request, 'overview/main.html', context)


@login_required
def homepage_json_data(request):

    # Get all current projects
    projects = Project.objects.filter(status='V teku').order_by('project_start_date')
    print(projects)

    data = {

    }

    for project in projects:
        data[str(project.project_name)] = {
            'name': project.project_name,
            'start_date': project.project_start_date,
            'end_date': project.project_end_date
        }

        

    print(data)
    return JsonResponse(data)