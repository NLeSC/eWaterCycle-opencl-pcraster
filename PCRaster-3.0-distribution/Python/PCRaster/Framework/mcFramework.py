#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import staticFramework
import dynamicFramework
import sys
import os, shutil
import system
import forkscript
import types
import time


from frameworkBase import generateNameT, generateNameS, generateNameST

## \brief Framework for Monte Carlo simulations
#
class MonteCarloFramework(frameworkBase.FrameworkBase, forkscript.ForkScript):
  ## \brief
  def __init__(self, userModel, nrSamples=0):
    frameworkBase.FrameworkBase.__init__(self)
    forkscript.ForkScript.__init__(self)

    self._d_model = userModel
    self._testRequirements()

    # adding framework specific attributes and methods

    # keep this fttb
    self._addMethodToClass(self._readmapNew)
    self._addMethodToClass(self._reportNew)

    assert type(nrSamples) == types.IntType
    try:
      self._setSampleNumbers(1, nrSamples)
    except Exception, msg:
      sys.stderr.write('Error: %s\n' % str(msg))
      sys.exit(1)

    # Consecutive model runs by default
    self._d_forkSamples = False

    self._initialiseSampleDirectories()

  ## \brief Sets the forking of samples on or off.
  #
  # \param fork True or False.
  #
  # When forking is on EVERY sample will be forked to its own
  # process. This is mainly useful on a cluster with automatic
  # process migration or on SMP machines.
  #
  # \warning setrandomseed does not work when forking is enabled
  # \warning not available on Windows
  def setForkSamples(self, fork, nrCPUs=1):
    if (sys.platform == "win32"):
      self.showWarning("Forking not available on Windows platforms")
      self._d_nrProcessors = 1
      self._d_forkSamples = False
    else:
      # default detect nrCPUs
      if(nrCPUs == 1):
        self._d_nrProcessors = system.nrCPUs()
      else:
        self._d_nrProcessors = nrCPUs
      self._d_forkSamples = fork

  ## \brief Returns whether samples should be forked.
  def _forkSamples(self):
    return self._d_forkSamples


  ## \brief Returns the class provided by the user
  def _userModel(self):
    return self._d_model._userModel()

  ## \brief Returns the framework provided by the user
  def _userFramework(self):
    return self._d_model

  def _testRequirements(self):
    if (not isinstance(self._userFramework(), staticFramework.StaticFramework)) and (not isinstance(self._userFramework(), dynamicFramework.DynamicFramework)):
      msg = "Cannot run MonteCarlo framework: User model must be type of \
StaticFramework or DynamicFramework"
      raise frameworkBase.FrameworkError(msg)

    if not hasattr(self._userModel(), "premcloop"):
      self.showWarning("No premcloop section defined.")

    if not hasattr(self._userModel(), "postmcloop"):
      self.showWarning("No postmcloop section defined.")


  ## \brief Re-implemented from ShellScript.
  #
  # Runs the user model in the Monte Carlo mode.
  def run(self, premc=True, postmc=True):
    self._atStartOfScript()
    self._check()

    if premc:
      self._runPremcloop()

    # Samples.
    sample = self._userModel()._firstSampleNumber()
    while sample <= self._userModel()._lastSampleNumber():

      if self._forkSamples():
        assert self.isParentProcess()
        while self._systemIsOccupied(self.nrChildProcesses()):
          if self._debug():
            self.showMessage("System is occupied")
          # Wait for some seconds.
          # But first handle finished children.
          for childProcess in self.handleFinishedChildProcesses():
            if not self._quiet():
              if self._debug():
                self.showMessage(childProcess.message())
          time.sleep(0.1)

        # Throw in another sample.
        if self._debug():
          self.showMessage("Starting sample %d" % (sample))
        self.fork(str(sample))

        if self.isParentProcess():
          # Stop parent process to enable child process to start and
          # the load to adjust.
          # But first handle finished children.
          for childProcess in self.handleFinishedChildProcesses():
            if not self._quiet():
              if self._debug():
                self.showMessage(childProcess.message())
          time.sleep(0.01)

      # Child processes start here.
      if not self._forkSamples() or \
         (self._forkSamples() and self.isChildProcess()):
        self._incrementIndentLevel()
        self._atStartOfSample(sample)
        self._userModel()._setCurrentSample(sample)
        # Execute model
        self._d_model.run()

        self._sampleFinished()
        self._decrementIndentLevel()

      # Child processes stop here.
      if self._forkSamples():
        if self.isChildProcess():
          os._exit(0)

      assert not self._forkSamples() or self.isParentProcess()
      sample += 1

    if self._forkSamples() and  self.isParentProcess():
      for childProcess in self.waitForChildProcessesToFinish():
        if not self._quiet():
          if self._debug():
            self.showMessage(childProcess.message())
      assert not self.childProcesses()

    if postmc:
      self._runPostmcloop()

    return 0



  ## \brief Creates the directories in which the sample data can be stored.
  #
  # \attention Already existing sample directories will be cleaned!
  def _initialiseSampleDirectories(self):
    sample = self._userModel()._firstSampleNumber()
    while sample <= self._userModel()._lastSampleNumber():
      dirname = "%d" % (sample)

      if not os.path.exists(dirname):
        # Create sample directory.
        os.mkdir(dirname)
      else :
        if not os.path.isdir(dirname):
          # Remove existing file with name of sample directory.
          os.remove(dirname)
          os.mkdir(dirname)
        else:
          # remove existing and create emtpy directories
          shutil.rmtree(dirname)
          os.mkdir(dirname)

      assert os.path.exists(dirname) and os.path.isdir(dirname)
      sample += 1


  ## \brief Used for the genetic algorithm
  def _setNrSamples(self, nrSamples):
    """Sets the number of samples to run."""
    assert nrSamples > 0
    self._setSampleNumbers(self._firstSampleNumber(),
         self._firstSampleNumber() + nrSamples - 1)


  def _setSampleNumbers(self, firstSampleNumber, lastSampleNumber):
    assert firstSampleNumber > 0
    if lastSampleNumber <= 0:
      msg = "number of samples argument (%s) of MonteCarloFramework must be > 0" % (lastSampleNumber)
      raise AttributeError(msg)
    assert lastSampleNumber >= firstSampleNumber

    self._userModel()._d_firstSampleNumber = firstSampleNumber
    self._userModel()._d_lastSampleNumber = lastSampleNumber

  ## \brief Returns true if new processes can be forked
  def _systemIsOccupied(self, nrChilds):
    return nrChilds >= self._d_nrProcessors





  ## Checks the current configuration of the script.
  def _check(self):
    if self._userModel().nrSamples() == 0:
      self.showWarning("""
   Since the number of samples to execute is 0, only the premcloop
   and the postmcloop functions will be executed. Any script that does
   something meaningful needs to calculate at least one "sample".""")




