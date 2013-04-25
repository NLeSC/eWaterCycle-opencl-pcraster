import glob, os, string
import pcr

# TODO see /usr/local/cubeadm/loadavg
# TODO mosctl getload

# Return true if system has a mosix patched kernel.
def systemHasMosixKernel():
    return os.path.exists("/proc/hpc") and pcr.execute("mosctl isup")[:-1] == "yes"

# Get the number of CPU's in an openMosix-cluster.
def nrCPUs():
    nrCPUs = 0
    for fileName in glob.glob("/proc/hpc/nodes/*/cpus"):
        # Keep trying as long as the contents of the file does not contain a valid
        # integer.
        success = False
        while not success:
            try:
                nr = int(file(fileName, "r").read())
                success = True
            except(ValueError):
                pass

        if nr != -101:
            assert nr > 0
            nrCPUs += nr

    return nrCPUs

# Returns the total load of the cluster. A load of 100.0 means one processor
# is fully occupied.
def load():
    totalLoad = 0.0
    for fileName in glob.glob("/proc/hpc/nodes/*/load"):
        # Keep trying as long as the contents of the file does not contain a valid
        # float.
        success = False
        while not success:
            try:
                load = float(file(fileName, "r").read())
                success = True
            except(ValueError):
                pass

        if load >= 0.0:
            totalLoad += load
    return totalLoad / 2.5

def loadPerCPU():
    return load() / nrCPUs()

# Unlock self -> ensure that the created process is unlocked.
def unlock():
    file("/proc/self/lock", "w").write(0)
