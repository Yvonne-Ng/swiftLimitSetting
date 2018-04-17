file(REMOVE_RECURSE
  "../x86_64-slc6-gcc62-opt/include/BayesianLib"
  "../x86_64-slc6-gcc62-opt/python/Bayesian/__init__.py"
  "../x86_64-slc6-gcc62-opt/include/BayesianLib"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/BayesianHeaderInstall.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
