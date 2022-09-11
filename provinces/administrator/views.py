# Rest framework
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from provinces.administrator import serializers as province_serializer
from provinces.models import Province

class ProvinceViewSet(BaseViewSet):

    serializer_class = province_serializer.ProvinceSerializer
    queryset = Province.objects.all().prefetch_related()
    
    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [ base_permissions.IsOwnerAdmin() ]
        return [ permissions.IsAdminUser() ]