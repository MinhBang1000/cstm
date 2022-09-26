from datetime import datetime
from . import storage_spaces_saving as sss
import sys

sys.setrecursionlimit(2000)

# Data 
# Improvement
# Data for initial (Minimum of unit is "cm")
# Dictionary structure of Storage space
storage_space = {
    "x_min": 0,
    "y_min": 0,
    "z_min": 0,
    "x_max": 53,
    "y_max": 22,
    "z_max": 25
}

space = {
    "x_min": 0,
    "y_min": 0,
    "z_min": 0,
    "x_max": 53,
    "y_max": 22,
    "z_max": 25
}

# A point which we want to know its temperature
point = {
    "x": 22,
    "y": 11,
    "z": 12
}

# Temperatures of eight sensors
storage_temperatures = {
    "p000": -17.11,
    "p100": -18.65,
    "p010": -17.11,
    "p110": -18.44,
    "p001": -14.99,
    "p101": -16.85,
    "p011": -14.44,
    "p111": -15.55
}

temperatures = {
    "p000": -17.11,
    "p100": -18.65,
    "p010": -17.11,
    "p110": -18.44,
    "p001": -14.99,
    "p101": -16.85,
    "p011": -14.44,
    "p111": -15.55
}

# Data of sensors
sensors = [
    {
        "location": {
            "x":0,
            "y":0,
            "z":0
        },
        "temperature": -17.11
    },
    {
        "location": {
            "x":53,
            "y":0,
            "z":0
        },
        "temperature": -18.65
    },
    {
        "location": {
            "x":0,
            "y":22,
            "z":0
        },
        "temperature": -17.11
    },
    {
        "location": {
            "x":53,
            "y":22,
            "z":0
        },
        "temperature": -18.44
    },
    {
        "location": {
            "x":0,
            "y":0,
            "z":25
        },
        "temperature": -14.99
    },
    {
        "location": {
            "x":53,
            "y":0,
            "z":25
        },
        "temperature": -16.85
    },
    {
        "location": {
            "x":0,
            "y":22,
            "z":25
        },
        "temperature": -14.44
    },
    {
        "location": {
            "x":53,
            "y":22,
            "z":25
        },
        "temperature": -15.55
    },
    {
        "location": {
            "x":26,
            "y":11,
            "z":12
        },
        "temperature": -16.36
    },
    {
        "location": {
            "x":13,
            "y":0,
            "z":0
        },
        "temperature": -16.54
    },
    {
        "location": {
            "x":37,
            "y":22,
            "z":18
        },
        "temperature": -16.32
    }
]

# Generate value which is used for one_point_interpolation
def c_generators(temperatures):
    return {
        "c0": temperatures.get("p000"),
        "c1": temperatures.get("p100") - temperatures.get("p000"),
        "c2": temperatures.get("p010") - temperatures.get("p000"),
        "c3": temperatures.get("p001") - temperatures.get("p000"),
        "c4": temperatures.get("p110") - temperatures.get("p010") - temperatures.get("p100") + temperatures.get("p000"),
        "c5": temperatures.get("p011") - temperatures.get("p001") - temperatures.get("p010") + temperatures.get("p000"),
        "c6": temperatures.get("p101") - temperatures.get("p001") - temperatures.get("p100") + temperatures.get("p000"),
        "c7": temperatures.get("p111") - temperatures.get("p011") - temperatures.get("p101") - temperatures.get("p110") + temperatures.get("p100") + temperatures.get("p001") + temperatures.get("p010") + temperatures.get("p000")
    }

def delta_generators(point, storage_space):
    return {
        "delta_x": (point.get("x") - storage_space.get("x_min")) / (storage_space.get("x_max") - storage_space.get("x_min")),
        "delta_y": (point.get("y") - storage_space.get("y_min")) / (storage_space.get("y_max") - storage_space.get("y_min")),
        "delta_z": (point.get("z") - storage_space.get("z_min")) / (storage_space.get("z_max") - storage_space.get("z_min"))
    }

