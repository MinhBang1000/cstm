# Django
from django.urls import path, include 

# Rest Framework
from rest_framework.routers import DefaultRouter

# Customize
from storage_invites.administrator.views import StorageEmployeeViewSet

router = DefaultRouter()
router.register('', StorageEmployeeViewSet, basename="storage_invites")

urlpatterns = [
    path('', include(router.urls)),
]