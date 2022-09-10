# Rest framework
from rest_framework import serializers

# Customize
from provinces.models import Province

class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = [ "province_name" ]