#!/usr/bin/env bash

#------------------------------------------
#check out packages and get GRL
function checkOutPackages {
    echo -e "\nchecking out packages"
    rc checkout_pkg atlasoff/PhysicsAnalysis/JetTagging/JetTagPerformanceCalibration/xAODBTaggingEfficiency/tags/xAODBTaggingEfficiency-00-00-23/
    #svn co svn+ssh://svn.cern.ch/reps/atlasphys-exo/Physics/Exotic/JDM/DiJet/RunII/DijetHelpers/trunk DijetHelpers
    rc checkout_pkg atlasphys-exo/Physics/Exotic/JDM/DiJet/RunII/DijetHelpers/tags/DijetHelpers-00-04-02
    #echo -e "\ndownloading GRL"
    #wget http://atlasdqm.web.cern.ch/atlasdqm/grlgen/All_Good/data15_13TeV.periodAllYear_DetStatus-v64-pro19_DQDefects-00-01-02_PHYS_StandardGRL_All_Good.xml -P DijetResonanceAlgo/data/
}

#------------------------------------------
#common setup
function commonSetup {
    echo -e "\nsetting up"
    rc find_packages
    rc compile
}

#------------------------------------------
#instructions
function printInstructions {
    echo -e "\nsetup-dijet.sh"
    echo "HOW TO: source setup-dijet.sh trunk/mc15/grid"
}

#------------------------------------------
case $# in
    #------------------------------------------
    0)
	printInstructions
	return
	;;
    #------------------------------------------
    1)
	case $1 in
	    #------------------------------------------
	    trunk)
		echo -e "\ntrunk setup\n"
		rcSetup Base,2.3.31
		svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UChicago/xAODAnaHelpers/trunk xAODAnaHelpers
		svn co svn+ssh://svn.cern.ch/reps/atlasphys-exo/Physics/Exotic/JDM/DiJet/RunII/DijetResonanceAlgo/trunk DijetResonanceAlgo
		python xAODAnaHelpers/scripts/checkoutASGtags.py 2.3.31
		checkOutPackages
		commonSetup
		;;
	    #------------------------------------------
	    mc15)
		echo -e "\nmc15 setup\n"
		rcSetup Base,2.3.31
		svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UChicago/xAODAnaHelpers/tags/xAODAnaHelpers-00-03-22 xAODAnaHelpers
		svn co svn+ssh://svn.cern.ch/reps/atlasphys-exo/Physics/Exotic/JDM/DiJet/RunII/DijetResonanceAlgo/tags/DijetResonanceAlgo-00-04-06 DijetResonanceAlgo
		python xAODAnaHelpers/scripts/checkoutASGtags.py 2.3.31
		checkOutPackages
		commonSetup
		;;
	    #------------------------------------------
	    grid)
		echo -e "\ngrid setup\n"
		setupATLAS --quiet
		localSetupDQ2Client --skipConfirm #set environment variable RUCIO_ACCOUNT=<your grid username> to skip the question asked
		voms-proxy-init -voms atlas -valid 48:00
		localSetupPandaClient currentJedi --noAthenaCheck
		rcSetup "" #keep the "" or it will use 'grid' as a parameter for rcSetup
		;;
	    #------------------------------------------
	    *)
		printInstructions
		return
		;;
	    #------------------------------------------

	esac
	;;
    #------------------------------------------
    *)
	printInstructions
	return
	;;
esac

#------------------------------------------
echo -e "\ndone"
return
