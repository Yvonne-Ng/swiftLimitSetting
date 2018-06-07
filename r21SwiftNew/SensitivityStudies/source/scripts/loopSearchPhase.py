#!/bin/python


import sys, os, math, argparse, ROOT
import sensitivityTools
import numpy as np
import os.path
from fileNamingTool import *
import json
import ROOT
from ROOT import TFile, TH1F, TCanvas

def searchPhaseOutput(fileName):
    return "SearchPhase_"+fileName


def loopSearchPhase(config):
    for i in range(len(config["inFileList"])):
        inFileList=config["inFileList"][i]
        outputRootList=[]
        printFile=open("loopSearchPhase"+inFileList[0][:-7]+".log", "w+")
        for inFile in inFileList:
            outputName=searchPhaseOutput(inFile)
            commandTemplate = "SearchPhase --config {0} --file {1} --histName {2} --noDE --outputfile {3}".format(config["configName"][0],  config["inFileDir"]+"/"+inFile,config["histName"],config["outputRootDir"]+outputName)
            os.system(commandTemplate)
            outputRootList.append(outputName)
            f1=TFile.Open(config["outputRootDir"]+"/"+outputName)
            try:
                (excludeWindow, windowLow, windowHigh)=f1.Get("excludeWindowNums")
                printFile.write("for %s window exclusion is %s"%(inFile, excludeWindow))
            except:
                printFile.write("the fit failed, fitFile: %s"%inFile)
        return outputRootList

def drawOutputRootResidual(inDir, spList):
    for inFile in spList:
        f1=TFile.Open(inDir+"/"+inFile)
        try:
            hist=f1.Get("residualHist")
        except:
            print("fit failed for file: ", inFile)
        #hist.GetXaxis().SetRangeUser(0, 1000)
        ROOT.gROOT.SetBatch(True)
        c1= TCanvas()
        hist.Draw()
        c1.SaveAs("pdf/"+inFile+".pdf")
        #hist.Close()
        f1.Close()


if __name__=="__main__":
#----gamma g150_2j25 inclusive
   # config={"inFileDir": "../input_dijetISR2018/bkg/",
   #         "inFileList": ["Fluctuated_dijetgamma_g150_2j25_inclusiveApr_0.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_1.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_2.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_3.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_4.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_5.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_6.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_7.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_8.root",
   #         "Fluctuated_dijetgamma_g150_2j25_inclusiveApr_9.root"],
   #         "histName": "background_mjj_var_fluctuated",
   #         "configName": "configurations/Step1_SearchPhase_Swift_dijetISR_g150_2j25_inclusive.config",
   #         "outputRootDir": "resultRoot/"}
#---gamma g150_2j25 2btagged
    #config={"inFileDir": "../input_dijetISR2018/bkg/",
    #        "inFileList": ["Fluctuated_dijetgamma_g150_2j25_2btaggedApr_0.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_1.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_2.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_3.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_4.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_5.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_6.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_7.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_8.root",
    #            "Fluctuated_dijetgamma_g150_2j25_2btaggedApr_9.root"],
    #        "histName": "background_mjj_var_fluctuated",
    #        "configName": "configurations/Step1_SearchPhase_Swift_dijetISR_g150_2j25_2btagged.config",
    #        "outputRootDir": "resultRoot/"}
#----trijet inclusive
   # config={"inFileDir": "../input_dijetISR2018/bkg/",
   #         "inFileList": ["Fluctuated_trijet_j380_inclusiveApr_0.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_1.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_2.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_3.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_4.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_5.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_6.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_7.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_8.root",
   #             "Fluctuated_trijet_j380_inclusiveApr_9.root"],
   #         "histName": "background_mjj_var_fluctuated",
   #         "configName": "configurations/Step1_SearchPhase_Swift_trijet_j380_inclusive.config",
   #         "outputRootDir": "resultRoot/"}
#-----trijet 2-btagged
    #config={"inFileDir": "../input_dijetISR2018/bkg/",
    #        "inFileList": ["Fluctuated_trijet_j380_2btaggedApr_0.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_1.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_2.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_3.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_4.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_5.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_6.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_7.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_8.root",
    #            "Fluctuated_trijet_j380_2btaggedApr_9.root"],
    #        "histName": "background_mjj_var_fluctuated",
    #        "configName": "configurations/Step1_SearchPhase_Swift_trijet_j380_2btagged.config",
    #        "outputRootDir": "resultRoot/"}
