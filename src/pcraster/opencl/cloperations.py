'''
Created on Apr 26, 2013

@author: niels
'''
import pyopencl as cl

import numpy
import numpy.linalg as la
import pcraster
    
context = cl.create_some_context()
command_queue = cl.CommandQueue(context, properties=
cl.command_queue_properties.PROFILING_ENABLE)

prg = cl.Program(context, """
        __kernel void sum(__global const float *a,
        __global const float *b, __global float *result, const int map_width)
        {
          int myX = get_global_id(0);
          int myY = get_global_id(1);
          int myIndex = map_width * myY + myX;
          uint ones = 0xffffffff;
          float pcr_nan = as_float(0xffffffff); 
          result[myIndex] = isnan(a[myIndex]) ?  : a[myIndex] + b[myIndex];
          //result[myIndex] = a[myIndex] + b[myIndex];
          
        }
        """).build()

#rather complicated way to generate a float with all bits set (missing value in the pcraster format)
onearray = numpy.empty(1, numpy.float32)
as_int_array = onearray.view(numpy.uint32)  
as_int_array[0] = int("0xffffffff", 16)
pcraster_float32_mv = onearray[0]

mf = cl.mem_flags

#FIXME we should not actually copy the data, just present a view of it 
def numpy2raster(ndarray, type):
    ndarray[numpy.isnan(ndarray)]=1e20
    return pcraster.numpy2pcr(type, ndarray, 1e20)

def raster2numpy(raster):
    return pcraster.pcr2numpy(raster, numpy.nan)

def new_scalar():
    return pcraster.newScalarField()

def as_numpy(map):
    return pcraster.pcr_as_numpy(map, numpy.nan)

def enqueue_sum(a_buffer, b_buffer, result_buffer, shape):
    width = numpy.int32(shape[0])
    event = prg.sum(command_queue, shape, a_buffer, b_buffer, result_buffer, width)
    event.wait()
    elapsed = 1e-9 * (event.profile.end - event.profile.start)
    print "Execution time: %g s" % elapsed

def do_copy(dst_array, src_buffer):    
    cl.enqueue_copy(command_queue, dst_array, src_buffer)
    
def create_readbuffer(ndarray):
    return cl.Buffer(context, mf.READ_ONLY | mf.USE_HOST_PTR, hostbuf=ndarray)

def create_writebuffer(size):
    return cl.Buffer(context, mf.WRITE_ONLY, size)

def set_mv(ndarray):
    #ndarray[numpy.isnan(ndarray)]= pcraster_float32_mv
    pass
    
def badd(arg1, arg2):
    '''binary add two maps together. returns a new map'''
   
    #pcraster maps as numpy arrays 
    a_ndarray = as_numpy(arg1)
    b_ndarray = as_numpy(arg2)
    
    a_buffer = create_readbuffer(a_ndarray)
    b_buffer = create_readbuffer(b_ndarray)
    
    result_buffer = create_writebuffer(a_ndarray.nbytes)

    enqueue_sum(a_buffer, b_buffer, result_buffer, a_ndarray.shape)

    #map for result
    result_map = new_scalar()
    result_ndarray = as_numpy(result_map)
    
    #copy result buffer into result map
    do_copy(result_ndarray, result_buffer)

    #explicitly set pcraster_mv if needed    
    set_mv(result_ndarray)
    
    return result_map