# Trilinear interpolation for all storage space
def trilinear_interpolation(storage_space, temperatures, lamda = 1):
    c_parameters = c_generators(temperatures)
    total = [[ ['#' for col in range(storage_space.get("z_max")+1)] for col in range(storage_space.get("y_max")+1)] for row in range(storage_space.get("x_max")+1)]
    max = -9999
    min = 9999
    count = 0
    sum_total = 0
    for x in range(storage_space.get("x_max")+1):
        for y in range(storage_space.get("y_max")+1):
            for z in range(storage_space.get("z_max")+1):
                point = {
                    "x": x,
                    "y": y,
                    "z": z
                }
                delta_parameters = delta_generators(point=point, storage_space=storage_space)
                total[x][y][z] = c_parameters.get("c0") + (c_parameters.get("c1")*delta_parameters.get("delta_x")) + (c_parameters.get("c2")*delta_parameters.get("delta_y")) + (c_parameters.get("c3")*delta_parameters.get("delta_z")) + (c_parameters.get("c4")*delta_parameters.get("delta_x")*delta_parameters.get("delta_y")) + (c_parameters.get("c5")*delta_parameters.get("delta_y")*delta_parameters.get("delta_z")) + (c_parameters.get("c6")*delta_parameters.get("delta_z")*delta_parameters.get("delta_x")) + (c_parameters.get("c7")*delta_parameters.get("delta_x")*delta_parameters.get("delta_y")*delta_parameters.get("delta_z"))
                if max <= total[x][y][z]:
                    max = total[x][y][z]
                if min >= total[x][y][z]:
                    min = total[x][y][z]
                count += 1
                sum_total += total[x][y][z]
    return {
        "min": min,
        "max": max,
        "average": sum_total/count,
        "time": datetime.today(),
        "values": total
    }

# Check it True if not in any sensor location
def is_not_in_sensor_zone(point, sensor_points):
    for sensor in sensor_points:
        if point["x"] == sensor["location"]["x"] and point["y"] == sensor["location"]["y"] and point["z"] == sensor["location"]["z"]:
            return False
    return True

# Value of temperature at one point which is got by interpolation
def one_point_interpolation(point, space, temperatures):
    c_parameters = c_generators(temperatures)
    delta_parameters = delta_generators(point=point, storage_space=space)
    value_of_point = c_parameters.get("c0") + (c_parameters.get("c1")*delta_parameters.get("delta_x")) + (c_parameters.get("c2")*delta_parameters.get("delta_y")) + (c_parameters.get("c3")*delta_parameters.get("delta_z")) + (c_parameters.get("c4")*delta_parameters.get("delta_x")*delta_parameters.get("delta_y")) + (c_parameters.get("c5")*delta_parameters.get("delta_y")*delta_parameters.get("delta_z")) + (c_parameters.get("c6")*delta_parameters.get("delta_z")*delta_parameters.get("delta_x")) + (c_parameters.get("c7")*delta_parameters.get("delta_x")*delta_parameters.get("delta_y")*delta_parameters.get("delta_z"))
    return value_of_point

# To divide list of sensor for primary sensors and secondary sensors 
def divide_sensor_list(space, list_of_sensor):
    plst = []
    clst = []
    x_range = [ space["x_min"], space["x_max"] ]
    y_range = [ space["y_min"], space["y_max"] ]
    z_range = [ space["z_min"], space["z_max"] ]
    for sensor in list_of_sensor:
        if sensor["location"]["x"] in x_range  and sensor["location"]["y"] in y_range and sensor["location"]["z"] in z_range:
            plst.append(sensor)
        else:
            clst.append(sensor)
    return {
        "primary_sensors": plst,
        "secondary_sensors": clst
    }

# Init list of secondary sensor
# secondary_sensors = divide_sensor_list(space, sensors)["secondary_sensors"]
secondary_sensors = []

# Init list of mark for secondary sensor (True is marked)
# mark_of_secondary_sensors = [ False for i in secondary_sensors ]
mark_of_secondary_sensors = []

# Init list of space 
total_spaces = []

# To know type of sensor (On face, on line, inside) - Can't use it
def get_type_sensor(sensor, space):
    x_sensor = sensor["location"]["x"]
    y_sensor = sensor["location"]["y"]
    z_sensor = sensor["location"]["z"]
    x_min = space["x_min"]
    x_max = space["x_max"]
    y_min = space["y_min"]
    y_max = space["y_max"]
    z_min = space["z_min"]
    z_max = space["z_max"]
    if (x_sensor > x_min and x_sensor < x_max) and (y_sensor > y_min and y_sensor < y_max) and (z_sensor > z_min and z_sensor < z_max):
        # Inside
        return 1 
    elif (y_sensor > y_min and y_sensor < y_max) and (z_sensor > z_min and z_sensor < z_max):
        # Must be validate input sensor inside range of Storage first
        # On face x
        if (x_sensor in [ x_min, x_max ]):
            return 2
    elif (x_sensor > x_min and x_sensor < x_max) and (z_sensor > z_min and z_sensor < z_max):
        # Must be validate input sensor inside range of Storage first
        # On face x
        if (y_sensor in [ y_min, y_max ]):
            return 2
    elif (y_sensor > y_min and y_sensor < y_max) and (x_sensor > x_min and x_sensor < x_max):
        # Must be validate input sensor inside range of Storage first
        # On face x
        if (z_sensor in [ z_min, z_max ]):
            return 2
    # On line
    return 3

