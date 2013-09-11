import math
import unittest
import numpy
import pcraster
import testcase


class TestNumPy(testcase.TestCase):
  def testBooleanRaster2Array(self):
    raster = pcraster.readmap("and_Expr1.map")
    mv = 99
    array = pcraster.pcr2numpy(raster, mv)
    self.assert_(isinstance(array[0][0], numpy.uint8))
    self.assertEqual(array[0][0], 1)
    self.assertEqual(array[0][1], 1)
    self.assertEqual(array[0][2], 0)
    self.assertEqual(array[1][0], 0)
    self.assertEqual(array[1][1], mv)
    self.assertEqual(array[1][2], 0)
    self.assertEqual(array[2][0], 1)
    self.assertEqual(array[2][1], 1)
    self.assertEqual(array[2][2], 0)


  def testNominalRaster2Array(self):
    raster = pcraster.readmap("areaarea_Class.map")
    mv = 99
    array = pcraster.pcr2numpy(raster, mv)
    self.assert_(isinstance(array[0][0], numpy.int32))
    self.assertEqual(array[0][0], 2)
    self.assertEqual(array[0][1], 6)
    self.assertEqual(array[0][2], 2)
    self.assertEqual(array[0][3], 2)
    self.assertEqual(array[0][4], mv)
    self.assertEqual(array[1][0], 6)
    self.assertEqual(array[1][1], 6)
    self.assertEqual(array[1][2], 2)
    self.assertEqual(array[1][3], 2)
    self.assertEqual(array[1][4], 2)
    self.assertEqual(array[2][0], 6)
    self.assertEqual(array[2][1], 6)
    self.assertEqual(array[2][2], 0)
    self.assertEqual(array[2][3], 0)
    self.assertEqual(array[2][4], 0)
    self.assertEqual(array[3][0], 6)
    self.assertEqual(array[3][1], 6)
    self.assertEqual(array[3][2], 0)
    self.assertEqual(array[3][3], 0)
    self.assertEqual(array[3][4], 0)
    self.assertEqual(array[4][0], 6)
    self.assertEqual(array[4][1], 3)
    self.assertEqual(array[4][2], 3)
    self.assertEqual(array[4][3], 4)
    self.assertEqual(array[4][4], 4)


  def testOrdinalRaster2Array(self):
    raster = pcraster.readmap("succ_Expr.map")
    mv = 99
    array = pcraster.pcr2numpy(raster, mv)
    self.assert_(isinstance(array[0][0], numpy.int32))
    self.assertEqual(array[0][0],-5)
    self.assertEqual(array[0][1], 9)
    self.assertEqual(array[0][2], 9)
    self.assertEqual(array[0][3], 0)
    self.assertEqual(array[1][0],-5)
    self.assertEqual(array[1][1],-5)
    self.assertEqual(array[1][2], 9)
    self.assertEqual(array[1][3], 0)
    self.assertEqual(array[2][0],-5)
    self.assertEqual(array[2][1], 9)
    self.assertEqual(array[2][2], 9)
    self.assertEqual(array[2][3], 2)
    self.assertEqual(array[3][0], 4)
    self.assertEqual(array[3][1], 4)
    self.assertEqual(array[3][2], 9)
    self.assertEqual(array[3][3],mv)


  def testScalarRaster2Array(self):
    raster = pcraster.readmap("abs_Expr.map")
    mv = 99
    array = pcraster.pcr2numpy(raster, mv)
    self.assert_(isinstance(array[0][0], numpy.float32))
    self.assertEqual(array[0][0],  2.0)
    self.assertEqual(array[0][1], -7.0)
    self.assertEqual(array[0][2],  3.5)
    self.assertEqual(array[1][0], -8.5)
    self.assertAlmostEqual(array[1][1], 3.6, 6)
    self.assertEqual(array[1][2], mv)
    self.assertEqual(array[2][0],  0.0)
    self.assertEqual(array[2][1], 14.0)
    self.assertAlmostEqual(array[2][2], -0.8)


  def testLddRaster2Array(self):
    raster = pcraster.readmap("accu_Ldd.map")
    mv = 99
    array = pcraster.pcr2numpy(raster, mv)
    self.assert_(isinstance(array[0][0], numpy.uint8))
    self.assertEqual(array[0][0], 2)
    self.assertEqual(array[0][1], 2)
    self.assertEqual(array[0][2], 2)
    self.assertEqual(array[0][3], 1)
    self.assertEqual(array[0][4], 1)
    self.assertEqual(array[1][0], 2)
    self.assertEqual(array[1][1], 2)
    self.assertEqual(array[1][2], 1)
    self.assertEqual(array[1][3], 1)
    self.assertEqual(array[1][4], 1)
    self.assertEqual(array[2][0], 3)
    self.assertEqual(array[2][1], 2)
    self.assertEqual(array[2][2], 1)
    self.assertEqual(array[2][3], 4)
    self.assertEqual(array[2][4], 1)
    self.assertEqual(array[3][0], 3)
    self.assertEqual(array[3][1], 2)
    self.assertEqual(array[3][2], 1)
    self.assertEqual(array[3][3], 4)
    self.assertEqual(array[3][4], 4)
    self.assertEqual(array[4][0], 6)
    self.assertEqual(array[4][1], 5)
    self.assertEqual(array[4][2], 4)
    self.assertEqual(array[4][3], 4)
    self.assertEqual(array[4][4], 4)


  def testBooleanArray2Raster(self):
    pcraster.setclone("boolean_Expr.map")
    try:
      a = numpy.array([ [1, 0, 1], [20, 1, 1], [1, 1, 0] ], numpy.uint8) # uint8 is bugzilla #271
      result = pcraster.numpy2pcr(pcraster.Boolean, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "boolean_Result.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))

  def testBooleanArray2RasterDomainError(self):
    pcraster.setclone("boolean_Expr.map")
    a = numpy.array([ [1, 0, 1], [20, 100, 1], [1, 1, 0] ]) # 100 is domain error
    self.assertRaises(Exception,pcraster.numpy2pcr,pcraster.Boolean, a, 20)

  def testNominalArray2Raster(self):
    pcraster.setclone("boolean_Expr.map")
    try:
      a = numpy.array([ [0, 1, 3], [20, -3, -2], [0, 9, 8] ])
      result = pcraster.numpy2pcr(pcraster.Nominal, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "nominal_Result.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))


  def testOrdinalArray2Raster(self):
    pcraster.setclone("boolean_Expr.map")
    try:
      a = numpy.array([ [0, 1, 3], [20, -3, -2], [0, 9, 8] ])
      result = pcraster.numpy2pcr(pcraster.Ordinal, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "ordinal_Result.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))

  def testScalarArray2Raster(self):
    pcraster.setclone("boolean_Expr.map")
    try:
      a = numpy.array([ [0.5, 0.34202, 0.310676], [20, 0, -0.981627], [0.707107, 0.144356, 0.0174524] ])
      result = pcraster.numpy2pcr(pcraster.Scalar, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "sin_Result.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))


  def testDirectionalArray2Raster(self):
    pcraster.setclone("boolean_Expr.map")
    pcraster.setglobaloption("degrees")
    try:
      a = numpy.array([ [math.radians(350),math.radians(0),math.radians(0.01)],\
         [20,math.radians(350),math.radians(21)],\
         [math.radians(359),math.radians(40),math.radians(0)] ])
      result = pcraster.numpy2pcr(pcraster.Directional, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "directional_Result2.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))


  def testLddArray2Raster(self):
    pcraster.setclone("and_Expr1.map")
    try:
      a = numpy.array([ [6, 5, 4], [6, 8, 7], [8, 8, 8] ])
      result = pcraster.numpy2pcr(pcraster.Ldd, a, 20)
      self.failUnless(self.mapEqualsValidated(result, "ldd_Result.map"), "test1: %s" % ("Result and validated result are not the same"))
    except Exception, exception:
      self.failUnless(False, "test1: %s" % (str(exception)))
