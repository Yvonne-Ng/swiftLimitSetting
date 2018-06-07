# README FOR CATERINA and KATE
## For Fluctuation

1. loopSearchPhase.py -> Runs SearchPhase in batch, current set to run one single file
2. loopStep1.py -> run step1 (fluctuating the background) in batch. current set to run on one sigle file
3. loopDrawSignalInjectionMassPoints.py->Draws all the signal injection ratio plots that I keep sending to mattermost. it uses the same config as loopStep1.py (you can copy it over)+ an output directory for the pdfs to be stored

## signal injection
1. batchDoSensitivity.py ->Runs everything in the UCI batch system   -> configure everything that you want to run on 
2. calls batchDoSensitivity.sh -> set up individual slurm jobs
3. calls doSensitivityScan2_rewrite.py
4. which calls :
a.     -> step02_rewrite.py -> performs signal injection
b.     ->step03_rewrite.py -> performs searchphase on the things from step02

## configuration guide
configuration is split into 3 levels:
1. batchDoSensitivity.py work as steeriing scripts. (loop over mass points, mass width , spectra etc)
2. jsonFiles within configDoSen/ are configuration for doSensitivityScan2_rewrite.py, it defines a data file/ searchphase config file to run on etc
3. files in configurations/ are the regular searchphase configurations


