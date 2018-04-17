import sys
import os
import subprocess


## User controlled ##

# 2016 data
fitFile = "lookInsideTheBoxNowWithNoTG3.root"
fitHistogram = "Nominal/DSJ100yStar06_TriggerJets_J100_yStar06_mjj_noTG3Scale_2016binning_TLArange_data"
lowEstimate = 530
highEstimate = 2081
highFit = 7500

# 2015 data
#fitFile = "/cluster/warehouse/kpachal/StatisticalAnalysis/samples/TLA2017_validateWith2015/SearchResultData_caseD_window13.root"
#fitHistogram = "basicData"
#lowEstimate = 440
#highEstimate = 1236
#highFit = 7500
#outDir = "results/data2015/%s/"%workTag

### Common

useBatch = False
templatescript = "scripts/batchScript_template.sh"

saveOutput = True

doAlternate = False

permitWindow = False

nPseudoExp = 1000

## Automatic ##
# stdout_redirect = "1>> results/data2017/validateSWIFT/output_{4}"

# Get current working directory
statspath = os.getcwd() # path used in outputFileName in config
headdir = statspath.split("/Bayesian")[0] # directory for whole package

#def batchSubmit(command,stringForNaming) :
#
#  # Perform setLimitsOneMassPoint on batch
#  batchcommand = command.split("|&")[0]
#  print batchcommand
#
#  # Open batch script as fbatchin
#  fbatchin = open(templatescript, 'r')
#  fbatchindata = fbatchin.read()
#  fbatchin.close()
#
#  # open modified batch script (fbatchout) for writing
#  batchtempname = '{0}/Step1_BatchScript_Template_SearchPhase_{1}.sh'.format(scriptArchive,stringForNaming)
#  fbatchout = open(batchtempname,'w')
#  fbatchoutdata = fbatchindata.replace("YYY",headdir) # In batch script replace YYY for path for whole package
#  fbatchoutdata = fbatchoutdata.replace("ZZZ",batchcommand) # In batch script replace ZZZ for submit command
#  fbatchout.write(fbatchoutdata)
#  modcommand = 'chmod 744 {0}'.format(batchtempname)
#  subprocess.call(modcommand, shell=True)
#  fbatchout.close()
#  submitcommand = "qsub {0}".format(batchtempname)
#  print submitcommand
#  subprocess.call(submitcommand, shell=True)
#
for case in ["5Param","4Param","UA2"]: #["A","B","C","D"] : #["UA2", "4Param", "5Param", "5ParamUA2Log"]
 for windowWidth in ["13", "12", "11", "10", "9"]: #[7,10,13,17] :
     
   workTag = "unblindingJ100yStar06_ww"+windowWidth+"_"+case
   outDir = "results/%s/"%workTag

   commandTemplate = "SearchPhase --config {0} --file {1} --histName {2} --noDE --outputfile {3}SearchResultData_{4}.root ".format("{0}",fitFile,fitHistogram,outDir,"{1}")

   scriptArchive = "submitConfigs/%s/"%workTag
   for directory in [outDir,scriptArchive]:
     if not os.path.exists(directory): os.makedirs(directory)
  
   
   for doSwift in [True] : #True] :

    configInName = "configurations/Step1_SearchPhase_Swift.config"
    configOutName = "submitConfigs/"+workTag+"/Step1_SearchPhase_case{0}_window{1}.config".format(case,windowWidth)
    configOut = open(configOutName,'w')
    with open(configInName) as configInData :
      for line in configInData :
        if "doSwift" in line:
          if (doSwift) :
            line = "doSwift true\n" 
          else :
            line = "doSwift false\n"
        if "minXForFit" in line :
          line = "minXForFit   {0}\n".format(lowEstimate)
        if "maxXForFit" in line :
          line = "maxXForFit   {0}\n".format(highEstimate)
        if "swift_minXAvailable"  in line :
          line = "swift_minXAvailable   {0}\n".format(lowEstimate)
        if "swift_maxXAvailable"  in line :
          line = "swift_maxXAvailable   {0}\n".format(highFit)
