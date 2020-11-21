from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def overview_page(request):
    context = {
        'username': request.user
    }
    return render(request, 'overview/main.html', context)
