#!/usr/bin/env python
import subprocess # So can use shell scripting in python
import os
import ROOT
from ROOT import *
import re

# *****************
# Lydia Beresford
# April 2015

# Script to run: Step 2 and Step 3
# - setLimitsOneMassPoint.cxx 
# - LimitSettingPhase.cxx 
# - plotLimitSetting_gjj.py to plot results of LimitSettingPhase.cxx
#
# Note:To change fit parameters, mjj cut (minXForFit) and other things, do this in Step2_setLimitsOneMassPoint.config!
# All log files stored 1 directory up in LogFiles directory, unless otherwise specified

# *****************

statspath = os.getcwd() # path used in outputFileName in config 
headdir = statspath.split("/Bayesian")[0] # directory for whole package 
logsdir =  headdir # Log Files Sent Here
print headdir
batchdir = logsdir+"/StatisticalAnalysis" #headdir # Folder to be copyied to batch, by default headdir unless otherwise specified 
Signals = {}

#---------------------------
# ***** User specifies *****
#---------------------------

# *NOTE* in path/file names use %d for mass, MMM for model !!!!!!!!!!!

#---------------------------
# Files and directories

dosetLimitsOneMassPoint =True # Set to True to run setLimitOneMassPoint.cxx 

doLimitSettingPhase = False# # ONLY set to True when Step 1 setLimitsOneMassPoint has finished running on the batch (or locally)!!!
                            # Set to True to run LimitSettingPhase.cxx
doPlotting = False # ONLY set to True when Step 3 LimitSettingPhase.cxx has/is being run!!!
                   # Set to True to run plotLimitSetting_gjj.py

#SearchPhaseresults = "%s/Bayesian/results/Step1_SearchPhase/dijetgamma2017MC/Step1_SearchPhase_Zprime_mjj_var_DataLike_LLLfb.root"%headdir
SearchPhaseresults = "%s/Bayesian/results/Step1_SearchPhase/RedoMCwithCutNoScaledijetgamma_g85_2j65/Step1_SearchPhase_Zprime_mjj_var.root"%headdir
                   # Can replace lumi in name with LLL and will be filled by Lumis value (must do this if running on multiple lumis)

##---------------------------
# Analysis quantities

lumiUnc = 0.029 # Size of luminosity uncertainty FIXME VALUE ONLY HERE FOR REFERENCE, actual value set in config, this script doesn't update config file, could make script update config like for other values!

Ecm = 13000.0 # Centre of mass energy in GeV

doPDFAccErr = True # Set to True to use PDF Acceptance Error 
PDFErrSize = 0.01

doISRAccErr = True # Set to True to use Photon Acceptance Error 
ISRErrSize = 0.03 

Lumis = ["15p45"] # Luminosities to scale limits to in fb e.g. "10" or 0p1, should have corresponding search phase ran for this lumi 

##---------------------------
# Run controls 
 
# For Step 2 running setLimitsOneMassPoint.cxx  
#setLimitsOneMassPointconfig = "./configurations/Step2_setLimitsOneMassPoint_gjj_MMM.config"   
setLimitsOneMassPointconfig = "./configurations/Step2_setLimitsOneMassPoint_gjj_MMM2017.config"   

useBatch = True # Set to True to run setLimitsOneMassPoint.cxx on the batch, or set to False to run locally. runs code in batchdir 
atOx = False # Set to True to use Oxford batch rather than lxbatch for running!

# Splits - parallelise running of limits for pseudo-experiments for uncertainty bands by running more batch jobs to speed it up!
nPETotal = 200 #Total number of pseudo-experiments to run for expected limit bands
nSplits = 8 # Number of divisions to split PEs into
nPEForExpected = nPETotal/nSplits # Calculating how many PEs per division (split) performing

#---------------------------
# Signal information

plotextension = "dijetgamma_data_hist_20160727_15p45fb_4Par_169_1493"  # folder name to store all plots, results, configs and outputs consistently
                                                                           # MUST keep name same when doing step 2 and 3

# Uncomment only 1 at a time depending which model and coupling you're running on

# ZPrime   

#Coupling = "gSM0p10" 
#Signals["ZPrimemR"]=["250","350","550"]
#outName = "ZPrime0p10"

