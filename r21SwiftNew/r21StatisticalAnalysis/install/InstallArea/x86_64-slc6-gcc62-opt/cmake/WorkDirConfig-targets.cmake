# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.5)
   message(WARNING "CMake >= 2.6.0 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.6)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Protect against multiple inclusion, which would fail when already imported targets are added once more.
set(_targetsDefined)
set(_targetsNotDefined)
set(_expectedTargets)
foreach(_expectedTarget WorkDir::BayesianPkg WorkDir::BayesianPkgPrivate WorkDir::BayesianLib WorkDir::SearchPhase WorkDir::SearchPhase_JESSysts WorkDir::LimitSettingPhase WorkDir::drawLimitBands WorkDir::doGaussianLimits WorkDir::setLimitsOneMassPoint WorkDir::detailedGaussianOnePoint WorkDir::testStartParams.cxx WorkDir::doSystOnSearchOutput WorkDir::simpleBumpHunter_example)
  list(APPEND _expectedTargets ${_expectedTarget})
  if(NOT TARGET ${_expectedTarget})
    list(APPEND _targetsNotDefined ${_expectedTarget})
  endif()
  if(TARGET ${_expectedTarget})
    list(APPEND _targetsDefined ${_expectedTarget})
  endif()
endforeach()
if("${_targetsDefined}" STREQUAL "${_expectedTargets}")
  unset(_targetsDefined)
  unset(_targetsNotDefined)
  unset(_expectedTargets)
  set(CMAKE_IMPORT_FILE_VERSION)
  cmake_policy(POP)
  return()
endif()
if(NOT "${_targetsDefined}" STREQUAL "")
  message(WARNING "Some (but not all) targets in this export set were already defined.\nTargets Defined: ${_targetsDefined}\nTargets not yet defined: ${_targetsNotDefined}\n")
endif()
unset(_targetsDefined)
unset(_targetsNotDefined)
unset(_expectedTargets)


# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
if(_IMPORT_PREFIX STREQUAL "/")
  set(_IMPORT_PREFIX "")
endif()

# Create imported target WorkDir::BayesianPkg
add_library(WorkDir::BayesianPkg INTERFACE IMPORTED)

set_target_properties(WorkDir::BayesianPkg PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/src/source"
)

# Create imported target WorkDir::BayesianPkgPrivate
add_library(WorkDir::BayesianPkgPrivate INTERFACE IMPORTED)

# Create imported target WorkDir::BayesianLib
add_library(WorkDir::BayesianLib SHARED IMPORTED)

set_target_properties(WorkDir::BayesianLib PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "\$<TARGET_PROPERTY:WorkDir::BayesianPkg,INTERFACE_INCLUDE_DIRECTORIES>;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/include"
  INTERFACE_LINK_LIBRARIES "$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libHist.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libTree.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libMinuit2.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libGpad.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libMathMore.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libMathCore.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libMatrix.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libRIO.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libGraf.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libCore.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libBATmodels.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libBATmtf.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libBATmvc.so;$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/lib/libBAT.so"
  INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "$ENV{TDAQ_RELEASE_BASE}/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/include"
)

# Create imported target WorkDir::SearchPhase
add_executable(WorkDir::SearchPhase IMPORTED)

# Create imported target WorkDir::SearchPhase_JESSysts
add_executable(WorkDir::SearchPhase_JESSysts IMPORTED)

# Create imported target WorkDir::LimitSettingPhase
add_executable(WorkDir::LimitSettingPhase IMPORTED)

# Create imported target WorkDir::drawLimitBands
add_executable(WorkDir::drawLimitBands IMPORTED)

# Create imported target WorkDir::doGaussianLimits
add_executable(WorkDir::doGaussianLimits IMPORTED)

# Create imported target WorkDir::setLimitsOneMassPoint
add_executable(WorkDir::setLimitsOneMassPoint IMPORTED)

# Create imported target WorkDir::detailedGaussianOnePoint
add_executable(WorkDir::detailedGaussianOnePoint IMPORTED)

# Create imported target WorkDir::testStartParams.cxx
add_executable(WorkDir::testStartParams.cxx IMPORTED)

# Create imported target WorkDir::doSystOnSearchOutput
add_executable(WorkDir::doSystOnSearchOutput IMPORTED)

# Create imported target WorkDir::simpleBumpHunter_example
add_executable(WorkDir::simpleBumpHunter_example IMPORTED)

if(CMAKE_VERSION VERSION_LESS 3.0.0)
  message(WARNING "This file relies on consumers using CMake 3.0.0 or greater.")
endif()

# Load information for each installed configuration.
get_filename_component(_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
file(GLOB CONFIG_FILES "${_DIR}/WorkDirConfig-targets-*.cmake")
foreach(f ${CONFIG_FILES})
  include(${f})
endforeach()

# Cleanup temporary variables.
set(_IMPORT_PREFIX)

# Loop over all imported files and verify that they actually exist
foreach(target ${_IMPORT_CHECK_TARGETS} )
  foreach(file ${_IMPORT_CHECK_FILES_FOR_${target}} )
    if(NOT EXISTS "${file}" )
      message(WARNING "The imported target \"${target}\" references the file
   \"${file}\"
but this file does not exist.  Possible reasons include:
* The file was deleted, renamed, or moved to another location.
* An install or uninstall procedure did not complete successfully.
* The installation package was faulty and contained
   \"${CMAKE_CURRENT_LIST_FILE}\"
but not all the files it references.
")
    endif()
  endforeach()
  unset(_IMPORT_CHECK_FILES_FOR_${target})
endforeach()
unset(_IMPORT_CHECK_TARGETS)

# This file does not depend on other imported targets which have
# been exported from the same project but in a separate export set.

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
cmake_policy(POP)
