import vtk
import numpy as np

def arrayFromVolume(volumeNode):
    """ Return voxel array from volume node as numpy array.
        Voxels values are not copied. Voxel values in the volume node can be modified
        by changing values in the numpy array.
        After all modifications has been completed, call :py:meth:`arrayFromVolumeModified`.
        .. warning:: Memory area of the returned array is managed by VTK, therefore
        values in the array may be changed, but the array must not be reallocated
        (change array size, shallow-copy content from other array most likely causes
        application crash). To allow arbitrary numpy operations on a volume array:
        1. Make a deep-copy of the returned VTK-managed array using :func:`numpy.copy`.
        2. Perform any computations using the copied array.
        3. Write results back to the image data using :py:meth:`updateVolumeFromArray`.
    """

    scalarTypes = ['vtkMRMLScalarVolumeNode', 'vtkMRMLLabelMapVolumeNode']
    vectorTypes = ['vtkMRMLVectorVolumeNode', 'vtkMRMLMultiVolumeNode', 'vtkMRMLDiffusionWeightedVolumeNode']
    tensorTypes = ['vtkMRMLDiffusionTensorVolumeNode']
    vimage = volumeNode.GetImageData()
    nshape = tuple(reversed(volumeNode.GetImageData().GetDimensions()))
    
    # import vtk.util.numpy_support
    narray = None

    if volumeNode.GetClassName() in scalarTypes:
        narray = vtk.util.numpy_support.vtk_to_numpy(vimage.GetPointData().GetScalars()).reshape(nshape)
    
    elif volumeNode.GetClassName() in vectorTypes:
        components = vimage.GetNumberOfScalarComponents()
    
    if components > 1:
        nshape = nshape + (components,)
        narray = vtk.util.numpy_support.vtk_to_numpy(vimage.GetPointData().GetScalars()).reshape(nshape)
    
    elif volumeNode.GetClassName() in tensorTypes:
        narray = vtk.util.numpy_support.vtk_to_numpy(vimage.GetPointData().GetTensors()).reshape(nshape+(3,3))
    
    else:
        raise RuntimeError("Unsupported volume type: "+volumeNode.GetClassName())
    
    return narray

def updateVolumeFromArray(volumeNode, narray):
    """Return voxel array of a segment's binary labelmap representation as numpy array.
    Voxels values are copied.
    If binary labelmap is the master representation then voxel values in the volume node can be modified
    by changing values in the numpy array.
    After all modifications have been completed, call::
      segmentationNode.GetSegmentation().GetSegment(segmentID).Modified()
    .. warning:: Important: memory area of the returned array is managed by VTK,
    therefore values in the array may be changed, but the array must not be reallocated.
    See :py:meth:`arrayFromVolume` for details.
    """

    vshape = tuple(reversed(narray.shape))
    if len(vshape) == 3:
    # Scalar volume
        vcomponents = 1

    elif len(vshape) == 4:
    # Vector volume
        vcomponents = vshape[0]
        vshape = vshape[1:4]
    else:
    # TODO: add support for tensor volumes
        raise RuntimeError("Unsupported numpy array shape: "+str(narray.shape))

    vimage = volumeNode.GetImageData()
    if not vimage:
        # import vtk
        vimage = vtk.vtkImageData()
        volumeNode.SetAndObserveImageData(vimage)
    # import vtk.util.numpy_support
    vtype = vtk.util.numpy_support.get_vtk_array_type(narray.dtype)

    # Volumes with "long long" scalar type are not rendered corectly.
    # Probably this could be fixed in VTK or Slicer but for now just reject it.
    if vtype == vtk.VTK_LONG_LONG:
        raise RuntimeError("Unsupported numpy array type: long long")

    vimage.SetDimensions(vshape)
    vimage.AllocateScalars(vtype, vcomponents)

    narrayTarget = arrayFromVolume(volumeNode)
    narrayTarget[:] = narray

    return narray


narray = np.load('maskdatamaskedimages_test.npy')
volumeNode = 

updateVolumeFromArray(volumeNode, narray)