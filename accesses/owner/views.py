# Django
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as bases_permissions
from accesses.owner import serializers as access_serializers
from accesses.models import Access

User = get_user_model()

class AccessViewSet(BaseViewSet):

    permission_classes = [ bases_permissions.IsOwnerAdmin ]
    filterset_fields = [ 
        "access_storage__storage_code",
        "access_storage__storage_name"
    ]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return access_serializers.AccessAcceptSerializer
        return access_serializers.AccessSerializer

    def get_queryset(self):
        from_owner =  self.request.query_params.get("access_from_owner", None)
        if from_owner != None:
            from_owner = bool(from_owner == "true")
            return Access.objects.filter(access_storage__storage_branch__branch_company__company_owner = self.request.user, access_from_owner__in = [from_owner])
        return Access.objects.filter(access_storage__storage_branch__branch_company__company_owner = self.request.user)

    def perform_create(self, serializer):
        if self.request.data.get("access_employee_code", False) == False:
            raise ValidationError(errors.get_error(errors.NOT_REQUEST_EMPLOYEE_CODE))
        try:
            employee = User.objects.get( profile_code = self.request.data["access_employee_code"] )
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_EMPLOYEE))
        if employee.role != "Anonymous":
            raise ValidationError(errors.get_error(errors.ONE_MAN_TO_ONE_ROLE))
        serializer.save( access_employee = employee )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.access_from_owner == True:
            instance.access_accept = False 
            instance.save()
            raise ValidationError(errors.get_error(errors.CAN_NOT_ACCEPT))
        