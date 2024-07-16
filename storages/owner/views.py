# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet, base64_encoding
from bases import errors, permissions as base_permissions
from branch_accesses.models import BranchAccess
from storages.owner import serializers as storage_serializer
from storages.models import Storage
from storage_accesses.models import StorageAccess

class StorageViewSet(BaseViewSet):
    serializer_class = storage_serializer.StorageSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    view_name = "storage"
    filterset_fields = [ 
            "id",
            "storage_name", 
            "storage_length", 
            "storage_width", 
            "storage_height",
            "storage_code",
            "storage_street",
            "storage_branch__id",
            "storage_branch__branch_name",
            "storage_branch__branch_company__company_name",
            "storage_branch__branch_company__id",
            "storage_district__district_name",
            "storage_district__district_province__province_name",
            "storage_branch__branch_company__company_owner__email"
        ]
        
    # Needing filter for owner and employee only see storage
    # Update and destroy were effect in this list
    def get_queryset(self):
        if self.is_owner() == True:
            return Storage.objects.filter(storage_branch__branch_company__company_owner = self.request.user)
        # One to One is a relationship of user and storage
        access = None
        try:
            access = StorageAccess.objects.get( access_employee = self.request.user )
        except:
            pass
        if access == None:
            try:
                access = BranchAccess.objects.get( access_employee = self.request.user )
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Storage.objects.filter( storage_branch = access.access_branch )
        # Return type is array of querydict
        return Storage.objects.filter(pk = access.access_storage.id)

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        # self_check = self.is_permission(self.view_name)
        # if self_check == False:
        #     raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)

    def perform_create(self, serializer):
        # Check owner or employee 
        if self.is_owner() == True:
            pass
        else:
            access = None
            try:
                access = BranchAccess.objects.filter( access_employee = self.request.user ).first()
            except:
                pass 
            if access == None:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH))
        # To create storage code for storage
        user = self.request.user
        storage = serializer.save(storage_code = 'default-code-will-be-replaced!')
        storage_code = user.email + "@" + str(storage.id)
        storage_code = base64_encoding(storage_code)
        storage.storage_code = storage_code
        storage.save()

    def perform_destroy(self, instance):
        # Check owner or employee 
        if self.is_owner() == True:
            pass
        else:
            access = None
            try:
                access = BranchAccess.objects.filter( access_employee = self.request.user ).first()
            except:
                pass 
            if access == None:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH))
        return super().perform_destroy(instance)
    
    def perform_update(self, serializer):
        # Check owner or employee 
        try:
            storage = Storage.objects.get( pk = self.kwargs["pk"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        branch = storage.storage_branch 
        if self.is_owner() == True:
            if self.request.user != branch.branch_company.company_owner:
                raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
        else:
            access = None
            try:
                access = StorageAccess.objects.filter( access_employee = self.request.user, access_storage = storage ).first()
            except:
                pass 
            if access == None:
                try:
                    access = BranchAccess.objects.filter( access_employee = self.request.user, access_branch = branch ).first()
                except:
                    pass 
                if access == None:
                    raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
        return super().perform_update(serializer)