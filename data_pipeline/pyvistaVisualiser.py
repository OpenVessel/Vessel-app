import numpy as np
import pyvista as pv

data_matrix = np.load('maskdatamaskedimages_test.npy')

opacity = [0, 0, 0, 4, 8, 0, 0] 

data = pv.wrap(data_matrix)
pv.set_plot_theme("night")

data.save("lung.vtk")

data.plot(volume=True, cmap="cool", opacity = opacity, shade = False)