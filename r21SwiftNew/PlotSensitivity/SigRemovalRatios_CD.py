#!/bin/python
#import sys, os, argparse, ROOT, glob
import ROOT, glob, math, argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gROOT.LoadMacro("RootStyle/atlasstyle-00-03-05/AtlasStyle.C");

ROOT.SetAtlasStyle();

ROOT.gROOT.LoadMacro("RootStyle/atlasstyle-00-03-05/AtlasUtils.C");from fileNamingTool import *

parser = argparse.ArgumentParser(description='%prog [options]')
#parser.add_argument('--bkgFile', dest='inputBkgFileName', default='', required=True, help='input nominal file name')
#parser.add_argument('--aboveFile', dest='inputAboveFileName', default='', required=True, help='input nominal file name')
#parser.add_argument('--belowFile', dest='inputBelowFileName', default='', required=True, help='input nominal file name')
#parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
parser.add_argument('--dir', dest='dir', default='default', help='directory for input files')
parser.add_argument('--seriesName', dest='seriesName', required=True, help='seires name of the file')
parser.add_argument('--notes', dest='notes', default='29.7', help='notes for plotting')
args = parser.parse_args()

gaussianWidthList = [7]#,7]#,5, 10 done]
#gaussianMeanList = [650,750,850,950,1050,1250,1450,1650,1850]
gaussianMeanList = [450, 550,650,  750, 850, 950,1000, 1100, 1200]#, 1050, 1750, 1850]#,750,850,950,1050]
#gaussianMeanList = [1200]#, 1050, 1750, 1850]#,750,850,950,1050]
windowWidthList = [13]

bkgOnlyFileName = ""
aboveFileName = ""
belowFileName = ""

c = ROOT.TCanvas('c', 'c', 100, 50, 800, 600)

def gaussianModel(gaussWidth):
    model="Gauss_width"+str(gaussWidth)
    return model


#c.Print(args.dir+"/SignalRemovalRatios.GaussianWidth5."+args.dir+".WindowWidth.pdf[")
#c.Print("SignalRemovalRatios.GaussianWidth5."+args.dir+".WindowWidth.pdf[")

for gaussianWidth in gaussianWidthList:
  print "GAUSSIAN WIDTH 1", gaussianWidth

  for windowWidth in windowWidthList:
    print "GAUSSIAN WIDTH 2", gaussianWidth

    c.Print(args.dir+"/SignalRemovalRatios_GaussianWidth_"+str(gaussianWidth)+"_WindowWidth_"+str(windowWidth)+".pdf[")

    for gaussianMean in gaussianMeanList:

      #being lazy and inflexible
      #this remains the same everywhere as it's bkg only
      #bkgOnlyFileName = "BkgOnly/searchphase.Gauss_width5.650.GeV.0p0.ifb.mjj_Gauss.4.par.401.seed.BHpvalDep.window9.root"
        gaussModel=gaussianModel(gaussianWidth)
        try:
          bkgOnlyFileName=findLabelledFileName(args.dir, "NOSIGNAL", gaussModel,gaussianMean, windowWidth,args.seriesName)
        except :
            print ("oops, there is no bkgnd only file for mass point", gaussianMean, " and windowWidth: ", windowWidth)
            #raise ValueError
            continue
        try:
          aboveFileName=findLabelledFileName(args.dir, "JUSTABOVE", gaussModel,gaussianMean, windowWidth, args.seriesName)
        except:
            print ("oops, there is no JUSTabove file for mass point", gaussianMean, " and windowWidth: ", windowWidth)
            #raise ValueError
            continue

        try:
          belowFileName=findLabelledFileName(args.dir, "JUSTBELOW", gaussModel,gaussianMean, windowWidth, args.seriesName)
        except:
            print ("oops, there is no JUSTBELOW file for mass point", gaussianMean, " and windowWidth: ", windowWidth)
            #raise ValueError
            continue

      #bkgOnlyFileName = "BkgOnly/searchphase.Gauss_width5.650.GeV.0p0.ifb.mjj_Gauss.4.par.401.seed.BHpvalDep.window9_pseudodata.root"
      #list all the files that are available
        print "GAUSSIAN WIDTH 3", gaussianWidth

        print args.dir+"/*"+str(gaussianWidth)+"*."+str(gaussianMean)+"*ww"+str(windowWidth)+"*.root"
        fileList = sorted(glob.glob(args.dir+"/*"+str(gaussianWidth)+"*."+str(gaussianMean)+"*ww"+str(windowWidth)+"*.root"))
        print fileList
      #look for the last lumi, if we're lucky that is a discovery
