#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import frameworkBase
import types

class StaticBase(object):
  def __init__(self):
    if self.__class__ is StaticBase:
      raise NotImplementedError

    self.inInitial = False

  def initial(self):
    """  """
    msg = "Class needs to implement 'initial' method"
    raise NotImplementedError(msg)

  def setDebug(self):
    """  """
    msg = "Class needs to implement 'setDebug' method"
    raise NotImplementedError(msg)


  def _inInitial(self):
    return self.inInitial

  def _setInInitial(self, value):
    assert type(value) == types.BooleanType
    self.inInitial = value