# Is sensor inside this space
def is_inside_space(sensor, space):
    x_sensor = sensor["location"]["x"]
    y_sensor = sensor["location"]["y"]
    z_sensor = sensor["location"]["z"]
    x_min = space["x_min"]
    x_max = space["x_max"]
    y_min = space["y_min"]
    y_max = space["y_max"]
    z_min = space["z_min"]
    z_max = space["z_max"]
    if (x_sensor >= x_min and x_sensor <= x_max) and (y_sensor >= y_min and y_sensor <= y_max) and (z_sensor >= z_min and z_sensor <= z_max):
        return True
    return False

# Get space follow sensor type
def get_space_follow_sensor_type(sensor, parent_space):
    x_sensor = sensor["location"]["x"]
    y_sensor = sensor["location"]["y"]
    z_sensor = sensor["location"]["z"]
    x_min = parent_space["x_min"]
    x_max = parent_space["x_max"]
    y_min = parent_space["y_min"]
    y_max = parent_space["y_max"]
    z_min = parent_space["z_min"]
    z_max = parent_space["z_max"]
    child_spaces = [   
            {
                "x_min": x_min,
                "y_min": y_min,
                "z_min": z_min,
                "x_max": x_sensor,
                "y_max": y_sensor,
                "z_max": z_sensor
            },
            {
                "x_min": x_sensor,
                "y_min": y_min,
                "z_min": z_min,
                "x_max": x_max,
                "y_max": y_sensor,
                "z_max": z_sensor
            },
            {
                "x_min": x_sensor,
                "y_min": y_sensor,
                "z_min": z_min,
                "x_max": x_max,
                "y_max": y_max,
                "z_max": z_sensor
            },
            {
                "x_min": x_min,
                "y_min": y_sensor,
                "z_min": z_min,
                "x_max": x_sensor,
                "y_max": y_max,
                "z_max": z_sensor
            },
            {
                "x_min": x_min,
                "y_min": y_min,
                "z_min": z_sensor,
                "x_max": x_sensor,
                "y_max": y_sensor,
                "z_max": z_max
            },
            {
                "x_min": x_sensor,
                "y_min": y_min,
                "z_min": z_sensor,
                "x_max": x_max,
                "y_max": y_sensor,
                "z_max": z_max
            },
            {
                "x_min": x_sensor,
                "y_min": y_sensor,
                "z_min": z_sensor,
                "x_max": x_max,
                "y_max": y_max,
                "z_max": z_max
            },
            {
                "x_min": x_min,
                "y_min": y_sensor,
                "z_min": z_sensor,
                "x_max": x_sensor,
                "y_max": y_max,
                "z_max": z_max
            }
        ]
    result_spaces = []
    for space in child_spaces:
        if (space["x_min"] != space["x_max"]) and (space["y_min"] != space["y_max"]) and (space["z_min"] != space["z_max"]):
            result_spaces.append(space)
    return result_spaces

# To travesal all of sensor
def init_list_of_space(space):
    flag = True
    for i in range(len(secondary_sensors)):
        sensor = secondary_sensors[i]
        if mark_of_secondary_sensors[i] == False and is_inside_space(sensor, space):
            mark_of_secondary_sensors[i] = True
            flag = False
            # Regression here
            child_spaces = get_space_follow_sensor_type(sensor, space)
            for ch_space in child_spaces:
                init_list_of_space(ch_space)
    if flag == True:
        total_spaces.append(space)

# First interpolation to get sensor value for the number of spaces which was got by travesal
def get_first_interpolation(sensors, space):
    x_max = space["x_max"]
    y_max = space["y_max"]
    z_max = space["z_max"]
    # first_interpolation = [[ ['#' for col in range(z_max+1)] for col in range(y_max+1)] for row in range(x_max+1)]
    first_interpolation = trilinear_interpolation(storage_space, storage_temperatures)["values"]
    for sensor in sensors:
        x_sensor = sensor["location"]["x"]
        y_sensor = sensor["location"]["y"]
        z_sensor = sensor["location"]["z"]
        first_interpolation[x_sensor][y_sensor][z_sensor] = sensor["temperature"]
    return first_interpolation

