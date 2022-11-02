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
from storages.models import Storage
from bases import errors, permissions as base_permissions
from bases.solving_code.SpaceSaver import SpaceSaver
from branch_accesses.models import BranchAccess
from storage_accesses.models import StorageAccess

# Show running time 
import time
import copy

# Sklearn
from sklearn.metrics import mean_squared_error

@api_view(["GET"])
@permission_classes([base_permissions.IsAnyOne])
def get_temperatures_testing(request, storage_id):
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
        pass

    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read(storage.id)

    # Add sensor in Database to Sensor Model 
    sensors = []
    sensor_instances = Sensor.objects.filter(sensor_storage = storage.id)
    for s_item in sensor_instances:
        sensor = SensorClass(s_item)
        sensors.append(sensor)
        
    # List temperatures
    storage_obj = StorageClass(storage)
    interpolation = InterpolationClass(storage=storage_obj, sensors=sensors)

    # Create c parameters
    interpolation.generate_c()

    for space in total_spaces:
        interpolation.prepare_unknown_sensors(space)

    # Block
    result = {}
    index_of_blocks = 1

    for space in total_spaces:
        x_min = space["x_min"]
        x_max = space["x_max"]
        y_min = space["y_min"]
        y_max = space["y_max"]
        z_min = space["z_min"]
        z_max = space["z_max"]
        # Generate new c paramesters
        interpolation.set_temperatures(space)
        interpolation.generate_c()
        # All elements of Block
        block = []
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
                        block.append("["+str(x)+"]["+str(y)+"]["+str(z)+"] =" + str(val))
        result["block_"+str(index_of_blocks)] = block
        index_of_blocks += 1        

    return Response(result)

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
    # Check owner or employee of storage or superior level
    access = None 
    if user.role.role_creater == -1:
        pass 
    else:
        try:
            access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
        except:
            pass 
        if access == None:
            try:
                access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
    # Check permissions of user --> read_storage
    lst_block_permissions = [ block.block_permission.id for block in user.user_blocks.all() ] 
    accept_permission = user.role.role_permissions.filter(permission_name = "read", permission_entity__entity_name = "storage").first()
    if accept_permission == None:
        raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))
    if accept_permission.id in lst_block_permissions:
        raise ValidationError(errors.get_error(errors.DO_NOT_PERMISSION))
    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read(storage.id)
    
    # Init variable max, min, total
    max = -9999
    min = 9999
    total = 0
    max_delta = -9999

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
    # This is wrong c paramester must be follow the space, 8 points in the space you in

    for space in total_spaces:
        interpolation.prepare_unknown_sensors(space)

    for space in total_spaces:
        x_min = space["x_min"]
        x_max = space["x_max"]
        y_min = space["y_min"]
        y_max = space["y_max"]
        z_min = space["z_min"]
        z_max = space["z_max"]
        # Generate new c paramesters
        interpolation.set_temperatures(space)
        interpolation.generate_c()
        pre_val = None
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
                        # get max delta of two near points
                        if pre_val != None:
                            delta = abs(abs(pre_val) - abs(val))
                            if max_delta < delta:
                                max_delta = delta
                        pre_val = val

    result = {
        "number_of_blocks": interpolation.number_of_blocks,
        "minimun_temperature": min,
        "maximun_temperature": max,
        "average_temperature": total/interpolation.number_of_blocks,
        "maximun_delta_temperature": max_delta,
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
    # Check owner or employee of storage or superior level
    access = None 
    if user.role.role_creater == -1:
        pass 
    else:
        try:
            access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
        except:
            pass 
        if access == None:
            try:
                access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
    
    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read(storage.id)

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
        # Generate new c paramesters
        interpolation.set_temperatures(space)
        interpolation.generate_c() 
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

@api_view(["POST"])
@permission_classes([base_permissions.IsAnyOne])
def get_list_temperatures(request, storage_id):
    if request.data == None:
        raise ValidationError(errors.get_error(errors.DATA_NOT_FILLED))
    start_time = time.time()
    # Get Storage
    user = request.user
    try:
        storage = Storage.objects.get(pk = storage_id)
    except:
        raise ValidationError(errors.get_error(errors.NOT_FOUND_STORAGE))        
    # Check owner or employee of storage or superior level
    access = None 
    if user.role.role_creater == -1:
        pass 
    else:
        try:
            access = StorageAccess.objects.filter( access_employee = user, access_storage = storage ).first()
        except:
            pass 
        if access == None:
            try:
                access = BranchAccess.objects.filter( access_employee = user, access_branch = storage.storage_branch ).first()
            except:
                raise ValidationError(errors.get_error(errors.YOU_NOT_IN_BRANCH_OR_STORAGE))
    # Read for total space which had saved in server
    reader = SpaceSaver()
    total_spaces = reader.local_read(storage.id)

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

    # Find a space which is any point was in
    actual_points = request.data
    total_list_temperatures = copy.deepcopy(actual_points)
    mark_of_points = [ False for i in range(len(actual_points)) ]
    for index in range(len(actual_points)):
        point = actual_points[index]
        for space in total_spaces:
            if mark_of_points[index] == True:
                break
            if point["x"] >= space.get("x_min") and point["x"] <= space.get("x_max") and point["y"] >= space.get("y_min") and point["y"] <= space.get("y_max") and point["z"] >= space.get("z_min") and point["z"] <= space.get("z_max"): 
                mark_of_points[index] = True
                to_value_point = {
                    "x": point["x"],
                    "y": point["y"],
                    "z": point["z"]
                }
                interpolation.generate_delta(to_value_point, space)
                total_list_temperatures[index]["temperature"] = interpolation.generate_temperature(to_value_point)

    print("Runtime is : ", (time.time() - start_time))
    y_predict = [ item["temperature"] for item in total_list_temperatures ]
    y_actual = [ float(item["temperature"]) for item in actual_points ]
    print(y_predict, y_actual)
    rmse = mean_squared_error(y_actual, y_predict, squared=False)
    result = {
        "interpolation_points": total_list_temperatures,
        "rmse": rmse
    }
    # Need to save in database step in here
    return Response(result)