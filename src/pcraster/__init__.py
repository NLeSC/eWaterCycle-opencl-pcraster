#Note: order is significant!

use_opencl = False

if use_opencl:
    from pcraster.opencl import *
else:
    from operations import *
    import operators
    from _pcraster import *
    from _pcraster_modflow import *
    from aguila import *
    from numpy_operations import *
