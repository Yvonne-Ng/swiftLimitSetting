#!/bin/env python
#******************************************


print("test if this gets runs first frist!")
#perform sensitivity scan by looping over all masses on a range of luminosity values
#EXAMPLE python -u doSensitivityScan.py --config <config file> --tag <tag> --batch --debug
#based on code from Hanno
#re-written by yvonne


#******************************************
#import stuff
import sys, os, math, argparse, ROOT
import sensitivityTools
import numpy as np
import os.path
from fileNamingTool import *
import json

#def removeOldLabelledFile(spResultDir, label, mass, window, gauss):
#    """test to see if old labelled file of the mass point /window width and gaussian width is still arround, if so delete them"""
#    OldTaggedFileMayExist=True
#    i=0
#    while(OldTaggedFileMayExist and i<20):
#        try:
#            testFile=findLabelledFileName(spResultDir, label, mass , window, gauss=15)
#            #print("TaggedFileToBe ", nosignalFN)
#            #os.rename(testFile,noSignalFN)
#            #if the above returns something instead of raising an error,
#            i=i+1
#        except ValueError:
#            OldTaggedFileMayExist=False
#            print("no other duplicatedly labelled file from previous runs ")
#
#        else :
#            print ("removing this file: ", testFile)
#            os.remove(testFile)
print("test if this gets runs first!")

def createWorkTag(window, sigScale, mass):
    workTag="ww"+Window+"sigScale"+sigScale+"_mass"+mass
    return workTag

def injectionFileExist(localdir,signalScale, config, model, mass):
    """Check if the singal injected bkg file exist for this signal scale and window and mass"""
    """signalplusbackground.TrijetAprSelection.Gauss_width7.SigNum100.mjj_Gauss_sig__smooth.root"""
    injectionFile="signalplusbackground."+config["SeriesName"]+"."+model+".mass"+ mass+"."+"SigNum"+str(signalScale)+"."+config["histBasedNameSig"].format("")+".root"
    if not os.path.isdir(localdir+"/"+config["signalInjectedFileDir"]):
        print("this direcotyr is missing:", localdir+"/"+config["signalInjectedFileDir"])
        raise RuntimeError
    if injectionFile in os.listdir(localdir+"/"+config["signalInjectedFileDir"]):
        return True
    else:
        return False

def injectionFile(localdir, signalScale, config, model, mass):
    """returning the step2 output file of bkgnd data file with signal injected"""
    """signalplusbackground.TrijetAprSelection.Gauss_width7.SigNum100.mjj_Gauss_sig__smooth.root"""
    injectionFile=localdir+"/"+config["signalInjectedFileDir"]+"/"+"signalplusbackground."+config["SeriesName"]+"."+model+".mass"+mass+"."+"SigNum"+str(signalScale)+"."+config["histBasedNameSig"].format("")+".root"
    return injectionFile

def fluctuatedBkgFile(localdir, config):
    print("fluctuatedBkgFile: ", localdir+"/"+config["QCDFileDir"]+"/"+config["QCDFile"])
    return localdir+"/"+config["QCDFileDir"]+"/"+config["QCDFile"]

def spExcludeWindow(windowVector):
    excludeWindow=windowVector[0]
    excludeWindowLow=windowVector[1]
    excludeWindowHigh=windowVector[2]
    return (excludeWindow, excludeWindowLow, excludeWindowHigh)

def step2step3Run(localdir, signalScale, config, configArgs, mass, window, model):
# running step2 and step3 return whether redoing is needed
    print("check1")
    excludeWindow="redo"
    if not injectionFileExist(localdir,signalScale, config, model, mass):
        #this is the equilvalant of step02
        #generateInjectedFile(window, signalScale)
        command2="python -u step02_rewrite.py --config %s --sigScale %s --debug --model %s --mass %s"%(configArgs,signalScale, model, mass)
        print("command", command2)
        if args.debug:
            print ("command for step2: ", command2)
        try:
            os.system(command2)
            print("command step2 ran")
        except:
            print("step2 failed. aborting")
            raise RuntimeError
        if not injectionFileExist(localdir, signalScale, config, model, mass):
            print("didn't produce the correct injection file:",injectionFile(localdir, signalScale, config, model, mass) )
            raise ValueError
    else:
        print ("file already exist:",  injectionFile(localdir, signalScale, config, model, mass))
    # Now that we know the injection file exist, run step03

    # step3
    print("check2")
    step2File=injectionFile(localdir, signalScale, config, model, mass)

    command3="python step03_rewrite.py --config %s --mass %s --window %s --file %s --debug --model %s"%(configArgs, mass, window,step2File, model)
    #command3="sbatch -c 16 -p atlas_slow -t 1440 step03_rewrite.py --config {0} --mass {1} --window {2} --file {3} --debug ".format(args.config, mass, window,step2File)
    os.system(command3)

    print("check3")
    if signalScale==0:

        spFileName=searchPhaseResultNameNoSignal2(model,window, config["SeriesName"],mass)
    else:
        spFileName=searchPhaseResultName(model,mass, signalScale,window, config["SeriesName"])

    print("check3")
    spFile = ROOT.TFile(localdir+"/"+config["spResultDir"]+"/"+spFileName,'READ')

    print("check4")
    print(" does the file exsist?")
    print(os.path.isfile(localdir+"/"+config["spResultDir"]+"/"+spFileName))

    print("check5")

    print(spFile.Get('excludeWindowNums'))
    try:
        (excludeWindow, excludeWindowLow, excludeWindowHigh)=spExcludeWindow(spFile.Get('excludeWindowNums'))
    except:
        print("fit failed for spFile: ", spFileName)
        redo=True
    else:
        redo=False
    return redo, excludeWindow


