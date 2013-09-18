import pcraster._pcraster as pcr
import numpy

'''
Created on May 8, 2013

@author: niels
'''
# def pcr_as_numpy(
#         map,
#         mv):
#     """
#     View a map as a numpy array. Changes in map will be reflected in numpy array and vice versa
# 
#     map -- Map you want to convert.
#     mv -- Value to use in the result array cells as a missing value.
# 
#     Returns an array.
#     """
#     return pcr.pcr_as_numpy(pcr.clone(), map.pcrmap, mv)
from pcraster.opencl.field import Field

def pcr2numpy(
        map,
        mv):
    """
    Convert entities from PCRaster to NumPy.

    map -- Map you want to convert.
    mv -- Value to use in the result array cells as a missing value.

    Returns an array.
    """
    return pcr.pcr2numpy(pcr.clone(), map.pcrmap, mv)


def numpy2pcr(
        dataType,
        array,
        mv):
    """
    Convert entities from NumPy to PCRaster.

    dataType -- Either Boolean, Nominal, Ordinal, Scalar, Directional or
                Ldd.
    array -- Array you want to convert.
    mv -- Value that identifies a missing value in the array.

    Returns a map.
    """
    if dataType == pcr.Scalar or dataType == pcr.Directional:
        array = array.astype(numpy.float64)

    return Field(pcr.numpy2pcr(pcr.clone(), dataType, array, mv))