# -*- coding: utf-8 -*-
import sys
import re
import os
import inspect
import copy
import Index as CollIndex
import PCRaster

class ValueFromParameterTable(object):
  """
  Class to be used for initialisation of collection indices from an external parameter file

  Parameter:

  varName
    name of the collection variable used in the external file

  fileName
    filename of the external file

  dataType
    PCRaster data type. Use None when reading maps from disk
  """
  def __init__(self, varName, fileName, dataType=None):
    if len(varName) == 0:
      raise Exception("Length of variable name must be greater that 0")
    self._varName = varName
    self._fileName = fileName
    self._dataType = dataType

  def value(self, nrColumns, externalNames, keyDict):
    """
    returns the parameter value
    """

    parameterFile = None
    parameterFile = open(self._fileName, "rU")

    lineNo = 1
    lines = parameterFile.readlines()
    parameterFile.close()

    for line in lines:
      result = self._parseLine(line, lineNo, nrColumns, externalNames, keyDict)
      lineNo += 1


  def _parseLine(self, line, lineNumber, nrColumns, externalNames, keyDict):

    line = re.sub("\n","",line)
    line = re.sub("\t"," ",line)
    result = None

    # read until first comment
    content = ""
    content,sep,comment = line.partition("#")
    if len(content) > 1:
      collectionVariableName, sep, tail = content.partition(" ")
      if collectionVariableName == self._varName:
        tail = tail.strip()
        key, sep, variableValue = tail.rpartition(" ")

        if len(key.split()) != nrColumns:
          tmp = re.sub("\(|\)|,","",str(key))
          msg = "Error reading %s line %d, order of columns given (%s columns) does not match expected order of %s columns" %(self._fileName, lineNumber, len(key.split()) + 2, int(nrColumns) + 2)
          raise ValueError(msg)

        variableValue = re.sub('\"', "", variableValue)

        tmp = None
        try:
          tmp = int(variableValue)
          if self._dataType == PCRaster.Boolean:
            tmp = PCRaster.boolean(tmp)
          elif self._dataType == PCRaster.Nominal:
            tmp = PCRaster.nominal(tmp)
          elif self._dataType == PCRaster.Ordinal:
            tmp = PCRaster.ordinal(tmp)
          elif self._dataType == PCRaster.Ldd:
            tmp = PCRaster.ldd(tmp)
          else:
            msg = "Conversion to %s failed" % (self._dataType)
            raise Exception(msg)
        except ValueError, e:
          try:
            tmp = float(variableValue)
            if self._dataType == PCRaster.Scalar:
              tmp = PCRaster.scalar(tmp)
            elif self._dataType == PCRaster.Directional:
              tmp = PCRaster.directional(tmp)
            else:
              msg = "Conversion to %s failed" % (self._dataType)
              raise Exception(msg)

          except ValueError,e:
            variableValue = re.sub("\\\\","/",variableValue)
            variableValue = variableValue.strip()
            path = os.path.normpath(variableValue)
            try:
              tmp = PCRaster.readmap(path)
            except RuntimeError, e:
              msg = "Error reading %s line %d, %s" %(self._fileName, lineNumber, e)
              raise ValueError(msg)

        # test if key is an external name
        transformedKeys = []
        counter = 0

        for k in key.split():
          k = k.strip()
          if externalNames[counter].get(k):
            transformedKeys.append(externalNames[counter].get(k))
          else:
            transformedKeys.append(k)
          counter += 1

        key = tuple(transformedKeys)

        if not keyDict.has_key(key):
          tmp = re.sub("\(|\)|,","",str(key))
          msg = "Error reading %s line %d, %s unknown collection index" %(self._fileName, lineNumber, tmp)
          raise ValueError(msg)


        if not keyDict[key] is None:
          tmp = re.sub("\(|\)|,","",str(key))
          msg = "Error reading %s line %d, %s %s already initialised" %(self._fileName, lineNumber, self._varName, tmp)
          raise ValueError(msg)

        keyDict[key] = tmp




