# Django
from django.urls import path, include 

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from provinces.administrator.views import ProvinceViewSet

router = DefaultRouter()
router.register('', ProvinceViewSet, basename="provinces")

urlpatterns = [
    path('', include(router.urls))
]