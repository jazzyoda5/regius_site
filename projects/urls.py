from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_overview),
    path('novprojekt/', views.add_project),
    path('novastranka/', views.add_client),
    #path('<int:project_id>/', views.project_details)
]