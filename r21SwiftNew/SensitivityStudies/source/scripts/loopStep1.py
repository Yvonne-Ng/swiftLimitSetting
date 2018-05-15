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
        #------photon g150_2j25 inlusive
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_dijetgamma_g150_2j25_inclusiveApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/dijetgamma_mjj_g150_2j25_inclusive.root",
        #------photon g150_2j25 2 btagged
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_dijetgamma_g150_2j25_2btaggedApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/dijetgamma_mjj_g150_2j25_nbtag2.root",

        #------trijet j380 inlusive
            "outputRootTemplate": "../input_dijetISR2018/bkg/FluctuatedSearchPhase_trijet_j380_inclusiveApr_%s.root",
            "inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/resultRoot/SearchPhase_trijet_mjj_inclusive.root",

        #------trijet  j280  2 btagged
            #"outputRootTemplate": "../input_dijetISR2018/bkg/Fluctuated_trijet_j380_2btaggedApr_%s.root",
            #"inputRoot":"/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/trijet_mjj_nbtag2.root",
            "numOfOutput": 10}
    loopStep01(config)
