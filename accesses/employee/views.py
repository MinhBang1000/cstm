# Django
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as bases_permissions
from accesses.employee import serializers as access_serializers
from accesses.models import Access
from storages.models import Storage

User = get_user_model()

class AccessViewSet(BaseViewSet):

    permission_classes = [ bases_permissions.IsAnonymus ]
    filterset_fields = [ 
        "access_storage__storage_code",
        "access_storage__storage_name"
    ]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return access_serializers.AccessAcceptSerializer
        return access_serializers.AccessSerializer

    # Found way to solve djongo not working with filter feature for boolean fields
    def get_queryset(self):
        from_owner =  self.request.query_params.get("access_from_owner", None)
        if from_owner != None:
            from_owner = bool(from_owner == "true")
            return Access.objects.filter(access_employee = self.request.user, access_from_owner__in = [from_owner])
        return Access.objects.filter(access_employee = self.request.user)

    def perform_create(self, serializer):
        employee = self.request.user
        if self.request.data.get("access_storage_code", False) == False:
            raise ValidationError(errors.get_error(errors.NOT_REQUEST_STORAGE_CODE))
        try:
            storage = Storage.objects.get( storage_code = self.request.data["access_storage_code"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        serializer.save( access_employee = employee, access_storage = storage )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.access_from_owner == False:
            instance.access_accept = False
            instance.save()
            raise ValidationError(errors.get_error(errors.CAN_NOT_ACCEPT))
        