# from Sensor import Sensor
# from Space import Space 
# from SpaceDividing import SpaceDividing


# Testing for divide spaces
# whole_space = Space(0,0,0,10,10,10)
# sensor = Sensor(5,5,5)
# sensor = Sensor(0,0,8)
# sensor = Sensor(0,5,5)
# smaller_spaces = SpaceDividing(storage_space=whole_space)
# total_spaces = smaller_spaces.generate_spaces_by_sensors(sensor, whole_space)
# print_spaces = [ space.get_space() for space in total_spaces ]
# for space in print_spaces:
#     print(space,"\n")

# Testing regression
# whole_space = Space(0,0,0,10,10,10)
# sensors = [ Sensor(5,5,5), Sensor(4,0,4), Sensor(0,0,8) ]
# smaller_spaces = SpaceDividing(storage_space=whole_space)
# smaller_spaces.secondary_sensors = sensors
# smaller_spaces.generate_mark_secondary_sensors()
# smaller_spaces.generate_total_spaces(whole_space)
# print_spaces = [ space.get_space() for space in smaller_spaces.spaces ]
# for space in print_spaces:  
#     print(space,"\n")

# # 20/10/2022
# from SpaceSaver import SpaceSaver
# from Interpolation import Interpolation
# from Sensor import Sensor
# from Storage import Storage

# reader = SpaceSaver()
# total_spaces = reader.local_read(4)
# # Prepare storage
# # storage_space = total_spaces[0]
# # Increase a smooth
# storage_space = {
#     "x_min": 0,
#     "x_max": 50,
#     "y_min": 0,
#     "y_max": 50,
#     "z_min": 0,
#     "z_max": 20
# }
# storage = Storage()
# storage.init_storage(storage_space["x_max"], storage_space["y_max"], storage_space["z_max"])

# # Prepare sensors
# x_range = [ storage_space["x_min"], storage_space["x_max"] ]
# y_range = [ storage_space["y_min"], storage_space["y_max"] ]
# z_range = [ storage_space["z_min"], storage_space["z_max"] ]

# sensors = []
# for x in x_range:
#     for y in y_range:
#         for z in z_range:
#             sensor = Sensor()
#             sensor.init_sensor(x,y,z,0)
#             sensors.append(sensor)
# sensor_temperatures = [-10,-11.4,-11.5,-11.572,-11,-10.644,-10.5,-11.32]
# for index in range(len(sensors)):
#     sensors[index].temperature = sensor_temperatures[index]
# sensor = Sensor()
# sensor.init_sensor(0,0,20,-11.4)
# sensors.append(sensor)
# for sensor in sensors:
#     print(sensor.x,sensor.y,sensor.z,"->",sensor.temperature)

# interpolation = Interpolation(sensors=sensors, storage=storage)
# interpolation.generate_c()

# blocks = []

# for x in range(storage.x_min, storage.x_max + 1):
#     for y in range(storage.y_min, storage.y_max + 1):
#         for z in range(storage.z_min, storage.z_max + 1):
#             if interpolation.mark_interpolation[x][y][z] != False:
#                 interpolation.mark_interpolation[x][y][z] == False
#                 if interpolation.first_interpolation[x][y][z] == "#": 
#                     point = {
#                         "x": x,
#                         "y": y,
#                         "z": z
#                     }
#                     interpolation.generate_delta(point, storage_space)
#                     interpolation.first_interpolation[x][y][z] = interpolation.generate_temperature(point)
#                 blocks.append(str(x)+" "+str(y)+" "+str(z)+" -> "+str(interpolation.first_interpolation[x][y][z]))

# print("block_1: ")
# for block in blocks:
#     print(block)