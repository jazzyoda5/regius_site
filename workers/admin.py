from django.contrib import admin
from .models import *

admin.site.register(Worker)
admin.site.register(WorkerInfo)
admin.site.register(AssignedToProject)
admin.site.register(WorkerAvailability)
