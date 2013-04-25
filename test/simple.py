from PCRaster import *

setclone("mask.map")

# map with location of rainstation

SoilMap = readmap("dem.map")

result = SoilMap * scalar(2)

report(result, "result.map")

