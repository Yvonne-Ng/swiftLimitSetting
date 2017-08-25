#!/bin/sh -v

# Leave combinations of three capital letters as they are, these are replaced during batch submission script i.e. Run_Limits.py

# LXBATCH uses a setup already established, so assuming your environment was set up correctly to run, this should work as is.

# Go to temporary directory
#TMPDIR=~/tmpdir
#cd ${TMPDIR}

# Copy inputs
#cp -r /afs/cern.ch/work/y/ywng/workspace/DijetISR-Resolved/r21StatisticalAna/source/StatisticalAnalysis/* .  

# Setup stuff
#export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
#source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
cd /cluster/warehouse/kpachal/TLA2016/StatisticalAnalysis
source ./rcSetup.sh
#rcSetup Base,2.3.19 # Careful make match version you're using!
#rc find_packages

cd Bayesian

# Run
setLimitsOneMassPoint --config /afs/cern.ch/work/y/ywng/workspace/DijetISR-Resolved/r21StatisticalAna/source/LogFiles/dijetgamma_data_hist_20160727_15p45fb_4Par_169_1493/Step2_setLimitsOneMassPoint/ConfigArchive/Step2_ZPrime0p10250_15p45fb.config --mass 250 --PDFAccErr 0.010000 --ISRAccErr 0.030000 --seed 251 --outfile /afs/cern.ch/work/y/ywng/workspace/DijetISR-Resolved/r21StatisticalAna/source/Bayesian/results/Step2_setLimitsOneMassPoint/dijetgamma_data_hist_20160727_15p45fb_4Par_169_1493/Step2_setLimitsOneMassPoint_ZPrime0p10250_15p45fb_1.root
 
  
