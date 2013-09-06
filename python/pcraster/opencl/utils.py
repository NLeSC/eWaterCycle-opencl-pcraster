'''
Created on Apr 26, 2013

@author: niels
'''
import pyopencl as cl

import numpy
import numpy.linalg as la
import pcraster
    
context = cl.create_some_context()
command_queue = cl.CommandQueue(context, properties= cl.command_queue_properties.PROFILING_ENABLE)

prg = cl.Program(context, """
        __kernel void sum(__global const float *a,
        __global const float *b, __global float *result, const int map_width)
        {
          int myX = get_global_id(0);
          int myY = get_global_id(1);
          int myIndex = (get_global_size(0) * myY) + myX;
          
          if (a[myIndex] == 1e20f) {
              result[myIndex] = 1e20f;
          } else if (b[myIndex] == 1e20f) {
              result[myIndex] = 1e20f;
          } else {
              result[myIndex] = a[myIndex] + b[myIndex];
          }
        }
        """).build()
        
#          uint ones = 0xffffffff;
#          float pcr_nan = as_float(0xffffffff); 
#          result[myIndex] = isnan(a[myIndex]) ?  : a[myIndex] + b[myIndex];


#rather complicated way to generate a float with all bits set (missing value in the pcraster format)
onearray = numpy.empty(1, numpy.float32)
as_int_array = onearray.view(numpy.uint32)  
as_int_array[0] = int("0xffffffff", 16)
pcraster_float32_mv = onearray[0]

mf = cl.mem_flags

def numpy2raster(ndarray):
    #ndarray[numpy.isnan(ndarray)]=1e20
    return pcraster.numpy2pcr(pcraster.Scalar, ndarray, 1e20)

def raster2numpy(raster):
    return pcraster.pcr2numpy(raster, 1e20)

def new_scalar():
    return pcraster.newScalarField()

def as_numpy(map):
    return pcraster.pcr_as_numpy(map, numpy.nan)

def enqueue_sum(a_buffer, b_buffer, result_buffer, shape):
    width = numpy.int32(shape[0])
    #prg.sum(command_queue, shape, a_buffer, b_buffer, result_buffer, width)
    event = prg.sum(command_queue, shape, a_buffer, b_buffer, result_buffer, width)
#    event.wait()
#    elapsed = 1e-9 * (event.profile.end - event.profile.start)
#    print "Execution time: %g s" % elapsed

def do_copy(src_buffer, dst_array):    
    cl.enqueue_copy(command_queue, dst_array, src_buffer)
    
def create_readbuffer(ndarray):
    return cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ndarray)

def create_writebuffer(size):
    return cl.Buffer(context, mf.WRITE_ONLY, size)

def set_mv(ndarray):
    #ndarray[numpy.isnan(ndarray)]= pcraster_float32_mv
    pass
    
def badd(arg1, arg2):
    '''binary add two maps together. returns a new map'''

#    print "start of badd operation"
   
    #pcraster maps as numpy arrays 
    a_ndarray = raster2numpy(arg1)
    b_ndarray = raster2numpy(arg2)
    
#    print "a array = ", a_ndarray
#    print "b array = ", b_ndarray
    
    a_buffer = create_readbuffer(a_ndarray)
    b_buffer = create_readbuffer(b_ndarray)
    
    result_buffer = create_writebuffer(a_ndarray.nbytes)

    enqueue_sum(a_buffer, b_buffer, result_buffer, a_ndarray.shape)

    result_ndarray = numpy.empty_like(a_ndarray)

#    print "result array = ", result_ndarray
    
    #copy result buffer into result map
    do_copy(result_buffer, result_ndarray)

    #explicitly set pcraster_mv if needed    
    set_mv(result_ndarray)
    
    return numpy2raster(result_ndarray)
