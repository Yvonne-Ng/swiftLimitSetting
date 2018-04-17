# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# This file is here to intercept find_package(Doxygen) calls, and extend the
# environment setup file of the project with the correct Doxygen paths.
#

# The LCG include(s):
include( LCGFunctions )

# Use the helper macro to do most of the work:
lcg_wrap_find_module( Doxygen )

# Set some extra variable(s), to make the environment configuration easier:
if( DOXYGEN_EXECUTABLE )
   get_filename_component( DOXYGEN_BINARY_PATH ${DOXYGEN_EXECUTABLE} PATH )
endif()

# This is just needed to set up a proper dependency on graphviz:
if( DOXYGEN_DOT_FOUND )
   set( GRAPHVIZ_FOUND TRUE )
endif()

# Set up the RPM dependency:
lcg_need_rpm( doxygen )
lcg_need_rpm( graphviz )
