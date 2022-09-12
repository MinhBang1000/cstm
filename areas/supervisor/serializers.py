# Django
from django.contrib.auth import get_user_model

# Rest framework
from rest_framework import serializers
from rest_framework.serializers import ValidationError

# Customize
# from storages.administrator.serializers import StorageRelatedSerializer
from users.employee.serializers import EmployeeSerializer
from bases import errors
from areas.models import Area

class AreaSerializer(serializers.ModelSerializer):

    # storage = StorageRelatedSerializer(read_only = True)
    employee = EmployeeSerializer(read_only = True)

    class Meta:
        model =  Area
        fields = [ "id","x_min","x_max","y_min","y_max","z_min","z_max","monitor_from","monitor_to","temperature_min","temperature_max","storage","employee","status" ]
        read_only_fields = [ "id" ]

    def validate(self, attrs):
        # Valid day's time
        daytime = [ i for i in range (0,24) ]
        if attrs.get("monitor_from", False) != False and attrs["monitor_from"] not in daytime:
            raise ValidationError(errors.get_error(errors.DAY_TIME))
        if attrs.get("monitor_to", False) != False and attrs["monitor_to"] not in daytime:
            raise ValidationError(errors.get_error(errors.DAY_TIME))
        # Valid min and max of temperature
        if attrs.get("temperature_min", False) != False and attrs.get("temperature_max", False) != False:    
            if attrs["temperature_min"] >= attrs["temperature_max"]:
                raise ValidationError(errors.get_error(errors.TEMPERATURE_VALID))
        return attrs
    