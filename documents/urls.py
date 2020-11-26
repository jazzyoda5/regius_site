from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.create_project_doc)
]