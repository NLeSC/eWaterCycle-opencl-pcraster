#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import pfBase
import re
import os
import PCRaster



class ParticleFilterModel(pfBase.ParticleFilterBase):
    def __init__(self):
        pfBase.ParticleFilterBase.__init__(self)

    # # \brief Reports a map into the state variable directory
    def reportState(self, variable, variableName):
        sample = str(self.currentSampleNumber())
        if re.search(".map", variableName):
            filename = variableName
        else:
            filename = frameworkBase.generateNameT(variableName, self.currentTimeStep())
        name = os.path.join(sample, "stateVar", filename)
        PCRaster.report(variable, name)

    # # \brief Reads a state variable map
    def readState(self, variableName):
        sample = str(self.currentSampleNumber())
        if re.search(".map", variableName):
            filename = variableName
        else:
            timestep = self.firstTimeStep() - 1
            filename = frameworkBase.generateNameT(variableName, timestep)
        name = os.path.join(sample, "stateVar", filename)
        import PCRaster
        return PCRaster.readmap(name)
