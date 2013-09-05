#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import os
import sys
import types
from frameworkBase import generateNameT

## \brief Framework for dynamic models
#
#
class DynamicFramework(frameworkBase.FrameworkBase):
  ## \brief Constructor
  #
  # \param userModel class containing the user model
  # \param lastTimeStep last timestep to run
  # \param firstTimestep sets the starting timestep of the model (optional,
  #        default is 1)
  #
  def __init__(self, userModel, lastTimeStep=0, firstTimestep=1):
    frameworkBase.FrameworkBase.__init__(self)

    self._d_model = userModel
    self._testRequirements()


    # fttb
    self._addMethodToClass(self._readmapNew)
    self._addMethodToClass(self._reportNew)

    try:
      self._userModel()._setNrTimeSteps(lastTimeStep)
      self._d_firstTimestep = firstTimestep
      self._userModel()._setFirstTimeStep(self._d_firstTimestep)
    except Exception, msg:
      sys.stderr.write('Error: %s\n' % str(msg))
      sys.exit(1)


  def _userModel(self):
    """ Returns the class provided by the user """
    return self._d_model





  ## \brief Re-implemented from ShellScript.
  #
  # Runs a dynamic user model.
  def run(self):
    self._atStartOfScript()
    if(hasattr(self._userModel(), "resume")):
      if self._userModel().firstTimeStep() == 1:
        self._runInitial()
      else:
        self._runResume()
    else:
      self._runInitial()

    self._runDynamic()

    # only execute this section while running filter frameworks
    if hasattr(self._userModel(), "suspend") and hasattr(self._userModel(), "filterPeriod"):
      self._runSuspend()

    return 0


  ## \brief testing the requirements for the dynamic framework
  #
  # To use the dynamic framework the user must implement the following methods
  # in this class:
  # - either "run" or "initial" and "dynamic"
  def _testRequirements(self):
    if hasattr(self._userModel(), "_userModel"):
      msg = "The _userModel method is deprecated and obsolete"
      self.showWarning(msg)

    if( not hasattr(self._userModel(), "dynamic") and not hasattr(self._userModel(), "run")):
      msg = "Cannot run dynamic framework: Implement dynamic method"
      raise frameworkBase.FrameworkError(msg)


    if not hasattr(self._userModel(), "initial"):
      if self._debug():
        self.showWarning("No initial section defined.")

  def setQuiet(self, quiet):
    self._d_quiet = quiet
