from django.urls import path
from . import views
from .views import CreateWorker 

urlpatterns = [
    path('', views.workers_overview, name='workers_overview'),
    path('<int:worker_id>/', views.worker_details, name='worker_details'),
    path('<int:worker_id>/izbrisi/', views.delete_worker, name='delete_worker'),
    path('novdelavec/', CreateWorker.as_view(), name='create_worker'),
    path('<int:worker_id>/uredi/', views.edit_worker_info, name="edit_worker_info"),
    
]