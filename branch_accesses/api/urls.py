# Django 
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from branch_accesses.api.views import BranchAccessViewSet

router = DefaultRouter()
router.register('', BranchAccessViewSet, basename="branch_accesses")

urlpatterns = [
    path('', include(router.urls))
]