#Coupling = "gSM0p20" 
#Signals["ZPrimemR"]=["250","350","450","550","750"] 
#outName = "ZPrime0p20"

#Coupling = "gSM0p30" 
#Signals["ZPrimemR"]=["200","250","300","350","400","450","500","550","750","950"] 
#outName = "ZPrime0p30"

#Coupling = "gSM0p40" 
#Signals["ZPrimemR"]=["750"] 
#outName = "ZPrime0p40"
#2017 Yvonne Edit

Coupling="gSM0p3"
Ph="100"
Signals["ZPrimemR"]=["1500", "450", "950", "250", "500", "300","350","550", "400", "750"  ]
outName = "Ph100_Zprime0p3"

Coupling="gSM0p4"
Ph="100"
Signals["ZPrimemR"]=["1500", "750"  ]
outName = "Ph100_Zprime0p4"

Coupling="gSM0p2"
Ph="100"
Signals["ZPrimemR"]=["250", "550", "350", "750", "450"  ]
outName = "Ph100_Zprime0p2"

Coupling="gSM0p1"
Ph="100"
Signals["ZPrimemR"]=["250", "550", "350", "450"]
outName = "Ph100_Zprime0p1"

Coupling="gSM0p2"
Ph="50"
Signals["ZPrimemR"]=["1500", "550", "250","750", "350", "950", "450"  ]
outName = "Ph100_Zprime0p2"
##Coupling="gSM0p3"
##Ph="50
#Signals["ZPrimemR"]=["1500", "550", "500", "750", "250", "950", "350", "300", "450", "400"]
#outName = ["Ph50_Zprime0p10"]
#
#Coupling="gSM0p3"
#Ph="100
#Signals["ZPrimemR"]=["1500", "550", "500", "750", "250", "950", "350", "300", "450", "400"]
#outName = ["Ph100_Zprime0p10"]
#
#can change later
LimitSettingPhaseconfig = "./configurations/Step3_LimitSettingPhase_gjj_MMM_%s.config"%Coupling # Path/file of LimitSettingPhase config
#changed
signalFileName = "inputs//KMCSignal/Chopped_Ph{0}_MMM%d_{1}.root".format(Ph,Coupling)
                                                                                                         #
#signalFileName = "inputs/KMCSignal/Chopped_MMM%d{0}.root".format(Coupling)

#----------------------------------
# ***** End of User specifies *****
#----------------------------------

#----------------------
# Preliminary steps
#----------------------

# Make directories to store outputs if they don't exist already!
if dosetLimitsOneMassPoint: # For Step2 setLimitsOneMassPoint
  Step2_ConfigArchive = "%s/LogFiles/%s/Step2_setLimitsOneMassPoint/ConfigArchive"%(logsdir,plotextension)
  Step2_ScriptArchive = "%s/LogFiles/%s/Step2_setLimitsOneMassPoint/ScriptArchive"%(logsdir,plotextension)
  Step2_CodeOutput = "%s/LogFiles/%s/Step2_setLimitsOneMassPoint/CodeOutput"%(logsdir,plotextension)
  BATplotDirectory = "%s/LogFiles/%s/Step2_setLimitsOneMassPoint/BATPlots/"%(logsdir,plotextension)
  directories = ["./results/Step2_setLimitsOneMassPoint/%s"%plotextension,Step2_ConfigArchive,Step2_ScriptArchive,Step2_CodeOutput,BATplotDirectory]
  for directory in directories:
    if not os.path.exists(directory):
      os.makedirs(directory)

if doLimitSettingPhase: # For Step3 LimitSettingPhase
  Step3_ConfigArchive = "%s/LogFiles/%s/Step3_LimitSettingPhase/ConfigArchive"%(logsdir,plotextension)
  Step3_CodeOutput = "%s/LogFiles/%s/Step3_LimitSettingPhase/CodeOutput"%(logsdir,plotextension)
  directories = ["./results/Step3_LimitSettingPhase/%s"%plotextension, Step3_ConfigArchive, Step3_CodeOutput]
  for directory in directories:
    if not os.path.exists(directory):
      os.makedirs(directory)


