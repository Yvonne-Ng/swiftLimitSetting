#!/usr/bin/env python

import ROOT
from art.morisot import Morisot
from array import array
import sys, os
import math

####### Get input #########
filenametemp = "/home/beresford/TriJet/StatisticalAnalysis/Bayesian/results/Step1_SearchPhase/Spurious_dijetgamma_mc_hist_20160714_9p50fb_4Par/Step1_SearchPhase_Zprime_mjj_var_Scaled_9p50fb.root"

folder = "./plotting/SpuriousSignal/plots/SpuriousSignal_dijetgamma_20160714_9p50_4Par"

signalFolder = "/home/beresford/TriJet/StatisticalAnalysis/Bayesian/inputs/xsecandacceptance/"
signalDir = "dijetgamma_g150_2j25"
sampleChoices = ["ZPrimemR200gSM0p30","ZPrimemR300gSM0p30","ZPrimemR400gSM0p30","ZPrimemR500gSM0p30"] 

# Get Scaled results for MC stat uncert
initialInputFile = ROOT.TFile.Open("./inputs/hist_20160714/OUT_dijetgamma_mc/datalike-noNeff/hist.root","READ") # Need original scaled file as basicData in searchInputFile has root N errors
MCScaledHist = initialInputFile.Get(signalDir+"/Zprime_mjj_var_Scaled_9p50fb")

doAlternate = True

luminosity = 9500

lowfit = 203
highfit = 1493

###########################

# make plots folder i.e. make folder extension
if not os.path.exists(folder):
    os.makedirs(folder)

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("Teals")
myPainter.setLabelType(4)
myPainter.setEPS(False)


# Get search phase result
searchInputFile = ROOT.TFile.Open(filenametemp,"READ")

# Retrieve search phase inputs
basicData = searchInputFile.Get("basicData")
basicBkgFrom4ParamFit = searchInputFile.Get("basicBkgFrom4ParamFit")

nomPlus1 = searchInputFile.Get("nominalBkgFromFit_plus1Sigma")
nomMinus1 = searchInputFile.Get("nominalBkgFromFit_minus1Sigma")


if doAlternate :
  valueNewFuncErrDirected = searchInputFile.Get("nomOnDataWithDirectedRMSScaleFuncChoiceErr")


# Now make plot comparing spurious signal to stat uncertainty on function; signals.
# Use relative difference: |mc - fit|/fit or |unc band size|/fit or nSignalEvents/fit.
relSpuriousSignal = basicData.Clone("relSpurSig")
relSpuriousSignal.SetDirectory(0)
relSpuriousSignal.Add(basicBkgFrom4ParamFit,-1)
relSpuriousSignal.Divide(basicBkgFrom4ParamFit)

# set to absolute value? seems to be necessary
absRelSpuriousSignal = basicData.Clone("absRelSpurSig")
for bin in range(1,basicData.GetNbinsX()+1) :
  absRelSpuriousSignal.SetBinContent(bin,math.fabs(relSpuriousSignal.GetBinContent(bin)))

nomPlus1Scaled = nomPlus1.Clone()
nomPlus1Scaled.SetName("nomPlus1Scaled")
nomPlus1Scaled.Add(basicBkgFrom4ParamFit,-1)
nomPlus1Scaled.Divide(basicBkgFrom4ParamFit)

poissonUncert = basicData.Clone("poissonUncert")
poissonUncert.Add(basicData,-1)
for bin in range(1,poissonUncert.GetNbinsX()+1) :
  #print "Empty?",poissonUncert.GetBinContent(bin)
  N = float(basicBkgFrom4ParamFit.GetBinContent(bin))
  if N != 0.:
    print (math.sqrt(N))/N
    poissonUncert.SetBinContent(bin,((math.sqrt(N))/N))
    poissonUncert.SetBinError(bin,0.)
  else: 
    poissonUncert.SetBinContent(bin,0.)
    poissonUncert.SetBinError(bin,0.)


MCStatUncert = MCScaledHist.Clone("MCStatUncert")
MCStatUncert.Add(MCScaledHist,-1)

