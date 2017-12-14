# Description
This is the code used to perform fitting, searching and limit setting for the Dijet+ISR analysis.  The following 
people can help you if you have issues :
- Yvonne Ng - [ying.wun.yvonne.ng@cern.ch](mailto:ying.wun.yvonne.ng@cern.ch) (running and debugging)
- Kate Pachal - [Katherine.Pachal@cern.ch](mailto:Katherine.Pachal@cern.ch) (conceptual fitting issues)
- Sam Meehan - [samuel.meehan@cern.ch](mailto:samuel.meehan@cern.ch) (docker issues)

## References
These are some of the key external references for this package
- [ATL-COM-GEN-2017-001](https://cds.cern.ch/record/2241353/files/ATL-COM-GEN-2017-001.pdf) : How to run the code
- [1101.0390](https://arxiv.org/abs/1101.0390) : Original BumpHunter paper
- [CERN-THESIS-2015-179](https://cds.cern.ch/record/2063032?ln=en) : Kate's thesis 

# Initial Setup
This code relies on the AnalysisBase release of ATLAS and there are 
two ways to allow for this use.
- [CVMFS](https://twiki.cern.ch/twiki/bin/view/AtlasProtected/PhysicsAnalysisWorkBookRel21ComputingSetup#The_Analysis_Release) : Working on lxplus (or your local Tier3) which has access to CVMFS_
- [Docker](https://docs.docker.com) : Working with a docker image of AnalysisBase
The interaction with GitLab to obtain the code, compile, and run it are largely the 
same, with the primary difference being the initial setup.  Start by creating a high level directory
in which your work will live
```
mkdir Fitting
cd Fitting
```
and proceed to setting up the environment with which you will work.

## CVMFS
Set up the AnalysisBase release
```
setupATLAS
asetup AnalysisBase,21.2.3,here
export PYTHONPATH=./install/InstallArea/x86_64-slc6-gcc62-opt/src/Bayesian/plotting/PythonModules:${PYTHONPATH}
```

## Docker
This describes the initial setup steps to be able to use a docker image for working with this code
- Start by installing the docker application on your local machine.
- Obtain the docker image for AnalysisBase : `docker pull atlas/analysisbase:21.2.3`
- Launch this docker image from the appropriate location : `docker run --rm -it -v $PWD:$PWD -u root -e DISPLAY -w $PWD atlas/analysisbase:21.2.3`
   - There are a number of arguments here and you can parse them here ([documentation](https://docs.docker.com/engine/reference/commandline/run/)).  
   However, the main thing to 
   appreciate is that these will "bind" the local directories into the docker image so that you can access local files (code,
   text, etc.) on your laptop using whatever editor you like and have access to run and build it within the image
   - It is necessary to launch this from a sufficienctly top level directory such that the subdiretories with the code *and* the 
   input histograms for fitting are contained beneath it
- Setup the work environment : `source /home/atlas/release_setup.sh`
   - It tells you to do this when you launch the image
   - This is equivalent to `setupATLAS & asetup AnalysisBase,21.2.3,here` in CVMFS but the output is not the same
   
## Obtaining/Building Code
Start by obtaining the project in the normal way 
```
git clone https://gitlab.cern.ch/ywng/r21StatisticalAnalysis
```
Using cmake to configure, build, and install the code :
```
mkdir build
cd build

# configure
cmake ../source
# building
make 
# installing
make install DESTDIR=../install
```
The final step is to export the executables from the building via the `setup.sh` script in your install area
```
source ../install/InstallArea/${AnalysisBase_PLATFORM}/setup.sh
```
The code is now set up and compiled and ready to fit some spectra.

## After the First Time
After you build the code the first time, the setup of the work area will be largely the same in terms of configuring
the software release.  If you are only going to rerun the fitting then you only need to execute 
the `source ../install/InstallArea/${AnalysisBase_PLATFORM}/setup.sh`
setup command.  However, if you modify the fitting, BumpHunter, or limit setting, then it will (of course) be necessary
to recompile the package using cmake.

# Fitting Inputs
The fitting inputs are generally stored on eos at `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/dijet/statsinputs/RunII/`.

One example of the inputs is here :
```
/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/dijet/statsinputs/RunII/ICHEP_DijetISR/inputs/hist_20160801/OUT_dijetgamma_mc/datalike-noNeff/
```
These inputs can be stored anywhere as the path will be specified in the [LINK TO RUN SCRIPTS] script which is the top level script you will run.

# Running Fitting
A comprehensive guide to the technical and pedagogical aspects of running the code if found in the references above.  
However, a bare minimum start to running this is to start with the [SearchPhase](source/Bayesian/util/SearchPhase.cxx) 
which itself will perform the fitting and execute the BumpHunter algorithm.  This can be run on its own by creating a config 
file similar to the ones found in [the configurations directory](source/Bayesian/configurations).  However, there exist steering 
scripts such as [Run_gjjSearchPhase.py](source/Bayesian/Run_gjjSearchPhase.py) which facilitates running this on batch systems, 
among other things.

To try a single first run 
- Obtain the inputs `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/dijet/statsinputs/RunII/ICHEP_DijetISR/inputs/hist_20160801/OUT_dijetgamma_mc/datalike-noNeff/`
- Within the [Run_gjjSearchPhase.py](source/Bayesian/Run_gjjSearchPhase.py) steering scriptconfigure the user input parameters
to point at the contents of this input file
- Execute the script as `python Run_gjjSearchPhase.py`

You should see the initial fit performed and then a number of pseudoexperiments for estimating the error and finally the execution of 
more pseudoexperiments to estimate the significance of the largest excess.  For details beyond this, please refer to [ATL-COM-GEN-2017-001](https://cds.cern.ch/record/2241353/files/ATL-COM-GEN-2017-001.pdf)



