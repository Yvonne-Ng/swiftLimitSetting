# README FOR CATERINA and KATE
##For Fluctuation

loopSearchPhase.py -> Runs SearchPhase in batch, current set to run one single file
loopStep1.py -> run step1 (fluctuating the background) in batch. current set to run on one sigle file
loopDrawSignalInjectionMassPoints.py->Draws all the searchPhase output you set. 

##signal injection
batchDoSensitivity.py ->Runs everything in the UCI batch system   -> configure everything that you want to run on 
calls batchDoSensitivity.sh -> set up individual slurm jobs
calls doSensitivityScan2_rewrite.py
which calls :
    -> step02_rewrite.py -> performs signal injection
    ->step03_rewrite.py -> performs searchphase on the things from step02

##configuration guide
configuration is split into 3 levels:
1. batchDoSensitivity.py work as steeriing scripts. (loop over mass points, mass width , spectra etc)
2. jsonFiles within configDoSen/ are configuration for doSensitivityScan2_rewrite.py, it defines a data file/ searchphase config file to run on etc
3. files in configurations/ are the regular searchphase configurations


