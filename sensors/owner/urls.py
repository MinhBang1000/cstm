# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from sensors.owner.views import SensorViewSet

router = DefaultRouter()
router.register('',SensorViewSet,basename="sensors")

urlpatterns = [
    path('', include(router.urls))    
]