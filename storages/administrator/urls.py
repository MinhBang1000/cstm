# Django
from django.urls import path, include 

# Rest Framework
from rest_framework.routers import DefaultRouter

# Customize
from storages.administrator.views import StorageViewSet

router = DefaultRouter()
router.register('', StorageViewSet, basename="storages")

urlpatterns = [
    path('', include(router.urls))
]
