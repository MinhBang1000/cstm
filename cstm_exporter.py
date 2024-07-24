import numpy as np
from mayavi import mlab
from tvtk.api import tvtk

# temperature_data = 

# Convert to NumPy array
# temperature_array = np.array(temperature_data)

temperature_array = np.load("temperature_data_ID_5.npy")

# Create x, y, z coordinates
x = np.arange(temperature_array.shape[0])
y = np.arange(temperature_array.shape[1])
z = np.arange(temperature_array.shape[2])
X, Y, Z = np.meshgrid(x, y, z)

# Flatten the arrays for plotting
temperatures = temperature_array.flatten()
X = X.flatten()
Y = Y.flatten()
Z = Z.flatten()

# Create the Mayavi figure
fig = mlab.figure(size=(800, 600), bgcolor=(1, 1, 1))

# 3D scatter plot with cubes
points = mlab.points3d(X, Y, Z, temperatures, mode='cube', scale_factor=1.0, colormap='cool', scale_mode='none')

# Customize appearance
points.glyph.color_mode = 'color_by_scalar'

# Add and customize the axes
axes = mlab.axes(points, nb_labels=5)

# Customize label properties
axes.label_text_property.color = (0, 0, 0)
axes.label_text_property.font_size = 14
axes.label_text_property.justification = 'centered'

# Customize title properties
axes.title_text_property.color = (0, 0, 0)
axes.title_text_property.font_size = 16

# Get the colorbar actor and customize
colorbar = mlab.colorbar(orientation="vertical", label_fmt="%4.1f")
colorbar.scalar_bar.label_text_property.color = (0, 0, 0)
colorbar.scalar_bar.label_text_property.font_size = 14

# Show the plot
mlab.show()

