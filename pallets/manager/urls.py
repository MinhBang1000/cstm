# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from pallets.manager.views import PalletViewSet

router = DefaultRouter()
router.register('',PalletViewSet,basename="pallets")

urlpatterns = [
    path('', include(router.urls))    
]