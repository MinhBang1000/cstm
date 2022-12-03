# Rest framework
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from districts.administrator import serializers
from districts.models import District

class DistrictViewSet(BaseViewSet):
    serializer_class = serializers.DistrictSerializer
    queryset = District.objects.all().select_related("district_province")
    filterset_fields = [ "id","district_name","district_province__province_name","district_province__id" ]
    
    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [ permissions.IsAuthenticated() ]
        return [ permissions.IsAdminUser() ]

    