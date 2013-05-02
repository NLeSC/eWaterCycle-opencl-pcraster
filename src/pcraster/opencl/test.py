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
