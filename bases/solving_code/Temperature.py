class Temperature():
    p000 = 0
    p100 = 0
    p010 = 0
    p110 = 0
    p001 = 0
    p101 = 0
    p011 = 0
    p111 = 0

    isvalid = True

    # def generate_temperatures(self, sensors, storage):
    #     count = 0
    #     for sensor in sensors:
    #         if sensor.x == storage.x_min and sensor.y == storage.y_min and sensor.z == storage.z_min:
    #             count += 1
    #             self.p000 = sensor.temperature

    #         elif sensor.x == storage.x_max and sensor.y == storage.y_min and sensor.z == storage.z_min:
    #             count += 1
    #             self.p100 = sensor.temperature

    #         elif sensor.x == storage.x_min and sensor.y == storage.y_max and sensor.z == storage.z_min:
    #             count += 1
    #             self.p010 = sensor.temperature

    #         elif sensor.x == storage.x_max and sensor.y == storage.y_max and sensor.z == storage.z_min:
    #             count += 1
    #             self.p110 = sensor.temperature

    #         elif sensor.x == storage.x_min and sensor.y == storage.y_min and sensor.z == storage.z_max:
    #             count += 1
    #             self.p001 = sensor.temperature

    #         elif sensor.x == storage.x_max and sensor.y == storage.y_min and sensor.z == storage.z_max:
    #             count += 1
    #             self.p101 = sensor.temperature

    #         elif sensor.x == storage.x_min and sensor.y == storage.y_max and sensor.z == storage.z_max:
    #             count += 1
    #             self.p011 = sensor.temperature

    #         elif sensor.x == storage.x_max and sensor.y == storage.y_max and sensor.z == storage.z_max:
    #             count += 1
    #             self.p111 = sensor.temperature

    #     if count != 8:
    #         self.isvalid = False 

    def generate_temperatures(self, first_interpolation, storage):
        x_min = storage.x_min 
        y_min = storage.y_min
        z_min = storage.z_min 
        x_max = storage.x_max
        y_max = storage.y_max
        z_max = storage.z_max
        self.p000 = first_interpolation[x_min][y_min][z_min]
        self.p100 = first_interpolation[x_max][y_min][z_min]
        self.p110 = first_interpolation[x_max][y_max][z_min]
        self.p001 = first_interpolation[x_min][y_min][z_max]
        self.p101 = first_interpolation[x_max][y_min][z_max]
        self.p010 = first_interpolation[x_min][y_max][z_min]
        self.p011 = first_interpolation[x_min][y_max][z_max]
        self.p111 = first_interpolation[x_max][y_max][z_max]

    def __str__(self) -> str:
        return str({
            "p000": self.p000,
            "p100": self.p100,
            "p010": self.p010,
            "p110": self.p110,
            "p001": self.p001,
            "p101": self.p101,
            "p011": self.p011,
            "p111": self.p111
        })