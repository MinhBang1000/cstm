# Django
from django.urls import path, include

# Customize
from temperatures.supervisor.views import get_temperatures

urlpatterns = [
    path('<int:storage_id>/', get_temperatures, name="get_temperatures")
]