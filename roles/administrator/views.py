# Customize 
from bases.views import BaseViewSet
from roles.models import Role 
from roles.administrator import serializers as role_serializers

class RoleViewSet(BaseViewSet):
    serializer_class = role_serializers.RoleSerializer
    queryset = Role.objects.all()
