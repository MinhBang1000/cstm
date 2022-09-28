# Rest framework
from os import access
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

# Customize
from bases.solving_code.Temperature import Temperature as TemperatureClass
from bases.solving_code.Interpolation import Interpolation as InterpolationClass
from bases.solving_code.Sensor import Sensor as SensorClass
from bases.solving_code.Storage import Storage as StorageClass
from sensors.models import Sensor
from accesses.models import Access
from storages.models import Storage
from bases import errors, permissions as base_permissions
from bases.solving_code.SpaceSaver import SpaceSaver

# Show running time 
import time


@api_view(["GET"])
@permission_classes([base_permissions.IsAnyOne])
def get_temperatures(request, storage_id):
    start_time = time.time()
    # Get Storage
    user = request.user
    try:
        storage = Storage.objects.get(pk = storage_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))        
    owner = False
    if storage.storage_branch.branch_company.company_owner == user:
        # Is Owner 
        owner = True
    else:
        # Is employee 
        try:
            access = Access.objects.filter(access_storage = storage.id, access_employee = user.id)
        except:
            raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
    
    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read()

    # Init variable max, min, total
    max = -9999
    min = 9999
    total = 0

    # Add sensor in Database to Sensor Model 
    sensors = []
    sensor_instances = Sensor.objects.filter(sensor_storage = storage.id)
    for s_item in sensor_instances:
        sensor = SensorClass(s_item)
        sensors.append(sensor)
        
    # List temperatures
    storage_obj = StorageClass(storage)
    interpolation = InterpolationClass(storage=storage_obj, sensors=sensors)

    interpolation.generate_c()

    for space in total_spaces:
        interpolation.prepare_unknown_sensors(space)

    for space in total_spaces:
        x_min = space["x_min"]
        x_max = space["x_max"]
        y_min = space["y_min"]
        y_max = space["y_max"]
        z_min = space["z_min"]
        z_max = space["z_max"] 
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    if interpolation.mark_interpolation[x][y][z] != False:
                        interpolation.mark_interpolation[x][y][z] = False
                        if interpolation.first_interpolation[x][y][z] == "#":
                            point = {
                                "x": x,
                                "y": y,
                                "z": z
                            }
                            interpolation.generate_delta(point, space)
                            val = interpolation.generate_temperature(point)
                            interpolation.first_interpolation[x][y][z] = val
                        else:
                            val = interpolation.first_interpolation[x][y][z]
                        total += val 
                        if max <= val:
                            max = val
                        if min >= val:
                            min = val 

    result = {
        "number_of_blocks": interpolation.number_of_blocks,
        "minimun_temperature": min,
        "maximun_temperature": max,
        "average_temperature": total/interpolation.number_of_blocks,
        "temperatures": interpolation.first_interpolation
    }
    print("Runtime is : ", (time.time() - start_time))
    return Response(result)

@api_view(["GET"])
@permission_classes([base_permissions.IsAnyOne])
def get_face_temperatures(request, storage_id):
    start_time = time.time()
    # Get Storage
    user = request.user
    try:
        storage = Storage.objects.get(pk = storage_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))        
    owner = False
    if storage.storage_branch.branch_company.company_owner == user:
        # Is Owner 
        owner = True
    else:
        # Is employee 
        try:
            access = Access.objects.filter(access_storage = storage.id, access_employee = user.id)
        except:
            raise ValidationError(errors.get_error(errors.CAN_ACCESS_STORAGE))
    
    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read()

    # Init variable max, min, total
    max = -9999
    min = 9999
    total = 0

    # Add sensor in Database to Sensor Model 
    sensors = []
    sensor_instances = Sensor.objects.filter(sensor_storage = storage.id)
    for s_item in sensor_instances:
        sensor = SensorClass(s_item)
        sensors.append(sensor)
        
    # List temperatures
    storage_obj = StorageClass(storage)
    interpolation = InterpolationClass(storage=storage_obj, sensors=sensors)

    interpolation.generate_c()

    for space in total_spaces:
        interpolation.prepare_unknown_sensors(space)

    # Init count for six faces
    faces_count = 0

    for space in total_spaces:
        x_min = space["x_min"]
        x_max = space["x_max"]
        y_min = space["y_min"]
        y_max = space["y_max"]
        z_min = space["z_min"]
        z_max = space["z_max"] 
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    if x in [ storage_obj.x_min, storage_obj.x_max ] or y in [ storage_obj.y_min, storage_obj.y_max ] or z in [ storage_obj.z_min, storage_obj.z_max ]:
                        if interpolation.mark_interpolation[x][y][z] != False:
                            faces_count += 1
                            interpolation.mark_interpolation[x][y][z] = False
                            if interpolation.first_interpolation[x][y][z] == "#":
                                point = {
                                    "x": x,
                                    "y": y,
                                    "z": z
                                }
                                interpolation.generate_delta(point, space)
                                val = interpolation.generate_temperature(point)
                                interpolation.first_interpolation[x][y][z] = val
                            else:
                                val = interpolation.first_interpolation[x][y][z]
                            total += val 
                            if max <= val:
                                max = val
                            if min >= val:
                                min = val 

    result = {
        "number_of_blocks": faces_count,
        "minimun_temperature": min,
        "maximun_temperature": max,
        "average_temperature": total/faces_count,
        "temperatures": interpolation.first_interpolation
    }
    print("Runtime is : ", (time.time() - start_time))
    return Response(result)