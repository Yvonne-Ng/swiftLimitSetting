#!/usr/bin/env python
import subprocess # So can use shell scripting in python
import os
import ROOT
from ROOT import *
import re

# *****************
# Lydia Beresford
# April 2015

# Script to run Step 1: 
# - SearchPhase.cxx 
# - plotSearchPhase.py to plot results of SearchPhase.cxx

# Note:To change fit parameters, mjj cut (minXForFit) and other things, do this in Step1_SearchPhase.config!
# All log files stored 1 directory up in LogFiles directory, unless otherwise specified
# *****************

statspath = os.getcwd() # path used in outputFileName in config 
headdir = statspath.split("/Bayesian")[0] # directory for whole package 
logsdir = headdir # Log Files Sent Here
batchdir = logsdir+"/StatisticalAnalysis" #headdir # Folder to be copyied to batch, by default headdir unless otherwise specified 
UserfileHistDict = {}

# *****************
#---------------------------
# ***** User specifies *****
#---------------------------

#---------------------------
# Files and directories

doSearch = True # Set to True to run SearchPhase.cxx

doPlotting = True # Set to True to run plotSearchPhase.py 

folderextension = "Spurious_trijet_tla_mc_hist_20160711_6p69fb_3Par"

inputFileDir = "./inputs/hist_20160711/OUT_dijetjet_tla/datalike/"

UserfileHistDict[inputFileDir+"hist.root"] = ["Zprime_mjj_var_Scaled_6p69fb"]  

HistDir = "trijet_j430_2j25"

# Turn to true if doing Spurious Signal test?
useScaled = True # Set to true if using scaled histograms instead of Datalike histograms FIXME do in limits too!? 

#---------------------------
# Analysis quantities 
Ecm = 13000.0 # Centre of mass energy in GeV

##---------------------------
# Run controls  
config = "./configurations/Step1_Spurious_3Par.config" # Path and name of config file
useBatch = False # Set to True to run SearchPhase.cxx on the batch, or set to False to run locally. runs code in batchdir
atOx = False # Set to True to use Oxford batch rather than lxbatch for running!

#----------------------------------
# ***** End of User specifies *****
#----------------------------------

#----------------------
# Preliminary steps
#----------------------

# Check inputs
if not inputFileDir.endswith("/"):
  raise SystemExit("Error: inputFileDir specified by user in Run_SearchPhase.py must end with /")

# Make directories to store outputs if they don't exist already!
directories = ["%s/LogFiles/%s/Step1_SearchPhase/CodeOutput"%(logsdir,folderextension),"%s/LogFiles/%s/Step1_SearchPhase/ConfigArchive"%(logsdir,folderextension),"./results/Step1_SearchPhase/%s"%folderextension,"%s/LogFiles/%s/Step1_SearchPhase/ScriptArchive"%(logsdir,folderextension)]

for directory in directories:
  if not os.path.exists(directory):
    os.makedirs(directory)

Step1_ScriptArchive = "%s/LogFiles/%s/Step1_SearchPhase/ScriptArchive"%(logsdir,folderextension)

fileHistDict = {}

fileHistDict = UserfileHistDict    

print "fileHistDict"
print fileHistDict    

#-------------------------------------
# Performing Step 1: Search Phase for files histogram combinations in fileHistDict using SearchPhase.cxx
#-------------------------------------

