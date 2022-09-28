# Django
from django.urls import path, include

# Customize
from temperatures.supervisor.views import get_face_temperatures, get_temperatures

urlpatterns = [
    path('<int:storage_id>/', get_temperatures, name="get_temperatures"),
    path('faces/<int:storage_id>/',get_face_temperatures, name="get_face_temperatures"),
]