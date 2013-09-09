'''

Functions for reading and writing maps

Created on May 7, 2013
 
@author: Niels Drost
'''

import pcraster._pcraster as _pcraster
from pcraster.opencl.map import OpenCLMap

Scalar = _pcraster.Scalar

clone = None

def clone():
    '''Get the clone map
    '''
    print "get clone in opencl pcraster"
    return clone

def setclone(filename):
    '''Set the clone.
   
    map -- Filename of clone map.\n
    '''
    print "set clone in opencl pcraster"
    _pcraster.setclone(filename)
    clone = OpenCLMap(_pcraster.clone())

# def report(source, destination):
# FIXME: also support a filename as a source for report
#     '''Write data from a file to a file.
#     
#     filename -- Filename of data you want to open and write.
#     filename -- Filename to use.
#     '''

def report(map, filename):
    ''''Write a map to a file.
    
    map -- Map you want to write.
    filename -- Filename to use.
    '''
    print "opencl report"
    _pcraster.report(map.pcrmap, filename)

def readmap(filename):
    '''Read a map.
    
    filename -- Filename of a map to read.
    '''
    print "opencl readmap"
    
    pcrmap = _pcraster.readmap(filename)
    
    return OpenCLMap(pcrmap)
    

# def cellvalue(map, index):
#     '''Return a cell value from a map.
#     
#     map -- Map you want to query.
#     index -- Linear index of a cell in the map, ranging from [1, number-of-cells].
#     
#     Returns a tuple with two elements: the first is the cell value, the second
#     is a boolean value which shows whether the first element, is valid or not.
#     If the second element is False, the cell contains a missing value.
#     See also: cellvalue(map, row, col)
#     '''
#     return _pcraster.cellvalue(map, index)

def cellvalue(map, row, col = -1):
    '''Return a cell value from a map.
    
    map -- Map you want to query.
    row -- Row index of a cell in the map, ranging from [1, number-of-rows].
    col -- Col index of a cell in the map, ranging from [1, number-of-cols].
    
    Returns a tuple with two elements: the first is the cell value,
    the second is a boolean value which shows whether the first element,
    is valid or not.
    If the second element is False, the cell contains a missing value.
    See also: cellvalue(map, index)
    '''
    if col == -1:
        return _pcraster.cellvalue(map, row)
    
    return _pcraster.cellvalue(map, row, col)
    
def setglobaloption(option):
    '''Set the global option.
    
    Not supported currently.
    '''
    
    raise Exception("Setting global options not supported currently.")
