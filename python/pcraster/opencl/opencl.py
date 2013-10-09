'''
OpenCL kernels and state.

Created on Oct 7, 2013

@author: Niels Drost
'''
import pyopencl as cl
import numpy

class OpenCL(object):

    ''' PCRaster operations implemented in opencl kernels
    '''
    OPENCL_SOURCE = """
        __kernel void sum(__global const float *a,
        __global const float *b, __global float *result, const int width)
        {
          int myX = get_global_id(0);
          int myY = get_global_id(1);
          int myIndex = (myY * width) + myX;
          result[myIndex] = a[myIndex] + b[myIndex];
        }
        """
    
    context = cl.create_some_context()
    queue = cl.CommandQueue(context)
    
    program = cl.Program(context, OPENCL_SOURCE).build()

    
    @classmethod
    def convert_to_pcraster(cls, argument):
        pass
    
    
    
#     @staticmethod
#     def create_opencl_buffer():
#         clone_space = clone.clone()
# 
#         if self.is_spatial:
#             self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, clone_space.map_data_size)
#         else:
#             # single data item
#             self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, numpy.dtype(numpy.float32).itemsize)
# 
#     @staticmethod
#     def copy_from_pcraster_field(self, pcraster_field):
#         numpy_array = numpy_operations.pcr_as_numpy(pcraster_field)
#         self.buffer = pyopencl.Buffer(opencl_context, pyopencl.mem_flags.READ_WRITE, clone().map_data_size)
#         # pyopencl.en
#         pass
#         
#     
#     def to_pcraster_field(self):
#         pass
# 
#     
#     @staticmethod
#     def pcrbadd(arg1, arg2):
#         result = Field(context)
# 
#     
#     @classmethod
#     def convert_to_pcraster(cls, argument):
#         pass
    
    
        
 
                     

    
    