#----trijet 2 btagged #testing a working fit to see if something else is failing
    #config={"inFileDir": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21Rebuild/input/feb2018/",
    #        "inFileList": ["trijet_HLT_j380_nbtag2.root"],

    config={"inFileDir": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/may2018/",
            "inFileList": [["FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_0.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_1.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_2.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_3.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_4.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_5.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_6.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_7.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_8.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_inclusive_9.root"],
            ["FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_0.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_1.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_2.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_3.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_4.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_5.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_6.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_7.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_8.root",
            "FluctuatedSearchPhase_dijetgamma_compound_trigger_nbtag2_9.root"],
            ["FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_0.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_1.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_2.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_3.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_4.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_5.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_6.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_7.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_8.root",
            "FluctuatedSearchPhase_dijetgamma_single_trigger_inclusive_9.root"],
            ["FluctuatedSearchPhase_trijet_inclusive.root_0.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_1.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_2.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_3.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_4.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_5.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_6.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_7.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_8.root",
            "FluctuatedSearchPhase_trijet_inclusive.root_9.root"],
            ["FluctuatedSearchPhase_trijet_nbtag2_0.root",
            "FluctuatedSearchPhase_trijet_nbtag2_1.root",
            "FluctuatedSearchPhase_trijet_nbtag2_2.root",
            "FluctuatedSearchPhase_trijet_nbtag2_3.root",
            "FluctuatedSearchPhase_trijet_nbtag2_4.root",
            "FluctuatedSearchPhase_trijet_nbtag2_5.root",
            "FluctuatedSearchPhase_trijet_nbtag2_6.root",
            "FluctuatedSearchPhase_trijet_nbtag2_7.root",
            "FluctuatedSearchPhase_trijet_nbtag2_8.root",
            "FluctuatedSearchPhase_trijet_nbtag2_9.root"],
    ["SearchPhase_dijetgamma_single_trigger_nbtag2_0.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_1.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_2.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_3.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_4.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_5.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_6.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_7.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_8.root",
    "SearchPhase_dijetgamma_single_trigger_nbtag2_9.root"]],
            "histName": "basicBkgFrom4ParamFit_fluctuated",
            "configName": ["configurations/may2018/Step1_SearchPhase_dijetgamma_compound_trigger_inclusive.config",
                "configurations/may2018/Step1_SearchPhase_dijetgamma_compound_trigger_nbtag2.config",
                "configurations/may2018/Step1_SearchPhase_dijetgamma_single_trigger_inclusive.config",
                "configurations/may2018/Step1_SearchPhase_trijet_inclusive.config",
                "configurations/may2018/Step1_SearchPhase_trijet_nbtag2.config",
                "configurations/may2018/Step1_SearchPhase_dijetgamma_single_trigger_nbtag2.config"],
            #"configName": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/r21StatisticalAnalysis/source/configurations/Step1_SearchPhase_Swift_dijetISR-2.config",
            "outputRootDir": "resultRoot/"}

# check for caterina  6/6/2018

    config={"inFileDir": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/may2018",
            "inFileList": [["dijetgamma_single_trigger_ystar0p75_inclusive.root"]],

            "histName": "background_mjj_var",
            "configName": ["/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/configurations/may2018/kateConfig/Step1_SearchPhase_dijetgamma_single_trigger_inclusive.config"],
            #"configName": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/r21StatisticalAnalysis/source/configurations/Step1_SearchPhase_Swift_dijetISR-2.config",
            "outputRootDir": "resultRootCatDogCheck/"}

   # config={"inFileDir": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/",
   #         "inFileList": ["trijet_mjj_inclusive.root"],
   #         "histName": "background_mjj_var",
   #         "configName": "configurations/Step1_SearchPhase_Swift_trijet_j380_inclusive.config",
   #         #"configName": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/r21StatisticalAnalysis/source/configurations/Step1_SearchPhase_Swift_dijetISR-2.config",
   #         "outputRootDir": "resultRoot/"}

    # new correct fittable fluctuated search phase for trijet window 10 done with kate
   # config={"inFileDir": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/",
   #         "inFileList": ["FluctuatedSearchPhase_trijet_j380_inclusiveApr_0.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_1.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_2.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_3.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_4.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_5.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_6.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_7.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_8.root",
   #             "FluctuatedSearchPhase_trijet_j380_inclusiveApr_9.root"],
   #         "histName": "basicBkgFrom4ParamFit_fluctuated",
   #         "configName": "configurations/Step1_SearchPhase_Swift_trijet_j380_inclusive.config",
   #         #"configName": "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/r21StatisticalAnalysis/source/configurations/Step1_SearchPhase_Swift_dijetISR-2.config",
   #         "outputRootDir": "resultRoot/"}
    #----trijet 2b-tagged
    spList=loopSearchPhase(config)
    #drawOutputRootResidual(config["outputRootDir"], spList)
