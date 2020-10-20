try:    
    import pyvista as pv
except:
    print('import pyvista failed')
import numpy as np

def run_model(dicom_list, keyword1, keyword2, keyword3, keyword4):

    def machine_learning(*args):

        data = pv.wrap(np.array(*args))
        return data

    data = machine_learning(keyword1, keyword2, keyword3, keyword4)
    

    return data # pyvista object

