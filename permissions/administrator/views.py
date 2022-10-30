# Rest framework
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from permissions.administrator import serializers as permission_serializers
from permissions.models import Permission

class PermissionViewSet(BaseViewSet):
    permission_classes = [ permissions.IsAdminUser ]
    serializer_class = permission_serializers.PermissionSerializer
    queryset = Permission.objects.all()