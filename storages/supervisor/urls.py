# Django 
from django.urls import path, include 

# Customize
from storages.supervisor.views import monitor_temperatures

urlpatterns = [
    path("<int:storage_id>/", monitor_temperatures, name="monitor_temperatures")
]