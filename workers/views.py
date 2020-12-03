from django.shortcuts import render


def workers_overview(request):
    return render(request, 'workers/workers_overview.html')
