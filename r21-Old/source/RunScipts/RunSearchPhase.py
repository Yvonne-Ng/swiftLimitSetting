import argparse 
import yaml
import sys
import os
from os.path import basename, expanduser
import json
import shutil
import subprocess

def argParser():
    parser = argparse.ArgumentParser(description="script to either run search phase or draw result from search phase")
    parser.add_argument('--config', type=str, default="/lustre/SCRATCH/atlas/ywng/r21/r21Rebuild/r21StatisticalAnalysis/source/Configurations/SearchPhase_test.json", help="set the configuration file")
    parser.add_argument("--action", type=str, default="run", help="either \"run\" or \"draw\"")
    args = parser.parse_args()
    return args

def setPaths(): #ALL PATHS ARE SET RELATIVE TO THE THE CURRENT DIRECTORY
    runPath = os.getcwd()#current path where the run files are 
    headPath = runPath.split("/RunScipts")[0] 
    archivePath = headPath+"/LogFiles"
    batchPath = headPath+"/BatchOuput" 
    return runPath, headPath, archivePath, batchPath

def checkPath(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

def check_key(tag, dict_obj, key): # checking key for the yaml config
  if key not in dict_obj:
    die(tag + " does not contain '" + key + "' key.")

def logFileNameMake(jsonConfig,archivePath):
    pathL1=archivePath+"/%s/"%(jsonConfig["configName"])
    pathL2=pathL1+"/Step1_SearchPhase/"
    pathL3=pathL2+"/CodeOutput/"
    checkPath([pathL1, pathL2, pathL3])
    logFile=archivePath+"/%s/Step1_SearchPhase/CodeOutput/Step1_%s.txt"%(jsonConfig["configName"],jsonConfig["inputHisto"])
    print("Log file saved to: ", logFile)
    return logFile

def configFileCopy(config, jsonConfig, archivePath):
    pathL1=archivePath+"/%s/"%(jsonConfig["configName"])
    pathL2=pathL1+"/Step1_SearchPhase/"
    pathL3=pathL2+"/ConfigArchive/"
    copyFile="Step1_%s.txt"%(jsonConfig["inputHisto"])
    checkPath([pathL1, pathL2, pathL3])
    print("config archive file saved to: ", pathL3+copyFile)
    shutil.copy(config, pathL3+copyFile) #making a copy
    return pathL3+copyFile

def scriptArchiveFileMake(config, jsonConfig, archivePath):
    pathL1=archivePath+"/%s/"%(jsonConfig["configName"])
    pathL2=pathL1+"/Step1_SearchPhase/"
    pathL3=pathL2+"/SciptArchive/"
    copyFile="Step1_%s.txt"%(jsonConfig["inputHisto"])
    checkPath([pathL1, pathL2, pathL3])
    print("script archive file saved to: ", pathL3+copyFile)
    shutil.copy(config, pathL3+copyFile) #making a copy
    return pathL3+copyFile
    

def commandBuilding(action, logFile, configFile):
    with open (configFile) as datafile:
        jsonConfig = json.load(datafile) #use meaningful config names 
        if action=="run":
            command="SearchPhase "
            if jsonConfig["useScale"]:
                command+="--useScaled "
            command +="--config "+configFile+" "
            command +="|& tee " + logFile 
        if action=="draw":
            pass
    print("Command: ", command)
    return command 
    
#---making an argument parser
args=argParser()
#---setting paths
runPath, headPath, archivePath, batchPath=setPaths()
#---checking if the path actually exist 
checkPath([runPath,headPath,archivePath,batchPath])

#----opening the yaml file 
'''
with open(args.config, 'r') as f: yamlConf = yaml.load(f)
check_key("yaml config"+args.config, yamlConf, "inputRootDir")
inputRootDir = yamlConf['inputRootDir']
print (inputRootDir)
''' 
#----opening the json config file
with open (args.config) as datafile:
    jsonConfig = json.load(datafile) #use meaningful config names 


#---making a logFile 
logFile=logFileNameMake(jsonConfig, archivePath)

#-- making a config file copy
configFile=configFileCopy(args.config,jsonConfig, archivePath)

#----Making SearchPhase run command 
command=commandBuilding(args.action, logFile, args.config)

#---Batch run or local run?
if jsonConfig["useGPBatch"]:
    command=command.split("|& tee ")[0]
    batchTemplate=open('./scripts/Step1_BatchScript_Template.sh', 'r') 
    
    batchContent = batchTemplate.read()
    batchTemplate.close()

    batchContent=batchContent.replace("YYY",batchPath)
    batchContent=batchContent.replace("ZZZ", command)
    
    sciptArch=scriptArchiveFileMake(config, jsonConfig, archivePath)
    batchOutput=open("%s/Step1_BatchScript_Template_%s.sh"%(scriptArch, jsonConfig["inputHisto"]), "w")
    batchOutput.write(batchContent)
    pass
else:
    subprocess.call(command, shell=True)
