'''
Created on Oct 3, 2013

@author: Niels Drost
'''
from pcraster import _pcraster
from pcraster.opencl.rasterspace import RasterSpace
current_clone = None

def clone():
    '''Get the clone raster space
    '''
    print "get clone in opencl pcraster"
    return current_clone

def setclone(*args):
    '''Set the clone. Either from a file (supply filename) or from nrRows, nrCols, cellSize, west and north.
    '''
    
    global current_clone
    
    print "setting clone in opencl pcraster!"
    
    print "clone seems to be", current_clone
    
    if current_clone is not None:
        raise Exception("clone map already set, cannot re-set")
    
    if (len(args) == 1):
        print "set clone in opencl pcraster"
        _pcraster.setclone(args[0])
        pcrasterClone = _pcraster.clone()
        current_clone = RasterSpace(pcrasterClone.nrRows(), pcrasterClone.nrCols(), pcrasterClone.cellSize(), pcrasterClone.west(), pcrasterClone.north())
    elif (len(args) == 5):
        current_clone = RasterSpace(*args)
        _pcraster.setclone(*args)
    else:
        raise Exception("setclone requires either a filename or the number of rows and columns, cellsize, west and north of the rasterspace.")
