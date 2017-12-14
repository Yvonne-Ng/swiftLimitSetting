#!/bin/sh -v 

# Leave combinations of three capital letters as they are, these are replaced during batch submission script i.e. Run_Limits.py

# LXBATCH uses a setup already established, so assuming your environment was set up correctly to run, this should work as is.

# Go to temporary directory
cd ${TMPDIR}

# Copy inputs
cp -r YYY/* .  

# Setup stuff
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
rcSetup Base,2.3.23 # Careful make match version you're using!

cd Bayesian

# Run 
ZZZ
