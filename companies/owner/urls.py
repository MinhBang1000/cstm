# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from companies.owner.views import CompanyViewSet

router = DefaultRouter()
router.register('', CompanyViewSet, basename="companies")

urlpatterns = [
    path('', include(router.urls))
]