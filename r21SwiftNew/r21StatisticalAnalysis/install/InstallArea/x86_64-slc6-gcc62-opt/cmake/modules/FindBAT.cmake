# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# Module used for finding BAT during an ATLAS software build.
#

# Make use of the AtlasCMake code...
include( AtlasInternals )

# Declare the module:
atlas_external_module( NAME BAT
   INCLUDE_SUFFIXES include INCLUDE_NAMES BAT/BCDataSet.h
   LIBRARY_SUFFIXES lib
   COMPULSORY_COMPONENTS BAT
   DEFAULT_COMPONENTS BATmodels BATmtf BATmvc )

# Implement the standard find_package behaviour:
include( FindPackageHandleStandardArgs )
find_package_handle_standard_args( BAT DEFAULT_MSG
   BAT_INCLUDE_DIR BAT_INCLUDE_DIRS BAT_LIBRARIES )
mark_as_advanced( BAT_FOUND )
