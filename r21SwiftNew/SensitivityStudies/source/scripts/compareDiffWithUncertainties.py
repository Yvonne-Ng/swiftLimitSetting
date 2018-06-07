#!/bin/python
import ROOT
from ROOT import TH1F, TFile, TCanvas, TPad, TGraphErrors, TGraph
import numpy
from fileNamingTool import *
import argparse
import array
import ROOT as r

def getDiffInMass(SPFileDir, bkgCountOfMass, mass, windowWidth ):
    """For each mass point figure out the difference between the case where there is no signal and just below"""
    rootName=findLabelledFileName(SPFileDir, mass, windowWidth)
    f=TFile.Open(rootName)
    h1=f.Get("basicBkgFrom4ParamFit")
    binNum=h1.FindBin(mass)
    yh1.GetBinContent(binNum)

def loopDiffInMass(windowWidth):
    """for each window width and eventually signal width , looop through different mass points to find the difference bwteen justbelow and no signal event counts bkg estimate in the mass point"""
    for mass in massRange:
        getDiffInMass

    rootName=findLabelledFileName(SPFileDir, mass, windowWidth)

def loopbkgUncertainties(histogram, massRange):
    """return a list of the bkgUncertainties """


#TODO verification that all no signal files have very similar estimates
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--rootFileDir", default="")
    parser.add_argument("--config", default="")
    args=parser.parse_args()


    #---reading configuration
    #I should eventually fix the config file....
    #default config for testing
    #only plotting the mass points
    if args.config=="":
        config={"massRange":[400, 500, 600, 700, 800, 900],
                "windowWidthRange": [12,10],
                #"lowBinEdge":[169.0, 180.0, 191.0, 203.0, 216.0, 229.0, 243.0, 257.0, 272.0, 287.0, 303.0, 319.0, 335.0, 352.0, 369.0, 387.0, 405.0, 424.0, 443.0, 462.0, 482.0, 502.0, 523.0, 544.0, 566.0, 588.0, 611.0, 634.0,  657.0, 681.0, 705.0, 730.0, 755.0, 781.0, 807.0, 834.0, 861.0, 889.0, 917.0, 946.0, 976.0, 1006.0, 1037.0, 1068.0, 1100.0, 1133.0, 1166.0, 1200.0, 1234.0, 1269.0, 1305.0, 1341.0, 1378.0, 1416.0, 1454.0, 1493.0, 1533.0, 1573.0, 1614.0, 1656.0,1698.0, 1741.0, 1785.0, 1830.0, 1875.0, 1921.0,1968.0, 2016.0, 2065.0, 2114.0, 2164.0, 2215.0, 2267.0, 2320.0, 2374.0, 2429.0, 2485.0, 2542.0, 2600.0, 2659.0, 2719.0, 2780.0, 2842.0, 2905.0, 2969.0, 3034.0, 3100.0, 3167.0, 3235.0, 3305.0, 3376.0, 3448.0, 3521.0, 3596.0, 3672.0, 3749.0, 3827.0, 3907.0, 3988.0, 4070.0, 4154.0, 4239.0, 4326.0, 4414.0, 4504.0, 4595.0, 4688.0, 4782.0, 4878.0, 4975.0, 5074.0, 5175.0, 5277.0, 5381.0, 5487.0, 5595.0, 5705.0, 5817.0, 5931.0, 6047.0, 6165.0, 6285.0,6407.0, 6531.0, 6658.0, 6787.0,6918.0, 7052.0, 7188.0, 7326.0, 7467.0, 7610.0, 7756.0, 7904.0, 8055.0, 8208.0, 8364.0, 8523.0, 8685.0, 8850.0, 9019.0, 9191.0, 9366.0, 9544.0, 9726.0, 9911.0, 10100.0, 10292.0, 10488.0, 10688.0, 10892.0, 11100.0, 11312.0, 11528.0, 11748.0, 11972.0, 12200.0, 12432.0, 12669.0, 12910.0, 13156.0]}
                "lowBinEdge":[169.0, 180.0, 191.0, 203.0, 216.0, 229.0, 243.0, 257.0, 272.0, 287.0, 303.0, 319.0, 335.0, 352.0, 369.0, 387.0, 405.0, 424.0, 443.0, 462.0, 482.0, 502.0, 523.0, 544.0, 566.0, 588.0, 611.0, 634.0,  657.0, 681.0, 705.0, 730.0, 755.0, 781.0, 807.0, 834.0, 861.0, 889.0, 917.0, 946.0, 976.0, 1006.0, 1037.0, 1068.0, 1100.0, 1133.0, 1166.0, 1200.0, 1234.0],
                "modelName":"Gauss_width7",  # can only take one value
                "SeriesName":"TrijetAprInclusiveSearchPhaseFluctuation"
                }

        #for windowWidth
