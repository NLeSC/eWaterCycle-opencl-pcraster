try:
    import numpy
except:
    raise ImportError, "Import of module 'numpy' failed."

_minimal_numpy_version = "1.2.1"
if numpy.__version__[:5] < _minimal_numpy_version:
    raise ImportError, "NumPy needs to be of version %s or higher, %s is installed" % (_minimal_numpy_version, numpy.__version__[:5])

import PCRaster
import _NumPy


def pcr2numpy(
         map,
         mv):
    """
    Convert entities from PCRaster to NumPy.

    map -- Map you want to convert.
    mv -- Value to use in the result array cells as a missing value.

    Returns an array.
    """
    return _NumPy.pcr2numpy(PCRaster.clone(), map, mv)

def pcr2numarray(
         map,
         mv):
    """
    DEPRECATED: use pcr2numpy().
    """
    return _NumPy.pcr2numarray(PCRaster.clone(), map, mv)

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

    if dataType == PCRaster.Scalar or dataType == PCRaster.Directional:
        array = array.astype(numpy.float64)

    return _NumPy.numpy2pcr(PCRaster.clone(), dataType, array, mv)

def numarray2pcr(
         dataType,
         array,
         mv):
    """
    DEPRECATED: use numpy2pcr().
    """

    if dataType == PCRaster.Scalar or dataType == PCRaster.Directional:
        array = array.astype(numpy.float64)

    return _NumPy.numarray2pcr(PCRaster.clone(), dataType, array, mv)
