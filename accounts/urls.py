from django.urls import path
from . import views
from .views import PasswordChange, EditProfile, PasswordReset, PasswordResetConfirm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('submitlogin/', views.submit_login, name='submit_login'),
    path('submitlogout/', views.submit_logout, name='submit_logout'),
    path('adduser/', views.add_user, name='add_user'),
    path('nastavitve/uredi/', EditProfile, name='edit_profile'),
    path('nastavitve/', views.settings, name='settings'),
    path('nastavitve/spremenigeslo/', PasswordChange.as_view(), name='password_change'),
    path('nastavitve/password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('nastavitve/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name='password_reset_done'),
    path('nastavitve/reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('nastavitve/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name='password_reset_complete')
]
