class Sensor():
    x = 0
    y = 0
    z = 0
    temperature = 0

    def __init__(self, model_instance):
        self.x = model_instance.sensor_x
        self.y = model_instance.sensor_y
        self.z = model_instance.sensor_z
        self.temperature = model_instance.sensor_temperature

    def __str__(self) -> str:
        return str({
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "temperature": self.temperature
        })