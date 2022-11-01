# Django 
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from storage_accesses.api.views import StorageAccessViewSet

router = DefaultRouter()
router.register('', StorageAccessViewSet, basename="storage_accesses")

urlpatterns = [
    path('', include(router.urls))
]