def doSensitivityScan(args):
    #---------Setting local directory
    print ("calling function doSensitivityScan")
    localdir = os.path.dirname(os.path.realpath(__file__))
    #---------Open config file
    json_data = open(args.config)
    config=json.load(json_data)
    try:
        json_data = open(args.config)
        config=json.load(json_data)
    except:
        print("can't open json file. Abort.")
        raise RuntimeError
    conciseLog=open(localdir+"/log/%s.log"%(config["SeriesName"]), 'w+')
    #---------fluctuates bkg data file --using a fixed step1 file
    #signalInjectedFiles
    #for window in config["windows"]:
    # do the no signal file
    print("running no sig step3")

    print("check-1")

    removeOldLabelledFile(config["spResultDir"], "NOSIGNAL", args.mass, args.window, args.model, config["SeriesName"])
    noSignalFile=FluctuatedBkgFile(localdir, config)
    command3NoSig="python step03_rewrite.py --config %s --file %s --mass %s --window %s --model %s"%(args.config, noSignalFile, args.mass, args.window, args.model)
    print("check-2")
    #setting mass to 0 for no signal files
    os.system(command3NoSig)
    print("nosig search phase done")
    conciseLog.write("starting window%s \n"%(args.window))
    conciseLog.write("searchPhase done for no signal case \n")

    spFileNameNoSignal=searchPhaseResultNameNoSignal2(args.model, args.window, config["SeriesName"], args.mass)
    try:
        spFileNoSig = ROOT.TFile(localdir+"/"+config["spResultDir"]+"/"+spFileNameNoSignal,'READ')
    except:
        conciseLog.write("opening search phase no signal file failed \n")
        #raise RuntimeError
        sys.exit()
    try:
        (excludeWindow, excludeWindowLow, excludeWindowHigh)=spExcludeWindow(spFileNoSig.Get('excludeWindowNums'))
    except:
        conciseLog.write("Search phase no sig fitFailed, excludeWindow can't be opened \n")
        print("Search phase no sig fitFailed, excludeWindow can't be opened ")
        #raise RuntimeError
        sys.exit()
    else:
        print("search phase no sig fit sucessful")
        conciseLog.write("Search phase no sig fit sucessful \n")
    print("the excludeWindow is: ",excludeWindow)
    if excludeWindow==1:
        conciseLog.write("Search phase no sig fitFailed, excludeWindow=1 \n")
        #raise RuntimeError
        sys.exit()
    histogram=spFileNoSig.Get("basicBkgFrom4ParamFit")
    binNum=histogram.FindBin(int(args.mass))
    binContent=histogram.GetBinContent(binNum)

    # start at 1.7 sigma away from the center, assume that it's spread out in 6 bins (at least)
    startingSignalScale=np.sqrt(binContent)*1.7*6

    previousSignalScale=0
    previousSPFile=None
    print("step2")
    #for mass in config["signalMasses"]:
#using the no signal injected result, calculate a reasonable starting point

    for signalScale in config["signalScales"]:
        if signalScale<startingSignalScale:
            continue

        redo=False
        haveRedone=False
        conciseLog.write("starting with mass  %s signal Scale %s\n "%(args.mass, signalScale))
        redo, excludeWindow=step2step3Run(localdir, signalScale, config, args.config, args.mass, args.window, args.model)
        print("ran step2 and step3, exclude window=", excludeWindow)
        if redo:
            conciseLog.write("failed for signalScale: %s \n "%(signalScale))
            #conciseLog.write("failed for signalScale: %s"%(signalScale))
            print("redoing")
            print("redoing")
        redoCount=0
        while redo and redoCount<11:
           #redo step2
            conciseLog.write("signalScale: %r\n"%signalScale)
            conciseLog.write("previoussignalScale: %r\n"% previousSignalScale)
            redoSigScale=(signalScale-previousSignalScale)/2+previousSignalScale
            conciseLog.write("nextSignalScale: %r\n"% redoSigScale)
            signalScale=redoSigScale
            conciseLog.write("redoing for signalScale, %s\n"%(signalScale))
            print("redoing for signalScale, %s".format(signalScale))
            redo, excludeWindow=step2step3Run(localdir, signalScale, config, args.config, args.mass, args.window, args.model)
            if redo:
                conciseLog.write("failed for signalScale: %s\n "%(signalScale))
                print("failed for signalScale: %s".format(signalScale))
                print("redo #for mass point: ", args.mass, "signalScale: ", signalScale)
                previousSignalScale=signalScale
            redoCount=redoCount+1
            haveRedone=True

        if redo and redoCount>=11:
            conciseLog.write("Tried redoing 10 times but failed, skipping mass point:%s, window: %s, seriesName: %s\n"%(args.mass, args.window, config["SeriesName"]))
            print("Tried redoing 10 times but failed, skipping mass point:%s, window: %s, seriesName: %s"%(args.mass, args.window, config["SeriesName"]))
            break


        spFileName=searchPhaseResultName(args.model,args.mass, signalScale,args.window, config["SeriesName"])
        #spFileName=searchPhaseResultName(args.model,args.mass, signalScale,args.window, config["SeriesName"])
        spFile = ROOT.TFile(localdir+"/"+config["spResultDir"]+"/"+spFileName,'READ')

        #-----Tagging files
        #remove old tags
        spBHPValue=spFile.Get("bumpHunterStatOfFitToDataInitial")[1]
        removeOldLabelledFile(config["spResultDir"], "JUSTABOVE", args.mass, args.window, args.model, config["SeriesName"])
        removeOldLabelledFile(config["spResultDir"], "JUSTBELOW", args.mass, args.window, args.model, config["SeriesName"])
        #removeOldLabelledFile(config["spResultDir"], "NOSIGNAL", args.mass, args.window, args.model, config["SeriesName"])
        #if spBHPValue<0.01 and excludeWindow==1:
        if excludeWindow==1:
          conciseLog.write("Discovery, with window removal\n")
          print("Discovery, with window removal")
          print "just above SPFile: ", spFileName
          #---finding the justabove file
          justAboveFN=justAboveFileName(spFileName)
          conciseLog.write("just aboveSPFile: %s\n "%justAboveFN)
          os.rename(localdir+"/"+config["spResultDir"]+"/"+spFileName, localdir+"/"+config["spResultDir"]+"/"+justAboveFN)
          print("Search phase BH p value: ", spBHPValue)
          if previousSPFile==None:
              conciselog.write("window: %r, mass: %r, signalscale: %r need to start at a lower signal scale\n"%(args.window, args.mass, signalscale))
              print("window: %r, mass: %r, signalscale: %r need to start at a lower signal scale"%(args.window, args.mass, signalscale))


              #skipping the mass point
              break
          else:# if previousSP file is not none
          #----finding the just below file name
              justBelowFN=justBelowFileName(previousSPFile)
              conciseLog.write("just belowSPFile: %s\n "%justBelowFN)
              conciseLog.write("next mass point!")
              os.rename(localdir+"/"+config["spResultDir"]+"/"+previousSPFile,localdir+"/"+config["spResultDir"]+"/"+justBelowFN)
              break #going to the next mass point
        else: #if exclusion of widnow didn't happen
          if haveRedone:
              conciseLog.write("skipping mass point %s, window: %s\n "%(args.mass, args.window))
              conciseLog.write("skipping mass point %s, window: %s"%(args.mass, args.window))
              print("need to add in more points after signalScale: %s"%(signalScale))
              print("need to add in more points after signalScale: %s"%(signalScale))
              break

          previousSPFile=spFileName
          print("window: %r, mass: %r, signalScale: %r No exclusion yet."%(args.window, args.mass, signalScale))
          print("Search phase BH p value: ", spBHPValue)

          #TODO:
          # fix the signal injection scale increments
          # write out all the missiong function defined above
          # run to test plotting results
          #beautifing:
          # remove step1 step2 and step3 and turn them into functions
          previousSignalScale=signalScale

if __name__ == '__main__':
    print("starting of doSensitivity_rewrite.y")
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('--config', dest='config', default='../configs/sensitivityScan.Test.config', required=True, help='sensitivity scan config file')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--model', '--model', dest='model', default="Gauss_width15", help='model')
    parser.add_argument('--signalMass', '--signalMass', dest='mass', help='mass')
    parser.add_argument('--window', '--window', dest='window', help='window')

    args = parser.parse_args()
    doSensitivityScan(args)