#      aboveFileName = fileList[-1]#last lumi
#      belowFileName = fileList[len(fileList)-2]

      #belowFileName = args.dir+"/searchphase.Gauss_width5.650.GeV.79p9.ifb.mjj_Gauss.4.par.401.seed.NLO2015_29p7_sensitivityScan_ww9.root"
      #aboveFileName = args.dir+"/searchphase.Gauss_width5.650.GeV.81p1.ifb.mjj_Gauss.4.par.401.seed.NLO2015_29p7_sensitivityScan_ww9.root"

#      print 'bkgOnlyFileName: '+str(bkgOnlyFileName)+", aboveFileName: "+aboveFileName+", belowFileName: "+belowFileName


        c = ROOT.TCanvas('c', 'c', 100, 50, 800, 600)

        textSize=23
        #pads
        outpad = ROOT.TPad("extpad","extpad", 0.17, 0.12,   1, 1)
        pad1   = ROOT.TPad("pad1",  "pad1",   0., 0.66, 1., 1)
        helperPad1   = ROOT.TPad("pad1",  "pad1",   0.5, 0.5, 1., 1)
        pad2   = ROOT.TPad("pad2",  "pad2",   0., 0.33,   1., 0.66)
        helperPad2   = ROOT.TPad("pad1",  "pad1",   0.5, 0.25, 1, 0.75)
        pad3   = ROOT.TPad("pad3",  "pad3",   0., 0.,   1., 0.33+0.06)
        helperPad3   = ROOT.TPad("pad1",  "pad1",   0.5, 0., 1.0, 0.5)

        #setup drawing options
        outpad.SetFillStyle(4000)#transparent
        helperPad1.SetFillStyle(4000)#transparent
        helperPad2.SetFillStyle(4000)#transparent
        helperPad3.SetFillStyle(4000)#transparent
        pad1.SetBottomMargin(0.00001)
        pad1.SetBorderMode(0)
        pad1.SetFillColor(0)#transparent
        pad2.SetFillColor(0)#transparent
        pad2.SetFrameFillStyle(4000)#transparent
        pad2.SetTopMargin(0.00001)
        pad2.SetBottomMargin(0)
        pad2.SetBorderMode(0)
        pad3.SetFillColor(0)#transparent
        pad3.SetFrameFillStyle(4000)#transparent
        pad3.SetTopMargin(0.00001)
        pad3.SetBottomMargin(0.3)
        pad3.SetBorderMode(0)
        pad1.Draw()
        pad2.Draw()
        pad3.Draw()
        outpad.Draw()
        helperPad1.Draw()
        helperPad2.Draw()
        helperPad3.Draw()

      #bkgOnlyFileName = args.inputBkgFileName
      #aboveFileName = args.inputAboveFileName
      #belowFileName = args.inputBelowFileName

      #bkgOnlyFileName = "searchphase.Gauss_width5.850.GeV.0p0.ifb.mjj_Gauss.4.par.34.seed.WinEx.window16.root"
      #aboveFileName = "searchphase.Gauss_width5.850.GeV.20p0.ifb.mjj_Gauss.4.par.34.seed.WinEx.window16.root"
      #belowFileName = "searchphase.Gauss_width5.850.GeV.12p0.ifb.mjj_Gauss.4.par.34.seed.WinEx.window16.root"




      #gaussianWidth = bkgOnlyFileName.split('Gauss_width')[1].split('.')[0]
        gaussianWidth = str(gaussianWidth)
        #print gaussianWidth
        #gaussianMean = bkgOnlyFileName.split('.')[2]
        gaussianMean = str(gaussianMean)
        windowWidth = str(windowWidth)      #print windowWidth

#        discoveryXsecAbove = round(float(aboveFileName.split('.GeV.')[1].split('.')[0].replace('p','.'))/29.7,2)
#        #print discoveryXsecAbove

