# Django
from django.urls import path, include 

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from areas.supervisor.views import AreaViewSet

# Create router for views in here
router = DefaultRouter()
router.register('', AreaViewSet, basename="areas")

urlpatterns = [
    path('', include(router.urls))
]
