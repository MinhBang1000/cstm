# Rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

# Customize
from bases.permissions import IsOwnerSupervisor
from storages.models import Storage
from storage_invites.models import StorageEmployee
from bases import errors, trilinear_interpolation

@api_view(["POST"])
@permission_classes([IsOwnerSupervisor])
def monitor_temperatures(request, storage_id):
    # Find a storage with ID
    try:
        storage = Storage.objects.get(pk=storage_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))
    # Check user's role in the storage
    if request.user.role != "Owner":
        try:
            storage_invite = StorageEmployee.objects.get(employee = request.user, storage = storage)
        except:
            raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
        if storage_invite.accepted == False:
            raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
    # Get parameters we need
    storage_space = {
        "x_min": 0,
        "y_min": 0,
        "z_min": 0,
        "x_max": storage.length,
        "y_max": storage.width,
        "z_max": storage.height
    }
    # Check data valid
    if request.data.get("temperatures", False) == False:
        raise ValidationError(errors.get_error(errors.DATA_TYPE_INVALID))
    temperatures = request.data["temperatures"]
    tri_dimension_lst = trilinear_interpolation.trilinear_interpolation(storage_space=storage_space, temperatures=temperatures)
    return Response(tri_dimension_lst)