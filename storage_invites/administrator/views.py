# Django
from django.contrib.auth import get_user_model

# Rest Framework
from rest_framework.serializers import ValidationError

# Customize
from bases.errors import get_error, NOT_FOUND_OPERATE, NOT_ANONYMUS, ROLE_NOT_EXISTS,NOT_FOUND_STORAGE, ONE_MAN_TO_ONE_ROLE
from bases.views import BaseViewSet, base64_decoding
from bases.permissions import IsOwner
from storages.models import Storage
from storage_invites.models import StorageEmployee
from storage_invites.administrator.serializers import StorageEmployeeSerializer

class StorageEmployeeViewSet(BaseViewSet):

    serializer_class = StorageEmployeeSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return StorageEmployee.objects.filter(storage__owner = self.request.user)
    
    def perform_create(self, serializer):
        # Find a storage of inviter
        try:
            storage = Storage.objects.get(pk=self.request.data["storage_id"], owner = self.request.user)
        except:
            raise ValidationError(get_error(NOT_FOUND_STORAGE))  
        # Decode and find a user
        email = base64_decoding(self.request.data["employee_code"])
        try:
            user = get_user_model().objects.get(email=email)
        except:
            raise get_user_model().DoesNotExist 
        # Check role 
        if user.role != "Anonymous":
            raise ValidationError(get_error(NOT_ANONYMUS))
        # Check role which is available
        if self.request.data.get("for_role", None) != None and self.request.data["for_role"] not in ["Supervisor", "Manager"]:
            raise ValidationError(get_error(ROLE_NOT_EXISTS))
        # Save serializer
        try:
            serializer.save(employee = user, storage = storage)
        except:
            raise ValidationError(get_error(ONE_MAN_TO_ONE_ROLE))
    
    def update(self, request, *args, **kwargs):
        raise ValidationError(get_error(NOT_FOUND_OPERATE))