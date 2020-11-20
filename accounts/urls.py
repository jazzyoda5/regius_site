from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('submitlogin/', views.submit_login)
]
