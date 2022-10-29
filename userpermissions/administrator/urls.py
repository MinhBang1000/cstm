# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter
from userpermissions.administrator.views import UserPermissionViewSet

router = DefaultRouter()
router.register('', UserPermissionViewSet, basename="user_permissions")

urlpatterns = [
    path('', include(router.urls))
]