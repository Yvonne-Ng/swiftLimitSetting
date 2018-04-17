atlas_subdir( SensitivityStudies )

find_package( ROOT COMPONENTS Hist Roofit Tree Minuit2
    Gpad MathMore MathCore Matrix RIO Graf)

atlas_add_library( BayesianLib Bayesian/*.h Root/*.cxx
    PUBLIC_HEADERS BayesianLib
    INCLUDE_DIRS ${ROOT_INCLUDE_DIR}
    LINK_LIBRARIES ${ROOT_LIBRARIES} ${BAT_LIBRARIES}
    )

atlas_add_executable( SearchPhase util/SearchPhase.cxx
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} ${BOOST_INCLUDE_DIRS}
    LINK_LIBRARIES BayesianLib ${ROOT_LIBRARIES} ${BOOST_LIBRARIES}
    ${BAT_LIBRARIES}
     )
