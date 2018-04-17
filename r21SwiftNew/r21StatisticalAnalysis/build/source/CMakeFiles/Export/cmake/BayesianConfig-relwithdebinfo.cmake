#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "BayesianLib" for configuration "RelWithDebInfo"
set_property(TARGET BayesianLib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(BayesianLib PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libBayesianLib.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libBayesianLib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS BayesianLib )
list(APPEND _IMPORT_CHECK_FILES_FOR_BayesianLib "${_IMPORT_PREFIX}/lib/libBayesianLib.so" )

# Import target "SearchPhase" for configuration "RelWithDebInfo"
set_property(TARGET SearchPhase APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(SearchPhase PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/SearchPhase"
  )

list(APPEND _IMPORT_CHECK_TARGETS SearchPhase )
list(APPEND _IMPORT_CHECK_FILES_FOR_SearchPhase "${_IMPORT_PREFIX}/bin/SearchPhase" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
