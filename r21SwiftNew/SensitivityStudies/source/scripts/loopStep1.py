#!/bin/python
import os

def loopStep01(config):
    for i in range(config["numOfOutput"]):
        commandTemplate="python step01_rewrite.py --initRoot %s --outputRoot %s"%(config["inputRoot"],config["outputRootTemplate"])
        print("commandTemplate", commandTemplate)
        commandTemplate=commandTemplate%(str(i))
        print("commandTemplate", commandTemplate)
        os.system(commandTemplate)


if __name__=="__main__":
    config={
#-----------april 2018
        #------photon g150_2j25 inlusive
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_dijetgamma_g150_2j25_inclusiveApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/dijetgamma_mjj_g150_2j25_inclusive.root",
        #------photon g150_2j25 2 btagged
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_dijetgamma_g150_2j25_2btaggedApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/dijetgamma_mjj_g150_2j25_nbtag2.root",

        #------trijet j380 inlusive
            #"outputRootTemplate": "../input_dijetISR2018/bkg/FluctuatedSearchPhase_trijet_j380_inclusiveApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/resultRoot/SearchPhase_trijet_mjj_inclusive.root",

        #------trijet  j280  2 btagged
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_trijet_j380_2btaggedApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/trijet_mjj_nbtag2.root",
#-----------may 2018
        #-----dijetgamma_compound_trigger_inclusive
            #"outputRootTemplate": "../input_dijetISR2018/bkg/may2018/FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_dijetgamma_compound_trigger_inclusive.root",
  #      #-----dijetgamma_compound_trigger_nbtag2.root
            #"outputRootTemplate": "../input_dijetISR2018/bkg/may2018/FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_dijetgamma_compound_trigger_nbtag2.root",
  #      #-----dijetgamma_single_trigger_inclusive.root
  #          "outputRootTemplate": "../input_dijetISR2018/bkg/may2018/FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_%s.root",
  #          "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_dijetgamma_single_trigger_inclusive.root",

  #      #-----dijetgamma_single_trigger_nbtag.root
  #          "outputRootTemplate": "../input_dijetISR2018/bkg/may2018/SearchPhase_dijetgamma_single_trigger_nbtag2_%s.root",
  #          "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_dijetgamma_single_trigger_nbtag2.root",

  #      #-----dijetgamma_single_trigger_nbtag2.root
          #  "outputRootTemplate": "../input_dijetISR2018/bkg/may2018/FluctuatedSearchPhase_trijet_nbtag2_%s.root",
          #  "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_trijet_nbtag2.root",

  #      #------trijet j380 inlusive
  #          "outputRootTemplate": "../input_dijetISR2018/bkg/may2018/FluctuatedSearchPhase_trijet_inclusive.root_%s.root",
  #          "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018/SearchPhase_trijet_inclusive.root",


        #-----dijetgamma_single_trigger_inclusive.root
            "outputRootTemplate": "../input_dijetISR2018/bkg/may2018/CatDogCrossCheckFluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_%s.root",
            "inputRoot":"/SearchPhase_dijetgamma_single_trigger_ystar0p75_inclusive.root",
        #------trijet  j280  2 btagged


            "numOfOutput": 10}
    loopConfig=[
        #-----dijetgamma_compound_trigger_inclusive
            {"outputRootTemplate": "../input_dijetISR2018/bkg/may20185Params/CatDogCrossCheckFluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_%s.root",
            "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/resultRootCatDogCheck/SearchPhase_dijetgamma_compound_trigger_ystar0p75_inclusive.root",
            "numOfOutput": 3},
        #-----dijetgamma_single_trigger_inclusive.root
            {"outputRootTemplate": "../input_dijetISR2018/bkg/may20185Params/CatDogCrossCheckFluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_%s.root",
            "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/resultRootCatDogCheck/SearchPhase_dijetgamma_single_trigger_ystar0p75_inclusive.root",
            "numOfOutput": 3},

        #------trijet j380 inlusive
            {"outputRootTemplate": "../input_dijetISR2018/bkg/may20185Params/CatDogCrossCheckFluctuatedSearchPhase_trijet_inclusive.root_%s.root",
            "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/resultRootCatDogCheck/SearchPhase_trijet_ystar0p75_inclusive.root",

            "numOfOutput": 3}]
    for config in loopConfig:
        loopStep01(config)
