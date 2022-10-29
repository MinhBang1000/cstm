# Rest framework
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from companies.owner import serializers as owner_serializer
from companies.models import Company

class CompanyViewSet(BaseViewSet):

    serializer_class = owner_serializer.CompanySerializer
    # permission_classes = [ base_permissions.IsOwnerAdmin ]
    filterset_fields = [ "id", "company_name", "company_street", "company_district__district_name", "company_district__district_province__province_name" ]
    
    def get_queryset(self):
        return Company.objects.filter( company_owner = self.request.user )
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save( company_owner = user )

    def update(self, request, *args, **kwargs):
        if request.data.get("company_owner", False) != False:
            raise ValidationError(errors.get_error(errors.COMPANY_CHANGE_OWNER))
        return super().update(request, *args, **kwargs)