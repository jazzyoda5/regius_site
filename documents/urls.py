from django.urls import path
from . import views

urlpatterns = [
    path('projektnilist/<int:project_id>/', views.create_project_doc),
    path('izbrisi-projektni-list/<int:document_id>/', views.delete_project_doc)
]