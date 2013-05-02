import pyopencl as cl
import numpy

a = numpy.random.rand(5000, 5000).astype(numpy.float32)
b = numpy.random.rand(5000, 5000).astype(numpy.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)


prg = cl.Program(ctx, """
        __kernel void sum(__global const float *a,
        __global const float *b, __global float *result, const int width)
        {
          int myX = get_global_id(0);
          int myY = get_global_id(1);
          int myIndex = (myY * width) + myX;
          result[myIndex] = a[myIndex] + b[myIndex];
        }
        """).build()

width = numpy.int32(5000)


for i in range(1000):
    prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf, width)

a_plus_b = numpy.empty_like(a)
cl.enqueue_copy(queue, a_plus_b, dest_buf)


rndx = numpy.random.randint(4990)
rndy = numpy.random.randint(4990)

print rndx
print rndy
print a[rndx][rndy:rndy + 10]
print b[rndx][rndy:rndy + 10]
print a_plus_b[rndx][rndy:rndy + 10]

def badd_test(arg1, arg2):
    '''binary add two maps together. returns a new map'''
    
    aview = pcraster.pcr_as_numpy(arg1, numpy.nan)

    print 'a-view'    
    print aview[20]
   
#    print 'a-copy'    
    a = raster2numpy(arg1)
    print a[20]

    b = raster2numpy(arg2)
    type = arg1.dataType()
    
    mf = cl.mem_flags
    a_buf = cl.Buffer(context, mf.READ_ONLY | mf.USE_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer(context, mf.READ_ONLY | mf.USE_HOST_PTR, hostbuf=b)
#    a_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
#    b_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    dest_buf = cl.Buffer(context, mf.WRITE_ONLY, b.nbytes)
 
#    prg.sum(command_queue, a.shape, None, a_buf, b_buf, dest_buf)

#    print a.shape
    width = numpy.int32(a.shape[0])
    prg.sum(command_queue, a.shape, a_buf, b_buf, dest_buf, width)
 
    result_map = pcraster.newScalarField()
 
    a_plus_b = pcraster.pcr_as_numpy(result_map, numpy.nan)
    
    #a_plus_b = numpy.empty_like(a)
    
    cl.enqueue_copy(command_queue, a_plus_b, dest_buf)
    
    print a[20]
    print b[20]
    print a_plus_b[20]
    
    #rather complicated way to generate a float with all bits set (missing value in the pcraster format)
    onearray = numpy.empty(1, numpy.float32)
    as_int_array = onearray.view(numpy.uint32)  
    as_int_array[0] = int("0xffffffff", 16)
    pcraster_float32_mv = onearray[0]

    print numpy.version.version
    
    print as_int_array
    print hex(as_int_array[0])

    print onearray
    
    
    #a_plus_b[numpy.isnan(a_plus_b)]= onearray[0]
    a_plus_b[numpy.isnan(a_plus_b)]= pcraster_float32_mv
    
    
#    print "a_plus_b nan->1e20"
#    print a_plus_b[20]
    
#     return numpy2raster(a_plus_b, type)
    return result_map