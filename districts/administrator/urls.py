# Django 
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from districts.administrator.views import DistrictViewSet

router = DefaultRouter()
router.register('', DistrictViewSet, basename="districts")

urlpatterns = [
    path('', include(router.urls))
]