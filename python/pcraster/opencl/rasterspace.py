'''
Created on Sep 18, 2013

Extend of a map such as number of rows, colums, cell size, etc. Mostly used for the clone map.

@author: Niels Drost
'''
import numpy
class RasterSpace(object):
    
    def __init__(self, nrRows, nrCols, north, west, cellSize):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.north = north
        self.west = west
        self.cellSize = cellSize
        
        self.map_data_size = nrRows * nrCols * numpy.dtype(numpy.float32).itemsize
