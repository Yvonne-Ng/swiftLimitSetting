#!bin/bash
setupATLAS
asetup AnalysisBase,21.2.3,here
export PYTHONPATH=./install/InstallArea/x86_64-slc6-gcc62-opt/src/Bayesian/plotting/PythonModules:${PYTHONPATH}
