# Django
from django_filters.rest_framework import DjangoFilterBackend

# Rest Framework
import base64
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class BaseViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # To get which action does user doing ?
    def get_action(self):
        if self.action in ["retrieve","list"]:
            return "read"
        elif self.action == "destroy":
            return "delete"
        else:
            return self.action

    # To list permissions of one user
    def list_permissions(self):
        user = self.request.user 
        block_permissions = user.user_blocks.all()
        lst_block_permissions = [ block.block_permission.id for block in block_permissions ]
        lst_permissions = []
        for permission in user.role.role_permissions.all():
            if permission.id not in lst_block_permissions:
                lst_permissions.append(permission.get_str())
        return lst_permissions

    # To check user have permission which is needing for this action
    def is_permission(self, model_name):
        need_permission = self.get_action()+"_"+model_name
        return need_permission in self.list_permissions()

    def list(self, request, *args, **kwargs):  
        is_paginate = bool(request.query_params.get("paginate",False) == "true")
        if is_paginate:
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def is_owner(self):
        return self.request.user.role.role_creater == -1 

# Function of encoding base64
def base64_encoding(value):
    value = value.encode('ascii')
    value = base64.b64encode(value)
    value = value.decode('ascii')
    return value

# Function of decoding base64
def base64_decoding(value):
    value = value.encode('ascii')
    value = base64.b64decode(value)
    value = value.decode('ascii')
    return value