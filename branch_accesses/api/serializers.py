# Rest framework
from rest_framework import serializers

# Customize
from branch_accesses.models import BranchAccess

class BranchAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchAccess
        fields = [ "id","access_branch","access_employee" ]

class BranchAccessReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchAccess
        fields = [ "id","access_branch" ]
        depth = 1