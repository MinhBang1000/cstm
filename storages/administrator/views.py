# Django
from django.contrib.auth import get_user_model

# Rest Framework
from rest_framework.serializers import ValidationError

# Customize
from bases.errors import get_error, CHANGE_OWNER, NOT_FOUND_OPERATE
from bases.views import BaseViewSet, base64_encoding
from bases.permissions import IsOwnerAnonymus
from storages.models import Storage
from storages.administrator.serializers import StorageSerializer


class StorageViewSet(BaseViewSet):
    serializer_class = StorageSerializer
    permission_classes = [IsOwnerAnonymus]
    filterset_fields  = ["id","storage_name","length","width","height","owner","storage_code"]
    search_fields = ["storage_name","length","width","height","storage_code"]
    ordering_fields = ["id","storage_name","length","width","height"]

    def get_queryset(self):
        return Storage.objects.filter(owner=self.request.user).select_related("owner")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "Anonymous":
            user.role = "Owner"
            user.save()
        storage = serializer.save(owner = self.request.user)
        storage_code = user.email + "@" + str(storage.id)
        storage_code = base64_encoding(storage_code)
        storage.storage_code = storage_code
        storage.save()

    def update(self, request, *args, **kwargs):
        if request.data.get("owner",None):
            raise ValidationError(get_error(CHANGE_OWNER))
        return super().update(request, *args, **kwargs)

