from django.urls import path
from . import views

urlpatterns = [
    path('projektnilist/<int:project_id>/', views.create_project_doc)
]