# To get temperature in first interpolation
# "storage_" is a prefix which is identify all items of primary component such as: Storage space and temperatures list of eight sensor
def get_temperatures_of_first_interpolation(first_interpolation, space, storage_temperatures, storage_space):
    x_min = space["x_min"]
    x_max = space["x_max"]
    y_min = space["y_min"]
    y_max = space["y_max"]
    z_min = space["z_min"]
    z_max = space["z_max"]
    return {
        "p000": first_interpolation[x_min][y_min][z_min],
        "p100": first_interpolation[x_max][y_min][z_min],
        "p010": first_interpolation[x_min][y_max][z_min],
        "p110": first_interpolation[x_max][y_max][z_min],
        "p001": first_interpolation[x_min][y_min][z_max],
        "p101": first_interpolation[x_max][y_min][z_max],
        "p011": first_interpolation[x_min][y_max][z_max],
        "p111": first_interpolation[x_max][y_max][z_max]
    }
    # return {
    #     "p000": first_interpolation[x_min][y_min][z_min] if first_interpolation[x_min][y_min][z_min] != "#" else one_point_interpolation({ "x":x_min, "y":y_min, "z":z_min }, storage_space, storage_temperatures),
    #     "p100": first_interpolation[x_max][y_min][z_min] if first_interpolation[x_max][y_min][z_min] != "#" else one_point_interpolation({ "x":x_max, "y":y_min, "z":z_min }, storage_space, storage_temperatures),
    #     "p010": first_interpolation[x_min][y_max][z_min] if first_interpolation[x_min][y_max][z_min] != "#" else one_point_interpolation({ "x":x_min, "y":y_max, "z":z_min }, storage_space, storage_temperatures),
    #     "p110": first_interpolation[x_max][y_max][z_min] if first_interpolation[x_max][y_max][z_min] != "#" else one_point_interpolation({ "x":x_max, "y":y_max, "z":z_min }, storage_space, storage_temperatures),
    #     "p001": first_interpolation[x_min][y_min][z_max] if first_interpolation[x_min][y_min][z_max] != "#" else one_point_interpolation({ "x":x_min, "y":y_min, "z":z_max }, storage_space, storage_temperatures),
    #     "p101": first_interpolation[x_max][y_min][z_max] if first_interpolation[x_max][y_min][z_max] != "#" else one_point_interpolation({ "x":x_max, "y":y_min, "z":z_max }, storage_space, storage_temperatures),
    #     "p011": first_interpolation[x_min][y_max][z_max] if first_interpolation[x_min][y_max][z_max] != "#" else one_point_interpolation({ "x":x_min, "y":y_max, "z":z_max }, storage_space, storage_temperatures),
    #     "p111": first_interpolation[x_max][y_max][z_max] if first_interpolation[x_max][y_max][z_max] != "#" else one_point_interpolation({ "x":x_max, "y":y_max, "z":z_max }, storage_space, storage_temperatures)
    # }

def generate_total_spaces(storage_space):
    init_list_of_space(storage_space)
    sss.local_write(total_spaces)

def get_total_spaces():
    return sss.local_read()
 
# Uncommment until here
# n = int(input("Enter you choice (Spaces - 1/ Interpolation - 2): "))

# # Show running time 
# import time
# start_time = time.time()

# if n == 1:
#     # Got total_spaces
#     init_list_of_space(storage_space) 

#     # Saving spaces of storage into local file
#     sss.local_write(total_spaces)



# else:
#     total_spaces = sss.local_read()
#     x_max = storage_space["x_max"]
#     y_max = storage_space["y_max"]
#     z_max = storage_space["z_max"] 
#     first_interpolation = get_first_interpolation(sensors, space) # Got first intepolation for any point which has fiction value
#     total_interpolation = [[ ['#' for col in range(z_max+1)] for col in range(y_max+1)] for row in range(x_max+1)] # Return final !
#     for space in total_spaces:
#         x_min = space["x_min"]
#         x_max = space["x_max"]
#         y_min = space["y_min"]
#         y_max = space["y_max"]
#         z_min = space["z_min"]
#         z_max = space["z_max"] 
#         temperatures = get_temperatures_of_first_interpolation(first_interpolation=first_interpolation, space=space, storage_temperatures=storage_temperatures, storage_space=storage_space)
#         for x in range(x_max + 1):
#             for y in range(y_max + 1):
#                 for z in range(z_max + 1):
#                     # if x in [x_min, x_max] and y in [y_min,y_max] and z in [z_min, z_max]:
#                     #     continue
#                     point = {
#                         "x": x,
#                         "y": y,
#                         "z": z
#                     }
#                     total_interpolation[x][y][z] = one_point_interpolation(point, space, temperatures)

#     # Update temperatures at sensor point again 
#     for sensor in sensors:
#         x_sensor = sensor["location"]["x"]
#         y_sensor = sensor["location"]["y"]
#         z_sensor = sensor["location"]["z"]
#         total_interpolation[x_sensor][y_sensor][z_sensor] = sensor["temperature"]

#     print("First interpolation:\n")
#     for x in range(37,54):
#         for y in range(11,23):
#             for z in range(18, 26):
#                 if x in [37, 53] and y in [11, 22] and z in [18,25]:
#                     print("[",x,"]","[",y,"]","[",z,"] = ",first_interpolation[x][y][z])

# print("Runtime is : ", (time.time() - start_time))