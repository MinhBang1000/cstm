# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize 
from bases.views import BaseViewSet
from bases.permissions import IsAdminOrOwner
from bases import errors
from roles.models import Role 
from roles.administrator import serializers as role_serializers
from permissions.models import Permission

class RoleViewSet(BaseViewSet):
    serializer_class = role_serializers.RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [ IsAdminOrOwner ]

    def get_queryset(self):
        value = self.request.query_params.get("role_level", None)
        if value!=None:
            value = int(value)
            if self.is_owner() == True:
                return Role.objects.filter(role_creater = self.request.user.id, role_level = value) | Role.objects.filter(role_creater = 1, role_level = value)
                # Get standard role and own role which have specific level
            return Role.objects.filter(role_creater = self.request.user.id, role_level = value)
        if self.is_owner() == True:
            return Role.objects.filter(role_creater = self.request.user.id) | Role.objects.filter(role_creater = 1)
            # Get standard role and own role
        return Role.objects.filter(role_creater = self.request.user.id)

    # def get_queryset(self):
    #     value = self.request.query_params.get("role_level", None)
    #     if value!=None:
    #         value = int(value)
    #         if self.is_owner() == True:
    #             return Role.objects.filter(role_creater = self.request.user.id, role_level__gte = value) | Role.objects.filter(role_creater = 1, role_level__gte = value)
    #     if self.is_owner() == True:
    #         return Role.objects.filter(role_creater = self.request.user.id) | Role.objects.filter(role_creater = 1)
    #     return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return role_serializers.RoleReadSerializer
        return super().get_serializer_class()

    # def list(self, request, *args, **kwargs):
    #     user = self.request.user 
    #     if user.role.id not in [1,2]:
    #         raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))    
    #     return super().list(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     user = self.request.user 
    #     if user.role.id not in [1,2]:
    #         raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))   
    #     return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        role_creater = 0
        role_level = 3
        if self.request.data.get("role_creater", None) != None:
            role_creater = self.request.data.get("role_creater", None)
        if self.request.data.get("role_level", None) != None:
            role_level = self.request.data.get("role_level", None)
        if self.request.user != None:
            if self.request.user.role.id != 1 and self.request.user.role.role_creater == -1: # Là owner mới có quyền tạo role 
                owner_permissions = self.request.user.role.role_permissions.all()
                owner_permission_ids = [ per.id for per in owner_permissions ] 
                wish_permissions = self.request.data.get('role_permissions', None)
                if wish_permissions != None:
                    for id in wish_permissions:
                        if id not in owner_permission_ids:
                            raise ValidationError(errors.get_error(errors.DO_NOT_HAVE_PERMISSION))
                        try:
                            permission_obj = Permission.objects.get(pk = id)
                        except:
                            raise ValidationError(errors.get_error(errors.NOT_FOUND_PERMISSION))
                        read_permission = Permission.objects.get(permission_name = "read", permission_entity = permission_obj.permission_entity)
                        if read_permission.id not in wish_permissions:
                            raise ValidationError(errors.get_error("You can't create a role without a read permission but has CUD permissions!"))
                serializer.save(role_creater = self.request.user.id, role_level = role_level)
            elif self.request.user.role.id == 1: # Admin
                serializer.save(role_creater = role_creater, role_level = role_level)
            else:
                raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
        else:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
        
    def perform_update(self, serializer):
        if self.request.user != None:
            if self.request.user.role.id != 1 and self.request.user.role.role_creater == -1: # Là owner mới có quyền tạo role 
                role_obj = Role.objects.get(pk = self.kwargs["pk"])
                if role_obj.role_creater == 0:
                    raise ValidationError(errors.get_error(errors.ONLY_ADMIN))
                if self.request.user.id != role_obj.role_creater:
                    raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
                owner_permissions = self.request.user.role.role_permissions.all()
                owner_permission_ids = [ per.id for per in owner_permissions ] 
                wish_permissions = self.request.data.get('role_permissions', None)
                if wish_permissions != None:
                    for id in wish_permissions:
                        if id not in owner_permission_ids:
                            raise ValidationError(errors.get_error(errors.DO_NOT_HAVE_PERMISSION))
                        try:
                            permission_obj = Permission.objects.get(pk = id)
                        except:
                            raise ValidationError(errors.get_error(errors.NOT_FOUND_PERMISSION))
                        read_permission = Permission.objects.get(permission_name = "read", permission_entity = permission_obj.permission_entity)
                        if read_permission.id not in wish_permissions:
                            raise ValidationError(errors.get_error("You can't create a role without a read permission but has CUD permissions!"))
                serializer.save()
            elif self.request.user.role.id == 1: # Admin
                serializer.save()
            else:
                raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))
        else:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER_ADMIN))