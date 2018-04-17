# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# Module looking up NumPy.
#
# Sets:
#   - NUMPY_FOUND
#   - NUMPY_INCLUDE_DIRS
#

# We need python if we are to find NumPy:
if( NumPy_FIND_QUIETLY )
   find_package( PythonInterp QUIET )
else()
   find_package( PythonInterp )
endif()

# If Python is found, try to find NumPy with it:
if( PYTHONINTERP_FOUND )

   # Find out the include path:
   execute_process(
      COMMAND "${PYTHON_EXECUTABLE}" -c
      "try: import numpy; print( numpy.get_include() )\nexcept:pass\n"
      OUTPUT_VARIABLE _numpy_path
      OUTPUT_STRIP_TRAILING_WHITESPACE )

   # And the version:
   execute_process(
      COMMAND "${PYTHON_EXECUTABLE}" -c
      "try: import numpy; print( numpy.__version__ )\nexcept:pass\n"
      OUTPUT_VARIABLE _numpy_version
      OUTPUT_STRIP_TRAILING_WHITESPACE )

   # Look for a characteristic numpy header:
   find_path( NUMPY_INCLUDE_DIR numpy/arrayobject.h
      PATHS ${_numpy_path} )
   set( NUMPY_INCLUDE_DIRS ${NUMPY_INCLUDE_DIR} )

endif()

# Handle the standard find_package arguments:
include( FindPackageHandleStandardArgs )
find_package_handle_standard_args( NumPy
   FOUND_VAR NUMPY_FOUND
   REQUIRED_VARS NUMPY_INCLUDE_DIR
   VERSION_VAR _numpy_version )

# Clean up:
unset( _numpy_path )
unset( _numpy_version )