for File, HistList in fileHistDict.iteritems():
  for Hist in HistList:
    if doSearch:
      # open modified config file (fout) for writing
      fout = open("%s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config"%(logsdir,folderextension,Hist), 'w')

      # read in config file as fin and replace relevant fields with user input specified at top of this file
      with open('%s'%config, 'r') as fin:
        for line in fin:
          if (line.startswith("inputFileName") or line.startswith("dataHist") or line.startswith("outputFileName") or line.startswith("Ecm")): 
            if line.startswith("inputFileName"):
              line = "inputFileName %s\n"%File  
              fout.write(line)
            if line.startswith("dataHist"): 
              line = "dataHist %s/%s\n"%(HistDir,Hist)
              fout.write(line)
  
            if line.startswith("outputFileName"):
              line = "outputFileName %s/results/Step1_SearchPhase/%s/Step1_SearchPhase_%s.root\n"%(statspath,folderextension,Hist)
              fout.write(line)

            if line.startswith("Ecm"):
              line = "Ecm %d"%Ecm
              fout.write(line)
          else:
            fout.write(line)  
            
      fin.close()
      fout.close()
     
      # Perform search phase locally (use tee to direct output to screen and to log file)
      if (useScaled):
        #command = "SearchPhase --noDE --useScaled --config %s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config |& tee %s/LogFiles/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(logsdir,folderextension,Hist,logsdir,folderextension,Hist) # noDE option means no DataErr, uses only MCErr
        command = "SearchPhase --useScaled --config %s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config |& tee %s/LogFiles/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(logsdir,folderextension,Hist,logsdir,folderextension,Hist) # noDE option means no DataErr, uses only MCErr
      else:
        #command = "SearchPhase --noDE --config %s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config |& tee %s/LogFiles/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(logsdir,folderextension,Hist,logsdir,folderextension,Hist) # noDE option means no DataErr, uses only MCErr
        command = "SearchPhase --config %s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config |& tee %s/LogFiles/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(logsdir,folderextension,Hist,logsdir,folderextension,Hist) # noDE option means no DataErr, uses only MCErr
      print command
      # Perform setLimitsOneMassPoint locally
      if not useBatch:  
        subprocess.call(command, shell=True)
  
      # Use batch i.e. perform setLimitsOneMassPoint on the batch   
      if useBatch:
        if atOx:
          # Perform setLimitsOneMassPoint on Oxford batch
          print "Ox Batch!!"
          batchcommand = command.split("|&")[0]
          CodeOutputName = (command.split("|& tee ")[1]).split(".txt")[0] # Name of files for code output to be stored as
          print batchcommand
          
          # Open batch script as fbatchin
          fbatchin = open('./scripts/OxfordBatch/Step1_BatchScript_Template_Oxford.sh', 'r') 
          fbatchindata = fbatchin.read()
          fbatchin.close()
        
          # open modified batch script (fbatchout) for writing
          fbatchout = open('%s/Step1_BatchScript_Template_%s.sh'%(Step1_ScriptArchive,Hist),'w')
          fbatchoutdata = fbatchindata.replace("YYY",batchdir) # In batch script replace YYY for path for whole package
          fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
          fbatchoutdata = fbatchoutdata.replace("OOO",CodeOutputName) # In batch script replace OOO (i.e. std output stream) to CodeOutput directory
          fbatchoutdata = fbatchoutdata.replace("EEE",CodeOutputName) # In batch script replace EEE (i.e. output error stream) to CodeOutput directory
          fbatchout.write(fbatchoutdata)    
        
          fbatchout.close()
          subprocess.call("qsub < %s/Step1_BatchScript_Template_%s.sh"%(Step1_ScriptArchive,Hist), shell=True)

        else:
          # Perform setLimitsOneMassPoint on batch
          print "Batch!!"
          batchcommand = command.split("|&")[0]
          CodeOutputName = (command.split("|& tee ")[1]).split(".txt")[0] # Name of files for code output to be stored as
          print batchcommand
          
          # Open batch script as fbatchin
          fbatchin = open('./scripts/Step1_BatchScript_Template.sh', 'r') 
          fbatchindata = fbatchin.read()
          fbatchin.close()
          
          # open modified batch script (fbatchout) for writing
          fbatchout = open('%s/Step1_BatchScript_Template_%s.sh'%(Step1_ScriptArchive,Hist),'w')
          fbatchoutdata = fbatchindata.replace("YYY",batchdir) # In batch script replace YYY for path for whole package
          fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
          fbatchoutdata = fbatchoutdata.replace("OOO",CodeOutputName) # In batch script replace OOO (i.e. std output stream) to CodeOutput directory
          fbatchoutdata = fbatchoutdata.replace("EEE",CodeOutputName) # In batch script replace EEE (i.e. output error stream) to CodeOutput directory
          fbatchout.write(fbatchoutdata)    
      
         
          modcommand = 'chmod 744 %s/Step1_BatchScript_Template_%s.sh'%(Step1_ScriptArchive,Hist)
          print modcommand
          subprocess.call(modcommand, shell=True)
          subprocess.call("ls -l {0}".format(Step1_ScriptArchive), shell=True)
  
          fbatchout.close()
          command = "bsub -q 1nh %s/Step1_BatchScript_Template_%s.sh"%(Step1_ScriptArchive,Hist)
          print command
          subprocess.call(command, shell=True)
    
    #-------------------------------------
    # Plotting for Hists in HistList using plotSearchPhase.py
    #-------------------------------------
    
    if doPlotting:
      # Use regex to find lumi of hist
      lumi = 0
      if (re.search('_[0-9]+fb',Hist) is not None):
        lumi = re.search('_[0-9]+fb',Hist).group()
        lumi = lumi.strip("_")
        lumi = lumi.strip("fb") 
        lumi = float(lumi)*1000

      if (re.search('_[0-9]+p[0-9]+fb',Hist) is not None):
        lumi = re.search('_[0-9]+p[0-9]+fb',Hist).group()
        lumi = lumi.replace("p",".")
        lumi = lumi.strip("_")
        lumi = lumi.strip("fb") 
        lumi = float(lumi)*1000
      if lumi == 0: raise SystemExit('\n***Zero lumi*** regex issue')
      # open modified plotSearchPhase.py (fout) for writing
      fout = open('plotting/SearchPhase/plotSearchPhase_%s.py'%Hist, 'w')

      # read in plotSearchPhase as fin and replace relevant fields
      with open('./plotting/SearchPhase/plotSearchPhase.py', 'r') as fin:
        for line in fin:
          if (line.startswith("searchInputFile") or line.startswith("folderextension") or line.startswith("luminosity") or line.startswith("Ecm")): 
          
            if line.startswith("searchInputFile"):
              line = "searchInputFile = ROOT.TFile('./results/Step1_SearchPhase/%s/Step1_SearchPhase_%s.root')\n"%(folderextension,Hist)
              fout.write(line)
            if line.startswith("folderextension"): 
              line = "folderextension = './plotting/SearchPhase/plots/%s/%s/'\n"%(folderextension,Hist)
              fout.write(line)
   
            if line.startswith("luminosity"):
              line = "luminosity = %s\n"%str(lumi)
              fout.write(line)

            if line.startswith("Ecm"):
              line = "Ecm = %d\n"%(Ecm/1000) 
              fout.write(line)
          else:
            fout.write(line)  
            
      fin.close()
      fout.close()
      
      subprocess.call("python plotting/SearchPhase/plotSearchPhase_%s.py -b"%Hist, shell=True)
      os.remove("./plotting/SearchPhase/plotSearchPhase_%s.py"%Hist)



