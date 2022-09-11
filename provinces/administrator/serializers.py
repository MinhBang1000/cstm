# Rest framework
from rest_framework import serializers

# Customize
from bases import errors
from provinces.models import Province

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [ "id","province_name" ]

    def validate_province_name(self, value): 
        try:
            province = Province.objects.get(province_name__icontains = value)
        except:
            province = False
        if province != False:
            raise serializers.ValidationError(errors.PROVINCE_EXISTS)
        return value