from pcraster import *

def main():
    setclone("Global_CloneMap_30min.map")



    inputMap = readmap("Global_InterceptCapacity-Grassland_0000-12-18_30min.map")

    result = inputMap + inputMap

    report(result, "result.map")

if __name__ == "__main__":
    main()

