#!/usr/bin/env python

# Basic imports
import time
import os
import subprocess
import ROOT

statspath = os.getcwd() # path used in outputFileName in config 
headdir = statspath.split("/Bayesian")[0] # directory for whole package 
logsdir = headdir # Log Files Sent Here
batchdir =logsdir+"/StatisticalAnalysis" #headdir # Folder to be copyied to batch, by default headdir unless otherwise specified 
starttime = time.time()

# *****************
#---------------------------
# ***** User specifies *****
#---------------------------

#---------------------------
# Files and directories

# NOTE RUNNING WITH DIJET RESOLUTION FOR RESOLUTION CURVE -> Actually a functional form so approx models resolution at low masses*

doGaussianLimits = False # Set to True to run doGaussianLimits.cxx

doPlotting = True # Set to True to run plotGaussians_gjj.py 

lumis = ['15p45']

ratios = [-1,0.07,0.10,0.15] # -1 is resolution width!

subranges = [[350,450],[450,550],[550,650],[650,750],[750,850],[850,950],[950,1050],[1050,1150],[1150,1250],[1250,1350],[1350,1450]]

plotextension = "test"

doISRAccErr = False # Set to True to use Photon Acceptance Error 
ISRErrSize = 0.03 

##---------------------------
# Run controls 
 
config = 'configurations/Step4_GenericGaussians_gjj.config'

useBatch = False
templatescript = './scripts/OxfordBatch/Step2_BatchScript_Template_Oxford.sh'

#templatefile = "%s/Bayesian/results/Step1_SearchPhase/dijetgamma_data_hist_20160727_15p45fb_4Par_169_1493/Step1_SearchPhase_Zprime_mjj_var_DataLike_LLLfb.root"%headdir
templatefile = "/lustre/SCRATCH/atlas/ywng/r21/r21-Old/source/Bayesian/results/Step1_SearchPhase/test/Step1_SearchPhase_Zprime_mjj_var.root"


JESFile = "" # No longer needed as using flat JES %s/Bayesian/inputs/JESshifts/QStarJESShifts1invfbJES1Component3_1SigmaDown.root"%headdir 

#----------------------------------
# ***** End of User specifies *****
#----------------------------------

#----------------------
# Preliminary steps
#----------------------

resultsdir = "%s/Bayesian/results/Step4_GaussianLimits/%s/"%(headdir,plotextension)

#if not useBatch :
#  resultsdir = resultsdir + "interactive/"

# Make directories to store outputs if they don't exist already!
ConfigArchive = "{0}/LogFiles/{1}/Gaussians/ConfigArchive".format(logsdir,plotextension)
ScriptArchive = "{0}/LogFiles/{1}/Gaussians/ScriptArchive".format(logsdir,plotextension)
CodeOutput = "{0}/LogFiles/{1}/Gaussians/CodeOutput".format(logsdir,plotextension)

directories = [resultsdir,ConfigArchive,ScriptArchive,CodeOutput]#,BATplotDirectory]
for directory in directories:
  if not os.path.exists(directory):
    os.makedirs(directory)

# Functions
def batchSubmit(command, ratio=-1) :

  # Perform setLimitsOneMassPoint on batch
  batchcommand = command.split("|&")[0]
  CodeOutputName = (command.split("|& tee ")[1]).split(".txt")[0] # Name of files for code output to be stored as
  print batchcommand
          
  # Open batch script as fbatchin
  fbatchin = open(templatescript, 'r') 
  fbatchindata = fbatchin.read()
  fbatchin.close()
          
  # open modified batch script (fbatchout) for writing
  if ratio < 0 :
    batchtempname = '{0}/Gaussian_BatchScript_Template_{1}fb_resolution_{2}.sh'.format(ScriptArchive,lumi,subrange[0])
  else :
    batchtempname = '{0}/Gaussian_BatchScript_Template_{1}fb_r{2}_{3}.sh'.format(ScriptArchive,lumi,int(100*ratio),subrange[0])
  fbatchout = open(batchtempname,'w')
  fbatchoutdata = fbatchindata.replace("YYY",batchdir) # In batch script replace YYY for path for whole package
  fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
  fbatchoutdata = fbatchoutdata.replace("OOO",CodeOutputName) # In batch script replace OOO (i.e. std output stream) to CodeOutput directory
  fbatchoutdata = fbatchoutdata.replace("EEE",CodeOutputName) # In batch script replace EEE (i.e. output error stream) to CodeOutput directory
  fbatchout.write(fbatchoutdata)    
  modcommand = 'chmod 744 {0}'.format(batchtempname)
  subprocess.call(modcommand, shell=True)
  fbatchout.close()
  submitcommand = "qsub {0}".format(batchtempname)
  print submitcommand
  subprocess.call(submitcommand, shell=True)


#-------------------------------------
# Performing Step 2: Limit setting for each model, mass, lumi combo using setLimitsOneMassPoint.cxx
#-------------------------------------

