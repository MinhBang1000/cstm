# Customize
from bases.views import BaseViewSet
from bases import permissions as base_permissions
from companies.owner import serializers as owner_serializer
from companies.models import Company

class CompanyViewSet(BaseViewSet):

    serializer_class = owner_serializer.CompanySerializer
    permission_classes = [ base_permissions.IsOwnerAnonymus ]
    
    def get_queryset(self):
        return Company.objects.filter( company_owner = self.request.user )
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "Owner":
            user.role = "Owner"
            user.save()
        serializer.save( company_owner = user )