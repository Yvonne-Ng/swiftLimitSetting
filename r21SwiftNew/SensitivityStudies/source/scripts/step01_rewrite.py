#!/bin/python
from ROOT import TFile, TH1F,TCanvas
import ROOT
import argparse
from random import *
import numpy as np

def scaleHist(histName, initialfb, desiredfb):
    pass
    #return scaledHistogram

def fluctuateHist(initHist, histName, seed):
    # fluctuate histogram
    ROOT.gROOT.SetBatch(True)
    histFluctuated=ROOT.TH1F(histName+"_fluctuated", histName+"_fluctuated", initHist.GetXaxis().GetNbins(), initHist.GetXaxis().GetXbins().GetArray())
    seed = randint(1, 100)    # Pick a random number between 1 and 100.
    print("seed: ",seed)
    binSeed =  int( round(seed*1e5))
    #binSeed =  int( round(initHist.GetBinCenter(i)+seed*1e5))
    rand3 = ROOT.TRandom3(binSeed)
   # for i in range(initHist.GetXaxis().GetNbins()+1):
    print "end bin: ", initHist.GetBinCenter(initHist.GetNbinsX())
    for i in range(initHist.GetNbinsX()+2):
        bincontent= initHist.GetBinContent(i)
        bincontent = int( round( rand3.PoissonD(bincontent)))
        histFluctuated.SetBinError(i, np.sqrt(bincontent))
        histFluctuated.SetBinContent(i,bincontent)
    c1=TCanvas()
    c1.SetLogy()
    c1.SetLogx()
    initHist.Draw()
    histFluctuated.SetLineColor(2)
    histFluctuated.Draw("same")
    c1.SaveAs(histName+"_fluctuated.pdf")
    return histFluctuated


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('--initLumi',  default='0.',  help='desired luminosity [fb^-1]')
    parser.add_argument('--desiredLumi',  default='0.', help='init luminosity [fb^-1]')
    parser.add_argument('--initRoot', default='/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/input_dijetISR2018/bkg/preFluctuation/dijetgamma_mjj_g150_2j25_nbtag2.root',  help='init root')
    parser.add_argument('--seed',  default=1., help='seed for the random number generatro')
    parser.add_argument('--outputRoot', default='../input_dijetISR2018/bkg/Fluctuated_dijetgamma_g150_2j25_2btaggedApr_9.root',  help='init root')
    #parser.add_argument('--histName', default='background_mjj_var',  help='init histogram')
    parser.add_argument('--histName', default='basicBkgFrom4ParamFit',  help='init histogram')

    args =parser.parse_args()
    fIn=TFile.Open(args.initRoot)
    ROOT.gROOT.SetBatch(True)

    initHist=fIn.Get(args.histName)
    print("initHist", initHist)
    #scaledHist=scaledHist(histName, 0.001, 80
    fluctuatedHist=fluctuateHist(initHist, args.histName, args.seed)
    #for i in range(fluctuatedHist.GetNbinsX()+1):
    #    print("flucbin: ",i, "  bincontent", fluctuatedHist.GetBinContent(i))

    fOut=TFile(args.outputRoot, "RECREATE")
    fluctuatedHist.Write()
    fOut.Write()
    fOut.Close()