#        discoveryXsecBelow = round(float(belowFileName.split('.GeV.')[1].split('.')[0].replace('p','.'))/29.7,2)
        #print discoveryXsecBelow

        # hardcoding right now
        #discoveryXsecAbove=0.4
        #discoveryXsecBelow=0.3
        discoverySigNumAbove=getDiscoveryEventNum(aboveFileName)
        discoverySigNumBelow=getDiscoveryEventNum(belowFileName)

        bkgOnlyFile = ROOT.TFile.Open(bkgOnlyFileName,"READ")
        aboveFile = ROOT.TFile.Open(aboveFileName,"READ")
        belowFile = ROOT.TFile.Open(belowFileName,"READ")

        #bkgOnlyHist = bkgOnlyFile.Get("theSwiftFit").Clone("bkgOnly")
        bkgOnlyHist = bkgOnlyFile.Get("basicBkgFrom4ParamFit").Clone("bkgOnly")
        print bkgOnlyHist.GetNbinsX()

        aboveHist = aboveFile.Get("basicBkgFrom4ParamFit").Clone("above")

        print aboveHist.GetNbinsX()
        belowHist = belowFile.Get("basicBkgFrom4ParamFit").Clone("below")
        print belowHist.GetNbinsX()

        basicDataHist = bkgOnlyFile.Get("basicData").Clone("basicData")

        bandUpper = basicDataHist.Clone()
        bandLower = basicDataHist.Clone()
        for bin in range(bandUpper.GetNbinsX()):
          if bandUpper.GetBinContent(bin) > 0:
            bandUpper.SetBinContent(bin,1+math.sqrt(basicDataHist.GetBinContent(bin))/basicDataHist.GetBinContent(bin))
            bandUpper.SetBinError(bin,0)
            bandLower.SetBinContent(bin,1-math.sqrt(basicDataHist.GetBinContent(bin))/basicDataHist.GetBinContent(bin))
            bandLower.SetBinError(bin,0)
          else:
            bandUpper.SetBinContent(bin,1)
            bandLower.SetBinContent(bin,1)
            bandUpper.SetBinError(bin,0)
            bandLower.SetBinError(bin,0)

        c.cd()
        pad1.cd()

        RatioBelowBkgOnly = belowHist.Clone("BelowRatio")
        RatioBelowBkgOnly.GetYaxis().SetTitle("Fit Ratio")
        RatioBelowBkgOnly.GetYaxis().SetNdivisions(7)
        RatioBelowBkgOnly.GetYaxis().SetTitleFont(43)
        RatioBelowBkgOnly.GetYaxis().SetTitleSize(textSize)
        RatioBelowBkgOnly.GetYaxis().SetTitleOffset(1.5)
        RatioBelowBkgOnly.GetYaxis().SetLabelFont(43)
        RatioBelowBkgOnly.GetYaxis().SetLabelSize(textSize)

        RatioBelowBkgOnly.Divide(bkgOnlyHist)
        RatioBelowBkgOnly.SetLineColor(ROOT.kBlue)
        RatioBelowBkgOnly.GetXaxis().SetRangeUser(250,2750)
        #RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.995,RatioBelowBkgOnly.GetMaximum()+0.001)
        #RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.9975,2-0.9975)
        RatioBelowBkgOnly.GetYaxis().SetRangeUser(1.7,1.3)
        print "NOT CHANGING"
        if (float(gaussianMean) > 1800) :
            print "CHANGING 1800"
            RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.9975,1.03)
        elif (float(gaussianMean) > 1700) :
            print "CHANGING 1700"
            RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.9975,1.03)
        elif (float(gaussianMean) > 1400) :
            print "CHANGING 1400"
            RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.9975,1.02)
        elif (float(gaussianMean) > 1000) :
            print "CHANGING 1000"
            RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.9975,1.005)
        #RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.95,1.05)
        RatioBelowBkgOnly.GetYaxis().SetRangeUser(0.95,1.10)
        RatioBelowBkgOnly.GetYaxis().SetNdivisions(505)
        RatioBelowBkgOnly.SetMarkerStyle(1)

        for bin in range(RatioBelowBkgOnly.GetNbinsX()):
          RatioBelowBkgOnly.SetBinError(bin,0.0)
          if RatioBelowBkgOnly.GetBinContent(bin) == 0:
            RatioBelowBkgOnly.SetBinContent(bin,0.0)

        RatioAboveBkgOnly = aboveHist.Clone("AboveRatio")
        RatioAboveBkgOnly.Divide(bkgOnlyHist)
        RatioAboveBkgOnly.SetLineColor(ROOT.kGreen)
        RatioAboveBkgOnly.GetXaxis().SetRangeUser(250,2750)
        for bin in range(RatioAboveBkgOnly.GetNbinsX()):
          if RatioAboveBkgOnly.GetBinContent(bin) == 0:
            RatioAboveBkgOnly.SetBinContent(bin,0.0)

        for bin in range(RatioAboveBkgOnly.GetNbinsX()):
          RatioAboveBkgOnly.SetBinError(bin,0.0)

        RatioAboveBkgOnly.SetMarkerStyle(1)

        RatioBelowBkgOnly.Draw("h ][")
        RatioAboveBkgOnly.Draw("h same ][")

        bandUpper.SetMarkerStyle(0)
        bandUpper.SetMarkerSize(0)
        bandLower.SetMarkerSize(0)
        bandUpper.SetMarkerSize(0)
        bandUpper.SetMarkerColor(5)
        bandUpper.SetLineColor(ROOT.kGray+2)
        bandLower.SetLineColor(ROOT.kGray+2)
        bandUpper.SetLineStyle(2)
        bandLower.SetLineStyle(2)
        bandUpper.Draw("h same")
        bandLower.Draw("h same")
        bandUpper2 = bandUpper.Clone()
        bandLower2 = bandLower.Clone()
        for bin in range(bandUpper2.GetNbinsX()+1):
          bandUpper2.SetBinContent(bin,1+(bandUpper2.GetBinContent(bin)-1)*2)
          bandLower2.SetBinContent(bin,1+(bandLower2.GetBinContent(bin)-1)*2)
        bandUpper2.SetLineColor(ROOT.kGray+1)
        bandLower2.SetLineColor(ROOT.kGray+1)
        bandUpper2.Draw("h same")
        bandLower2.Draw("h same")
        bandUpper3 = bandUpper.Clone()
        bandLower3 = bandLower.Clone()
        for bin in range(bandUpper3.GetNbinsX()+1):
          bandUpper3.SetBinContent(bin,1+(bandUpper3.GetBinContent(bin)-1)*3)
          bandLower3.SetBinContent(bin,1+(bandLower3.GetBinContent(bin)-1)*3)
        bandUpper3.SetLineColor(ROOT.kGray)
        bandLower3.SetLineColor(ROOT.kGray)
        bandUpper3.Draw("h same")
        bandLower3.Draw("h same")

        lineHorizontal = ROOT.TLine()

        lineHorizontal.SetLineColor(0)

        lineHorizontal.SetLineWidth(3)
        lineHorizontal.SetLineStyle(0)
        #lineHorizontal.DrawLine( 2200, 1,
        #                2850, 1 )
        #lineHorizontal.DrawLine( 2200, 1,
        #                2850, 1)

        pad1.Update()

        pad2.cd()

        residualAboveHist = aboveFile.Get("residualHist")

        residualAboveHist.GetXaxis().SetTitle("M_{jj} [GeV]")
        residualAboveHist.GetXaxis().SetTitleFont(43)
        residualAboveHist.GetXaxis().SetTitleSize(textSize)
        residualAboveHist.GetXaxis().SetTitleOffset(3.0)
        residualAboveHist.GetXaxis().SetLabelFont(43)
        residualAboveHist.GetXaxis().SetLabelSize(textSize)
        residualAboveHist.GetXaxis().SetRangeUser(250,2750)

        residualAboveHist.GetYaxis().SetTitle("Significance")
        residualAboveHist.GetYaxis().SetTitleFont(43)
        residualAboveHist.GetYaxis().SetTitleSize(textSize)
        residualAboveHist.GetYaxis().SetTitleOffset(1.5)
        residualAboveHist.GetYaxis().SetLabelFont(43)
        residualAboveHist.GetYaxis().SetLabelSize(textSize)
        residualAboveHist.GetYaxis().SetNdivisions(510)

        #residualAboveHist.GetYaxis().SetRangeUser(-5.,fitHist.GetMaximum*1.1)
        #residualAboveHist.GetYaxis().SetRangeUser(-3,3)

        residualAboveHist.SetLineColor(ROOT.kBlack)
        residualAboveHist.SetLineWidth(2)
        residualAboveHist.SetFillColor(ROOT.kGreen)
        residualAboveHist.SetFillStyle(1001)



        residualBkgOnlyHist = bkgOnlyFile.Get("residualHist")

        residualBkgOnlyHist.GetXaxis().SetTitle("M_{jj} [GeV]")
        residualBkgOnlyHist.GetXaxis().SetTitleFont(43)
        residualBkgOnlyHist.GetXaxis().SetTitleSize(textSize)
        residualBkgOnlyHist.GetXaxis().SetTitleOffset(3.0)
        residualBkgOnlyHist.GetXaxis().SetLabelFont(43)
        residualBkgOnlyHist.GetXaxis().SetLabelSize(textSize)
        residualBkgOnlyHist.GetXaxis().SetRangeUser(250,2750)

        residualBkgOnlyHist.GetYaxis().SetTitle("Significance")
        residualBkgOnlyHist.GetYaxis().SetTitleFont(43)
        residualBkgOnlyHist.GetYaxis().SetTitleSize(textSize)
        residualBkgOnlyHist.GetYaxis().SetTitleOffset(1.5)
        residualBkgOnlyHist.GetYaxis().SetLabelFont(43)
        residualBkgOnlyHist.GetYaxis().SetLabelSize(textSize)

        residualBkgOnlyHist.SetLineColor(ROOT.kRed)
        residualBkgOnlyHist.SetLineStyle(2)
        residualBkgOnlyHist.SetLineWidth(2)
        residualBkgOnlyHist.SetFillColorAlpha(ROOT.kRed,0.2)

        residualBkgOnlyHist.SetFillStyle(1001)
        #residualAboveHist.GetYaxis().SetRangeUser(2*residualBkgOnlyHist.GetMinimum(),-2*residualBkgOnlyHist.GetMinimum())
        residualAboveHist.SetMinimum(-5.9)
        residualAboveHist.SetMaximum(5.5)
        #residualAboveHist.GetYaxis().SetRangeUser(2*residualBkgOnlyHist.GetMinimum(),1.1*residualAboveHist.GetMaximum())
        #residualAboveHist.GetYaxis().SetRangeUser(-4.5,4.5)

        residualAboveHist.Draw()
        residualBkgOnlyHist.Draw("same")


        #vector
        bumpHunterPLowHighAbove = aboveFile.Get('bumpHunterPLowHigh')
        bumpHunterStatValueAbove = bumpHunterPLowHighAbove[0]
        bumpLowEdgeAbove         = bumpHunterPLowHighAbove[1]
        bumpHighEdgeAbove        = bumpHunterPLowHighAbove[2]

        #bumpHunterStatOfFitToDataAbove = aboveFile.Get("bumpHunterStatOfFitToData")
        bumpHunterStatOfFitToDataAbove = aboveFile.Get("bumpHunterStatOfFitToDataInitial")
        bumpHunterPValueAbove    = bumpHunterStatOfFitToDataAbove[1]

        bumpFoundVectorAbove = aboveFile.Get("bumpFound")
        bumpFoundAbove = bumpFoundVectorAbove[0]

        line = ROOT.TLine()

        line.SetLineColor(ROOT.kGreen+1)

        line.SetLineWidth(1)
        line.DrawLine( bumpLowEdgeAbove, -10,
                        bumpLowEdgeAbove, 10 )
        line.DrawLine( bumpHighEdgeAbove, -10,
                        bumpHighEdgeAbove, 10)

        lineHorizontal3 = ROOT.TLine()

        lineHorizontal3.SetLineColor(0)

        lineHorizontal3.SetLineWidth(3)
        lineHorizontal3.DrawLine( 2079+73, 0,
                        2777+77, 0 )
        lineHorizontal3.DrawLine( 2079+73, 0,
                        2777+77, 0)
        lineHorizontal4 = ROOT.TLine()

        lineHorizontal4.SetLineColor(1)

        lineHorizontal4.SetLineWidth(1)
        lineHorizontal4.DrawLine( 2693+73, 0,
                        2779+77, 0 )
        lineHorizontal4.DrawLine( 2693+73, 0,
                        2779+77, 0)

