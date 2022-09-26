class Storage():
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    z_min = 0
    z_max = 0

    def __init__(self, model_instance):
        self.x_max = model_instance.storage_length
        self.y_max = model_instance.storage_width
        self.z_max = model_instance.storage_height

    