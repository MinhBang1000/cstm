# Rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status

# Customize
from bases import permissions, errors
from storage_invites.administrator.serializers import StorageEmployeeSerializer
from storage_invites.models import StorageEmployee
from storages.models import Storage

@api_view(["PUT"])
@permission_classes([permissions.IsAnonymus])
def accept_invite(request, invite_id):
    try:
        invite = StorageEmployee.objects.get(pk = invite_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_INVITATION))
    if invite.employee != request.user:
        raise ValidationError(errors.get_error(errors.NOT_YOUR_INVITATION))
    if invite.from_owner == False:
        raise ValidationError(errors.get_error(errors.NOT_YOUR_PERMIT))
    invite.accepted = True 
    invite.save()
    request.user.role = invite.for_role
    request.user.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.IsAnonymus])
def request_access(request, storage_code):
    # Find a storage of inviter
    try:
        storage = Storage.objects.get(storage_code = storage_code)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))  
    # Check role 
    if request.user.role != "Anonymous":
        raise ValidationError(errors.get_error(errors.NOT_ANONYMUS))
    # Check role which is available
    if request.data.get("for_role", None) != None and request.data["for_role"] not in ["Supervisor", "Manager"]:
        raise ValidationError(errors.get_error(errors.ROLE_NOT_EXISTS))
    # Save serializer
    serializer = StorageEmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save(employee = request.user, storage = storage, from_owner = False)
    except:
        raise ValidationError(errors.get_error(errors.ONE_MAN_TO_ONE_ROLE))
    return Response(data=serializer.data,status=status.HTTP_201_CREATED)