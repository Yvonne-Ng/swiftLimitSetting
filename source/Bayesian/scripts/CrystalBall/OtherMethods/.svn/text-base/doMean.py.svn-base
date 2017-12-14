#!/usr/bin/env python
import os
import ROOT
import math
from ROOT import *

#from art.options import Options # Include it to apply ATLAS style settings
#from art.morisot import Morisot

###############################
# user definitions input path, plotDir ...

inDir = 'inDir/jjj/Chopped'
plotDir = "MeanPlots_jjj_Chopped"
isChopped = True
MassList = ["350","450","550"] 

#inDir = 'inDir/jjj/NoMjj'
#plotDir = "MeanPlots_jjj_NoMjj"
#isChopped = False
#MassList = ["350","450","550"]

#inDir = 'inDir/gjj/Chopped'
#plotDir = "MeanPlots_gjj_Chopped"
#isChopped = True
#MassList=["200","250","300","350","400","450","500","550","750","950"] 

#inDir = 'inDir/gjj/NoMjj'
#plotDir = "MeanPlots_gjj_NoMjj"
#isChopped = False
#MassList=["200","250","300","350","400","450","500","550","750","950"] 


###############################
if not os.path.exists(plotDir):
  os.makedirs(plotDir)

pdf="{0}/ZPrimegSM0p30_JESShifts1fb_1Sigma.pdf".format(plotDir)
pdf1="{0}/ZPrimegSM0p30_JESShifts1fbComponent1_1Sigma.pdf".format(plotDir)
pdf2="{0}/ZPrimegSM0p30_JESShifts1fbComponent2_1Sigma.pdf".format(plotDir)
pdf3="{0}/ZPrimegSM0p30_JESShifts1fbComponent3_1Sigma.pdf".format(plotDir)
pdf4="{0}/ZPrimegSM0p30_JESShifts1fbComponent4_1Sigma.pdf".format(plotDir)
pdfquad="{0}/ZPrimegSM0p30_JESShifts1fb_Quadrature_1Sigma.pdf".format(plotDir)

markerstyle=20
markersize=0.8

gStyle.SetOptStat(0)

Signals = {}
nBins = len(MassList)
InputFileList = []

canvas=ROOT.TCanvas("Beginning","Beginning",0,0,800,600)
canvas.Print(pdf+"(")

for Mass in MassList:
  if isChopped:
    myfile = inDir+'/Chopped_ZPrimemR%sgSM0p30.root'%(Mass)
  else:
    myfile = inDir+'/ZPrimemR%sgSM0p30.root'%(Mass)
  InputFileList.append(ROOT.TFile(myfile))

CompDown1Diff = ROOT.TH1D("CompDown1Diff","",nBins,0,nBins)
CompUp1Diff = ROOT.TH1D("CompUp1Diff","",nBins,0,nBins)
CompDown2Diff = ROOT.TH1D("CompDown2Diff","",nBins,0,nBins)
CompUp2Diff = ROOT.TH1D("CompUp2Diff","",nBins,0,nBins)
CompDown3Diff = ROOT.TH1D("CompDown3Diff","",nBins,0,nBins)
CompUp3Diff = ROOT.TH1D("CompUp3Diff","",nBins,0,nBins)
CompDown4Diff = ROOT.TH1D("CompDown4Diff","",nBins,0,nBins)
CompUp4Diff = ROOT.TH1D("CompUp4Diff","",nBins,0,nBins)

QuadDown = ROOT.TH1D("QuadDown","",nBins,0,nBins)
QuadUp = ROOT.TH1D("QuadUp","",nBins,0,nBins)

canvas1=ROOT.TCanvas("Canvas1","Canvas1",0,0,800,600)
canvas2=ROOT.TCanvas("Canvas2","Canvas2",0,0,800,600)
canvas3=ROOT.TCanvas("Canvas3","Canvas3",0,0,800,600)
canvas4=ROOT.TCanvas("Canvas4","Canvas4",0,0,800,600)
canvasquad=ROOT.TCanvas("Canvasquad","Canvasquad",0,0,800,600)

lXmin = 0.60
lXmax = 0.80
lYmin = 0.65
lYmax = 0.85

leg1 = ROOT.TLegend(lXmin, lYmin, lXmax, lYmax)
leg2 = ROOT.TLegend(lXmin, lYmin, lXmax, lYmax)
leg3 = ROOT.TLegend(lXmin, lYmin, lXmax, lYmax)
leg4 = ROOT.TLegend(lXmin, lYmin, lXmax, lYmax)
legquad = ROOT.TLegend(lXmin, lYmin, lXmax, lYmax)

