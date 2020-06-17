import numpy as np
import sys
import pyvista as pv

data_matrix = np.load('maskdatamaskedimages_test.npy')

# np.savetxt("array.txt", data_matrix[1])

# np.set_printoptions(threshold=sys.maxsize)

# print(data_matrix[1])

opacity = [0, 0, 0, 4, 8, 0, 0] # 7

data = pv.wrap(data_matrix)
pv.set_plot_theme("night")
data.plot(volume=True, cmap="cool", opacity = opacity, shade = False)

# "sigmoid_6"
