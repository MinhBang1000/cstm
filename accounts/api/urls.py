# Django 
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from accounts.api.views import EmployeeViewSet

router = DefaultRouter()
router.register('', EmployeeViewSet, basename="accounts")

urlpatterns = [
    path('', include(router.urls))
]