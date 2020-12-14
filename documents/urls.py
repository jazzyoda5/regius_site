from django.urls import path
from . import views

urlpatterns = [
    path('projektnilist/<int:project_id>/', views.create_project_doc),
    path('pogodba/<int:project_id>/', views.create_contract_doc),
    path('izbrisi-projektni-list/<int:document_id>/', views.delete_project_doc),
    path('izbrisi-pogodba/<int:document_id>/', views.delete_contract_doc),
    path('aneks/<int:project_id>/<int:anex_id>/', views.create_anex, name='create_anex')
]