#-> throw this into a function if possible
        windowWidth=12
        for windowWidth in config["windowWidthRange"]:
            print ("gh 1")
            ROOT.gROOT.SetBatch(True)
            c1=TCanvas()
            NSMassPoint=TH1F("NoSignal_"+str(windowWidth), "NoSignal_"+str(windowWidth),len(config["lowBinEdge"])-1, array.array("f",config["lowBinEdge"]))
            print("NSWMassPoint after new window: ", windowWidth, ": ",NSMassPoint)
            JBMassPoint=TH1F("Just above", "just above",len(config["lowBinEdge"])-1, array.array("f", config["lowBinEdge"]))
            NSErrorBar=TGraphErrors(len(config["massRange"]))
            JBGraph=TGraph(len(config["massRange"]))
            # diff between JBMassPpint and the NSMAssPoint
            diffInMassPoint=TH1F("diff", "diff", len(config["lowBinEdge"])-1, array.array("f", config["lowBinEdge"]))
            diffGraph=TGraph(len(config["massRange"]))
            #pointY=zero, error bar= bkg estimate error bar
            diffGraphError=TGraphErrors(len(config["massRange"]))

            print ("gh 2")
            i=0
            for mass in config["massRange"]:
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                try:
                    noSignalRootFile=findLabelledFileName(args.rootFileDir, "NOSIGNAL", config["modelName"],  mass, windowWidth, config["SeriesName"])
                except:
                    continue

                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                fBkg=TFile.Open(noSignalRootFile)
                r.gROOT.cd()
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                hBkgEstimate=fBkg.Get("basicBkgFrom4ParamFit")
    # finding the contnet /error in each of the mass point
                # set bin for just below
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                bkgBin=hBkgEstimate.FindBin(mass)
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                bkgBinCenter=hBkgEstimate.GetBinCenter(bkgBin)
                print("hBkgEstimate", hBkgEstimate)
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                NSMassPoint.SetBinContent(bkgBin, hbkgestimate.getbincontent(bkgbin))
                print("print bin content":hbkgestimate.getbincontent(bkgbin))

                NSMassPoint.SetBinError(i, hBkgEstimate.GetBinError(bkgBin))
                NSErrorBar.SetPoint(i,bkgBinCenter,  hBkgEstimate.GetBinContent(bkgBin))
                NSErrorBar.SetPointError(i, 0.0, hBkgEstimate.GetBinError(bkgBin))
                print("i: ", i, "x: ", mass, "y: ", hBkgEstimate.GetBinContent(bkgBin))

                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                justBelowRootFile= findLabelledFileName(args.rootFileDir, "JUSTBELOW", config["modelName"],mass, windowWidth, config["SeriesName"])
                print("just below: ", justBelowRootFile)
                print("checkpt1")
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                fJustBelow=TFile.Open(justBelowRootFile)
                r.gROOT.cd()
                print("NSWMassPoint @ new mass: ",mass, ": ",NSMassPoint)
                hJustBelow=fJustBelow.Get("basicBkgFrom4ParamFit")
                # set  bin for just above
                jaBin=hJustBelow.FindBin(mass)
                #JBMassPoint.SetBinContent(jaBin, hJustBelow.GetBinContent(jaBin))
                JBGraph.SetPoint(i,bkgBinCenter, hJustBelow.GetBinContent(jaBin))
                #JBMassPoint.SetBinError(jaBin, hJustBelow.GetBinError(jaBin))
                diffInMassPoint.SetBinContent(jaBin, hJustBelow.GetBinContent(jaBin)-hBkgEstimate.GetBinContent(jaBin))
                diffGraph.SetPoint(i,bkgBinCenter, hJustBelow.GetBinContent(jaBin)-hBkgEstimate.GetBinContent(jaBin))
                diffGraphError.SetPoint(i, bkgBinCenter, 0.0)
                diffGraphError.SetPointError(i, 0.0, hBkgEstimate.GetBinError(bkgBin))
                i=i+1

            print ("gh 3")
        #-----Canvas things (stolen from morisot)
            print ("gh 3.5")
            #c1.SetLogx()
            #c1.SetLogy()

            print ("gh 4")
            # Dimensions: xlow, ylow, xup, yup
            outpad = ROOT.TPad("extpad","extpad",0,0,1,1) # For marking outermost dimensions
            pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,0.95) # For main histo
            pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.3) # For residuals histo

            print ("gh 5")
            # Set up to draw in right orientations
            outpad.SetFillStyle(4000) #transparent
            pad1.SetBottomMargin(0.00001)
            pad1.SetBorderMode(0)
            #pad1.SetLogy(1)
            #        pad1.SetLogx()
            pad2.SetTopMargin(0.00003)
            pad2.SetBottomMargin(0.43)
            pad2.SetBorderMode(0)
            #pad2.SetLogx()
            pad1.Draw()
            pad2.Draw()
            outpad.Draw()

            # Publication-friendly margins
            pad1.SetLeftMargin(0.1)
            pad2.SetLeftMargin(0.1)
            pad1.SetTopMargin(0.09)
            pad1.SetRightMargin(0.02)
            pad2.SetRightMargin(0.02)
            outpad.Draw()
        #-------end of canvas BS
    #--drawing on pad1

            print ("gh 6")
            pad1.cd()
            NSMassPoint.GetXaxis().SetLabelSize(0.15)
            NSMassPoint.GetYaxis().SetLabelSize(0.05)
            NSMassPoint.GetYaxis().SetTitleOffset(0.42) # 1.2 = 20% larger
            NSMassPoint.SetTitleOffset(0.42) # 1.2 = 20% larger
            NSMassPoint.SetTitle("Bkg Estimtae in each signal injected mass point: Trijet Inclusive Window: "+str(windowWidth))
            NSMassPoint.SetMarkerStyle(1)
            NSMassPoint.GetYaxis().SetRange(1, 1000000)
            NSMassPoint.SetMarkerColor(0)
            NSMassPoint.SetLineColor(0)
            NSMassPoint.Draw() #this is to make sure the x axis of pad1 mataches that of pad2
            NSErrorBar.SetFillColor(29)
            NSErrorBar.SetMarkerColor(1)
            NSErrorBar.Draw("LE3 same")
            NSErrorBar.Draw("P same")
            #NSMassPoint.Draw("E same")
            print("N : ", NSErrorBar.GetN())
            #NSErrorBar.Draw("P")

            #JBMassPoint.SetMarkerStyle(2)
            #JBMassPoint.SetMarkerColor(2)
            #JBMassPoint.SetLineColor(2)
            #JBMassPoint.Draw("P same")
            JBGraph.SetMarkerStyle(5)
            JBGraph.SetMarkerColor(2)
            JBGraph.SetLineColor(2)
            JBGraph.Draw("P same")
            r.gStyle.SetOptStat(0);

            #leg = ROOT.TLegend(0.5,0.34,0.81,0.51)
            leg = ROOT.TLegend(0.6,0.7,0.99,0.90)

            #leg.SetTextAlign(32)
            #leg.SetFillColor(0)
            #leg.SetFillStyle(0)
            #leg.SetTextFont(43)
            #leg.SetTextSize(20)
            #leg.SetBorderSize(0)
            leg.AddEntry(NSErrorBar,"\"No Signal\" Bkg Pred. With Error","lfp")
            leg.AddEntry(JBGraph,"\"Just Below\" Bkg Pred. ","p")
            leg.Draw("same")
    #----drawing on pad 2 (the difference )
            pad2.cd()
            #----bs to set the difference correctly
            diffInMassPoint.GetYaxis().SetTitleSize(0.06)
            diffInMassPoint.SetTitle("")
            diffInMassPoint.GetYaxis().SetTitleOffset(0.42) # 1.2 = 20% larger
            diffInMassPoint.GetYaxis().SetLabelSize(0.05)

            diffInMassPoint.GetYaxis().SetTitle("\"JustBelow\" - \"NoSignal\" pred.")
            diffInMassPoint.GetXaxis().SetLabelSize(0.05)
            diffInMassPoint.GetXaxis().SetTitleSize(0.07)
            diffInMassPoint.GetXaxis().SetTitleOffset(1.2)
            diffInMassPoint.GetXaxis().SetTitle("mass where signal is injected")
            diffInMassPoint.GetYaxis().SetNdivisions(805)#5,10,0)

            diffInMassPoint.SetFillColor(0)
            diffInMassPoint.SetLineColor(0)
            diffInMassPoint.SetLineColor(0)
            #diffInMassPoint.GetYaxis().SetRange(0,1200)
            diffInMassPoint.Draw()
            diffGraphError.SetFillColor(29)
            diffGraphError.Draw("E3 same")

            diffGraph.SetMarkerStyle(5)
            diffGraph.SetMarkerSize(2)
            diffGraph.SetMarkerColor(r.kBlue)
            diffGraph.Draw("l same")

            r.gStyle.SetOptStat(0);
            #leg2 = ROOT.TLegend(0.6,0.7,0.95,0.95)
            leg2 = ROOT.TLegend(0.6,0.7,0.99,0.95)

            #leg2.SetTextAlign(32)
            #leg2.SetFillColor(0)
            #leg2.SetFillStyle(0)
            #leg2.SetTextFont(43)
            #leg2.SetTextSize(20)
            #leg2.SetBorderSize(0)
            leg2.AddEntry(diffGraphError,"\"No Signal\" Bkg Pred. Error","f")
            leg2.AddEntry(diffGraph,"\"Just Below\"- \"No Signal\" Bkg Pred","l")
            leg2.Draw("same")

            print ("gh 7")
            c1.SaveAs("/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftClean/swiftLimitSetting/r21SwiftNew/SensitivityStudies/source/scripts/testLine_"+config["modelName"]+"_"+"windowWidth"+str(windowWidth)+".pdf")
            #hJustBelow.IsA.Destructor(hJustBelow)
            #hJustAbove.IsA.Destructor(hJustAbove)

            print("NSWMassPoint: ", NSMassPoint)
            NSMassPoint.IsA().Destructor(NSMassPoint)
            diffInMassPoint.IsA().Destructor(diffInMassPoint)
            c1.Close()


            #--- end of bs to set the difference pad correctly