if doGaussianLimits:
  for lumi in lumis :

    # open modified config file (fout) for writing
    fout = open('{0}/Gaussians_{1}fb.config'.format(ConfigArchive,lumi), 'w')

    # read in config file as fin and replace relevat fields with user inout specified at top of this file
    with open(config, 'r') as fin:
      for line in fin:
        if line.startswith("inputFileName"):
          thefile = templatefile.replace("LLL",lumi)
          line = "inputFileName {0}\n".format(thefile)
          fout.write(line)
        elif line.startswith("outputFileName"):
          theoutfile = resultsdir+"GenericGaussians_{0}\n".format(lumi)
          line = "outputFileName {0}\n".format(theoutfile)
          fout.write(line)
        elif line.startswith("plotDirectory"):
          line = "plotDirectory {0}/\n".format(BATplotDirectory)
          fout.write(line)
        else:
          fout.write(line)
      fout.write("JESFile {0}\n".format(JESFile))
    fin.close()
    fout.close()

    for subrange in subranges :
      for ratio in ratios :

        # Setting command to be submitted (use tee to direc output to screen and to log file)
        if ratio > 0.0:
          if doISRAccErr:
            command = "doGaussianLimits --config {0}/Gaussians_{1}fb.config --ratio {2} --rangelow {3} --rangehigh {4} --ISRAccErr {5} |& tee {6}/Gaussians_{1}_{2}_{3}_{4}_fb.txt".format(ConfigArchive,lumi,ratio,subrange[0],subrange[1],ISRErrSize,CodeOutput)
          else:
            command = "doGaussianLimits --config {0}/Gaussians_{1}fb.config --ratio {2} --rangelow {3} --rangehigh {4} |& tee {5}/Gaussians_{1}_{2}_{3}_{4}_fb.txt".format(ConfigArchive,lumi,ratio,subrange[0],subrange[1],CodeOutput)
        else:
          if doISRAccErr:
            command = "doGaussianLimits --config {0}/Gaussians_{1}fb.config --ratio {2} --useresolutionwidth --rangelow {3} --rangehigh {4} --ISRAccErr {5} |& tee {6}/Gaussians_{1}_{2}_{3}_{4}_fb.txt".format(ConfigArchive,lumi,ratio,subrange[0],subrange[1],ISRErrSize,CodeOutput)
          else:
            command = "doGaussianLimits --config {0}/Gaussians_{1}fb.config --ratio {2} --useresolutionwidth --rangelow {3} --rangehigh {4} |& tee {5}/Gaussians_{1}_{2}_{3}_{4}_fb.txt".format(ConfigArchive,lumi,ratio,subrange[0],subrange[1],CodeOutput)
        print command

        # Perform setLimitsOneMassPoint locally
        if not useBatch:  
          subprocess.call(command, shell=True)
  
        # Use batch i.e. perform setLimitsOneMassPoint on the batch   
        if useBatch:
  
          # Perform setLimitsOneMassPoint on batch
          batchSubmit(command,ratio)
  


#-------------------------------------
# Plotting results of running doGaussianLimits.cxx using plotGaussians_gjj.py
#-------------------------------------
    
if doPlotting:

  for lumi in lumis :
    if "p" in lumi: # converting to pb
      Lumi = lumi.replace("p",".")
      Lumi = float(Lumi)*1000
    else: # converting to pb
      Lumi = float(lumi)*1000

    # open modified plotGaussians_gjj.py (fout) for writing
    fout = open('plotting/LimitSettingPhase/plotGaussians_gjj_%sfb.py'%(lumi), 'w')

    # read in plotGaussians_gjj fin
    with open('./plotting/LimitSettingPhase/plotGaussians_gjj.py', 'r') as fin:
      for line in fin:
        if (line.startswith("luminosity") or line.startswith("subranges") or line.startswith("folderextension") or line.startswith("basicInputFileTemplate")): 
              
          if line.startswith("luminosity"):
            line = "luminosity = %d\n"%Lumi
            fout.write(line)
          if line.startswith("subranges"):
            line = "subranges = %s\n"%(str(subranges))
            fout.write(line)
          if line.startswith("folderextension"): 
            line = "folderextension = './plotting/LimitSettingPhase/plots/%s/%s/'\n"%(plotextension,lumi)
            fout.write(line)
          if line.startswith("basicInputFileTemplate"): 
            line = "basicInputFileTemplate = './results/Step4_GaussianLimits/%s/GenericGaussians_%s_low{0}_high{1}_{2}.root'\n"%(plotextension,lumi)
            fout.write(line)
        else:
          fout.write(line)  
    fin.close()
    fout.close()

    # do plotting locally
    subprocess.call("python plotting/LimitSettingPhase/plotGaussians_gjj_%sfb.py -b"%(lumi), shell=True)
    os.remove("./plotting/LimitSettingPhase/plotGaussians_gjj_%sfb.py"%(lumi)) # Remove modified plotGaussians_gjj after plotting

print "Done."
