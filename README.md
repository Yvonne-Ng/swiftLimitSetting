# Statistics Analysis code for DijetISR in Release 21
### Installation guide

Git clone the repo :
```
git clone https://gitlab.cern.ch/ywng/r21StatisticalAnalysis
```
Using cmake to build the installation area:
```
source Setup.sh
source building.sh
```
Setting up the environment variables for the limit
setting code
```
cd ./install/InstallArea/x<version>/
source setup.sh
cd src/Bayesian
```
Get a hold of some input files, and put them under
inputs in install/InstallArea/x<version>/src/Bayesian
If you want to using 2016 ICHEP result:
```
cp -r /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/dijet/statsinputs/RunII/ICHEP_DijetISR/inputs/ ./install/InstallArea/x86_64-slc6-gcc62-opt/src/Bayesian/
```
To run the code, check out this awesome guide:

https://cds.cern.ch/record/2241353/files/ATL-COM-GEN-2017-001.pdf

### When you update the code
After git pulling
```
source Setup.sh
source building.sh
```
