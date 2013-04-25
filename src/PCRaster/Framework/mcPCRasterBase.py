#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import mcBase
import PCRaster



class MonteCarloModel(mcBase.MonteCarloBase):
    def __init__(self):
        mcBase.MonteCarloBase.__init__(self)

    def premcloop(self):
        print "premcloop not implemented"

    def postmcloop(self):
        print "postmcloop not implemented"

    # # \brief Reporting map data to disk
    # standard extension is "map" in initial and timestep in the dynamic
    # section
    # output directory will be sample directory
    def report(self, variable, name):
        self._reportNew(variable, name)

    # # \brief Reading sample data from disk
    # returns the map of the current time step from the current sample directory
    def readmap(self, name):
        return self._readmapNew(name)

    # # \brief Reading deterministic data from disk
    # returns the map of the file with current time step, from the current working directory
    def readDeterministic(self, name):
        if self._inPremc() or self._inPostmc() or self._inInitial():
            newName = name + ".map"
        else:
            newName = frameworkBase.generateNameT(name, self.currentTimeStep())


        return PCRaster.readmap(newName)
