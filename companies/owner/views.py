# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from companies.owner import serializers as owner_serializer
from companies.models import Company
from branch_accesses.models import BranchAccess
from storage_accesses.models import StorageAccess

class CompanyViewSet(BaseViewSet):

    serializer_class = owner_serializer.CompanySerializer
    permission_classes = [ permissions.IsAuthenticated ]
    filterset_fields = [ "id", "company_name", "company_street", "company_district__district_name", "company_district__district_province__province_name" ]
    view_name = "company"

    def get_queryset(self):
        if self.is_owner():
            return Company.objects.filter( company_owner = self.request.user )
        access = None
        try:
            access = BranchAccess.objects.get( access_employee = self.request.user )
        except:
            pass 
        if access == None:
            try:
                access = StorageAccess.objects.get( access_employee = self.request.user )
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Company.objects.filter( pk = access.access_storage.storage_branch.branch_company.id )
        return Company.objects.filter( pk = access.access_branch.branch_company.id )

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        # self_check = self.is_permission(self.view_name)
        # if self_check == False:
        #     raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)
    
    def perform_create(self, serializer):
        user = self.request.user
        # Only owner can do that
        if self.is_owner() == False:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER))
        serializer.save( company_owner = user )

    def update(self, request, *args, **kwargs):
        # Only owner can do that
        if self.is_owner() == False:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER))
        if request.data.get("company_owner", False) != False:
            raise ValidationError(errors.get_error(errors.COMPANY_CHANGE_OWNER))
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only owner can do that
        if self.is_owner() == False:
            raise ValidationError(errors.get_error(errors.ONLY_OWNER))       
        return super().destroy(request, *args, **kwargs)