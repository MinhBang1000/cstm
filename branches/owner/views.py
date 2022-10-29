# Rest framework
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from branches.owner import serializers as branch_serializer
from branches.models import Branch

class BranchViewSet(BaseViewSet):

    serializer_class = branch_serializer.BranchSerializer
    # permission_classes = [ base_permissions.IsOwnerAdmin ]
    filterset_fields = [ "id","branch_name","branch_street","branch_district__district_name","branch_company__company_name"]
    
    def get_queryset(self):
        return Branch.objects.filter( branch_company__company_owner = self.request.user )

    def perform_create(self, serializer):
        serializer.save(branch_manager = self.request.user)
    
    def update(self, request, *args, **kwargs):
        if request.data.get("branch_company", False) != False:
            raise ValidationError(errors.get_error(errors.BRANCH_CHANGE_COMPANY))
        return super().update(request, *args, **kwargs)
