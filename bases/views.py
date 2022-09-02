# Rest Framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class BaseViewSet(ModelViewSet):
    
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