class ValueTimeoutputTimeseries(object):
  """
  Class to be used in initialisation of collection variables for timeseries output
  Parameters:

  varName
    name of the variable, used to generate the timeseries output filename

  model
    reference to the Dynamic or Static user model class

  idMap
    sample locations

  noHeader
    if False only column values will be written to file

  """
  def __init__(self, varName, model, idMap=None, noHeader=False):
    if len(varName) == 0:
      raise Exception("Length of variable name must be greater that 0")
    self._varName = varName
    self._model = model
    self._idMap = idMap
    self._noHeader = noHeader


  def value(self, keys):
    varName = self._varName + "-" + "-".join(keys)
    return PCRaster.Framework.TimeoutputTimeseries(varName, self._model, self._idMap, self._noHeader)



class VariableCollection(object):
  """
  Creating arrayed variables

  Parameter:

  keys
    a list of Index classes

  value
    all array indices will be initialised with defaultValue.
    If defaultValue is a callable, the callable return value will be
    assigned to the collection item. The callable will be called with for each
    item in the collection with 2 arguments:
     - name   of this VariableCollection
     - index  index tuple of item a value is generated for

  Example:

  PlantSpecies = Index([ "Species1", "Species2"])

  Variable1 = VariableCollection([PlantSpecies], value=0)
  """
  def __init__(self, keys, value=None):

    if not isinstance(keys, list):
      raise ValueError("Argument %s must be of type list" % (keys))
    for key in keys:
      if not isinstance(key, CollIndex.Index):
        msg = "Incorrect type of argument %s, must be of type Collection.Index" % (key)
        raise ValueError(msg)

    self._impl = {}
    self._keys = []
    self.__externalNames = []

    for k in keys:
      dim = {}
      for index in k:
        externalName =  k._getExternalName(index)
        dim[externalName] = index
      self.__externalNames.append(dim)

    com = list(self._product(*keys))

    for key in com:
      self._impl[key] = None
      self._keys.append(key)


    if isinstance(value, ValueFromParameterTable):
      # all keys will be initialised from file
      value.value(len(self._keys[0]), self.__externalNames, self._impl)
    else:
      for key in com:
        if isinstance(value, ValueTimeoutputTimeseries):
          self._impl[key] = value.value(key)
        else:
          self._impl[key] = value


  def __getitem__(self, key):
    if isinstance(key, str):
      key = tuple([key])
    return self._impl[key]


  def __setitem__(self, key, value):
    # block adding a new one
    if isinstance(key, str):
      key = tuple([key])
    if not self._impl.has_key(key):
       raise ValueError("cannot add elements to a VariableCollection")
    self._impl[key] = value


  #def keys(self):
    #"""
    #Returns a list of array indices
    #"""
    #return self._impl.keys()


  def __iter__(self):
    self._index = 0
    return self


  def next(self):
    """

    """
    if self._index >= len(self._keys):
      raise StopIteration

    val = self._impl[self._keys[self._index]]
    if val is None:
      while self._impl[self._keys[self._index]] is None:
        self._index += 1
      else:
        val = self._keys[self._index]
        self._index += 1
    else:
      val = self._keys[self._index]
      self._index += 1

    return val


  def _product(self, *args, **kwds):
    # whith 2.6 this method can be replaced by product
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)



  def __getVariableName(self, line):
    """
    returns the name of the variable the object is assigned to
    """
    variableName, sep, tail = line.partition("=")
    variableName = variableName.strip()

    if re.search(r"self.",variableName) != None:
      variableName = variableName[5:]

    return variableName



  #def reportCollection(self):
    #for i in self._impl:
      #name = self._name + "-" + "-".join(i) + ".map"
      #PCRaster.report(self._impl[i], name)

  #def sampleCollection(self):
    #for i in self._tssObjects:
      #self._tssObjects[i].sample(self._impl[i])