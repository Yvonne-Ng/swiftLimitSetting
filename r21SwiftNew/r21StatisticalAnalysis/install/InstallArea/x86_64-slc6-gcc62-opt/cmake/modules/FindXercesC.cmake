# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# - Locate XercesC library
# Defines:
#
#  XERCESC_FOUND
#  XERCESC_INCLUDE_DIR
#  XERCESC_INCLUDE_DIRS
#  XERCESC_<component>_FOUND
#  XERCESC_<component>_LIBRARY
#  XERCESC_LIBRARIES
#  XERCESC_LIBRARY_DIRS
#
# Can be steered using XERCESC_ROOT.
#

# The LCG include(s):
include( LCGFunctions )

# If we are to take the external from an LCG release, then hide the locally
# installed stuff from the code:
if( XERCESC_ROOT )
   set( _ignorePathBackup ${CMAKE_SYSTEM_IGNORE_PATH} )
   set( CMAKE_SYSTEM_IGNORE_PATH /usr/include /usr/bin /usr/lib /usr/lib32
      /usr/lib64 )
endif()

# Declare the external module:
lcg_external_module( NAME XercesC
   INCLUDE_SUFFIXES include INCLUDE_NAMES xercesc/util/XercesVersion.hpp
   LIBRARY_SUFFIXES lib
   COMPULSORY_COMPONENTS xerces-c )

# Handle the standard find_package arguments:
include( FindPackageHandleStandardArgs )
find_package_handle_standard_args( XercesC DEFAULT_MSG XERCESC_INCLUDE_DIR
   XERCESC_LIBRARIES )
mark_as_advanced( XERCESC_FOUND XERCESC_INCLUDE_DIR XERCESC_INCLUDE_DIRS
   XERCESC_LIBRARIES XERCESC_LIBRARY_DIRS )

# Set up the RPM dependency:
lcg_need_rpm( XercesC )

# Restore the CMAKE_SYSTEM_IGNORE_PATH value:
if( XERCESC_ROOT )
   set( CMAKE_SYSTEM_IGNORE_PATH ${_ignorePathBackup} )
   unset( _ignorePathBackup )
endif()
