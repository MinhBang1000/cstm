# Django
from django.contrib.auth import get_user_model

User = get_user_model()

# Rest framework
from rest_framework.serializers import ValidationError
from rest_framework import permissions

# Customize
from bases.views import BaseViewSet
from bases import errors, permissions as base_permissions
from branch_accesses.api import serializers as branch_access_serializers
from branches.models import Branch
from branch_accesses.models import BranchAccess
from users.employee.serializers import UserRoleSerializer
from roles.models import Role

class BranchAccessViewSet(BaseViewSet):
    serializer_class = branch_access_serializers.BranchAccessSerializer
    permission_classes = [ permissions.IsAuthenticated, base_permissions.IsOwner ]

    # Only Owner can add someone into branch which was created by him
    def get_queryset(self):
        owner = self.request.user 
        return BranchAccess.objects.filter( access_branch__branch_company__company_owner = owner, access_employee__creater = owner.id )

    def own_branches(self):
        # return list of id branch we have
        branches = [ branch.id for branch in self.request.user.own_company.company_branches.all() ]
        return branches

    def is_own_branch(self, branch_id):
        return branch_id in self.own_branches()

    def is_own_employee(self, user_id):
        try:
            employee = User.objects.get(pk = user_id)
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_EMPLOYEE))
        return employee.creater == self.request.user.id

    def perform_destroy(self, instance):
        employee = instance.access_employee
        employee.role = Role.objects.get(pk=10) # Back to guest
        employee.save()
        return super().perform_destroy(instance)

    def perform_create(self, serializer):
        user_id = self.request.data.get("access_employee", None)
        role_id = self.request.data.get("role_id", None)
        if role_id == None:
            raise ValidationError(errors.get_error(errors.DO_NOT_ENOUGH_PARAMS))
        try:
            employee = User.objects.get(pk = user_id)
        except:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_EMPLOYEE))
        data = {
            "role_id": role_id
        }
        user_serializer = UserRoleSerializer(instance=employee, data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        if user_id != None:
            if self.is_own_employee(user_id) == False:
                raise ValidationError(errors.get_error(errors.EMPLOYEE_NOT_OWN))
        branch_id = self.request.data.get("access_branch", None)
        if branch_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_BRANCH))
        if self.is_own_branch(branch_id) == False:
            raise ValidationError(errors.get_error(errors.BRANCH_NOT_OWN))
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        user_id = self.request.data.get("access_employee", None)
        if user_id != None:
            raise ValidationError(errors.get_error(errors.CAN_NOT_CHANGE_ACCESS_EMPLOYEE))
        branch_id = self.request.data.get("access_branch", None)
        if branch_id == None:
            raise ValidationError(errors.get_error(errors.NOT_FOUND_BRANCH))
        if self.is_own_branch(branch_id) == False:
            raise ValidationError(errors.get_error(errors.BRANCH_NOT_OWN))        
        return super().perform_update(serializer)