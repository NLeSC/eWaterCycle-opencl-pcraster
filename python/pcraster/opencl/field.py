'''
Created on Sep 6, 2013

@author: niels
'''

import native_operations as operations
from pcraster import _pcraster
from pcraster import numpy_operations

import pyopencl
import numpy
from pcraster.opencl.rasterspace import RasterSpace
from pcraster.opencl import clone

class Field(object):

    def __init__(self, opencl_context, original=None):
        if original is None:
            self.is_spatial = True
            
            self.buffer = self.create_opencl_buffer(opencl_context)
            
        elif isinstance(original, _pcraster.Field):
            if original.dataType != _pcraster.Scalar:
                raise Exception("OpenCL PCRaster only supports scalar fields")
            
            self.is_spatial = original.isSpatial
            self.buffer = self.copy_from_pcraster_field(opencl_context, original)
        
    def is_spatial(self):
        return self.is_spatial

    def create_opencl_buffer(self, opencl_context):
        clone_space = clone.clone()

        if self.is_spatial:
            self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, clone_space.map_data_size)
        else:
            # single data item
            self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, numpy.dtype(numpy.float32).itemsize)

    def copy_from_pcraster_field(self, opencl_context, pcraster_field):
        numpy_array = numpy_operations.pcr_as_numpy(pcraster_field)
        self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, clone().map_data_size)
        # pyopencl.en
        pass
        
    
    def to_pcraster_field(self):
        pass
    
    # Some syntactic sugar to allow the use of operators on fields.
    # See http://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
    # Note the reverse of the arguments in all reflected(swapped) operands when calling the operation
    #
    # TODO: also add in-place operators such as "+="
    
    def __and__(self, other):
        return operations.pcrand(self, other)
     
    def __rand__(self, other):
        return operations.pcrand(other, self)
     
    def __or__(self, other):
        return operations.pcror(self, other)
     
    def __ror__(self, other):
        return operations.pcror(other, self)
     
    def __xor__(self, other):
        return operations.pcrxor(self, other)
     
    def __invert__(self):
        return operations.pcrnot(self)
     
    def __ne__(self, other):
        return operations.pcrne(self, other)
     
    def __eq__(self, other):
        return operations.pcreq(self, other)
     
    def __gt__(self, other):
        return operations.pcrgt(self, other)
     
    def __ge__(self, other):
        return operations.pcrge(self, other)
     
    def __lt__(self, other):
        return operations.pcrlt(self, other)
     
    def __le__(self, other):
        return operations.pcrle(self, other)
     
    def __mul__(self, other):
        return operations.pcrmul(self, other)
     
    def __rmul__(self, other):
        return operations.pcrmul(other, self)
     
    def __div__(self, other):
        return operations.pcrfdiv(self, other)
     
    def __rdiv__(self, other):
        return operations.pcrfdiv(other, self)
     
    def __floordiv__(self, other):
        return operations.pcridiv(self, other)
     
    def __rfloordiv__(self, other):
        return operations.pcridiv(other, self)
     
    def __pow__(self, other):
        return operations.pcrpow(self, other)
     
    def __rpow__(self, other):
        return operations.pcrpow(other, self)
     
    def __mod__(self, other):
        return operations.pcrmod(self, other)
     
    def __rmod__(self, other):
        return operations.pcrmod(other, self)
     
    def __add__(self, other):
        return operations.pcrbadd(self, other)
     
    def __radd__(self, other):
        print 'radd'
        return operations.pcrbadd(other, self)
     
    def __sub__(self, other):
        return operations.pcrbmin(self, other)
     
    def __rsub__(self, other):
        return operations.pcrbmin(other, self)
     
    def __neg__(self):
        return operations.pcrumin(self)
     
    def __pos__(self):
        return operations.pcruadd(self)
    
    # TODO: implement
    
    def _bool(self):
        raise Exception("Not implemented")
    
    def _int(self):
        raise Exception("Not implemented")

    def _float(self):
        raise Exception("Not implemented")
            
    def __nonzero__(self):
        raise Exception("Not implemented")
