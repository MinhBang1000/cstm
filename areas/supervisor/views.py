# Rest framework
from rest_framework import permissions
from rest_framework.serializers import ValidationError

# Customize
from storages.models import Storage
from bases import errors
from bases.views import BaseViewSet
from areas.supervisor.serializers import AreaSerializer
from areas.models import Area


class AreaViewSet(BaseViewSet):
    filterset_fields  = ["id","x_min","x_max","y_min","y_max","z_min","z_max","monitor_from","monitor_to","temperature_min","temperature_max","storage","employee","status"]
    search_fields = ["x_min","x_max","y_min","y_max","z_min","z_max","monitor_from","monitor_to","temperature_min","temperature_max"]
    ordering_fields = ["x_min","x_max","y_min","y_max","z_min","z_max","monitor_from","monitor_to","temperature_min","temperature_max"]

    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Only area which is created by logged user
    def get_queryset(self):
        return Area.objects.filter(employee = self.request.user)

    def perform_create(self, serializer):
        # Find storage with ID 
        storage_id = self.request.data.get("storage_id", False)
        if storage_id != False:
            try:
                storage = Storage.objects.get(pk = storage_id)
            except:
                raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
        else:
            raise ValidationError(errors.get_error(errors.REQUEST_NOT_HAVE_STORAGE_ID))
        # Have logged user services this storage ?
        if storage.owner != self.request.user:
            try:
                storage_invite = StorageEmployee.objects.get(storage = storage, employee = self.request.user)
            except:
                raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
            if storage_invite.accepted == False:
                raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
        serializer.save(storage = storage, employee = self.request.user)

    def update(self, request, *args, **kwargs):
        if request.data.get("storage_id", False) != False:
            raise ValidationError(errors.get_error(errors.CHANGE_STORAGE))
        if request.data.get("employee", False) != False:
            raise ValidationError(errors.get_error(errors.CHANGE_EMPLOYEE))
        return super().update(request, *args, **kwargs)

    