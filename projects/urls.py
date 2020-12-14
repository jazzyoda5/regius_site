from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_overview),
    path('najdi/', views.project_overview_search),
    path('novprojekt/', views.add_project),
    path('<int:project_id>/dodajnaslov/', views.add_project_address),
    path('<int:project_id>/uredinaslov/', views.edit_project_address),
    path('novastranka/', views.add_client),
    path('<int:project_id>/', views.project_details),
    path('<int:project_id>/delavci/', views.project_details_workers),
    path('<int:project_id>/dokumenti/', views.project_details_documents),
    path('<int:project_id>/dokumenti/dodajaneks/', views.add_anex, name='add_anex'),
    path('<int:project_id>/dokumenti/odstranianeks/<int:anex_id>/', views.delete_anex, name='delete_anex'),
    path('<int:project_id>/dodajdelavca/', views.project_assign_worker),
    path('kontaktnipodatki/<int:project_id>', views.add_project_contact_info),
    path('kontaktnipodatki/<int:project_id>/uredi/', views.edit_project_contact_info),
    path('stranka/<int:client_id>/uredi/', views.edit_client_details),
    path('stranka/<int:client_id>/', views.client_details),
    path('<int:project_id>/uredi/', views.edit_project_details),
    path('<int:project_id>/izbrisi/', views.delete_project)
]