from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview_page, name='home')
]