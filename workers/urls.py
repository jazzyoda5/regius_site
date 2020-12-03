from django.urls import path
from . import views

urlpatterns = [
    path('', views.workers_overview, name='workers_overview'),
]