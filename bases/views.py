# Django
from django_filters.rest_framework import DjangoFilterBackend

# JWT
from rest_framework_simplejwt.authentication import JWTAuthentication

# Rest Framework
import base64
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class BaseViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
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