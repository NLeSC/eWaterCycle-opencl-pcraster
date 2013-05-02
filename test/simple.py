from pcraster import *

setclone("Global_CloneMap_30min.map")

inputMap = readmap("Global_InterceptCapacity-Grassland_0000-12-18_30min.map")
result = readmap("Global_InterceptCapacity-Grassland_0000-12-18_30min.map")

for i in range(1000):
    result = result + inputMap

report(result, "result.map")

