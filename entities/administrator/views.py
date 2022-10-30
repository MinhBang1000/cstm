# Customize
from bases.views import BaseViewSet
from entities.models import Entity
from entities.administrator import serializers as entity_serializers
from permissions.administrator.serializers import PermissionSerializer

class EntityViewSet(BaseViewSet):
    serializer_class = entity_serializers.EntitySerialzier
    queryset = Entity.objects.all()

    def perform_create(self, serializer):
        entity = serializer.save()
        features = [ "create","read","update","delete" ]
        for feature in features:
            data = { "permission_name": feature, "permission_entity": entity.id }
            permission = PermissionSerializer(data=data)
            permission.is_valid(raise_exception=True)
            permission.save()
        