# Install script for directory: /lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/source

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/InstallArea/x86_64-slc6-gcc62-opt")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/src/source" TYPE DIRECTORY FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/source/" USE_SOURCE_PERMISSIONS REGEX "/\\.svn$" EXCLUDE)
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process( COMMAND ${CMAKE_COMMAND}
      -E make_directory
      $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/include )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process( COMMAND ${CMAKE_COMMAND}
         -E create_symlink ../src/source/BayesianLib
         $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/include/BayesianLib )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/lib/libBayesianLib.so.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/lib/libBayesianLib.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase_JESSysts.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase_JESSysts.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase_JESSysts")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase_JESSysts" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase_JESSysts")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase_JESSysts")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/LimitSettingPhase.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/LimitSettingPhase.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/LimitSettingPhase")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/LimitSettingPhase" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/LimitSettingPhase")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/LimitSettingPhase")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/drawLimitBands.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/drawLimitBands.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/drawLimitBands")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/drawLimitBands" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/drawLimitBands")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/drawLimitBands")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doGaussianLimits.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doGaussianLimits.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doGaussianLimits")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doGaussianLimits" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doGaussianLimits")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doGaussianLimits")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/setLimitsOneMassPoint.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/setLimitsOneMassPoint.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/setLimitsOneMassPoint")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/setLimitsOneMassPoint" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/setLimitsOneMassPoint")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/setLimitsOneMassPoint")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/detailedGaussianOnePoint.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/detailedGaussianOnePoint.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/detailedGaussianOnePoint")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/detailedGaussianOnePoint" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/detailedGaussianOnePoint")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/detailedGaussianOnePoint")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/testStartParams.cxx.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/testStartParams.cxx.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/testStartParams.cxx")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/testStartParams.cxx" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/testStartParams.cxx")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/testStartParams.cxx")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doSystOnSearchOutput.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doSystOnSearchOutput.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/doSystOnSearchOutput")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doSystOnSearchOutput" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doSystOnSearchOutput")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/doSystOnSearchOutput")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Debug" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE FILE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/simpleBumpHunter_example.dbg")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/simpleBumpHunter_example.exe")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE OPTIONAL FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/simpleBumpHunter_example")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simpleBumpHunter_example" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simpleBumpHunter_example")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simpleBumpHunter_example")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/Bayesian" TYPE FILE RENAME "__init__.py" FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/source/plotting/PythonModules/__init__.py")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/lib/libBayesianLib.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libBayesianLib.so")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/x86_64-slc6-gcc62-opt/bin/SearchPhase")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/SearchPhase")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Main" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/BayesianConfig.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/BayesianConfig.cmake"
         "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/source/CMakeFiles/Export/cmake/BayesianConfig.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/BayesianConfig-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/BayesianConfig.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/source/CMakeFiles/Export/cmake/BayesianConfig.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/build/source/CMakeFiles/Export/cmake/BayesianConfig-relwithdebinfo.cmake")
  endif()
endif()

