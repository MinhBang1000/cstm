# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from entities.administrator.views import EntityViewSet

router = DefaultRouter()
router.register('', EntityViewSet, basename="entities")

urlpatterns = [
    path('', include(router.urls))
]