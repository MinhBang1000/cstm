from .Space import Space

class SpaceDividing():
    storage_space = None
    spaces = [] 
    sensors = []
    secondary_sensors = []
    mark_secondary_sensors = []

    def __init__(self, storage_space) -> None:
        self.storage_space = storage_space

    # To get all secondary sensors on this storage
    def generate_secondary_sensors(self, sensors):
        x_range = [ self.storage_space.x_min, self.storage_space.x_max ]
        y_range = [ self.storage_space.y_min, self.storage_space.y_max ]
        z_range = [ self.storage_space.z_min, self.storage_space.z_max ]
        for sensor in sensors:
            if sensor.x in x_range and sensor.y in y_range and sensor.z in z_range:
                continue 
            self.secondary_sensors.append(sensor)
        # To delete
        print("Secondary sensors:")
        for sensor in self.secondary_sensors:
            print(sensor.get_sensor())

    # To init value for mark sensors
    def generate_mark_secondary_sensors(self):
        self.mark_secondary_sensors = [ False for sensor in self.secondary_sensors]
    
    # To generate smaller spaces by sensors
    def generate_spaces_by_sensors(self, sensor, parent_space):
        space = parent_space
        result = [
                # Đáy
                Space(space.x_min, space.y_min, space.z_min, sensor.x, sensor.y, sensor.z),
                Space(sensor.x, space.y_min, space.z_min, space.x_max, sensor.y, sensor.z),
                Space(space.x_min, sensor.y, space.z_min, sensor.x, space.y_max, sensor.z),
                Space(sensor.x, sensor.y, space.z_min, space.x_max, space.y_max, sensor.z),
                # Mặt 
                Space(space.x_min, space.y_min, sensor.z, sensor.x, sensor.y, space.z_max),
                Space(sensor.x, space.y_min, sensor.z, space.x_max, sensor.y, space.z_max),
                Space(space.x_min, sensor.y, sensor.z, sensor.x, space.y_max, space.z_max),
                Space(sensor.x, sensor.y, sensor.z, space.x_max, space.y_max, space.z_max)
        ]
        total_spaces = []
        for space in result:
            if (space.x_min != space.x_max) and (space.y_min != space.y_max) and (space.z_min != space.z_max):
                total_spaces.append(space)
        return total_spaces

    # To generate smaller spaces in storage with 8 corner are actual sensor, started at whole space of storage
    def generate_regression_spaces(self, space):
        flag = True 
        # Retrieve each sensor in secondary sensor to divide smaller space
        for i in range(len(self.secondary_sensors)):
            sensor = self.secondary_sensors[i]
            if self.mark_secondary_sensors[i] == False and space.is_inside_space(sensor) == True:
                flag = False
                self.mark_secondary_sensors[i] = True 
                child_spaces = self.generate_spaces_by_sensors(sensor, space)
                for ch_space in child_spaces:
                    self.generate_regression_spaces(ch_space)
        # If you don't need to divide space anymore, you will add this space to result for smaller space
        if flag == True:
            self.spaces.append(space) 

    def generate_total_spaces(self):
        self.generate_regression_spaces(self.storage_space)
        # To delete
        spaces = [ space.get_space() for space in self.spaces ]
        print("Total space: ", len(spaces))
        for space in spaces:
            print(space)

    def reset_for_sure(self):
        self.secondary_sensors = []
        self.sensors = []
        self.spaces = []
