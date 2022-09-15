# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# Customize
from accesses.owner.views import AccessViewSet

router = DefaultRouter()
router.register('',AccessViewSet,basename="accesses")

urlpatterns = [
    path('', include(router.urls))
]