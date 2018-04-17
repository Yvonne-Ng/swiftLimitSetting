#!/bin/bash
#
#SBATCH -A hep2016-1-4
#SBATCH -p hep 
#SBATCH -t 900
#SBATCH -o /dev/null
#

# Setup stuff
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
cd /lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/r21StatisticalAnalysis/source
source ./rcSetup.sh
#rcSetup Base,2.3.19 # Careful make match version you're using!
#rc find_packages

cd Bayesian

# Run
setLimitsOneMassPoint --config submitConfigs/DijetISRMC//Step2_ZPrime0p05_mZ650_3p57fb.config --mass 650 --PDFAccErr 0.01 --seed 401