#        lineVert = ROOT.TLine()
#        lineVert.SetLineColor(1)
#        lineVert.SetLineWidth(1)
#        lineVert.DrawLine( 2780, 0.1,
#                        2780, -0.1 )

        lineBla = ROOT.TLine()
        lineBla.SetLineColor(0)
        lineBla.SetLineWidth(13)
        lineBla.DrawLine(300, -3.7, 435, -3.7)


        pad3.cd()

        residualBelowHist = belowFile.Get("residualHist")

        residualBelowHist.GetXaxis().SetTitle("M_{jj} [GeV]")
        residualBelowHist.GetXaxis().SetTitleFont(43)
        residualBelowHist.GetXaxis().SetTitleSize(textSize)
        residualBelowHist.GetXaxis().SetTitleOffset(3.0)
        residualBelowHist.GetXaxis().SetLabelFont(43)
        residualBelowHist.GetXaxis().SetLabelSize(textSize)
        residualBelowHist.GetXaxis().SetRangeUser(250,2750)

        residualBelowHist.GetYaxis().SetTitle("Significance")
        residualBelowHist.GetYaxis().SetTitleFont(43)
        residualBelowHist.GetYaxis().SetTitleSize(textSize)
        residualBelowHist.GetYaxis().SetTitleOffset(1.5)
        residualBelowHist.GetYaxis().SetLabelFont(43)
        residualBelowHist.GetYaxis().SetLabelSize(textSize)
        residualBelowHist.GetYaxis().SetNdivisions(505)
        #residualBelowHist.GetYaxis().SetRangeUser(-5.,fitHist.GetMaximum*1.1)
        #residualBelowHist.GetYaxis().SetRangeUser(-3,3)

        residualBelowHist.SetLineColor(ROOT.kBlack)
        residualBelowHist.SetLineWidth(2)
        residualBelowHist.SetFillColor(ROOT.kBlue)
        residualBelowHist.SetFillStyle(1001)

        residualBelowHist.GetYaxis().SetRangeUser(1.5*residualBkgOnlyHist.GetMinimum(),1.1*residualBelowHist.GetMaximum())
        residualBelowHist.GetYaxis().SetRangeUser(-3.7,5.5)

        residualBelowHist.Draw()
        residualBkgOnlyHist.Draw("same")

        bumpHunterPLowHighBelow = belowFile.Get('bumpHunterPLowHigh')
        bumpLowEdgeBelow         = bumpHunterPLowHighBelow[1]
        bumpHighEdgeBelow        = bumpHunterPLowHighBelow[2]

        excludeWindowVectorBelow = belowFile.Get('excludeWindowNums')
        excludedWindowBelow = excludeWindowVectorBelow[0]
        excludedWindowLowBelow = excludeWindowVectorBelow[1]
        excludedWindowHighBelow = excludeWindowVectorBelow[2]
        excludeWindowVectorAbove = aboveFile.Get('excludeWindowNums')
        excludedWindowAbove = excludeWindowVectorAbove[0]
        excludedWindowLowAbove = excludeWindowVectorAbove[1]
        excludedWindowHighAbove = excludeWindowVectorAbove[2]

        #bumpHunterStatOfFitToDataBelow = belowFile.Get("bumpHunterStatOfFitToData")
        bumpHunterStatOfFitToDataBelow = belowFile.Get("bumpHunterStatOfFitToDataInitial")
        bumpHunterPValueBelow    = bumpHunterStatOfFitToDataBelow[1]

        bumpFoundVectorBelow = belowFile.Get("bumpFound")
        bumpFoundBelow = bumpFoundVectorBelow[0]

        line2 = ROOT.TLine()

        line2.SetLineColor(ROOT.kBlue)

        line2.SetLineWidth(1)
        line2.DrawLine( bumpLowEdgeBelow, residualBelowHist.GetMinimum(),
                        bumpLowEdgeBelow, 2*residualBelowHist.GetMaximum() )
        line2.DrawLine( bumpHighEdgeBelow, residualBelowHist.GetMinimum(),
                        bumpHighEdgeBelow, 2*residualBelowHist.GetMaximum())

        lineHorizontal3 = ROOT.TLine()

        lineHorizontal3.SetLineColor(0)

        lineHorizontal3.SetLineWidth(3)
        lineHorizontal3.DrawLine( 2079+63, 0,
                        2777+77, 0 )
        lineHorizontal3.DrawLine( 2079+63, 0,
                        2777+77, 0)
        lineHorizontal4 = ROOT.TLine()

        lineHorizontal4.SetLineColor(1)

        lineHorizontal4.SetLineWidth(1)
        lineHorizontal4.DrawLine( 2730+63, 0,
                        2779+77, 0 )
        lineHorizontal4.DrawLine( 2730+63, 0,
                        2779+77, 0)


        c.Update()
        print "Gaussian Mean: ", gaussianMean
        outpad.cd()
        #ROOT.ATLAS_LABEL(0.66,0.9)
        #ROOT.myText(0.8,0.9,1,"Internal")
        helperPad1.cd()
        #ROOT.myText(0.5,0.75,1,args.notes+" fb^{-1}")
        ROOT.myText(0.81,0.81,0.07,32,1,"m_{sig} = "+gaussianMean+" GeV")
        ROOT.myText(0.81,0.74,0.07,32,1,"Signal Width = "+gaussianWidth+"%")

        ROOT.myText(0.81,0.55,0.07,32,1,"SWiFt Window Halfwidth: "+windowWidth)

        leg = ROOT.TLegend(0.5,0.34,0.81,0.51)

        leg.SetTextAlign(32)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(20)
        leg.SetBorderSize(0)
        leg.AddEntry(RatioBelowBkgOnly,"Below/Bkg","l")
        leg.AddEntry(RatioAboveBkgOnly,"Above/Bkg","l")
        leg.AddEntry(bandUpper,"Stat. err.","l")
        leg.Draw()

        helperPad2.cd()
        ROOT.myText(0.81,0.75,0.07,32,1,"Signal #event = "+str(discoverySigNumAbove)+" pb")
        ROOT.myText(0.81,0.66,0.07,32,1,"Bump range: %.0f - %.0f"%(bumpLowEdgeAbove,bumpHighEdgeAbove))
        #ROOT.myText(0.45,0.55,1,"bump range: "+str(bumpLowEdgeAbove)+" - "+str(bumpHighEdgeAbove))
        ROOT.myText(0.81,0.43,0.07,32,1,"BH #it{p}-value = "+str(bumpHunterPValueAbove))
        if int(excludedWindowAbove) == 1:
          ROOT.myText(0.81,0.35,0.07,32,1,"Bump range excluded")
        else:
          ROOT.myText(0.81,0.35,0.07,32,1,"Bump range not excluded")


        helperPad3.cd()

        ROOT.myText(0.81,0.70,0.07,32,1,"Signal #sigma = "+str(discoverySigNumBelow)+" pb")
        ROOT.myText(0.81,0.61,0.07,32,1,"Bump range: %.0f - %.0f"%(bumpLowEdgeAbove,bumpHighEdgeBelow))
        #ROOT.myText(0.45,0.55,1,"bump range: "+str(bumpLowEdgeAbove)+" - "+str(bumpHighEdgeAbove))
        ROOT.myText(0.81,0.38,0.07,32,1,"BH #it{p}-value = "+str(bumpHunterPValueBelow))
        if int(excludedWindowBelow) == 1:
          ROOT.myText(0.81,0.30,0.07,32,1,"Bump range excluded")
        else:
          ROOT.myText(0.81,0.30,0.07,32,1,"Bump range not excluded")

        c.Update()

        c.Print(args.dir+"/SigRemovalRatio_GaussWidth_"+gaussianWidth+"_GaussMean_"+gaussianMean+"_windowWidth_"+windowWidth+".pdf")
        c.Print(args.dir+"/SigRemovalRatio_GaussWidth_"+gaussianWidth+"_GaussMean_"+gaussianMean+"_windowWidth_"+windowWidth+".png")
        c.Print(args.dir+"/SignalRemovalRatios_GaussianWidth_"+gaussianWidth+"_"+args.dir+"_WindowWidth_"+windowWidth+".pdf")

    c.Print(args.dir+"/SignalRemovalRatios_GaussianWidth_"+str(gaussianWidth)+"_"+args.dir+"_WindowWidth_"+str(windowWidth)+".pdf]")
      #raw_input("Press Enter to continue...")

