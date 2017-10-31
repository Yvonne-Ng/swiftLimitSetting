#!bin/bash

setupATLAS
#asetup AtlasDerivation,21.0.19.1,here
#asetup AnalysisBaseExternals-21.2.0,here
asetup AnalysisBase,21.2.3,here

export PYTHONPATH=/afs/cern.ch/work/y/ywng/workspace/DijetISR-Resolved/r21StatisticalAna/install/InstallArea/x86_64-slc6-gcc62-opt/src/Bayesian/plotting/PythonModules:${PYTHONPATH}

#setup numpy
echo
echo "Running pyanalyssi setuppppp"
#lsetup /cvmfs/sft.cern.ch/lcg/releases/LCG_88/pyanalysis/2.0/x86_64-slc6-gcc62-opt/

#localSetupSFT /cvmfs/sft.cern.ch/lcg/releases/LCG_88/pyanalysis/2.0/x86_64-slc6-gcc62-opt/
#localSetupSFT pyanalys#is 
#/cvmfs/atlas.cern.ch/r#epo/sw/software/21.2/sw/lcg/releases/pyanalysis/2.0-32412
