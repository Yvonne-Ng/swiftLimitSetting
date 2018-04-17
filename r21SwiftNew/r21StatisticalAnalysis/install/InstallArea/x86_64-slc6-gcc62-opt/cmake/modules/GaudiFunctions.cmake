# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# This module collects functions used just for the ATLAS-style build of Gaudi.
#

# Provide a function for setting up the NightlyBuild.cmake and
# ExperimentalBuild.cmake scripts for building Gaudi.
#
# Usage: gaudi_ctest_setup()
#
macro( gaudi_ctest_setup )

   # First call the basic setup:
   atlas_ctest_setup()

   # Get the number of processor cores to use for the compilation.
   # Used by the release building script(s).
   atlas_cpu_cores( PROCESSOR_COUNT )

   # Get the name of the running machine. Needed for the CTest script(s).
   site_name( SITE_NAME )

   # Construct a platform name:
   atlas_platform_id( BUILDNAME )

   # Generate the build control script(s):
   find_file( _expBuild ExperimentalBuild.cmake.in
      PATH_SUFFIXES skeletons PATHS ${CMAKE_MODULE_PATH} )
   configure_file( ${_expBuild}
      ${CMAKE_BINARY_DIR}/ExperimentalBuild.cmake @ONLY )
   unset( _expBuild )
   find_file( _nightlyBuild NightlyBuild.cmake.in
      PATH_SUFFIXES skeletons PATHS ${CMAKE_MODULE_PATH} )
   configure_file( ${_nightlyBuild}
      ${CMAKE_BINARY_DIR}/NightlyBuild.cmake @ONLY )
   unset( _nightlyBuild )

   # Unset the now unnecessary variables:
   unset( PROCESSOR_COUNT )
   unset( SITE_NAME )

endmacro( gaudi_ctest_setup )
