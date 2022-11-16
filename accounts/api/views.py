# Django
from django.contrib.auth import get_user_model

User = get_user_model()

# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize 
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from users.employee.serializers import ProfileSerializer


class EmployeeViewSet(BaseViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, base_permissions.IsOwner]
    filterset_fields = [ 'id','email', 'first_name', 'last_name', 'dob', 'phone_no','role__id','profile_code','creater']

    def get_queryset(self):
        return User.objects.filter( creater = self.request.user.id )

    def perform_create(self, serializer):
        raise ValidationError(errors.get_error(errors.NOT_FOUND_API))

    def perform_update(self, serializer):
        raise ValidationError(errors.get_error(errors.NOT_FOUND_API))

    def destroy(self, request, *args, **kwargs):
        raise ValidationError(errors.get_error(errors.NOT_FOUND_API))