// This header first!
#include <boost/python.hpp>

#ifndef INCLUDED_BOOST_FORMAT
#include <boost/format.hpp>
#define INCLUDED_BOOST_FORMAT
#endif

#ifndef INCLUDED_BOOST_TEST_FLOATING_POINT_COMPARISON
#include <boost/test/floating_point_comparison.hpp>
#define INCLUDED_BOOST_TEST_FLOATING_POINT_COMPARISON
#endif


#ifndef INCLUDED_BOOST_PYTHON_DOCSTRING_OPTIONS
#include <boost/python/docstring_options.hpp>
#define INCLUDED_BOOST_PYTHON_DOCSTRING_OPTIONS
#endif

#ifndef INCLUDED_BOOST_PYTHON_NUMERIC
#include <boost/python/numeric.hpp>
#define INCLUDED_BOOST_PYTHON_NUMERIC
#endif

#ifndef INCLUDED_NUMPY_CORE_INCLUDE_NUMPY_ARRAYOBJECT
#include <numpy/core/include/numpy/arrayobject.h>
#define INCLUDED_NUMPY_CORE_INCLUDE_NUMPY_ARRAYOBJECT
#endif

#ifndef INCLUDED_DAL_UTILS
#include "dal_Utils.h"
#define INCLUDED_DAL_UTILS
#endif

#ifndef INCLUDED_CALC_FIELD
#include "calc_field.h"
#define INCLUDED_CALC_FIELD
#endif

#ifndef INCLUDED_CALC_SPATIAL
#include "calc_spatial.h"
#define INCLUDED_CALC_SPATIAL
#endif

#ifndef INCLUDED_GLOBALS
#include "Globals.h"
#define INCLUDED_GLOBALS
#endif



