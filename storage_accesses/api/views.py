# Django
from django.contrib.auth import get_user_model

User = get_user_model()

# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from storage_accesses.api import serializers as storage_access_serializers
from storage_accesses.models import StorageAccess

class StorageAccessViewSet(BaseViewSet):
    serializer_class = storage_access_serializers.StorageAccessSerializer
    permission_classes = [ permissions.IsAuthenticated, base_permissions.IsOwner ]

    # Only Owner can add someone into branch which was created by him
    def get_queryset(self):
        owner = self.request.user 
        return StorageAccess.objects.filter( access_storage__storage_branch__branch_company__company_owner = owner, access_employee__creater = owner.id )

    def own_storages(self):
        # return list of id branch we have
        storages = []
        for branch in self.request.user.own_company.company_branches.all():
            for storage in branch.branch_storages.all():
                storages.append(storage.id)
        return storages

    def is_own_storage(self, storage_id):
        return storage_id in self.own_storages()

    def is_own_employee(self, user_id):
        try:
            employee = User.objects.get(pk = user_id)
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_EMPLOYEE))
        return employee.creater == self.request.user.id

    def perform_create(self, serializer):
        user_id = self.request.data.get("access_employee", None)
        if user_id != None:
            if self.is_own_employee(user_id) == False:
                raise ValidationError(errors.get_error(errors.EMPLOYEE_NOT_OWN))
        storage_id = self.request.data.get("access_storage", None)
        if storage_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        if self.is_own_storage(storage_id) == False:
            raise ValidationError(errors.get_error(errors.STORAGE_NOT_OWN))
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        user_id = self.request.data.get("access_employee", None)
        if user_id != None:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_ACCESS_EMPLOYEE))
        storage_id = self.request.data.get("access_storage", None)
        if storage_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        if self.is_own_storage(storage_id) == False:
            raise ValidationError(errors.get_error(errors.STORAGE_NOT_OWN))        
        return super().perform_update(serializer)