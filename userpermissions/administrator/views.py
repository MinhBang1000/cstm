# Rest framework
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from userpermissions.administrator import serializers as userpermission_serializers
from userpermissions.models import UserPermission

class UserPermissionViewSet(BaseViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = userpermission_serializers.UserPermissionSerializer
    filterset_fields = [ "id","person__email", "person__id", "permission__id", "permission__permission_name","permission__permission_mission__mission_name","permission__permission_mission__id","is_active" ]
    
    def destroy(self, request, *args, **kwargs):
        raise   ValidationError(errors.get_error(errors.CAN_NOT_DO_THIS_FEATURE))

    def create(self, request, *args, **kwargs):
        raise   ValidationError(errors.get_error(errors.CAN_NOT_DO_THIS_FEATURE))

    def update(self, request, *args, **kwargs):
        if len(request.data) != 1:
            raise ValidationError(errors.get_error(errors.ONLY_IS_ACITVE_IS_UPDATED))
        if request.data.get('is_active', None) == None:
            raise ValidationError(errors.get_error(errors.ONLY_IS_ACITVE_IS_UPDATED))
        # Check if you are admin or creater of this account
        editor = self.request.user
        if editor.role.id == 1:
            pass
        elif editor.role.id in [2,3,4]:
            employee = UserPermission.objects.get(pk=kwargs["pk"]).person
            flag = False
            if editor.id == employee.employer:
                flag = True
            # Superior also can do that            
            count = 2
            # How many step in previous
            # Trường hợp nếu người tạo là Admin nhưng Manager chung kho vẫn có quyền thay đổi quyền
            if employee.role.id == 2:
                raise ValidationError(errors.get_error(errors.CAN_NOT_ACTIVE))
            elif employee.role.id == 3:
                count = 1
            elif employee.role.id == 4:
                count = 2
            else: 
                count = 3 
            for i in range(0,count):
                try:
                    superior = User.objects.get(pk=employee.employer)
                    if editor.id == superior.id:
                        flag = True
                        break
                except:
                    pass
                employee = superior               
            if flag == False:
                raise ValidationError(errors.get_error(errors.CAN_NOT_ACTIVE))
        else:
            raise ValidationError(errors.get_error(errors.CAN_NOT_ACTIVE))
        return super().update(request, *args, **kwargs)

        