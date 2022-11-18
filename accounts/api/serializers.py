# Django
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework import serializers

# Customize
from roles.administrator.serializers import RoleSerializer
from blocks.administrator.serializers import BlockSerializer
from branch_accesses.api.serializers import BranchAccessReadSerializer
from storage_accesses.api.serializers import StorageAccessReadSerializer

class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    storage_employee_access = StorageAccessReadSerializer()
    branch_employee_access = BranchAccessReadSerializer()
    block_permissions = BlockSerializer(many=True, read_only=True, source="user_blocks")
    class Meta:
        model = get_user_model()
        fields = [ 'id','email', 'first_name', 'last_name', 'dob', 'phone_no','role','profile_code','creater','block_permissions','storage_employee_access','branch_employee_access']
        read_only_fields = [ 'id', 'email', 'first_name', 'last_name', 'dob', 'phone_no','role','profile_code','creater','storage_employee_access','branch_employee_access']