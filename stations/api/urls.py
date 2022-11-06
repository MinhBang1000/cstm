# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from stations.api.views import StationViewSet

router = DefaultRouter()
router.register('',StationViewSet,basename="stations")

urlpatterns = [
    path('', include(router.urls))    
]