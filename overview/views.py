from django.shortcuts import render


def overview_page(request):
    context = {
        'username': request.user
    }
    return render(request, 'overview/main.html', context)
