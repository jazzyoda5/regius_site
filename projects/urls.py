from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_overview),
    path('novprojekt/', views.add_project),
    path('novprojekt/naslov/', views.add_project_address),
    path('novastranka/', views.add_client),
    path('<int:project_id>/', views.project_details),
    path('kontaktnipodatki/<int:project_id>', views.add_project_contact_info),
    path('stranka/<int:client_id>/', views.client_details)
]