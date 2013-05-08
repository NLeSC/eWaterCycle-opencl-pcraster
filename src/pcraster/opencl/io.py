'''

Functions for reading and writing maps

Created on May 7, 2013
 
@author: Niels Drost
'''

import pcraster._pcraster as _pcraster

def setclone(filename):
    '''Set the clone.
   
    map -- Filename of clone map.\n
    '''
    print "set clone in opencl pcraster"
    _pcraster.setclone(filename)

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
    _pcraster.report(map, filename)
    
def readmap(filename):
    '''Read a map.
    
    filename -- Filename of a map to read.
    '''
    print "opencl readmap"
    return _pcraster.readmap(filename)



    
# 
#   def("cellvalue", pp::fieldGetCellIndex,
#   "Return a cell value from a map.\n"
#   "\n"
#   "map -- Map you want to query.\n"
#   "index -- Linear index of a cell in the map, ranging from\n"
#   "         [1, number-of-cells].\n"
#   "\n"
#   "Returns a tuple with two elements: the first is the cell value, the second\n"
#   "is a boolean value which shows whether the first element, is valid or not.\n"
#   "If the second element is False, the cell contains a missing value.\n"
#   "See also: cellvalue(map, row, col)");
# 
#   def("cellvalue", pp::fieldGetCellRowCol,
#   "Return a cell value from a map.\n"
#   "\n"
#   "map -- Map you want to query.\n"
#   "row -- Row index of a cell in the map, ranging from [1, number-of-rows].\n"
#   "col -- Col index of a cell in the map, ranging from [1, number-of-cols].\n"
#   "\n"
#   "Returns a tuple with two elements: the first is the cell value,\n"
#   "the second is a boolean value which shows whether the first element,\n"
#   "is valid or not.\n"
#   "If the second element is False, the cell contains a missing value.\n"
#   "See also: cellvalue(map, index)");
# 
#   def("setglobaloption", pp::setGlobalOption,
#   "Set the global option. The option argument must not contain the leading\n"
#   "dashes as used on the command line of pcrcalc.\n"
#   "\n"
#   "Python example:\n"
#   "  setglobaloption(\"unitcell\")\n"
#   "\n"
#   "The pcrcalc equivalent:\n"
#   "  pcrcalc --unitcell -f model.mod\n"
#   );
# 
#   def("pcr2numpy", pcraster::python::field2Array);
#   def("pcr_as_numpy", pcraster::python::fieldAsArray);
#   def("numpy2pcr", pcraster::python::numpy2pcr,
#       return_value_policy<manage_new_object>());