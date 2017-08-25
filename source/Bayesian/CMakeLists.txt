atlas_subdir( Bayesian )

find_package( ROOT COMPONENTS Hist Roofit Tree Minuit2
    Gpad MathMore MathCore Matrix RIO Graf)

find_package( BAT REQUIRED
     )


atlas_add_library( BayesianLib Bayesian/*.h Root/*.cxx 
    PUBLIC_HEADERS BayesianLib
    SHARED
    INCLUDE_DIRS ${ROOT_INCLUDE_DIR} 
    LINK_LIBRARIES ${ROOT_LIBRARIES} ${BAT_LIBRARIES}
     
    )

#include_directories(
#    /cvmfs/atlas.cern.ch/repo/sw/software/21.2/AnalysisBaseExternals/21.2.0/InstallArea/x86_64-slc6-gcc62-opt/lib
#    )

#include_directories(
#    /cvmfs/atlas.cern.ch/repo/sw/software/21.2/AnalysisBaseExternals/21.2.0/InstallArea/x86_64-slc6-gcc62-opt/lib
#   )

atlas_add_executable( SearchPhase util/SearchPhase.cxx
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} 
    LINK_LIBRARIES BayesianLib ${ROOT_LIBRARIES}
    ${BAT_LIBRARIES}
     )


 atlas_add_executable( LimitSettingPhase util/LimitSettingPhase.cxx
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} 
    LINK_LIBRARIES BayesianLib ${ROOT_LIBRARIES}
    ${BAT_LIBRARIES}
     )

 atlas_add_executable( doGaussianLimits util/doGaussianLimits.cxx
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} 
    LINK_LIBRARIES BayesianLib ${ROOT_LIBRARIES}
    ${BAT_LIBRARIES}
     )

 atlas_add_executable( setLimitsOneMassPoint util/setLimitsOneMassPoint.cxx
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} 
    LINK_LIBRARIES BayesianLib ${ROOT_LIBRARIES}
    ${BAT_LIBRARIES}
     )
atlas_install_python_modules(
    ./plotting/PythonModules/*.py ./inputs/accDictionary/*py
    )
#making a configuration file
install( TARGETS BayesianLib SearchPhase
       EXPORT BayesianConfig
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib )
#create a configuration file
install( EXPORT BayesianConfig
         DESTINATION cmake)


message(CMAKE_MODULE_PATH:${CMAKE_MODULE_PATH})
