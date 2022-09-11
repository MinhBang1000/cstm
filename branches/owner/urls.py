# Django 
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from branches.owner.views import BranchViewSet

router = DefaultRouter()
router.register('', BranchViewSet, basename="branchs")

urlpatterns = [
    path('', include(router.urls))
]