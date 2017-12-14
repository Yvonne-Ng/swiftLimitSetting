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
# - plotSearchPhase_gjj.py to plot results of SearchPhase.cxx

# Note:To change fit parameters, mjj cut (minXForFit) and other things, do this in Step1_SearchPhase.config!
# All log files stored 1 directory up in LogFiles directory, unless otherwise specified
# *****************

statspath = os.getcwd() # path used in outputFileName in config 
headdir = statspath.split("/Bayesian")[0] # directory for whole package 
logsdir = headdir # Log Files Sent Here
batchdir = logsdir+"/StatisticalAnalysis" #headdir # Folder to be copyied to batch, by default headdir unless otherwise specified 
UserfileHistDict = {}

print "\n================================================"
print "System Paths"
print "(will be used to set up output directories locally)"
print "================================================"
print "statspath  : ",statspath
print "headdir    : ",headdir  
print "logsdir    : ",logsdir  
print "batchdir   : ",batchdir 


#---------------------------
# ***** User specifies *****
#---------------------------

#---------------------------
# Files and directories

# Set to True to run SearchPhase.cxx
doSearch = True

# Set to True to run plotSearchPhase_gjj.py 
doPlotting = False 

# Where the results will end up - for archives and checking
folderextension = "RedoMCwithCutNoScaledijetgamma_g85_2j65"

# Location of input root files that contain the histograms for fitting
inputFileDir = "../../../inputs/hist_20160801/OUT_dijetgamma_mc/datalike-noNeff/"

# Within the "inputFileDir" this is the name of the root file along with the spectra that you want to fit
UserfileHistDict[inputFileDir+"hist2.root"] = ["Zprime_mjj_var_Scaled_20p00fb"] 

# The TDirectory within the TFile where the histogram in the previous dictionary exists
HistDir = "dijetgamma_g130_2j25"

# Turn to true if doing Spurious Signal test!
# Set to true if using scaled histograms instead of Datalike histograms
useScaled = True

# Analysis quantities 
Ecm = 13000.0 # Centre of mass energy in GeV

# initial default config file - will be overwritten by user inputs if specified
config = "./configurations/Step1_SearchPhaseNoSyst_gjj_4Par.config" # Path and name of config file

# Set to True to run SearchPhase.cxx on the batch, or set to False to run locally 
# runs code in batchdir - (SAM) which type of batch system? lxbatch?
useBatch = False 

# Set to True to specifically use the Oxford batch system
atOx = False 

print "\n================================================"
print "User inputs"
print "(You should have changed these)"
print "================================================"
print "doSearch          : ",doSearch
print "doPlotting        : ",doPlotting
print "folderextension   : ",folderextension
print "inputFileDir      : ",inputFileDir
print "UserfileHistDict  : ",UserfileHistDict
print "HistDir           : ",HistDir
print "useScaled         : ",useScaled
print "Ecm               : ",Ecm
print "config            : ",config
print "useBatch          : ",useBatch
print "atOx              : ",atOx


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
print "\n================================================"
print "Creating run directories"
print "================================================"
directories = []
directories.append("%s/LogFiles/%s/Step1_SearchPhase/CodeOutput"%(logsdir,folderextension))
directories.append("%s/LogFiles/%s/Step1_SearchPhase/ConfigArchive"%(logsdir,folderextension))
directories.append("./results/Step1_SearchPhase/%s"%folderextension)
directories.append("%s/LogFiles/%s/Step1_SearchPhase/ScriptArchive"%(logsdir,folderextension))

for directory in directories:
  if not os.path.exists(directory):
    print "Directory (creating): ",directory
    os.makedirs(directory)
  else:
    print "Directory (exists):   ",directory

# only for batch running
Step1_ScriptArchive = "%s/LogFiles/%s/Step1_SearchPhase/ScriptArchive"%(logsdir,folderextension)

fileHistDict = {}
fileHistDict = UserfileHistDict    

print "\n================================================"
print "fileHistDict"
print "================================================"
print fileHistDict    

#-------------------------------------
# Performing Step 1: Search Phase for files histogram combinations in fileHistDict using 
# Bayesian/util/SearchPhase.cxx
# changes to SearchPhase require recompilation and installation
#-------------------------------------

for File, HistList in fileHistDict.iteritems():
  print "\n================================================"
  print "Running new hist"
  print "================================================"
  print "FilePath : ",File
  print "HistList : ",HistList
  for Hist in HistList:

    if doSearch:
    
      print "\n================================================"
      print "Creating new config file"
      print "(This is what will be fed to fitting/BumpHunter)"
      print "================================================"
      print "ConfigIn  : ",config
      name_fout = "%s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config"%(logsdir,folderextension,Hist)
      print "ConfigOut : ",name_fout
      fout = open(name_fout, 'w')

      # read in config file as fin and replace relevant fields with user input specified at top of this file
      with open('%s'%config, 'r') as fin:
        for line in fin:
          if line.startswith("inputFileName"):
            line = "inputFileName %s\n"%File  
            fout.write(line)
            print "Replaced (inputFileName) : ",line.strip()
          elif line.startswith("dataHist"): 
            line = "dataHist %s/%s\n"%(HistDir,Hist)
            fout.write(line)
            print "Replaced (dataHist) : ",line.strip()
          elif line.startswith("outputFileName"):
            line = "outputFileName %s/results/Step1_SearchPhase/%s/Step1_SearchPhase_%s.root\n"%(statspath,folderextension,Hist)
            fout.write(line)
            print "Replaced (outputFileName) : ",line.strip()
          elif line.startswith("Ecm"):
            line = "Ecm %d"%Ecm
            fout.write(line)
            print "Replaced (Ecm) : ",line.strip()
          else:
            fout.write(line)  
            
      fin.close()
      fout.close()
      
     
      # Perform search phase locally (use tee to direct output to screen and to log file)
      print "\n================================================"
      print "Preparing to run SearchPhase command"
      print "================================================"

      command="SearchPhase --useScaled --config %s/LogFiles/%s/Step1_SearchPhase/ConfigArchive/Step1_%s.config |& tee %s/LogFiles/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(logsdir,folderextension,Hist,logsdir,folderextension,Hist) # noDE option means no DataErr, uses only MCErr
      if not useScaled:
        command = command.replace("--useScaled","")

      print "Command : ",command
      # Perform setLimitsOneMassPoint locally
      print "Using Batch? : ",useBatch
      
      if not useBatch:  
        subprocess.call(command, shell=True)
  
      break
  
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
    # Plotting for Hists in HistList using plotSearchPhase_gjj.py
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
    #Yvonne hard set of the luminosity
      lumi = 36.09
      #if lumi == 0: raise SystemExit('\n***Zero lumi*** regex issue')
      # open modified plotSearchPhase_gjj.py (fout) for writing
      fout = open('plotting/SearchPhase/plotSearchPhase_gjj_%s.py'%Hist, 'w')

      # read in plotSearchPhase_gjj as fin and replace relevant fields
      with open('./plotting/SearchPhase/plotSearchPhase_gjj.py', 'r') as fin:
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
      
      subprocess.call("python plotting/SearchPhase/plotSearchPhase_gjj_%s.py -b"%Hist, shell=True)
      os.remove("./plotting/SearchPhase/plotSearchPhase_gjj_%s.py"%Hist)



