#!/bin/python
#---step01 result file name
import os

#---step02 result file name
def signalPlusBkgFileName(localdir, model, slumi,  nPar, seed, tag,signalName="mjj_Gauss_sig__smooth"):
    """File naming the result of step02"""
    signalPlusBackgroundFileName = localdir+'/../results2/signalplusbackground/signalplusbackground.'+model+'.'+slumi+'.ifb.'+"mjj_Gauss_sig__smooth"+'.%i'%nPar+'.par.%i'%seed+'.seed.'+tag+'.root'
    print("signalPlusBackgroundFileName: ", signalPlusBackgroundFileName)
    return signalPlusBackgroundFileName

#---step03 results file name
def searchPhaseResultName(localdir, model, mass, slumi,histName, nPar, seed, tag,windowwidth):
    """File Naming the result of step03"""
    outFileName = localdir+'/../results2/searchphase/searchphase.'+model+'.%i'%int(mass)+'.gev.'+slumi+'.ifb.'+histName+'.%i'%nPar+'.par.%i'%seed+'.seed.'+tag+'_ww'+str(windowwidth)+'.root'
    return outFileName

#----naming the just above/ just below, no signal search phase result file name or each mass point and window
def justAboveFileName(fileName):
    """naming the just above"""
    return fileName[:-5]+"_JUSTABOVE"+".root"

def justBelowFileName(fileName):
    """naming the just above"""
    return fileName[:-5]+"_JUSTBELOW"+".root"

def zeroLumiFileName(fileNameTemplate):
    """returning 0.0 xS of signal inject  SP flle Name (basically equivalent to background only), using fileNameTemplate of other luminosity(XS) """
    pos0=fileNameTemplate.find("gev") #start at gaussian width
    pos1=fileNameTemplate[pos0:].find(".")+pos0 # the next . after "Gassuainwidth" string, beginning of xpx
    pos_0=pos1+1 #+1 for length of "." # staring position of xpx
    pos_1=pos_0+fileNameTemplate[pos_0:].find(".") # find the end position of xpx
    fileName=fileNameTemplate[:pos_0]+"0p0"+fileNameTemplate[pos_1:]
    fileName=str(fileName)
    print fileName
    return fileName

def findDirFromFilePath(fileName):
    """supply a absolute file path, return the directory of where it file resides"""
    print("total filename: ", fileName)
    reverseFileName=fileName[::-1]
    reversePos=reverseFileName.find("/")
    stringlength=len(fileName)
    pos=stringlength-reversePos
    dirName=fileName[:pos]
    print(dirName)
    return dirName

def noSignalFileName(fileName):
    """naming the no signal file name """
    print ("noSignal filenmae : ", fileName)
    return fileName[:-5]+"_NOSIGNAL"+".root"

def countFilesInDirWithKeyword(directory, keyword):
    count=0
    for f in os.listdir(directory):
        if keyword in f:
            count=count+1
    return count

def findLabelledFileName(SPFileDir, label, mass, windowWidth):

    """Finding of a justAbove/justBelow/Nosignal fileName  FileName of a particular mass point/ window Width, if the file doesn't exist return ValueError  """

    print ("Directory:", SPFileDir)
    if label not in ["JUSTABOVE", "JUSTBELOW", "NOSIGNAL"]:
        print("ERROR, wrong tag: ", label)
        print("label need to be JUSTABOVE, JUSTBELOW or NOSIGNAL")
        raise ValueError
    massString=str(mass)
    windowString="ww"+str(windowWidth)
    for fileName in os.listdir(SPFileDir):
        if massString in fileName and  windowString in fileName and label in fileName: #finding the fileName of the right window and mass point with the right label
            print (label, ": ", fileName)
            return SPFileDir+"/"+fileName
    print "file not found, FileName: ", fileName
    raise ValueError
