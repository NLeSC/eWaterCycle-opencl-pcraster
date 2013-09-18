'''
Created on Sep 18, 2013

@author: Niels Drost
'''
clone = None

from pcraster import _pcraster
from . import RasterSpace

def clone():
    '''Get the clone raster space
    '''
    print "get clone in opencl pcraster"
    return clone

def setclone(*args):
    '''Set the clone. Either from a file (supply filename) or from nrRows, nrCols, cellSize, west and north.
    '''
    
    if clone is not None:
        raise Exception("clone map already set, cannot re-set")
    
    if (len(args) == 1):
        print "set clone in opencl pcraster"
        _pcraster.setclone(args[0])
        pcrasterClone = _pcraster.clone()
        clone = RasterSpace(pcrasterClone.nrRows, pcrasterClone.nrRows, pcrasterClone.cellSize, pcrasterClone.west, pcrasterClone.north)
    elif (len(args) == 5):
        clone = RasterSpace(*args)
        _pcraster.setclone(*args)
    else:
        raise Exception("setclone requires either a filename or the number of rows and columns, cellsize, west and north of the rasterspace.")
