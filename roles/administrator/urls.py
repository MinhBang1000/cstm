# Django
from django.urls import path, include 

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from roles.administrator.views import RoleViewSet

router = DefaultRouter()
router.register('', RoleViewSet, basename="provinces")

urlpatterns = [
    path('', include(router.urls))
]