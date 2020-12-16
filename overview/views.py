from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import Project
from django.http import JsonResponse, HttpResponse
from workers.models import AssignedToProject, Worker
from datetime import date, timedelta


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

    data = {}

    for project in projects:
        data[str(project.project_name)] = {
            'name': project.project_name,
            'start_date': project.project_start_date,
            'end_date': project.project_end_date
        }

    return JsonResponse(data)


def available_workers_json(request):
    today = date.today()

    # Create a list of all start and end dates for AssignedToProject 
    # Where the end date of the project is after today. Past projects
    # Are not relevant
    start_end_dates = [[], []]

    for i in range(365):
        date1 = today + timedelta(days=i)
        ass_objs = AssignedToProject.objects.filter(end_date=date1)

        if len(ass_objs) >= 1:
            for obj in ass_objs:
                start_end_dates[0].append(obj.start_date)
                start_end_dates[1].append(obj.end_date)
        
        # Save last date
        elif i == 364:
            last_date = date1

    # Sort dates
    sorted_start_dates = sorted(start_end_dates[0])
    sorted_end_dates = sorted(start_end_dates[1])

    # Get length of all worker objects
    workers = Worker.objects.all()
    num_of_workers = len(workers)

    # Smallest possible start date will be first date in a sorted list of dates
    date2 = sorted_start_dates[0]

    # Smallest start date could also be after today
    # In that case start looping from today
    if today < date2:
        date2 = today

    data = {}
    num_of_elements = 0
    while date2 < last_date:
        if date2 in sorted_start_dates:
            # How many times that date is in the list
            num_of_date2 = sorted_start_dates.count(date2)

            for i in range(num_of_date2):
                num_of_workers -= 1
        
        if date2 in sorted_end_dates:
            num_of_date2 = sorted_end_dates.count(date2)

            for i in range(num_of_date2):
                num_of_workers += 1

        # Update list, increase date
        data[str(num_of_elements)] = {
            'num_of_workers': num_of_workers,
            'date': date2
        }
        date2 += timedelta(days=1)
        num_of_elements += 1

    return JsonResponse(data)
