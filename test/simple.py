from pcraster import *

setclone("mask.map")

# map with location of rainstation

SoilMap = readmap("dem.map")
result = readmap("dem.map")

for i in range(1):
    result = result + SoilMap

report(result, "result.map")