#-------------------------------------
# Performing Step 2: Limit setting for each model, mass, lumi combo using setLimitsOneMassPoint.cxx
#-------------------------------------

# Loop over combination of models, masses and lumis
if dosetLimitsOneMassPoint:
  print "Performing setLimitsOneMassPoint"
  for Model in Signals.keys() :
    for Mass in sorted(Signals[Model]):
      for Lumi in Lumis:
        # open modified config file (fout) for writing
        fout = open('%s/Step2_%s%s_%sfb.config'%(Step2_ConfigArchive,outName,Mass,Lumi), 'w')

        # read in config file as fin and replace relevat fields with user inout specified at top of this file
        with open('%s'%setLimitsOneMassPointconfig.replace("MMM",Model), 'r') as fin:
          for line in fin:
            if (line.startswith("dataFileName") or line.startswith("signalFileName") or line.startswith("nominalSignalHist") or line.startswith("outputFileName") or line.startswith("plotDirectory") or line.startswith("plotNameExtension") or line.startswith("signame") or line.startswith("nominalTemplateJES") or line.startswith("nameTemp") or line.startswith("nPEForExpected")): 
              if line.startswith("dataFileName"):
                line = "dataFileName %s\n"%SearchPhaseresults.replace("LLL",Lumi)
                fout.write(line)
              if line.startswith("signalFileName"):
                line = "signalFileName %s\n"%signalFileName
                line = line.replace("MMM",Model)
                fout.write(line)
              if line.startswith("nominalSignalHist"):
                if Model == "ZPrimemR":
                  #line = "nominalSignalHist {0}/mjj_MMM%dCCC_1fb_Nominal\n".format(HistDir)
                  #line = "nominalSignalHist mjj_MMM%dCCC_1fb_Nominal\n"
                  #line = line.replace("MMM",Model)
                  #line = line.replace("CCC",Coupling)
                  
                  line ="nominalSignalHist dijetgamma_g85_2j65/Zprime_mjj_var"
                else:
                  line = "nominalSignalHist mjj_MMM%d_1fb_Nominal\n"
                  line = line.replace("MMM",Model)
                fout.write(line)
              if line.startswith("outputFileName"):
                line = "outputFileName %s/results/Step2_setLimitsOneMassPoint/%s/Step2_setLimitsOneMassPoint_%s%s_%sfb.root\n"%(statspath,plotextension,outName,Mass,Lumi)
                fout.write(line)
              if line.startswith("plotDirectory"):
                line = "plotDirectory %s/\n"%BATplotDirectory
                fout.write(line)
              if line.startswith("plotNameExtension"):
                line = "plotNameExtension %s/\n"%outName
                fout.write(line)
              if line.startswith("signame"):
                line = "signame %s/\n"%outName
                fout.write(line)
              if line.startswith("nPEForExpected"):
                line = "nPEForExpected %s\n"%nPEForExpected
                fout.write(line)
              if line.startswith("nominalTemplateJES"):
                if Model == "ZPrimemR":
                  #line = "nominalTemplateJES {0}/mjj_MMM%dCCC_1fb_Nominal\n".format(HistDir)
                  line = "nominalTemplateJES mjj_MMM%dCCC_1fb_Nominal\n"
                  line = line.replace("MMM",Model)
                  line = line.replace("CCC",Coupling)
                  fout.write(line)
                else:
                  fout.write(line)
              if line.startswith("nameTemp1"):
                if Model == "ZPrimemR":
                  #line = "nameTemp1 {0}/mjj_MMM%dCCC_1fb_JET_GroupedNP_1\n".format(HistDir)
                  line = "nameTemp1 mjj_MMM%dCCC_1fb_JET_GroupedNP_1\n"
                  line = line.replace("MMM",Model)
                  line = line.replace("CCC",Coupling)
                  fout.write(line)
                else:
                  fout.write(line)
              if line.startswith("nameTemp2"):
                if Model == "ZPrimemR":
                  #line = "nameTemp2 {0}/mjj_MMM%dCCC_1fb_JET_GroupedNP_2\n".format(HistDir)
                  line = "nameTemp2 mjj_MMM%dCCC_1fb_JET_GroupedNP_2\n"
                  line = line.replace("MMM",Model)
                  line = line.replace("CCC",Coupling)
                  fout.write(line)
                else:
                  fout.write(line)
              if line.startswith("nameTemp3"):
                if Model == "ZPrimemR":
                  #line = "nameTemp3 {0}/mjj_MMM%dCCC_1fb_JET_GroupedNP_3\n".format(HistDir)
                  line = "nameTemp3 mjj_MMM%dCCC_1fb_JET_GroupedNP_3\n"
                  line = line.replace("MMM",Model)
                  line = line.replace("CCC",Coupling)
                  fout.write(line)
                else:
                  fout.write(line)
              if line.startswith("nameTemp4"):
                if Model == "ZPrimemR":
                  #line = "nameTemp4 {0}/mjj_MMM%dCCC_1fb_JET_EtaIntercalibration_NonClosure\n".format(HistDir)
                  line = "nameTemp4 mjj_MMM%dCCC_1fb_JET_EtaIntercalibration_NonClosure\n"
                  line = line.replace("MMM",Model)
                  line = line.replace("CCC",Coupling)
                  fout.write(line)
                else:
                  fout.write(line)
            else:
              fout.write(line)
        fin.close()
        fout.close()

        print "Submitting %i jobs for mass %s"%(nSplits,Mass)
        for split in range (0,nSplits):

          print split
          # Set different seed and output file name for each split
          Seed = eval(Mass)+split
          print "SEED"
          print Seed
          print type(Seed)

          outfile = "%s/results/Step2_setLimitsOneMassPoint/%s/Step2_setLimitsOneMassPoint_%s%s_%sfb_%i.root\n"%(statspath,plotextension,outName,Mass,Lumi,split)

          # Setting command to be submitted (use tee to direc output to screen and to log file)

          if doPDFAccErr and doISRAccErr: # do PDF acceptance error and ISR acceptance error
            command = "setLimitsOneMassPoint --config %s/Step2_%s%s_%sfb.config --mass %s --PDFAccErr %f --ISRAccErr %f --seed %i --outfile %s |& tee %s/Step2_%s%s_%sfb_%i_withPDFAndISRAccErr.txt"%(Step2_ConfigArchive,outName,Mass,Lumi,Mass,PDFErrSize,ISRErrSize,Seed,outfile,Step2_CodeOutput,outName,Mass,Lumi,split)

          elif doPDFAccErr: # do PDF acceptance error
            command = "setLimitsOneMassPoint --config %s/Step2_%s%s_%sfb.config --mass %s --PDFAccErr %f --seed %i --outfile %s |& tee %s/Step2_%s%s_%sfb_%i_withPDFAccErr.txt"%(Step2_ConfigArchive,outName,Mass,Lumi,Mass,PDFErrSize,Seed,outfile,Step2_CodeOutput,outName,Mass,Lumi,split)

          elif doISRAccErr: # do ISR acceptance error
            command = "setLimitsOneMassPoint --config %s/Step2_%s%s_%sfb.config --mass %s --ISRAccErr %f --seed %i --outfile %s |& tee %s/Step2_%s%s_%sfb_%i_withISRAccErr.txt"%(Step2_ConfigArchive,outName,Mass,Lumi,Mass,ISRErrSize,Seed,outfile,Step2_CodeOutput,outName,Mass,Lumi,split)

          else: # do not do PDF or ISR acceptance error
            command = "setLimitsOneMassPoint --config %s/Step2_%s%s_%sfb.config --mass %s --seed %i --outfile %s  |& tee %s/Step2_%s%s_%sfb_%i.txt"%(Step2_ConfigArchive,outName,Mass,Lumi,Mass,Seed,outfile,Step2_CodeOutput,outName,Mass,Lumi,split)

	         
          # Perform setLimitsOneMassPoint locally
          if not useBatch:  
            subprocess.call(command, shell=True)

          # Use batch i.e. perform setLimitsOneMassPoint on the batch   
          if useBatch:
            if atOx:
              # Perform setLimitsOneMassPoint on batch
              print "Ox Batch!!"
              batchcommand = command.split("|&")[0]
              CodeOutputName = (command.split("|& tee ")[1]).split(".txt")[0] # Name of files for code output to be stored as
              print batchcommand
        
              # Open batch script as fbatchin
              fbatchin = open('./scripts/OxfordBatch/Step2_BatchScript_Template_Oxford.sh', 'r') 
              fbatchindata = fbatchin.read()
              fbatchin.close()
        
              # open modified batch script (fbatchout) for writing
              fbatchout = open('%s/Step2_BatchScript_Template_%s%s_%sfb_%i.sh'%(Step2_ScriptArchive,outName,Mass,Lumi,split),'w')
              fbatchoutdata = fbatchindata.replace("YYY",batchdir) # In batch script replace YYY for path for whole package
              fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
              fbatchoutdata = fbatchoutdata.replace("OOO",CodeOutputName) # In batch script replace OOO (i.e. std output stream) to CodeOutput directory
              fbatchoutdata = fbatchoutdata.replace("EEE",CodeOutputName) # In batch script replace EEE (i.e. output error stream) to CodeOutput directory
              fbatchout.write(fbatchoutdata)    
 
              fbatchout.close()
              subprocess.call("qsub < %s/Step2_BatchScript_Template_%s%s_%sfb_%i.sh"%(Step2_ScriptArchive,outName,Mass,Lumi,split), shell=True)
            else:
              # Perform setLimitsOneMassPoint on batch
              print "Batch!!"
              batchcommand = command.split("|&")[0]
              CodeOutputName = (command.split("|& tee ")[1]).split(".txt")[0] # Name of files for code output to be stored as
              print batchcommand
          
              # Open batch script as fbatchin
              fbatchin = open('./scripts/Step2_BatchScript_Template.sh', 'r') 
              fbatchindata = fbatchin.read()
              fbatchin.close()
          
              # open modified batch script (fbatchout) for writing
              fbatchout = open('%s/Step2_BatchScript_Template_%s%s_%sfb_%s.sh'%(Step2_ScriptArchive,outName,Mass,Lumi,split),'w')
              fbatchoutdata = fbatchindata.replace("YYY",batchdir) # In batch script replace YYY for path for whole package
              fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
              fbatchoutdata = fbatchoutdata.replace("OOO",CodeOutputName) # In batch script replace OOO (i.e. std output stream) to CodeOutput directory
              fbatchoutdata = fbatchoutdata.replace("EEE",CodeOutputName) # In batch script replace EEE (i.e. output error stream) to CodeOutput directory
              fbatchout.write(fbatchoutdata)    

              modcommand = 'chmod 744 %s/Step2_BatchScript_Template_%s%s_%sfb_%i.sh'%(Step2_ScriptArchive,outName,Mass,Lumi,split)
              print modcommand
              subprocess.call(modcommand, shell=True)
              subprocess.call("ls -l {0}".format(Step2_ScriptArchive), shell=True)
 
              fbatchout.close()
              command = "sbatch -c 2 -p atlas_all -t 300 %s/Step2_BatchScript_Template_%s%s_%sfb_%i.sh"%(Step2_ScriptArchive,outName,Mass,Lumi,split)
              print command
              subprocess.call(command, shell=True)


