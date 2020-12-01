from django.urls import path
from . import views
from .views import PasswordChange, EditProfile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('submitlogin/', views.submit_login, name='submit_login'),
    path('submitlogout/', views.submit_logout, name='submit_logout'),
    path('adduser/', views.add_user, name='add_user'),
    path('nastavitve/uredi/', EditProfile, name='edit_profile'),
    path('nastavitve/', views.settings, name='settings'),
    path('nastavitve/spremenigeslo/', PasswordChange.as_view(), name='password_change'),

]
