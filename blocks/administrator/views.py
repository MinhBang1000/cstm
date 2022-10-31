# Django
from django.contrib.auth import get_user_model

User = get_user_model()

# Rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status, permissions

# Customize
from bases import errors
from bases.views import BaseViewSet
from blocks.models import Block
from blocks.administrator import serializers as block_serializers
from permissions.models import Permission

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def block_permission(request):
    data = request.data 
    permission_id = data.get("block_permission",None)
    user_id = data.get("block_user", None)
    try:
        user_obj = User.objects.get(pk = user_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_USER))
    try:
        permission_obj = Permission.objects.get(pk = permission_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_PERMISSION))
    # Check is owner of user
    blocker = request.user 
    if blocker.role.id != 1 and blocker.role.role_creater != -1:
        raise ValidationError(errors.get_error(errors.CAN_NOT_DO_THIS_FEATURE))
    if user_obj.creater != blocker.id:
        raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
    serializer = block_serializers.BlockSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unblock_permission(request):
    data = request.data 
    permission_id = data.get("block_permission",None)
    user_id = data.get("block_user", None)
    try:
        user_obj = User.objects.get(pk = user_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_USER))
    try:
        permission_obj = Permission.objects.get(pk = permission_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_PERMISSION))
    # Check is owner of user
    blocker = request.user 
    if blocker.role.id != 1 and blocker.role.role_creater != -1:
        raise ValidationError(errors.get_error(errors.CAN_NOT_DO_THIS_FEATURE))
    if user_obj.creater != blocker.id:
        raise ValidationError(errors.get_error(errors.ARE_NOT_OWNER))
    block = Block.objects.filter(block_permission = permission_id, block_user = user_id).first()
    block.delete()
    return Response(status=status.HTTP_200_OK)


