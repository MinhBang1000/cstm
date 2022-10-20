# Django
from django.urls import path, include

# Customize
from temperatures.supervisor.views import get_face_temperatures, get_temperatures_testing,get_list_temperatures, get_temperatures

urlpatterns = [
    path('<int:storage_id>/', get_temperatures, name="get_temperatures"),
    path('testing/<int:storage_id>/', get_temperatures_testing, name="get_temperatures_testing"),
    path('faces/<int:storage_id>/',get_face_temperatures, name="get_face_temperatures"),
    path('compares/<int:storage_id>/',get_list_temperatures, name="get_list_temperatures"),
]