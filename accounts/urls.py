from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('submitlogin/', views.submit_login),
    path('submitlogout/', views.submit_logout),
    path('adduser/', views.add_user_page),
    path('adduser/submit/', views.add_user)
]
