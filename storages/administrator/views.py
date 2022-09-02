# Rest Framework
from rest_framework import permissions
from rest_framework.serializers import ValidationError

# Customize
from bases.errors import get_error, CHANGE_OWNER
from bases.views import BaseViewSet
from storages.models import Storage
from storages.administrator.serializers import StorageSerializer

class StorageViewSet(BaseViewSet):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Storage.objects.filter(owner=self.request.user).select_related("owner")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "Anonymous":
            user.role = "Owner"
            user.save()
        serializer.save(owner = self.request.user)
    
    def update(self, request, *args, **kwargs):
        if request.data["owner"]:
            raise ValidationError(get_error(CHANGE_OWNER))
        return super().update(request, *args, **kwargs)

    
    