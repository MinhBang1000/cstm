# Rest framework
from os import access
from rest_framework.serializers import ValidationError

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from pallets.manager import serializers as pallet_serializers
from pallets.models import Pallet

class PalletViewSet(BaseViewSet):
    queryset = Pallet.objects.all()
    serializer_class = pallet_serializers.PalletSerializer
    # permission_classes = [ base_permissions.IsOwnerManager ]
    filterset_fields = [ "id","pallet_x","pallet_y","pallet_y","pallet_length","pallet_width","pallet_height","pallet_drawers","pallet_storage__id" ]

    def list(self, request, *args, **kwargs):
        if request.query_params.get("pallet_storage__id",None) == None:
            raise ValidationError(errors.get_error(errors.MUST_HAVE_STORAGE_ID))
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get("pallet_storage_id", None) != None:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_STORAGE_OF_PALLET))
        return super().update(request, *args, **kwargs)