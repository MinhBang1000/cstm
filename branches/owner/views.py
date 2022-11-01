# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from branches.owner import serializers as branch_serializer
from branches.models import Branch
from branch_accesses.models import BranchAccess
from storage_accesses.models import StorageAccess

class BranchViewSet(BaseViewSet):
    queryset = Branch.objects.all()
    serializer_class = branch_serializer.BranchSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    filterset_fields = [ "id","branch_name","branch_street","branch_district__district_name","branch_company__company_name"]
    view_name = "branch"

    def get_queryset(self):
        if self.is_owner() == True:
            return Branch.objects.filter( branch_company__company_owner = self.request.user )
        # If user is employee
        try:
            access = BranchAccess.objects.filter(access_employee = self.request.user).first()
        except:
            pass 
        if access == None:
            try:
                access = StorageAccess.objects.get( access_employee = self.request.user )
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
            return Branch.objects.filter( pk = access.access_storage.storage_branch.id )
        return Branch.objects.filter( pk = access.access_branch.id )

    def check_permissions(self, request):
        # To check user permissions - do not review block permissions yet
        self_check = self.is_permission(self.view_name)
        if self_check == False:
            raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))        
        return super().check_permissions(request)
    
    def update(self, request, *args, **kwargs):
        if request.data.get("branch_company", False) != False:
            raise ValidationError(errors.get_error(errors.BRANCH_CHANGE_COMPANY))
        return super().update(request, *args, **kwargs)
