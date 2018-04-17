file(REMOVE_RECURSE
  "../x86_64-slc6-gcc62-opt/include/BayesianLib"
  "../x86_64-slc6-gcc62-opt/python/Bayesian/__init__.py"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/ATLAS_PACKAGES_TARGET.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
