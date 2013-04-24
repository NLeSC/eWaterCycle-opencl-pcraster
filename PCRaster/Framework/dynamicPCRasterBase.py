#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import dynamicBase
import types


import PCRaster._PCRaster as pcr
import sys


class DynamicModel(dynamicBase.DynamicBase):
  def __init__(self):
    dynamicBase.DynamicBase.__init__(self)
    self.silentModelOuput = False

  def initial(self):
    print "Implement 'initial' method"

  def dynamic(self):
    print  "Implement 'dynamic' method"

  ## \brief Sets the verbosity level of the model
  # \param value True shows progress of timesteps, False no output
  def setQuiet(self, value):
    assert type(value) == types.BooleanType
    self.silentModelOuput = value

  def _silentModelOuput(self):
    return self.silentModelOuput

  ## \brief Returns a list of time steps configured.
  def timeSteps(self):
    """
    Returns a list of time steps configured
    """
    return range(self.firstTimeStep(), self.nrTimeSteps() + 1)

  ## \brief Returns the number of time steps configured.
  #
  # \return 0 for static models, number of time steps otherwise
  def nrTimeSteps(self):
    assert self._d_nrTimeSteps
    return self._d_nrTimeSteps


  ## \brief Returns the current time step.
  #
  # \return 0 for static models, current time step in range from 1 to
  # nrTimeSteps() otherwise
  def currentTimeStep(self):
    assert self.currentStep >= 0
    return self.currentStep

  ## \brief returns first timestep of a model
  def firstTimeStep(self):
    assert self._d_firstTimeStep
    return self._d_firstTimeStep



  ## \brief Storing map data to disk.
  #
  # \param variable object containing the PCRaster map data
  # \param name name used as filename. Use filename with less than eight characters
  # and without extension. File extension for dynamic models is ".map" in initial section
  # and the 8.3 style format name in the dynamic section.
  # File extensions will be appended automatically.
  def report(self, variable, name, style=1):
    self._reportNew(variable, name)


  ## \brief Reading map data from disk.
  #
  # \param name name used as filename. Use filename with less than eight characters
  # and without extension. File extension for dynamic models is ".map" in initial section
  # and the 8.3 style format name in the dynamic section.
  # File extensions will be appended automatically.
  def readmap(self, name, style=1):
    return self._readmapNew(name)



  def _setNrTimeSteps(self, timeSteps):
    """
    in addition to the setting the number of timesteps we need to pass the value to the PCRaster runtime engine
    """
    dynamicBase.DynamicBase._setNrTimeSteps(self, timeSteps)

    pcr._rte().setNrTimeSteps(timeSteps)





  def _setCurrentTimeStep(self, step):
    """
    in addition to the setting the current timestep we need to pass the value to the PCRaster runtime engine
    """
    dynamicBase.DynamicBase._setCurrentTimeStep(self, step)

    pcr._rte().setCurrentTimeStep(step)