for bin in range(1,MCStatUncert.GetNbinsX()+1) :
  #print "Empty?",MCStatUncert.GetBinContent(bin)
  # Lydia N From Fit! N = float(basicBkgFrom4ParamFit.GetBinContent(bin))
  # N From Scaled MC bin content
  N = float(MCScaledHist.GetBinContent(bin))
  if N != 0.:
    print MCScaledHist.GetBinError(bin)/N
    # Lydia MCStatUncert.SetBinContent(bin,MCScaledHist.GetBinError(bin)/N)
    #MCStatUncert.SetBinContent(bin,math.sqrt(MCScaledHist.GetBinError(bin))/N)
    MCStatUncert.SetBinContent(bin,MCScaledHist.GetBinError(bin)/N)
    MCStatUncert.SetBinError(bin,0.)
  else: 
    MCStatUncert.SetBinContent(bin,0.)
    MCStatUncert.SetBinError(bin,0.)

if doAlternate:
  valueNewFuncErrDirectedScaled = valueNewFuncErrDirected.Clone()
  valueNewFuncErrDirectedScaled.SetName("valueNewFuncErrDirectedScaled")
  valueNewFuncErrDirectedScaled.Add(basicBkgFrom4ParamFit,-1)
  valueNewFuncErrDirectedScaled.Divide(basicBkgFrom4ParamFit)

sigList = []
sigListRel = []
for sample in sampleChoices :
  insigfile = ROOT.TFile(signalFolder+"ZPrime_gjj.root",'r')
  print "Getting"
  #print insigfile.ls()
  #print signalDir+"/Zprime_mjj_var_Scaled_{0}_1p00fb".format(sample)
  #sigHist = insigfile.Get(signalDir+"/Zprime_mjj_var_Scaled_{0}_1p00fb".format(sample))
  print "mjj_{0}_1fb_Nominal".format(sample)
  sigHist = insigfile.Get("mjj_{0}_1fb_Nominal".format(sample))
  sigHist.SetDirectory(0)
  print "Scaling signals to "+str(luminosity/1000.)
  sigHist.Scale(luminosity/1000.)
  sigList.append(sigHist)
  sigHistforRel = sigHist.Clone()
  sigHistforRel.SetName(sigHist.GetName()+"_forRel")
  sigHistforRel.SetDirectory(0)
  sigHistforRel.Divide(basicBkgFrom4ParamFit)
  sigListRel.append(sigHistforRel)
  insigfile.Close()

histograms = [absRelSpuriousSignal,nomPlus1Scaled, poissonUncert, MCStatUncert]
names = ["Spurious signal","Statistical uncertainty on fit", "Poisson Uncert", "MC Stat Uncert"]
figname = "{0}/compareSpuriousSignalToFuncAndSig_relativeDiff".format(folder)

#myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,"automatic","automatic",extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])
myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,0.,0.3,extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])


histograms = histograms+sigListRel
names = names + ["sig, 200 GeV","sig, 300 GeV", "sig, 400 GeV", "sig, 500 GeV"]
figname = "{0}/compareSpuriousSignalToFuncAndSig_relativeDiff_withSignals".format(folder)


#myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,"automatic","automatic",extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])
myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,0.,0.3,extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])

if doAlternate:
  histograms = [absRelSpuriousSignal,nomPlus1Scaled,valueNewFuncErrDirectedScaled,poissonUncert,MCStatUncert]
  names = ["Spurious signal","Statistical uncertainty on fit","Function choice","Poisson Uncert","MC Stat Uncert"]
  figname = "{0}/alternate_compareSpuriousSignalToFuncAndSig_relativeDiff".format(folder)

  myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,0.,0.3,extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])

  histograms = histograms+sigListRel
  names = names + ["sig, 200 GeV","sig, 300 GeV", "sig, 400 GeV", "sig, 500 GeV"]
  figname = "{0}/alternate_compareSpuriousSignalToFuncAndSig_relativeDiff_withSignals".format(folder)

  myPainter.drawManyOverlaidHistograms(histograms,names,"m_{jj} [GeV]","Relative difference from fit",figname,nomPlus1.FindBin(lowfit),nomPlus1.FindBin(highfit)-1,0.,0.3,extraLegendLines = [],doLogX=True,doLogY=False,doErrors=False,doRectangular=True,doLegend=True,doLegendLow=False,doLegendLocation="Right",doLegendOutsidePlot=False,doATLASLabel="Right",pairNeighbouringLines=False,dotLines = [],addHorizontalLines=[])

print "Done."
