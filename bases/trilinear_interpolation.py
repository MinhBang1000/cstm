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

storage_space = {
    "x_min": 0,
    "y_min": 0,
    "z_min": 0,
    "x_max": 53,
    "y_max": 22,
    "z_max": 25
}

point = {
    "x": 53/2,
    "y": 11,
    "z": 12.5
}

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

def trilinear_interpolation(storage_space, temperatures, lamda = 1):
    c_parameters = c_generators(temperatures)
    total = [[ ['#' for col in range(storage_space.get("z_max")+1)] for col in range(storage_space.get("y_max")+1)] for row in range(storage_space.get("x_max")+1)]
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
    return total

# lst_3d = trilinear_interpolation(storage_space=storage_space, temperatures=temperatures, lamda = 1)