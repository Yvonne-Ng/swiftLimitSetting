#!/usr/bin/env python
#####################################################################################################
# ChopTails.py
#
# This script chops signals to match fit range
#
#####################################################################################################

import ROOT, glob, os, time

################## Grab Signal Files ########################

signalFiles = glob.glob("./ZPrime*.root");
if len(signalFiles) == 0:
  print "ERROR, we found no potential "+args.signalType+" files in "+args.path
  exit(0)

################## Loop over signal files ########################

for signalFileName in signalFiles:

  print "Using Signal File: "+signalFileName

  signalFile = ROOT.TFile.Open(signalFileName, "READ")

  choppedFile = ROOT.TFile.Open('./'+os.path.basename(signalFileName).replace("ZPrime", 'Chopped_ZPrime'), "RECREATE")

  ################## Loop over directories in Dirs ########################

  hists = signalFile.GetListOfKeys()

  for hist in hists:

    histName = hist.GetName()

    #if "Nominal" not in histName:continue

    print "Signal", histName

    thisSignalHist = signalFile.Get(histName)
 
    ChoppedSignalHist = thisSignalHist.Clone()

    #firstBin = ChoppedSignalHist.GetXaxis().FindBin(272)
    print "Chopping 303 - 611, is this what you want?"
    firstBin = ChoppedSignalHist.GetXaxis().FindBin(303)
    lastBin = ChoppedSignalHist.GetXaxis().FindBin(611)

    # Chop Signal hist i.e. set bins and error to zero if out of fit range
    for bin in range(ChoppedSignalHist.GetNbinsX()+2) :
      if (bin < firstBin) or (bin > (lastBin-1)):
        #print "CHOPPING"
        ChoppedSignalHist.SetBinContent(bin,0) 
        ChoppedSignalHist.SetBinError(bin,0) 

    choppedFile.cd()
    ChoppedSignalHist.Write()
    signalFile.cd()

  choppedFile.Close()  
  signalFile.Close()


