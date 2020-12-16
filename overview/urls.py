from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview_page, name='home'),
    path('convert/projectsdata/', views.homepage_json_data, name="projects_data"),
    path('avail_data/', views.available_workers_json, name="aval_workers")
]