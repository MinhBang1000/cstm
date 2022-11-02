# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize 
from bases.views import BaseViewSet
from bases import errors
from roles.models import Role 
from roles.administrator import serializers as role_serializers

class RoleViewSet(BaseViewSet):
    serializer_class = role_serializers.RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [ permissions.IsAuthenticated ]

    def list(self, request, *args, **kwargs):
        user = self.request.user 
        if user.role.id not in [1,2]:
            raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))    
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user 
        if user.role.id not in [1,2]:
            raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))   
        return super().destroy(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     role_creater = 0
    #     if self.request.data.get("role_creater", None) != None:
    #         role_creater = self.request.data.get("role_creater", None)
    #     if self.request.user != None:
    #         if self.request.user.role.id != 1 and self.request.user.role.role_creater == -1: # Là owner mới có quyền tạo role 
    #             owner_permissions = self.request.user.role.role_permissions.all()
    #             owner_permission_ids = [ per.id for per in owner_permissions ] 
    #             wish_permissions = self.request.data.get('role_permissions', None)
    #             if wish_permissions != None:
    #                 for id in wish_permissions:
    #                     if id not in owner_permission_ids:
    #                         raise ValidationError(errors.get_error(errors.DO_NOT_HAVE_PERMISSION))
    #             serializer.save(role_creater = self.request.user.id)
    #         elif self.request.user.role.id == 1: # Admin
    #             serializer.save(role_creater = role_creater)
    #         else:
    #             raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
    #     else:
    #         raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
        
    def perform_update(self, serializer):
        if self.request.user != None:
            if self.request.user.role.id != 1 and self.request.user.role.role_creater == -1: # Là owner mới có quyền tạo role 
                role_obj = Role.objects.get(pk = self.kwargs["pk"])
                if role_obj.role_creater == 0:
                    raise ValidationError(errors.get_error(errors.ONLY_ADMIN))
                if self.request.user.role.id != role_obj.role_creater:
                    raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
                owner_permissions = self.request.user.role.role_permissions.all()
                owner_permission_ids = [ per.id for per in owner_permissions ] 
                wish_permissions = self.request.data.get('role_permissions', None)
                if wish_permissions != None:
                    for id in wish_permissions:
                        if id not in owner_permission_ids:
                            raise ValidationError(errors.get_error(errors.DO_NOT_HAVE_PERMISSION))
                serializer.save()
            elif self.request.user.role.id == 1: # Admin
                serializer.save()
            else:
                raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
        else:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))