for iBin,(Mass,InputFile) in enumerate(zip(MassList,InputFileList)):
  #print iBin
  #print Mass
  #nominalHisto =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_Nominal"%(HistDir,Mass))
  nominalHisto =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_Nominal"%(Mass))
  # 1 2 3 4 are components
  # Get 1down and 1 up as use 1 sigma shifts to assess uncertainty!!
  #Comp1DownHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_1__1down"%(HistDir,Mass))
  #Comp1UpHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_1__1up"%(HistDir,Mass))
  #Comp2DownHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_2__1down"%(HistDir,Mass))
  #Comp2UpHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_2__1up"%(HistDir,Mass))
  #Comp3DownHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_3__1down"%(HistDir,Mass))
  #Comp3UpHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_3__1up"%(HistDir,Mass))
  #Comp4DownHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_EtaIntercalibration_NonClosure__1down"%(HistDir,Mass))
  #Comp4UpHist =InputFile.Get("%s/mjj_ZPrimemR%sgSM0p30_1fb_JET_EtaIntercalibration_NonClosure__1up"%(HistDir,Mass))
  Comp1DownHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_1__1down"%(Mass))
  Comp1UpHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_1__1up"%(Mass))
  Comp2DownHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_2__1down"%(Mass))
  Comp2UpHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_2__1up"%(Mass))
  Comp3DownHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_3__1down"%(Mass))
  Comp3UpHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_GroupedNP_3__1up"%(Mass))
  Comp4DownHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_EtaIntercalibration_NonClosure__1down"%(Mass))
  Comp4UpHist =InputFile.Get("mjj_ZPrimemR%sgSM0p30_1fb_JET_EtaIntercalibration_NonClosure__1up"%(Mass))

  Comp1maxDownValue=(abs(Comp1DownHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp1maxUpValue=(abs(Comp1UpHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp2maxDownValue=(abs(Comp2DownHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp2maxUpValue=(abs(Comp2UpHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp3maxDownValue=(abs(Comp3DownHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp3maxUpValue=(abs(Comp3UpHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp4maxDownValue=(abs(Comp4DownHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  Comp4maxUpValue=(abs(Comp4UpHist.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean())
  
  QuadDownValue=math.sqrt(math.pow(Comp1maxDownValue,2)+math.pow(Comp2maxDownValue,2)+math.pow(Comp3maxDownValue,2)+math.pow(Comp4maxDownValue,2))
  QuadUpValue=math.sqrt(math.pow(Comp1maxUpValue,2)+math.pow(Comp2maxUpValue,2)+math.pow(Comp3maxUpValue,2)+math.pow(Comp4maxUpValue,2))

  CompDown1Diff.SetBinContent(iBin+1,Comp1maxDownValue)
  CompDown1Diff.SetBinError(iBin+1,0.0)
  CompDown1Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompUp1Diff.SetLineColor(kRed)
  CompUp1Diff.SetBinContent(iBin+1,Comp1maxUpValue)
  CompUp1Diff.SetBinError(iBin+1,0.0)
  CompUp1Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompDown2Diff.SetLineColor(kViolet)
  CompDown2Diff.SetBinContent(iBin+1,Comp2maxDownValue)
  CompDown2Diff.SetBinError(iBin+1,0.0)
  CompDown2Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompUp2Diff.SetLineColor(kOrange+1)
  CompUp2Diff.SetBinContent(iBin+1,Comp2maxUpValue)
  CompUp2Diff.SetBinError(iBin+1,0.0)
  CompUp2Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompDown3Diff.SetLineColor(kGreen+1)
  CompDown3Diff.SetBinContent(iBin+1,Comp3maxDownValue)
  CompDown3Diff.SetBinError(iBin+1,0.0)
  CompDown3Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompUp3Diff.SetLineColor(kYellow+3)
  CompUp3Diff.SetBinContent(iBin+1,Comp3maxUpValue)
  CompUp3Diff.SetBinError(iBin+1,0.0)
  CompUp3Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompDown4Diff.SetLineColor(kBlack+1)
  CompDown4Diff.SetBinContent(iBin+1,Comp4maxDownValue)
  CompDown4Diff.SetBinError(iBin+1,0.0)
  CompDown4Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  CompUp4Diff.SetLineColor(kGray+2)
  CompUp4Diff.SetBinContent(iBin+1,Comp4maxUpValue)
  CompUp4Diff.SetBinError(iBin+1,0.0)
  CompUp4Diff.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  QuadDown.SetLineColor(kBlack+1)
  QuadDown.SetBinContent(iBin+1,QuadDownValue)
  QuadDown.SetBinError(iBin+1,0.0)
  QuadDown.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  QuadUp.SetLineColor(kBlack+1)
  QuadUp.SetLineStyle(2)
  QuadUp.SetBinContent(iBin+1,QuadUpValue)
  QuadUp.SetBinError(iBin+1,0.0)
  QuadUp.GetXaxis().SetBinLabel(iBin+1, Mass) # +1 as Bins start at 1

  if iBin == 1:   
    leg1.AddEntry(CompDown1Diff, "Component 1, 1 #sigma down ", "l")
    leg1.AddEntry(CompUp1Diff, "Component 1, 1 #sigma up", "l")
    leg2.AddEntry(CompDown2Diff, "Component 2, 1 #sigma down ", "l")
    leg2.AddEntry(CompUp2Diff, "Component 2, 1 #sigma up ", "l")
    leg3.AddEntry(CompDown3Diff, "Component 3, 1 #sigma down ", "l")
    leg3.AddEntry(CompUp3Diff, "Component 3, 1 #sigma up ", "l")
    leg4.AddEntry(CompDown4Diff, "Component 4, 1 #sigma down ", "l")
    leg4.AddEntry(CompUp4Diff, "Component 4, 1 #sigma up ", "l")
    legquad.AddEntry(QuadDown, "JES, 1 #sigma down ", "l")
    legquad.AddEntry(QuadUp, "JES, 1 #sigma up ", "l")
  #n = len(y)
  #print relativeUncHisto.GetMean()
  #print nominalHisto.GetMean()
  #print "Relative difference: " , abs(relativeUncHisto.GetMean()-nominalHisto.GetMean())/nominalHisto.GetMean()
  ##print "Error on difference, assuming uncorrelated " , sqrt(pow(relativeUncHisto.GetMeanError(),2)+pow(nominalHisto.GetMeanError(),2))

  #canvas.SetLogy(True)
XName = "Mass Point [GeV]"
YName = "Relative uncertainty"
Offset = 1.5
canvas1.cd()
CompDown1Diff.GetXaxis().SetTitle(XName)
CompDown1Diff.GetYaxis().SetTitle(YName)
CompDown1Diff.GetYaxis().SetTitleOffset(Offset)
CompDown1Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.015)
CompDown1Diff.Draw("HIST")

CompUp1Diff.GetXaxis().SetTitle(XName)
CompUp1Diff.GetYaxis().SetTitle(YName)
CompUp1Diff.GetYaxis().SetTitleOffset(Offset)
CompUp1Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.015)
CompUp1Diff.Draw("HIST same")
leg1.Draw() 
canvas1.Print(pdf)
canvas1.Print(pdf1)

canvas2.cd()
CompDown2Diff.GetXaxis().SetTitle(XName)
CompDown2Diff.GetYaxis().SetTitle(YName)
CompDown2Diff.GetYaxis().SetTitleOffset(Offset)
CompDown2Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompDown2Diff.Draw("HIST")

CompUp2Diff.GetXaxis().SetTitle(XName)
CompUp2Diff.GetYaxis().SetTitle(YName)
CompUp2Diff.GetYaxis().SetTitleOffset(Offset)
CompUp2Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompUp2Diff.Draw("HIST same")
leg2.Draw() 
canvas2.Print(pdf)
canvas2.Print(pdf2)

canvas3.cd()
CompDown3Diff.GetXaxis().SetTitle(XName)
CompDown3Diff.GetYaxis().SetTitle(YName)
CompDown3Diff.GetYaxis().SetTitleOffset(Offset)
CompDown3Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompDown3Diff.Draw("HIST")
#MyDownFile = ROOT.TFile(root+"Down.root","RECREATE")
#CompDown3Diff.Write("CompDown3")#, ROOT.TObject.kOverwrite)
#MyDownFile.Close()

CompUp3Diff.GetXaxis().SetTitle(XName)
CompUp3Diff.GetYaxis().SetTitle(YName)
CompUp3Diff.GetYaxis().SetTitleOffset(Offset)
CompUp3Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompUp3Diff.Draw("HIST same")
leg3.Draw() 
canvas3.Print(pdf)
canvas3.Print(pdf3)
#MyUpFile = ROOT.TFile(root+"Up.root","RECREATE")
#CompUp3Diff.Write("CompUp3")#, ROOT.TObject.kOverwrite)
#MyUpFile.Close()

canvas4.cd()
CompDown4Diff.GetXaxis().SetTitle(XName)
CompDown4Diff.GetYaxis().SetTitle(YName)
CompDown4Diff.GetYaxis().SetTitleOffset(Offset)
CompDown4Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompDown4Diff.Draw("HIST")

CompUp4Diff.GetXaxis().SetTitle(XName)
CompUp4Diff.GetYaxis().SetTitle(YName)
CompUp4Diff.GetYaxis().SetTitleOffset(Offset)
CompUp4Diff.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.023)
CompUp4Diff.Draw("HIST same")
leg4.Draw() 
canvas4.Print(pdf)
canvas4.Print(pdf4)

canvasquad.cd()
QuadDown.GetXaxis().SetTitle(XName)
QuadDown.GetYaxis().SetTitle(YName)
QuadDown.GetYaxis().SetTitleOffset(Offset)
QuadDown.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.015)
QuadDown.Draw("HIST")

QuadUp.GetXaxis().SetTitle(XName)
QuadUp.GetYaxis().SetTitle(YName)
QuadUp.GetYaxis().SetTitleOffset(Offset)
QuadUp.GetYaxis().SetRangeUser(0,0.05)#.SetMinimum(0.015)
QuadUp.Draw("HIST same")
legquad.Draw() 
canvasquad.Print(pdf)
canvasquad.Print(pdfquad)

canvas=ROOT.TCanvas("Ending","Ending",0,0,800,600)
canvas.Print(pdf+")")


