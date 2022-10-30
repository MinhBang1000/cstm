# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from permissions.administrator.views import PermissionViewSet

router = DefaultRouter()
router.register('', PermissionViewSet, basename="permissions")

urlpatterns = [
    path('', include(router.urls))
]