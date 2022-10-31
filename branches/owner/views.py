# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from branches.owner import serializers as branch_serializer
from branches.models import Branch

class BranchViewSet(BaseViewSet):

    serializer_class = branch_serializer.BranchSerializer
    permission_classes = [ permissions.IsAuthenticated, base_permissions.IsOwner ]
    filterset_fields = [ "id","branch_name","branch_street","branch_district__district_name","branch_company__company_name"]
    view_name = "branch"

    def get_queryset(self):
        return Branch.objects.filter( branch_company__company_owner = self.request.user )

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
