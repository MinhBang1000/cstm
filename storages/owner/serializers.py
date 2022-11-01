# Django
from asyncore import write
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework import serializers

# Customize
from branches.models import Branch
from districts.models import District
from storages.models import Storage
from branches.owner import serializers as branch_serializer
from districts.administrator import serializers as district_serializer
from users.employee import serializers as employee_serializers

User = get_user_model()

class StorageSerializer(serializers.ModelSerializer):

    storage_branch = branch_serializer.BranchSerializer(read_only = True)
    storage_district = district_serializer.DistrictSerializer(read_only = True)
    storage_branch_id = serializers.PrimaryKeyRelatedField(
        queryset = Branch.objects.all(),
        write_only = True,
        source = "storage_branch"
    )
    storage_district_id = serializers.PrimaryKeyRelatedField(
        queryset = District.objects.all(),
        write_only = True,
        source = "storage_district"
    )

    class Meta:
        model = Storage 
        fields = [ 
            "id",
            "storage_name", 
            "storage_length", 
            "storage_width", 
            "storage_height",
            "storage_code",
            "storage_street",
            "storage_branch",
            "storage_branch_id",
            "storage_district",
            "storage_district_id",
        ]
        ready_only_fields = ["storage_code"]