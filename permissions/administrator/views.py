# Rest framework
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors
from permissions.administrator import serializers as permission_serializers
from permissions.models import Permission
from bases.permissions import IsAdminOrOwner

class PermissionViewSet(BaseViewSet):
    permission_classes = [ IsAdminOrOwner ]
    serializer_class = permission_serializers.PermissionSerializer
    queryset = Permission.objects.all()
    filterset_fields = [ "id" ]

    def get_queryset(self):
        value = self.request.query_params.get("permission_level", None)
        if value != None:
            value = int(value)
            if value not in [0,1,2,3]:
                raise ValidationError(errors.get_error(errors.INVALID_LEVEL))
            if self.is_owner() == True:
                # if value == 0:
                #     raise ValidationError(errors.get_error(errors.INVALID_LEVEL))
                # Get only permission of owner and greater than value
                return self.request.user.role.role_permissions.filter(permission_level__gte = value)    
        if self.is_owner() == True: # Except Company modify
            return self.request.user.role.role_permissions.filter(permission_level__gte = 1)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return permission_serializers.PermissionReadSerializer
        return super().get_serializer_class()

    
