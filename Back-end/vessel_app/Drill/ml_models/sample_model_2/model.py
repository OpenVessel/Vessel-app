try:    
    import pyvista as pv
except:
    print('import pyvista failed')
import numpy as np


def machine_learning(*args):

    data = pv.wrap(np.array(*args))
    return data # pyvista object


def run_model(dicom_list, my_number, condiment, color, my_number_2):

    data = machine_learning(my_number, condiment, color, my_number_2)
    return data # pyvista object