namespace pcraster {
namespace python {

//Wrap a map into an ndarray. DOES NOT COPY, DOES NOT CHECK
boost::python::numeric::array wrapFieldInArray(
         geo::RasterSpace const& space,
         calc::Field *field,
         double mv)
{
  PRECOND(field->isSpatial());
  PRECOND(field->dest());

  npy_intp dimensions[2];
  dimensions[0] = space.nrRows();
  dimensions[1] = space.nrCols();
  size_t nrValues = space.nrCells();

  boost::python::object object(boost::python::handle<>(PyArray_SimpleNewFromData(2, dimensions, PyArray_FLOAT32, field->dest())));

  return boost::python::extract<boost::python::numeric::array>(object);
}



//!
/*!
  \param     .
  \return    .
  \exception .
  \warning   .
  \sa        .
  \todo      Implement for non-spatials.
*/
boost::python::numeric::array field2Array(
         geo::RasterSpace const& space,
         calc::Field const* field,
         double mv)
{
  PRECOND(field->isSpatial());
  PRECOND(field->src());

  npy_intp dimensions[2];
  dimensions[0] = space.nrRows();
  dimensions[1] = space.nrCols();
  size_t nrValues = space.nrCells();

  switch(field->cr()) {
    case CR_UINT1: {
      boost::python::object object(boost::python::handle<>(
         PyArray_SimpleNew(2, dimensions, PyArray_UINT8)));
      char *data = ((PyArrayObject*)object.ptr())->data;
      field->beMemCpySrc(data);
      dal::fromStdMV<UINT1>((UINT1*)data, nrValues, static_cast<UINT1>(mv));
      return boost::python::extract<boost::python::numeric::array>(object);
      break;
    }
    case CR_INT4: {
      boost::python::object object(boost::python::handle<>(
         PyArray_SimpleNew(2, dimensions, PyArray_INT32)));
      char *data = ((PyArrayObject*)object.ptr())->data;
      field->beMemCpySrc(data);
      dal::fromStdMV<INT4>((INT4*)data, nrValues, static_cast<INT4>(mv));
      return boost::python::extract<boost::python::numeric::array>(object);
      break;
    }
    case CR_REAL4:
    default: {
      assert(field->cr() == CR_REAL4);
      boost::python::object object(boost::python::handle<>(
         PyArray_SimpleNew(2, dimensions, PyArray_FLOAT32)));
      char *data = ((PyArrayObject*)object.ptr())->data;
      field->beMemCpySrc(data);
      dal::fromStdMV<REAL4>((REAL4*)data, nrValues, static_cast<REAL4>(mv));
      return boost::python::extract<boost::python::numeric::array>(object);
      break;
    }
  }
}

// 
boost::python::numeric::array deprecatedField2Array(
         geo::RasterSpace const& space,
         calc::Field const* field,
         double mv)
{
  // KDJ: I don't think this works like expected. Reinder reports:
  //   d3 = pcraster.pcr2numarray(d3pcr, - 9999).astype(float64)
  //   plotgradientslope04Art.py:196: DeprecationWarning: 
  //   PyArray_FromDimsAndDataAndDescr: use PyArray_NewFromDescr.
  //     d3 = pcraster.pcr2numarray(d3pcr, - 9999).astype(float64)
  // Maybe the reported message comes from numpy C code, deeper down.
  //
  // OLS: indeed, solving 'PyArray_FromDims: use PyArray_SimpleNew' shows
  // the intended deprecation messages
  PyErr_WarnEx(PyExc_DeprecationWarning, "pcr2numarray() is deprecated, use pcr2numpy()", 1);
  return field2Array(space, field, mv);
}

static double getElementAsDouble(
                 const boost::python::numeric::array &array,
                 size_t i,
                 size_t j)
{
  int type = PyArray_TYPE(array.ptr());

  void * buffer = PyArray_GETPTR2(array.ptr(), i,j);
  double val = 0;
  switch (type)
  {
          case NPY_BOOL:
                  val = (*(::npy_bool*)buffer != 0);
                  break;
          case NPY_INT8:
                  val = (*(::npy_int8*)buffer);
                  break;
          case NPY_UINT8:
                  val = (*(::npy_uint8*)buffer);
                  break;
          case NPY_INT16:
                  val = (*(::npy_int16*)buffer);
                  break;
          case NPY_UINT16:
                  val = (*(::npy_int16*)buffer);
                  break;
          case NPY_INT32:
                  val = (*(::npy_int32*)buffer);
                  break;
          case NPY_UINT32:
                  val = (*(::npy_int32*)buffer);
                  break;
          case NPY_INT64:
                  val = (double)*(::npy_int64*)buffer;
                  break;
          case NPY_UINT64:
                  val = (double)*(::npy_int64*)buffer;
                  break;
          case NPY_FLOAT32:
                  val = (*(::npy_float32*)buffer);
                  break;
          case NPY_FLOAT64:
                  val = (*(::npy_float64*)buffer);
                  break;
  }
  return val;
}


/**
* \author OLS
* copying Python array to PCRaster map
*
* \param field new PCRaster map
* \param array Python numarray
* \param mv array values equating mv will be set to PCRaster MV
*
*/
template<typename T>
void array2Field(
                 geo::RasterSpace const& space,
                 calc::Spatial *field,
                 const boost::python::numeric::array &array,
                 double mv)
{
  T* cells = static_cast<T*>(field->dest());
  size_t pos = 0;
  // double since large ints like 2^30 can be off in float
  boost::test_tools::close_at_tolerance<double>
         tester(boost::test_tools::fraction_tolerance_t<double>(double(1e-4)),
         boost::test_tools::FPC_STRONG);


  for(size_t i = 0;i < space.nrRows(); ++i){
    for(size_t j = 0;j < space.nrCols(); ++j){
      // extract does not recognize numpy types
      // T value = boost::python::extract<T>(array[i][j]);
      // instead do
      double val = getElementAsDouble(array,i,j);
      if(tester(static_cast<double>(val), static_cast<double>(mv))){
        pcr::setMV(cells[pos]);
      }
      else{
        cells[pos] = static_cast<T>(val);
      }
      pos++;
    }
  }
}

/**
* \author OLS
* simple test for boolean/ldd input values in Python numarray
* numarray values not in interval or equal to mv result in program termination
*
* \param min minimal value
* \param max maximal value
* \param mv missing value
* \param array Python numarray
* \param nrCells size of numarray
*/
void testValues(
         geo::RasterSpace const& space,
         double min,
         double max,
         double mv,
         const boost::python::numeric::array &array,
         const std::string& type)
{
  // double since large ints like 2^30 can be off in float
  boost::test_tools::close_at_tolerance<double>
         tester(boost::test_tools::fraction_tolerance_t<double>(double(1e-4)),
         boost::test_tools::FPC_STRONG);

  for(size_t i = 0;i < space.nrRows(); i++){
    for(size_t j = 0;j < space.nrCols(); j++){
      // extract does not recognize numpy types
      // int value = boost::python::extract<int>(array[i][j]);
      // instead do:
      double value = getElementAsDouble(array,i,j);
      if(! ((value>=min)&&(value<=max)) ){
        if(tester(static_cast<double>(value), static_cast<double>(mv)) == false){
          throw std::logic_error((boost::format("Incorrect value %4% at input array [%1%][%2%] for %3% map")  % i % j % type % value).str().c_str());
        }
      }
    }
  }
}


/**
* \author OLS
*
* creating a PCRaster map from a 2D Python numarray
*
* \param VS valueScale boolean, nominal, ...
* \param array Python numarray
* \param mv array values equating mv will be set to PCRaster MV
*/
calc::Field* numpy2pcr(
         geo::RasterSpace const& space,
         VS valueScale,
         const boost::python::numeric::array &array,
         double mv)
{
  if(!space.valid()){
    throw std::logic_error("No valid raster defined: Set clone or load map from file");
  }
  if( (((PyArrayObject*)array.ptr())->nd) != 2){
    throw std::logic_error("Dimension error: Rank of input array must be 2");
  }

  size_t arrCells = ((PyArrayObject*)array.ptr())->dimensions[0] *
   ((PyArrayObject*)array.ptr())->dimensions[1];

  size_t nrCells = space.nrCells();

  if(arrCells != nrCells){
    throw std::logic_error((boost::format("Size mismatch: Number of array elements is %1%, number of raster cells is %2%")  % arrCells % nrCells).str().c_str());
  }

  calc::Spatial* field = NULL;

  switch(valueScale){
    case VS_B:{
      // test if only boolean values/MV
      testValues(space, 0, 1, mv, array,"Boolean");
      field = new calc::Spatial(VS_B, calc::CRI_1, nrCells);
      array2Field<UINT1>(space, field, array, mv);
      break;
    }
    case VS_L:{
      // test if only LDD values/MV
      testValues(space, 1, 9, mv, array, "LDD");
      field = new calc::Spatial(VS_L, calc::CRI_1, nrCells);
      array2Field<UINT1>(space, field, array, mv);
      break;
    }
    case VS_N:{
      testValues(space, INT4_MIN, INT4_MAX, mv, array, "Nominal");
      field = new calc::Spatial(VS_N, calc::CRI_4, nrCells);
      array2Field<INT4>(space, field, array, mv);
      break;
    }
    case VS_O:{
      testValues(space, INT4_MIN, INT4_MAX, mv, array, "Ordinal");
      field = new calc::Spatial(VS_O, calc::CRI_4, nrCells);
      array2Field<INT4>(space, field, array, mv);
      break;
    }
    case VS_S:{
      testValues(space, -REAL4_MAX, REAL4_MAX, mv, array, "Scalar");
      field = new calc::Spatial(VS_S, calc::CRI_f, nrCells);
      array2Field<REAL4>(space, field, array, mv);
      break;
    }
    case VS_D:{
      // TODO  degrees or radians? depended on global option?
      // testValues(space, 0, 360, mv, array, "Directional");
      testValues(space, -REAL4_MAX, REAL4_MAX, mv, array, "Directional");
      field = new calc::Spatial(VS_D, calc::CRI_f, nrCells);
      array2Field<REAL4>(space, field, array, mv);
      break;
    }
    default:{
      PRECOND(false);
      break;
    }
  }
  return field;
}


calc::Field* deprecatedNumarray2pcr(
         geo::RasterSpace const& space,
         VS valueScale,
         const boost::python::numeric::array &array,
         double mv)
{
  PyErr_WarnEx(PyExc_DeprecationWarning, "numarray2pcr() is deprecated, use numpy2pcr()", 1);
  return numpy2pcr(space, valueScale, array, mv);
}

} // namespace python
} // namespace pcraster



BOOST_PYTHON_MODULE(_numpy)
{
  using namespace boost::python;

  docstring_options doc_options(true, false);

  import_array(); // TODO Crashes icw NumPy-1.2.
  boost::python::numeric::array::set_module_and_type("numpy", "ndarray");

  def("wrapFieldInArray", pcraster::python::wrapFieldInArray);

  // Conversions.
  def("pcr2numpy", pcraster::python::field2Array);
  def("pcr2numarray", pcraster::python::deprecatedField2Array);

  def("numpy2pcr", pcraster::python::numpy2pcr,
         return_value_policy<manage_new_object>());
  def("numarray2pcr", pcraster::python::deprecatedNumarray2pcr,
         return_value_policy<manage_new_object>());

  // def("nonspatial2number", nonSpatial2Number);
  // def("array2raster", array2BooleanField,
  //        return_value_policy<manage_new_object>());
}