#        if "inputHistDir"  in line and fitHistogram == "mjj" :
#          continue
     
        if doAlternate and "doAlternateFunction" in line :
          line = "doAlternateFunction  true\n"
        if permitWindow and "permitWindow" in line :
          line = "permitWindow  true\n"
        if "nPseudoExp" in line :
          line = "nPseudoExp  {0}\n".format(nPseudoExp)
 
        if "swift_nBinsLeft" in line :
          line = "swift_nBinsLeft  {0}\n".format(windowWidth)
        elif "swift_nBinsRight" in line :
          line = "swift_nBinsRight  {0}\n".format(windowWidth)
        if "4Param" in case :
          if "swift_fixLow" in line :
            line = "swift_fixLow  true\n"
          if "swift_fixHigh" in line :
            line = "swift_fixHigh  true\n"
          if "swift_truncateHigh" in line :
            line = "swift_truncateHigh       false\n"
          if "functionCode" in line : 
            line = "functionCode  4\n"
          if "nParameters" in line : 
            line = "nParameters  4\n"
          if "alternateFunctionCode" in line : 
            line = "alternateFunctionCode  4\n"
          if "alternateNParameters" in line : 
            line = "alternateNParameters  4\n"

        if "UA2" in case :
          if "swift_fixLow" in line :
            line = "swift_fixLow  true\n"
          if "swift_fixHigh" in line :
            line = "swift_fixHigh  true\n"
          if "swift_truncateHigh" in line :
            line = "swift_truncateHigh       false\n"
          if "functionCode" in line : 
            line = "functionCode  1\n"
          if "nParameters" in line : 
            line = "nParameters  4\n"
          if "alternateFunctionCode" in line : 
            line = "alternateFunctionCode  1\n"
          if "alternateNParameters" in line : 
            line = "alternateNParameters  4\n"

        if "5Param" in case :
          if "swift_fixLow" in line :
            line = "swift_fixLow  true\n"
          if "swift_fixHigh" in line :
            line = "swift_fixHigh  true\n"
          if "swift_truncateHigh" in line :
            line = "swift_truncateHigh       false\n"
          if "functionCode" in line : 
            line = "functionCode  7\n"
          if "nParameters" in line : 
            line = "nParameters  5\n"
          if "alternateFunctionCode" in line : 
            line = "alternateFunctionCode  7\n"
          if "alternateNParameters" in line : 
            line = "alternateNParameters  5\n"

        if "5ParamUA2Log" in case :
          if "swift_fixLow" in line :
            line = "swift_fixLow  true\n"
          if "swift_fixHigh" in line :
            line = "swift_fixHigh  true\n"
          if "swift_truncateHigh" in line :
            line = "swift_truncateHigh       false\n"
          if "functionCode" in line : 
            line = "functionCode  24\n"
          if "nParameters" in line : 
            line = "nParameters  5\n"
          if "alternateFunctionCode" in line : 
            line = "alternateFunctionCode  24\n"
          if "alternateNParameters" in line : 
            line = "alternateNParameters  5\n"

        configOut.write(line)
    configOut.close()

    modcommand = "chmod 744 {0}".format(configOutName)
    subprocess.call(modcommand,shell=True)

    extraString = "case{0}_window{1}".format(case,windowWidth)
    if (doSwift) :  extraString = extraString + "_doSwift"
    else : extraString = extraString + "_noSwift"
    thisCommand = commandTemplate.format(configOutName,extraString)

    if useBatch :
      batchSubmit(thisCommand,extraString)
    else :
      if saveOutput :
        print thisCommand + "| tee "+outDir+"/"+workTag+"_log.txt \n"
      else :
        print thisCommand+"\n"



      #subprocess.call(thisCommand,shell=True)
