#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase


class MonteCarloBase(object):
  def __init__(self):
    if self.__class__ is MonteCarloBase:
      raise NotImplementedError

    self._d_firstSampleNumber = 0
    self._d_lastSampleNumber = 0
    self._d_currentSampleNumber = 1
    self._d_inSample = False
    self._d_inStochastic = True
    self._d_inPremc = False
    self._d_inPostmc = False

  def premcloop(self):
    msg = "Class needs to implement 'premcloop' method"
    raise NotImplementedError(msg)

  def postmcloop(self):
    msg = "Class needs to implement 'postmcloop' method"
    raise NotImplementedError(msg)


  ## \brief Returns the number of samples.
  #
  # \return 1 for static/dynamic models, number of samples otherwise
  def nrSamples(self):
    """
    Returns the number of samples
    """
    assert self._d_firstSampleNumber
    return self._d_lastSampleNumber - \
           self._d_firstSampleNumber + 1


  def currentSampleNumber(self):
    """
    Returns the current sample number
    """
    assert self._d_currentSampleNumber
    return self._d_currentSampleNumber


  def sampleNumbers(self):
    """
    Returns a list of sample numbers configured
    """
    assert self._d_firstSampleNumber
    return range(self._d_firstSampleNumber, \
           self._d_lastSampleNumber + 1)



  def _inStochastic(self):
    if not hasattr(self, "_d_inStochastic"):
      return False
    return self._d_inStochastic

  def _inPremc(self):
    return self._d_inPremc

  def _inPostmc(self):
    return self._d_inPostmc



  def _lastSampleNumber(self):
    return self._d_lastSampleNumber

  def _firstSampleNumber(self):
    return self._d_firstSampleNumber

  ## Sets the current sample number to nr.
  def _setCurrentSample(self, nr):
    assert nr >= self._firstSampleNumber()
    assert nr <= self._lastSampleNumber()
    self._d_currentSampleNumber = nr

  ## Returns whether a sample is currently executing.
  def _inSample(self):
    #if hasattr(self._userModel(), "_d_inSample"):
    return self._d_inSample
    #else:
    #  return False