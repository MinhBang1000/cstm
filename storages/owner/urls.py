# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter
from storages.owner.views import StorageViewSet

router = DefaultRouter()
router.register('', StorageViewSet, basename="storages")

urlpatterns = [
    path('', include(router.urls))
]