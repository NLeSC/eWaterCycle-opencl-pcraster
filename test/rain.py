#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PCRaster import *
from PCRaster.Framework import *

class RainModel(DynamicModel):
  def __init__(self, cloneMap):
    DynamicModel.__init__(self)
    setclone(cloneMap)

    # map with location of rainstations
    self.RainStations = readmap("rainstat.map")
    # timeseries with rain at rainstations
    self.RainTimeSeries = "rain.tss"
    # reported stack of maps with rain
    self.RainZones = "rainzone"
    # reported maps with rain (mm/6hours)
    self.SurfaceWater = "rainfall"

  def initial(self):
    # coverage of meteorological stations for the whole area
    rainZones = spreadzone(self.RainStations, 0, 1)
    self.report(rainZones, self.RainZones)

  def dynamic(self):
    # calculate and report maps with rainfall at each timestep (mm/6 hours)
    surfaceWater = timeinputscalar(self.RainTimeSeries, self.RainZones)
    self.report(surfaceWater, self.SurfaceWater)

myModel = RainModel("mask.map")
dynModelFw = DynamicFramework(myModel, lastTimeStep=28, firstTimestep=1)
dynModelFw.run()
