# Customize
from bases.views import BaseViewSet, base64_encoding
from bases import errors, permissions as base_permissions
from storages.owner import serializers as storage_serializer
from storages.models import Storage

class StorageViewSet(BaseViewSet):
    
    serializer_class = storage_serializer.StorageSerializer
    permission_classes = [base_permissions.IsOwnerAdmin]
    filterset_fields = [ 
            "id",
            "storage_name", 
            "storage_length", 
            "storage_width", 
            "storage_height",
            "storage_code",
            "storage_street",
            "storage_branch__branch_name",
            "storage_branch__branch_company__company_name",
            "storage_district__district_name",
            "storage_district__district_province__province_name"
        ]
    
    def get_queryset(self):
        return Storage.objects.filter( storage_branch__branch_company__company_owner = self.request.user )

    def perform_create(self, serializer):
        user = self.request.user
        storage = serializer.save()
        storage_code = user.email + "@" + str(storage.id)
        storage_code = base64_encoding(storage_code)
        storage.storage_code = storage_code
        storage.save()