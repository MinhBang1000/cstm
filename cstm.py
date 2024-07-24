import numpy as np


def rmse_3d(array1, array2):
    """
    Calculates the Root Mean Squared Error between two 3D arrays.

    Args:
        array1: First 3D numpy array.
        array2: Second 3D numpy array with the same shape as array1.

    Returns:
        The RMSE value (a scalar).
    """
    # Ensure arrays have the same shape
    if array1.shape != array2.shape:
        raise ValueError("Arrays must have the same shape")

    # Calculate squared differences
    squared_diffs = (array1 - array2) ** 2

    # Mean of squared differences
    mean_squared_diff = squared_diffs.mean()

    # RMSE
    rmse = np.sqrt(mean_squared_diff)
    return rmse

temperature_data_3 = np.load("temperature_data_3.npy")
temperature_data_4 = np.load("temperature_data_4.npy")
temperature_data_5 = np.load("temperature_data_5.npy")
delta = np.absolute(temperature_data_3 - temperature_data_4)
delta_1 = np.absolute(temperature_data_3 - temperature_data_5)
delta_2 = np.absolute(temperature_data_4 - temperature_data_5)
summary = np.sum(delta)
summary_1 = np.sum(delta_1)
summary_2 = np.sum(delta_2)

print("Tong do lech trung binh cua khoi 3 va 4 la ", summary)
print("Tong do lech trung binh cua khoi 3 va 5 la ", summary_1)
print("Tong do lech trung binh cua khoi 4 va 5 la ", summary_2)

do_lech_trung_binh = summary / np.size(delta)
do_lech_trung_binh_1 = summary_1 / np.size(delta_1)
do_lech_trung_binh_2 = summary_2 / np.size(delta_2)

print("Do lech trung binh cua khoi 3 va 4 la ", do_lech_trung_binh)
print("Do lech trung binh cua khoi 3 va 5 la ", do_lech_trung_binh_1)
print("Do lech trung binh cua khoi 4 va 5 la ", do_lech_trung_binh_2)