#-------------------------------------
# Performing Step 3: Combining mass points for Limit setting for each model and lumi combo using LimitSettingPhase.cxx
#-------------------------------------

if doLimitSettingPhase or doPlotting:
  for Model in Signals.keys() :
    for Lumi in Lumis:
      if doLimitSettingPhase: 
        print "Performing LimitSettingPhase"
        # open modified config file (fout) for writing
        fout = open('%s/Step3_%s_%sfb.config'%(Step3_ConfigArchive,outName,Lumi), 'w')

        # read in config file as fin and replace relevant fields
        with open('%s'%LimitSettingPhaseconfig.replace("MMM",Model), 'r') as fin:
          for line in fin:
            if (line.startswith("inputFileForm") or line.startswith("outputFileName") or line.startswith("luminosity") or line.startswith("nSplits1")): 
              if line.startswith("inputFileForm"): # Used %%d in line below as %d is special character in python so need extra % to allow %d
                line = "inputFileForm ./results/Step2_setLimitsOneMassPoint/%s/Step2_setLimitsOneMassPoint_%s%%d_%sfb_%%d.root\n"%(plotextension,outName,Lumi) 
                fout.write(line)
              if line.startswith("outputFileName"): 
                line = "outputFileName ./results/Step3_LimitSettingPhase/%s/Step3_LimitSettingPhase_%s_%sfb.root\n"%(plotextension,outName,Lumi)
                fout.write(line)
    
              if line.startswith("luminosity"):
                if "p" in Lumi: # converting to pb
                  lumi = Lumi.replace("p",".")
                  lumi = str(float(lumi)*1000)
                else: # converting to pb
                  lumi = str(float(Lumi)*1000)
                line = "luminosity %s\n"%lumi
                fout.write(line)
              if line.startswith("nSplits1"): 
                line = "nSplits1 %i\n"%(nSplits)
                fout.write(line)
            else:
              fout.write(line)
        fin.close()
        fout.close()
        # Perform LimitSettingPhase locally
        command = "LimitSettingPhase --config %s/Step3_%s_%sfb.config |& tee %s/Step3_%s%sfb.txt"%(Step3_ConfigArchive,outName,Lumi,Step3_CodeOutput,outName,Lumi)
        print command
        subprocess.call(command, shell=True)
 
      #-------------------------------------
      # Plotting results of running LimitSettingPhase.cxx using plotLimitSetting_gjj.py
      #-------------------------------------
    
      if doPlotting:
        if "p" in Lumi: # converting to pb
          lumi = Lumi.replace("p",".")
          lumi = float(lumi)*1000
        else: # converting to pb
          lumi = float(Lumi)*1000

        # open modified plotLimitSetting_gjj.py (fout) for writing
        fout = open('plotting/LimitSettingPhase/plotLimitSetting_gjj_%s_%sfb.py'%(outName,Lumi), 'w')

        # read in plotLimitSetting_gjj as fin
        with open('./plotting/LimitSettingPhase/plotLimitSetting_gjj.py', 'r') as fin:
          for line in fin:
            if (line.startswith("searchInputFile") or line.startswith("folderextension") or line.startswith("limitFileNameTemplate") or line.startswith("luminosity") or line.startswith("Ecm") or line.startswith("individualLimitFiles")): 
              
              if line.startswith("searchInputFile"):
                line = "searchInputFile = ROOT.TFile('%s')\n"%(SearchPhaseresults.replace("LLL",Lumi))
                fout.write(line)
              if line.startswith("folderextension"): 
                line = "folderextension = './plotting/LimitSettingPhase/plots/%s/%s/'\n"%(plotextension,Lumi)
                fout.write(line)
              if line.startswith("limitFileNameTemplate"): 
                line = "limitFileNameTemplate = './results/Step3_LimitSettingPhase/%s/Step3_LimitSettingPhase_{0}_%sfb.root'\n"%(plotextension,Lumi)
                fout.write(line)
              if line.startswith("individualLimitFiles"): 
                #line = "individualLimitFiles = './results/Step2_setLimitsOneMassPoint/%s/Step2_setLimitsOneMassPoint_{0}{1}_%sfb.root'\n"%(plotextension,Lumi)
                line = "individualLimitFiles = './results/Step2_setLimitsOneMassPoint/%s/Step2_setLimitsOneMassPoint_{0}{1}_%sfb_0.root'\n"%(plotextension,Lumi)
                fout.write(line)
              if line.startswith("luminosity"):
                line = "luminosity = %d\n"%lumi
                fout.write(line)
              if "Ecm" in line:
                line = "Ecm = %d\n"%(Ecm/1000) 
                fout.write(line)
            else:
              fout.write(line)  
        fin.close()
        fout.close()
        # do plotting locally
        subprocess.call("python plotting/LimitSettingPhase/plotLimitSetting_gjj_%s_%sfb.py -b"%(outName,Lumi), shell=True)
        os.remove("./plotting/LimitSettingPhase/plotLimitSetting_gjj_%s_%sfb.py"%(outName,Lumi)) # Remove modified plotLimitSetting_gjj after plotting

