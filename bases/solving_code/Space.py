class Space():
    x_min = 0
    y_min = 0
    z_min = 0
    x_max = 0
    y_max = 0
    z_max = 0

    def __init__(self, x_min, y_min, z_min, x_max, y_max, z_max) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min 
        self.y_max = y_max 
        self.z_min = z_min 
        self.z_max = z_max 

    def create_whole_space(self, storage_instance):
        self.x_min = storage_instance.x_min
        self.x_max = storage_instance.x_max
        self.y_min = storage_instance.y_min 
        self.y_max = storage_instance.y_max 
        self.z_min = storage_instance.z_min 
        self.z_max = storage_instance.z_max 
    
    def get_space(self):
        return {
            "x_min": self.x_min,
            "x_max": self.x_max,
            "y_min": self.y_min,
            "y_max": self.y_max,
            "z_min": self.z_min,
            "z_max": self.z_max
        }

    def is_inside_space(self, sensor):
        x_sensor = sensor.x
        y_sensor = sensor.y
        z_sensor = sensor.z
        x_min = self.x_min
        x_max = self.x_max 
        y_min = self.y_min
        y_max = self.y_max
        z_min = self.z_min
        z_max = self.z_max
        if (x_sensor >= x_min and x_sensor <= x_max) and (y_sensor >= y_min and y_sensor <= y_max) and (z_sensor >= z_min and z_sensor <= z_max):
            return True
        return False