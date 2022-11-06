# Django
from django.urls import path, include

# Customize
from temperatures.supervisor.views import start_real_time_temperatures, get_face_temperatures, get_temperatures_testing,get_list_temperatures, get_temperatures

urlpatterns = [
    path('start_real_time/<int:storage_id>/', start_real_time_temperatures, name="start_real_time_temperatures"),
    path('<int:storage_id>/', get_temperatures, name="get_temperatures"),
    path('testing/<int:storage_id>/', get_temperatures_testing, name="get_temperatures_testing"),
    path('faces/<int:storage_id>/',get_face_temperatures, name="get_face_temperatures"),
    path('compares/<int:storage_id>/',get_list_temperatures, name="get_list_temperatures"),
]