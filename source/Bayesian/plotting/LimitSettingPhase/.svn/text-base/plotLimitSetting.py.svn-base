#!/usr/bin/env python

import ROOT
import os,sys
from art.morisot import Morisot
from array import array
from pprint import pprint
from decimal import Decimal

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence) 
  return new.join(li)

# Get input
xseceffInputFile = ROOT.TFile('./inputs/xsecandacceptance/TheoryCurves_jjj.root')
templateInputFile = ROOT.TFile('./inputs/xsecandacceptance/ZPrime_jjj.root')

# Get results files
searchInputFile = ROOT.TFile('./results/Step1_SearchPhase/Step1_SearchPhase.root')
limitFileNameTemplate = "./results/Step3_LimitSettingPhase/Step3_LimitSettingPhase_{0}.root"
individualLimitFiles = "./results/Step2_setLimitsOneMassPoint/Step2_setLimitsOneMassPoint_{0}{1}_1p04fb.root"

# Options
doSyst = True
do2DZPrime = True
doMixedSignals = False
doMCComparison = False
folderextension = "./plots/"
plotextension = ""

# Define necessary quantities.
Ecm = 13
luminosity = 1000

# make plots folder i.e. make folder extension
if not os.path.exists(folderextension):
    os.makedirs(folderextension)

# Initialize painter
myPainter = Morisot()
#myPainter.setEPS(True)
myPainter.setColourPalette("ATLAS")
myPainter.setLabelType(1) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation
# 0 Just ATLAS    
# 1 "Preliminary"
# 2 "Internal"
# 3 "Simulation Preliminary"
# 4 "Simulation Internal"
# 5 "Simulation"
# 6 "Work in Progress"

# Will run for each signal type you include here.
#signalInputFileTypes = ["ZPrime0p16"]
signalInputFileTypes = ["ZPrime0p10","ZPrime0p20","ZPrime0p30","ZPrime0p40"]#,"ZPrime0p50"]#,"ZPrime0p60","ZPrime0p70","ZPrime0p80","ZPrime0p90"]
#signalInputFileTypes = ["ZPrime0p40"]

# Setup signal info

masses = {} # Define mass points for signals
masses["ZPrime0p16"]    = ["300","400","500","600","700","800","900","1000"]
masses["ZPrime0p10"]    = ["350","450","550"]
masses["ZPrime0p20"]    = ["350","450","550"]
masses["ZPrime0p30"]    = ["350","450","550"]
masses["ZPrime0p40"]    = ["350","450","550"]

SignalTitles = {  "ZPrime0p16": "Z' (g_{q} = 0.16)"
                , "ZPrime0p10": "Z' (g_{q} = 0.10)"
                , "ZPrime0p20": "Z' (g_{q} = 0.20)"
                , "ZPrime0p30": "Z' (g_{q} = 0.30)"
                , "ZPrime0p40": "Z' (g_{q} = 0.40)"
                }

SignalLegends = {  "ZPrime0p16": "Z'"
                , "ZPrime0p10":  "Z'"
                , "ZPrime0p20":  "Z'"
                , "ZPrime0p30":  "Z'"
                , "ZPrime0p40":  "Z'"
                }


SignalAxes = {"ZPrime0p16": {"X" : "m_{Z'} [GeV]", "Y":"#sigma #times #it{A} #times BR [pb]"},
              "ZPrime0p10": {"X" : "m_{Z'} [GeV]", "Y":"#sigma #times #it{A} #times BR [pb]"},
              "ZPrime0p20": {"X" : "m_{Z'} [GeV]", "Y":"#sigma #times #it{A} #times BR [pb]"},
              "ZPrime0p30": {"X" : "m_{Z'} [GeV]", "Y":"#sigma #times #it{A} #times BR [pb]"},
              "ZPrime0p40": {"X" : "m_{Z'} [GeV]", "Y":"#sigma #times #it{A} #times BR [pb]"},
             }

yranges = {}
yranges['ZPrime0p16'] = [5E-3,15]
yranges['ZPrime0p10'] = [5E-3,15]
yranges['ZPrime0p20'] = [5E-3,15]
yranges['ZPrime0p30'] = [5E-3,15]
yranges['ZPrime0p40'] = [5E-3,15]

xranges = {}
AllPlotMaterials = {}

ZPrimeLimits = {} # For 2D plot		
ZPrimeFullInfo = {} # For 2D plot with interpolation made by Karol in different script	
#ZPrimexsec = {'0.16' : {}}
ZPrimexsec = { '0.10' : {},		
               '0.20' : {},		
	       '0.30' : {},		
	       '0.40' : {}}

# Acceptance and efficiency dictionaries for dividing limits  by eff:
# FIXME update
#EffDict = {0.1: {250.0: {'acc': 0.2276500016450882,
#               'acceff': 0.18719999492168427,
#               'eff': 0.8223149289211671},
#       350.0: {'acc': 0.28780001401901245,
#               'acceff': 0.24044999480247498,
#               'eff': 0.8354759662610389},
#       450.0: {'acc': 0.33329999446868896,
#               'acceff': 0.273263156414032,
#               'eff': 0.8198714699939876},
#       550.0: {'acc': 0.33970001339912415,
#               'acceff': 0.28290000557899475,
#               'eff': 0.8327936250229308}},
# 0.2: {250.0: {'acc': 0.22450000047683716,
#               'acceff': 0.18457894027233124,
#               'eff': 0.8221779059255513},
#       350.0: {'acc': 0.3015500009059906,
#               'acceff': 0.24914999306201935,
#               'eff': 0.8262311136244793},
#       450.0: {'acc': 0.32739999890327454,
#               'acceff': 0.27024999260902405,
#               'eff': 0.8254428635134644},
#       550.0: {'acc': 0.3513000011444092,
#               'acceff': 0.28110000491142273,
#               'eff': 0.8001708055670365},
#       750.0: {'acc': 0.37904998660087585,
#               'acceff': 0.30254998803138733,
#               'eff': 0.7981796563152503}},
# 0.3: {100.0: {'acc': 0.014650000259280205,
#               'acceff': 0.011950000189244747,
#               'eff': 0.8156996571842985},
#       200.0: {'acc': 0.07074999809265137,
#               'acceff': 0.07294444739818573,
#               'eff': 1.031016952151159},
#       250.0: {'acc': 0.22020000219345093,
#               'acceff': 0.1836666613817215,
#               'eff': 0.8340901887020236},
#       300.0: {'acc': 0.26570001244544983,
#               'acceff': 0.2223999947309494,
#               'eff': 0.8370341901154775},
#       350.0: {'acc': 0.2992500066757202,
#               'acceff': 0.24639999866485596,
#               'eff': 0.8233917900354979},
#       400.0: {'acc': 0.3138499855995178,
#               'acceff': 0.2558000087738037,
#               'eff': 0.8150390967365292},
#       450.0: {'acc': 0.334850013256073,
#               'acceff': 0.2759000062942505,
#               'eff': 0.8239510090246253},
#       500.0: {'acc': 0.3404499888420105,
#               'acceff': 0.27764999866485596,
#               'eff': 0.8155382809946351},
#       550.0: {'acc': 0.335099995136261,
#               'acceff': 0.2797499895095825,
#               'eff': 0.8348254060577601},
#       750.0: {'acc': 0.36364999413490295,
#               'acceff': 0.29510000348091125,
#               'eff': 0.8114945916139303},
#       950.0: {'acc': 0.3780499994754791,
#               'acceff': 0.3027999997138977,
#               'eff': 0.800952255347213}},
# 0.4: {750.0: {'acc': 0.3655500113964081,
#               'acceff': 0.29357895255088806,
#               'eff': 0.8031156979845543}}}

SeveralLimitsMaterials = {}
SeveralLimitsMaterials["observed"] = []
SeveralLimitsMaterials["legend"] = []
SeveralList = signalInputFileTypes # ["ZPrime0p10","ZPrime0p20","ZPrime0p30","ZPrime0p40","ZPrime0p50"]

##### LOOP over signals in signalInputFileTypes #####

for signal in signalInputFileTypes :

  limitInputFile = ROOT.TFile(limitFileNameTemplate.format(signal))

  axisnames = SignalAxes[signal]
  xname = axisnames["X"]
  yname = axisnames["Y"]

  # Define necessary quantities.
  signalName = signal+"_graph"

  # Limit-setting plots
  outputName = folderextension+"Limits_"+signal+plotextension
  observedGraph = limitInputFile.Get('observedXSecAccVersusMass')
  expectedGraph1Sigma = limitInputFile.Get('expectedXSecAccVersusMass_oneSigma')
  expectedGraph2Sigma = limitInputFile.Get('expectedXSecAccVersusMass_twoSigma')

  if signal in SeveralList:
    SeveralLimitsMaterials["observed"].append(observedGraph)

  # X-check: Scaling observed graph by square root of the ratio of lumis to make equiv to 100 inv pb
  # to check if limits roughly agree with PUB note result for 1000 inv pb (1 inv fb)
  # Should be commented out, except for when doing x-checks!
  #for i in range (0,observedGraph.GetN()):
  # scale = pow(100.0/1000.0,0.5)
  # scale = float(scale) # needed by python to make sure get correct value
  # print "SCALING by "+str(scale)
  # observedGraph.GetY()[i] *= scale
  #for i in range (0,expectedGraph1Sigma.GetN()):
  # expectedGraph1Sigma.GetY()[i] *= scale
  #for i in range (0,expectedGraph2Sigma.GetN()):
  # expectedGraph2Sigma.GetY()[i] *= scale
  #### Scaled MC hereprint "SCALING by "+str(pow(1000/100,0.5))
  ####observedGraph.GetY()[i] *= pow(1000/100,0.5)

  if "ZPrime" in signal :
    code = signal.replace("0p","0")
    code = rreplace(code,"0","",1)
    signalGraph = xseceffInputFile.Get("{0}_graph".format(code))

  if signalGraph == None:
    signalGraph = ROOT.TGraph()
    signalGraph.SetPoint(0,-1,1)
    signalGraph.SetPoint(1,0,1)

  extrasignalGraph = 0
  extraextrasignalGraph = 0

  print "-"*50
  print "SIGNAL: "+signal
  print signalName
  print "-"*50
  print signal

  # Store all hists
  shiftedgraphs = []
  d1, d2 = ROOT.Double(0), ROOT.Double(0)
  for graph in [observedGraph,expectedGraph1Sigma,expectedGraph2Sigma,signalGraph,extrasignalGraph,extraextrasignalGraph] :
    if graph==0 :
      continue
    print graph
    newgraph = graph.Clone()
    newgraph.SetName(graph.GetName()+"_scaled")
    for np in range(newgraph.GetN()):
      newgraph.GetPoint(np,d1,d2)
      #print "Lydia removing first point in graph!" # FIXME
      #if ((graph.GetName() == "ZPrime03_graph") and (np ==0)): continue
      newgraph.SetPoint(np,d1,d2)
      #gSM_EffDict = float(signal.split("ZPrime")[1].replace("p","."))
      #eff = EffDict[gSM_EffDict][d1]['eff']
      #newgraph.SetPoint(np,d1,d2/eff) # Dividing by efficiency from dict NOTE
    shiftedgraphs.append(newgraph)

  # Setup plot axes
  thisx, thisy = ROOT.Double(0), ROOT.Double(0)
  thisyrange = yranges[signal]

  observedGraph.GetPoint(0,thisx,thisy)
  xlow = thisx - 100
  observedGraph.GetPoint(observedGraph.GetN()-1,thisx, thisy)
  xhigh = thisx + 100

  xranges[signal] = [float(xlow/1000),float(xhigh/1000)]
 
  # Fill dictionary for 2D plot
  if (do2DZPrime):
    if "ZPrime" in signal :
      localZPrimeDict = {}
      otherlocalZPrimeDict = {}
      coupling = signal[-4:].replace("p",".")
      print signal, coupling
      print "mass\texp\tobs\ttheory"
      for masspoint in range(shiftedgraphs[0].GetN()) :
        b1, b2, b3, b4,b5 = ROOT.Double(0), ROOT.Double(0),ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
        shiftedgraphs[0].GetPoint(masspoint,b1,b2)
        # For 2D plot made in this script
        thisdict = {}
        thisdict["obs"] = b2
        shiftedgraphs[1].GetPoint(masspoint,b1,b3)
        thisdict["exp"] = b3
        print b1,"\t",b3,"\t",
        print b2,"\t",
        shiftedgraphs[3].GetPoint(masspoint,b4,b5)
        print b5
        localZPrimeDict[b1] = thisdict
        ZPrimexsec[coupling][b4] = b5
        # For 2D plot with interpolation made by Karol in different script
        thisotherdict = {}
        thisotherdict["obs"] = b2
        thisotherdict["exp"] = b3
        thisotherdict["theory"] = b5
        otherlocalZPrimeDict[b1] = thisotherdict
      ZPrimeLimits[coupling] = localZPrimeDict
      ZPrimeFullInfo[coupling] = otherlocalZPrimeDict

      # Loop over mass points again to get 1 sigma and 2 sigma info for Karol
      print "mass\texp 1 sig low\t exp 1 sig high\texp 2 sig 1 low\t exp 2 sig 1 high"
      for masspoint in range(shiftedgraphs[0].GetN()) :
        b1, b2, b3, b4, b5, b6 = ROOT.Double(0), ROOT.Double(0),ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
        shiftedgraphs[1].GetPoint(masspoint,b1,b2)
        b3 = shiftedgraphs[1].GetErrorYlow(masspoint)
        b4 = shiftedgraphs[1].GetErrorYhigh(masspoint)
        b5 = shiftedgraphs[2].GetErrorYlow(masspoint)
        b6 = shiftedgraphs[2].GetErrorYhigh(masspoint)
        print b1,"\t",b3,"\t",b4,"\t",b5,"\t",b6

  # make GeV limit plot
  #newxname = xname.replace("G","T")
  [obs,exp] = myPainter.drawLimitSettingPlot2Sigma(shiftedgraphs[0],shiftedgraphs[1],shiftedgraphs[2],shiftedgraphs[3],SignalTitles[signal],\
     outputName,xname,yname,luminosity,Ecm,xlow,xhigh,thisyrange[0],thisyrange[1],False)

  if signal in SeveralList:
    SeveralLimitsMaterials["legend"].append(SignalTitles[signal])

  # Print out limit values!
  print "-"*50
  print "File",limitFileNameTemplate
  print "Signal",signal
  print "Observed limit at 95% CL:",obs
  print "Expected limit at 95% CL:",exp,"\n"

 
# Get materials for signal overlay plots

SignalMasses = {"ZPrime0p16" : [450],
                "ZPrime0p10" : [450],
                "ZPrime0p20" : [350],
                "ZPrime0p30" : [350],
                "ZPrime0p40" : [350],
                }

SignalScalingFactors = {"ZPrime0p16": 100,
                        "ZPrime0p10": 50,
                        "ZPrime0p20": 50,
                        "ZPrime0p30": 50,
                        "ZPrime0p40": 50,
		       }

# Get basic hists
datahist = searchInputFile.Get("basicData")
datahist.SetDirectory(0)
fithist = searchInputFile.Get("basicBkgFrom4ParamFit")
fithist.SetDirectory(0)
basicSignificancePlot = searchInputFile.Get("relativeDiffHist")
basicSignificancePlot.SetDirectory(0)
residual = searchInputFile.Get("residualHist")
residual.SetDirectory(0)

# get bump info
statOfFitToData = searchInputFile.Get('bumpHunterPLowHigh')
bumpHunterStatFitToData = statOfFitToData[0]
bumpLowEdge = statOfFitToData[1]
bumpHighEdge = statOfFitToData[2]
bumpHunterStatOfFitToData = searchInputFile.Get('bumpHunterStatOfFitToData')
bumpHunterPVal = bumpHunterStatOfFitToData[1]

# and fit info
fitRange = searchInputFile.Get("FitRange")

# Make TeV versions
standardbins = datahist.GetXaxis().GetXbins()
newbins = []#ROOT.TArrayD(standardbins.GetSize())

for np in range(standardbins.GetSize()) :
  newbins.append(standardbins[np]/1000)
newdatahist = ROOT.TH1D("basicData_TeV","basicData_TeV",len(newbins)-1,array('d',newbins))
newfithist = ROOT.TH1D("basicBkgFrom4ParamFit_TeV","basicBkgFrom4ParamFit_TeV",len(newbins)-1,array('d',newbins))
newbasicSignificancePlot = ROOT.TH1D("relativeDiffHist_TeV","relativeDiffHist_TeV",len(newbins)-1,array('d',newbins))
newresidual = ROOT.TH1D("residualHist_TeV","residualHist_TeV",len(newbins)-1,array('d',newbins))

for histnew,histold in [[newdatahist,datahist],[newfithist,fithist],[newbasicSignificancePlot,basicSignificancePlot],[newresidual,residual]] :
  for bin in range(histnew.GetNbinsX()+2) :
    histnew.SetBinContent(bin,histold.GetBinContent(bin))
    histnew.SetBinError(bin,histold.GetBinError(bin))
newsigtemplate = ROOT.TH1D("basicsignal_TeV","basicsignal_TeV",len(newbins)-1,array('d',newbins))

# Find range
firstBin =0
while (fithist.GetBinContent(firstBin)<1 and firstBin < fithist.GetNbinsX()) :
  firstBin+=1
lastBin = fithist.GetNbinsX()+1
while (fithist.GetBinContent(lastBin-1)==0 and lastBin > 0) :
  lastBin-=1
if (firstBin > lastBin) :
  firstBin=1
  lastBin = fithist.GetNbinsX()

mixedSignalCollection = []
mixedTitleCollection = []
mixedUserScaleTextCollection = ""
mixedSignalMassCollection = []
mixedExtLastBin = 0

##### LOOP over signals in signalInputFileTypes #####
for signal in signalInputFileTypes :
  print "in signal",signal

  if "FullSim" in signal :
    continue

  signalMasses = SignalMasses[signal][:]
  signalMassesTeV = SignalMasses[signal][:]
  for index in range(len(SignalMasses[signal])) :
    signalMassesTeV[index] = signalMasses[index]/1000.0
  signalPlots = []
  signalPlotsTeV = []
  sigratioPlots = []
  sigratioPlotsTeV = []
  legendlist = []
  legendlistTeV = []
  labellist = []
  labellistTeV = []
  sigToGet = signal

  if "ZPrime" in signal :
    sigToGet = "ZPrime"
  print "sigToGet is",sigToGet,"for signal",signal
  for mass in signalMasses :

    if "ZPrime" in signal :
      sigplotname = signal.replace("Prime","PrimemR{0}gSM".format(mass))
      #sigplot = templateInputFile.Get("dijetgamma_g130_2j25/Zprime_mjj_var_Scaled_"+sigplotname+"_1p00fb")
      #print "getting: dijetgamma_g130_2j25/mjj_"+sigplotname+"_1fb_nominal"
      print "getting: mjj_"+sigplotname+"_1fb_Nominal"
      #sigplot = templateInputFile.Get("dijetgamma_g130_2j25/mjj_"+sigplotname+"_1fb_Nominal")
      sigplot = templateInputFile.Get("mjj_"+sigplotname+"_1fb_Nominal")
    else :
      sigplot = templateInputFile.Get("mjj_"+sigToGet+"{0}_1fb_Nominal".format(mass))
    sigplot.SetDirectory(0)
    # TEMPORARY
    newsigGeV = datahist.Clone()
    newsigGeV.SetName("sigplot_{0}_{1}_GeV".format(signal,mass))
    for bin in range(newsigGeV.GetNbinsX()+2) :
      if bin < sigplot.GetNbinsX()+1 :
        newsigGeV.SetBinContent(bin,sigplot.GetBinContent(bin))
        newsigGeV.SetBinError(bin,sigplot.GetBinError(bin))
      else :
        newsigGeV.SetBinContent(bin,0.0)
        newsigGeV.SetBinError(bin,0.0)

    sigplottev = newdatahist.Clone()
    sigplottev.SetName("sigplot_{0}_{1}_TeV".format(signal,mass))
    # TEMPORARY: REBIN TO WHAT WE NEED
    # Also find new last bin.
    for bin in range(sigplottev.GetNbinsX()+2) :
      sigplottev.SetBinContent(bin,newsigGeV.GetBinContent(bin))
      sigplottev.SetBinError(bin,newsigGeV.GetBinError(bin))

    index = 0
    extLastBin = lastBin
    for thissigplot,thissuffix in [[newsigGeV,""],[sigplottev,"_TeV"]] :

      # Normalise to correct amount
      # Lydia Updated from thissigplot.Scale(luminosity) as new input templates are 1 inv fb not 1 inv pb
      luminosity = float(luminosity) # cast as float otherwise if divide e.g. 7 by 1000 get 0
      thissigplot.Scale(luminosity/1000)
      sigplotforfitplusbkg = thissigplot.Clone()
      sigplotforfitplusbkg.SetDirectory(0)
      sigplotforfitplusbkg.SetName(thissigplot.GetName()+"_forfitplusbkg"+thissuffix)
      sigplotforfitplusbkg.Scale(SignalScalingFactors[signal])

      sigplotforratio = thissigplot.Clone()
      sigplotforratio.SetDirectory(0)
      sigplotforratio.SetName(thissigplot.GetName()+"_forratio"+thissuffix)


      if index==0 :
        sigplotforratio.Divide(fithist)
        signalPlots.append(sigplotforfitplusbkg)
        sigratioPlots.append(sigplotforratio)
        thistitle = SignalLegends[signal] + ", %s= %d GeV" % (SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass)
        legendlist.append(thistitle)
        thislabel = SignalLegends[signal] + ", %s= %d GeV" % (SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass)
        UserScaleText = SignalTitles[signal]
        if SignalScalingFactors[signal] == 1 :
          UserScaleText = SignalTitles[signal]+", %s= %d GeV" % (SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass)
        else :
          UserScaleText = UserScaleText+", %s= %d GeV,  #sigma #times %s " % (SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass,str(SignalScalingFactors[signal]))
        print "LABELLLLLLLLLLLLL"
        print UserScaleText
        labellist.append(UserScaleText)

      else :
        sigplotforratio.Divide(newfithist)
        signalPlotsTeV.append(sigplotforfitplusbkg)
        sigratioPlotsTeV.append(sigplotforratio)
        thistitle = SignalLegends[signal] + ", {0}= {1} TeV".format(SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass/1000.0)
        legendlistTeV.append(thistitle)

        for bin in range(sigplotforfitplusbkg.GetNbinsX()+2) :
          if bin > extLastBin and sigplotforfitplusbkg.GetBinContent(bin) > 0.01 :
            extLastBin = bin
          if sigplotforfitplusbkg.GetBinLowEdge(bin) > 1.3*mass/1000.0 :
            continue
        if extLastBin < lastBin :
          extLastBin = lastBin 

        # For making mixed signals plot
        if (doMixedSignals):
          if (signal == "QStar" and signalMasses.index(mass) == 0) or (signal == "BlackMax" and signalMasses.index(mass) == 1) :
            mixedSignalCollection.append(sigplotforfitplusbkg)
            mixedTitleCollection.append(thistitle)
            if SignalScalingFactors[signal] == 1 :
              mixedUserScaleTextCollection += "{"+SignalTitles[signal]+"}"
            else :
              mixedUserScaleTextCollection+="{"+SignalTitles[signal]+",  #sigma #times "+str(SignalScalingFactors[signal])+"}"
            if mixedExtLastBin < extLastBin :
              mixedExtLastBin = extLastBin
            mixedSignalMassCollection.append(signalMassesTeV[signalMasses.index(mass)])

      index = index+1

  #UserScaleText = SignalTitles[signal]
  #if SignalScalingFactors[signal] == 1 :
  #  UserScaleText = SignalTitles[signal]
  #else :
  #  UserScaleText = UserScaleText+",  #sigma #times "+str(SignalScalingFactors[signal])

  ##################################################
  # Signal overlay plots, 'Fancy figures' 
  ##################################################

  # Do GeV plots
  #outputName = folderextension+"SignalsOnSignificancePlot_"+signal+plotextension
  #myPainter.drawSignalOverlaidOnBkgPlot(basicSignificancePlot,sigratioPlots,signalMasses,legendlist,\
  #          luminosity,Ecm,"[data - fit]/fit",outputName,firstBin,lastBin-1)

  #outputName = folderextension+"SignalsOnFitPlusBkg_"+signal+plotextension
  #myPainter.drawSignalOverlaidOnDataAndFit(newdatahist,newfithist,signalPlots,signalMasses,legendlist,\
   #         luminosity,Ecm,"Events",outputName,firstBin,lastBin-1,True,True)

  doRightLeg = False

  if "QStar" in signal or "WPrime" in signal or "ZPrime" in signal:
    doRightLeg = True

  outputName = folderextension+"FancyFigure1_"+signal+plotextension
  myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,signalPlots,\
     sigratioPlots,signalMasses,legendlist,"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
     outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,doRightLeg,labellist,True,bumpHunterPVal,False,-999,-999,None,5E3,5E6)

  outputName = folderextension+"FancyFigure1WithFitLabels_"+signal+plotextension
  myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,signalPlots,\
     sigratioPlots,signalMasses,legendlist,"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
     outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,doRightLeg,labellist,True,bumpHunterPVal,True,fitRange[0],fitRange[1],None,5E3,5E6)


  ##################################################
  # Systematics x-check plots
  ##################################################

  if (doSyst) :
    # Cross-check plots
    # NOT INCLUDING ISR ACC ATM!!!! systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity","JER":"JER", "PDFAcc":"PDF acceptance", "ISRAcc":"ISR acceptance","mjj_{0}_1fb_JET_GroupedNP_1":"Grouped NP 1","mjj_{0}_1fb_JET_GroupedNP_2":"Grouped NP 2","mjj_{0}_1fb_JET_GroupedNP_3":"Grouped NP 3","mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure":"#eta intercalibration non-closure"}
    systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity","JER":"JER", "PDFAcc":"PDF acceptance","mjj_{0}_1fb_JET_GroupedNP_1":"Grouped NP 1","mjj_{0}_1fb_JET_GroupedNP_2":"Grouped NP 2","mjj_{0}_1fb_JET_GroupedNP_3":"Grouped NP 3","mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure":"#eta intercalibration non-closure"}
    #systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity", "PDFAcc":"PDF acceptance"}
    for mass in masses[signal]:
      print "NOT MAKING ISR ACC POSTERIOR PLOT ATM!!!!!!!! ADD BK IN IF WANT IT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

      # Cross-check plots: compare residual from search phase to that
      # from comparing the best fit in all nuisance parameters, background, and signal to data
      filename = individualLimitFiles.format(signal, mass)

      inputfile = ROOT.TFile(filename)
      print "in input file",filename
      fit2 = inputfile.Get("BestFullPrediction")
      fit2.SetDirectory(0)
      residual2 = inputfile.Get("residual_bestfitToData")
      residual2.SetDirectory(0)

      newfit2 = ROOT.TH1D("fit2_TeV","fit2_TeV",len(newbins)-1,array('d',newbins))
      newresidual2 = ROOT.TH1D("residual2_TeV","residual2_TeV",len(newbins)-1,array('d',newbins))

      for histnew,histold in [[newfit2,fit2], [newresidual2,residual2]] :
        for bin in range(histnew.GetNbinsX()+2) :
          histnew.SetBinContent(bin,histold.GetBinContent(bin))
          histnew.SetBinError(bin,histold.GetBinError(bin))

      residual2.GetYaxis().SetNdivisions(604)

      outputName = folderextension+"NominalAndBestFits_{0}_m{1}TeV".format(signal,mass)+plotextension
      #myPainter.drawMultipleFitsAndResiduals(datahist,[fithist,fit2],[residual,residual2],["Nominal fit","Best fit in all #theta"],\
	#"m_{jj} [GeV]","Events",[" Significance","Significance   "],outputName,luminosity,Ecm,\
	#firstBin,lastBin-1,False,0,0,True,False,False,11,-1,True,["Nominal","Best Fit"],5E3,5E6)

      myPainter.drawMultipleFitsAndResiduals(datahist,[fithist,fit2],[residual,residual2],["Nominal fit","Best fit"],\
	"m_{jj} [GeV]","Events",[" Significance","Significance   "],outputName,luminosity,Ecm,\
	firstBin,lastBin-1,False,0,0,True,False,False,11,-1,True,["Nominal","Best Fit"],5E3,5E6)
      #outputName = folderextension+"NominalAndBestFits_{0}_m{1}TeV_megazoom".format(signal,mass)+plotextension
      #myPainter.drawMultipleFitsAndResiduals(newdatahist,[newfithist,newfit2],[newresidual,newresidual2],["Nominal fit","Best fit in all #theta"],\
      #"m_{jj} [TeV]","Events",["Nominal","Best Fit  "],outputName,luminosity,Ecm,\
      #newdatahist.FindBin(1.55),newdatahist.FindBin(1.74),False,0,0,True,False,notLogY=True)

      # Posteriors with CLs
      signalpost = inputfile.Get("likelihoodFunction")
      signalpost.SetDirectory(0)
      signalCL = inputfile.Get("CLOfRealLikelihood")[0]

      outputName = folderextension+"SignalPosteriorWith95CL_{0}_m{1}TeV".format(signal,mass)
      inlist = [signalpost,signalCL]
      myPainter.drawPosteriorsWithCLs([inlist],["Signal posterior"],luminosity,Ecm,outputName,2,True,False,True)

      for syst in systDict.keys() :

        gaus = ROOT.TF1("template_f", "gaus", 3.5,-3.5)
        gaus.SetParameters(1,0,1.0)

        sigplotname = signal.replace("Prime","PrimemR{0}gSM".format(mass))

        if 'JET_' in syst:
          print "Getting",syst.format(sigplotname)#sigToGet,int(mass))
          gaushist = inputfile.Get(syst.format(sigplotname)).Clone()
          #key = inputfile.GetKey(syst.format(sigplotname))
          #gaushist = key.ReadObjectAny(ROOT.TH1D.Class())
          #ROOT.TPython.ObjectProxy_FromVoidPtr(gaushist,"TH1D")
          #print "TUPE"
          #print type(gaushist)

        else:
          gaushist = inputfile.Get(syst).Clone()
        gaushist.Reset("ICE")

        for bin in range(1,gaushist.GetNbinsX()+1) :
          cent = gaushist.GetBinCenter(bin)
          width = gaushist.GetBinWidth(bin)
          gaushist.SetBinContent(bin,gaus.Eval(cent)*width)
          gaushist.SetBinError(bin,0)

        gaushist.Scale(1.0/gaushist.Integral())
        gaushist.SetDirectory(0)

        if 'JET_' in syst:
          #systhist = inputfile.Get(syst.format(sigToGet,int(mass))).Clone(syst+"_mine")
          systhist = inputfile.Get(syst.format(sigplotname)).Clone(syst+"_mine")
          systhist.SetDirectory(0)
        else:
          systhist = inputfile.Get(syst.format(mass)).Clone(syst+"_mine")
          systhist.SetDirectory(0)

        cl = -100
        systhist.Scale(1.0/systhist.Integral())
        pair = [systhist,[cl]]
        pairs = [pair]

        if 'JET_' in syst:
          outputname = folderextension+"posterior_"+syst.format(signal,mass)+"_{0}_{1}".format(signal,mass)+plotextension
        else:
          outputname = folderextension+"posterior_"+syst+"_{0}_{1}".format(signal,mass)+plotextension
        shortnames = [systDict[syst]]

        if 'FUNC' in syst :
          myPainter.drawPosteriorsWithCLs(pairs,shortnames,luminosity,Ecm,outputname,0,True,False,False,False,[gaushist],False,"Nuisance parameter [0 ,1]")
        else :
          myPainter.drawPosteriorsWithCLs(pairs,shortnames,luminosity,Ecm,outputname,0,True,False,False,False,[gaushist],False,"Nuisance parameter, #sigma")

      inputfile.Close()

##################################################
# Overlay observed limits for each Z' signal 
##################################################

myPainter.drawSeveralObservedLimits(SeveralLimitsMaterials["observed"],SeveralLimitsMaterials["legend"],folderextension+"MultiLimits"+plotextension,SignalAxes['ZPrime0p10']["X"],SignalAxes['ZPrime0p10']["Y"],luminosity,Ecm,200,1400,1.5E-2,1)#yranges['ZPrime0p10'][1])

##################################################
# Signal overlay plots, 'Fancy figures' no signals
##################################################

outputName = folderextension+"FancyFigure1_NoSignals"+plotextension
myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,[],\
  [],[],[],"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
  outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,False,"",False,-999,False,-999,-999,None,5E3,5E6)

outputName = folderextension+"FancyFigure1WithFitLabels_NoSignals"+plotextension
myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,[],\
  [],[],[],"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
  outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,False,"",True,bumpHunterPVal,True,fitRange[0],fitRange[1],None,5E3,5E6)

##################################################
# Signal overlay plots, 'Fancy figures' for mixed signals
##################################################

if (doMixedSignals):
  outputName = folderextension+"FancyFigure1_BothSignals"+plotextension
  myPainter.drawDataAndFitWithSignalsOverSignificances(newdatahist,newfithist,newbasicSignificancePlot,newresidual,mixedSignalCollection,\
  [],mixedSignalMassCollection,mixedTitleCollection,"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
  outputName,luminosity,Ecm,firstBin,mixedExtLastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,True,False,False)

  outputName = folderextension+"FancyFigure1WithFitLabels_BothSignals"+plotextension
  myPainter.drawDataAndFitWithSignalsOverSignificances(newdatahist,newfithist,newbasicSignificancePlot,newresidual,mixedSignalCollection,\
  [],mixedSignalMassCollection,mixedTitleCollection,"m_{jj} [GeV]","Events","[data-fit]/fit","1Significance ",\
  outputName,luminosity,Ecm,firstBin,mixedExtLastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,True,False,False,mixedUserScaleTextCollection,True,bumpHunterPVal,True,fitRange[0],fitRange[1])

##################################################
# Make 2D Z' limit plot
##################################################

if (do2DZPrime):

  TwoDPlotMaterials = {}
  aZPrime = False
  for signal in signalInputFileTypes :
    if "ZPrime" in signal : aZPrime = True
  if aZPrime :
    print "ZPrime cross sections times acceptances are"
    pprint(ZPrimexsec)
    print "And ZPrime observed limits are"
    pprint(ZPrimeLimits)
    print "And Full ZPrime info for Karol 2D plot made in other script are"
    pprint(ZPrimeFullInfo)

    couplings = ['0.10', '0.20', '0.30' , '0.40']#, '0.50']
    masses = [350.0,450.0,550.0]#,0.6,0.65,0.7,0.75]

    #h = ROOT.TH2F("mulimit","",4,0.15,0.55,10,0.,1.)
    h = ROOT.TH2F("mulimit","",3,300.,600.,5,0.,1.)


    print "ZPRIMELIMITS !!!!"
    print ZPrimeLimits

    print "ZPRIMEXSEC !!!!"
    print ZPrimexsec
    for g in couplings:
      for m in masses:
          if not g in ZPrimexsec: continue
          if not m in ZPrimeLimits[g].keys(): continue

          print "doing g, m",g,m
 
          print ZPrimexsec
          print "COMPARE"
          print ZPrimeLimits 
          print "Calculation is",ZPrimeLimits[g][m]["obs"],"/",(ZPrimexsec[g][m]),"=",ZPrimeLimits[g][m]["obs"]/(ZPrimexsec[g][m])

          thisval = ZPrimeLimits[g][m]["obs"]/(ZPrimexsec[g][m])
          writeval = float("%.2g" %thisval) #round(thisval,1)#'{0}'.format(float('%.3g' % thisval))
          #writeval = Decimal(thisval)
          print writeval
          h.Fill( m , g , writeval )

    TwoDPlotMaterials["hist"] = h
    TwoDPlotMaterials["xAxisName"] = "M_{Z'} [GeV]"
    TwoDPlotMaterials["yAxisName"] = "g_{q}"
    TwoDPlotMaterials["zAxisName"] = "#sigma_{limit}/#sigma_{theory}"
    TwoDPlotMaterials["signalLabel"] = "Z'"

    # Do the 2D Z' plot
    outputName = folderextension+"ZPrime_2D"
    #myPainter.draw2DLimit(h,outputName,"M_{Z'} [TeV]",0.3,0.6,"g_{q}",0.0,0.50,"#sigma_{limit}/#sigma_{theory}",luminosity,Ecm)
    myPainter.draw2DLimit(h,outputName,"M_{Z'} [GeV]",300.,600.,"g_{q}",0.0,0.8,"#sigma_{limit}/#sigma_{theory}",luminosity,Ecm)

##################################################
# Make figure 1 with MC comparison in ratio
##################################################

if (doMCComparison): # FIXME temporary solution to chop plot at 8 TeV, where JES bands end 

  mixedExtLastBin = 130

  mcfile = ROOT.TFile("./inputs/MCForComparison/mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final.root")		
  mchist = mcfile.Get("mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final")		
  mchist.SetDirectory(0)		
  mcfile.Close()

  mcUPfile = ROOT.TFile("./inputs/MCForComparison/mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final_UP.root")		
  mcUPhist = mcUPfile.Get("mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final_UP")		
  mcUPhist.SetDirectory(0)		
  mcUPfile.Close()

  mcDOWNfile = ROOT.TFile("./inputs/MCForComparison/mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final_DOWN.root")		
  mcDOWNhist = mcDOWNfile.Get("mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final_DOWN")	
  mcDOWNhist.SetDirectory(0)		
  mcDOWNfile.Close()

  tmpRatioHist = newdatahist.Clone()
  tmpRatioHist.SetMarkerColor(ROOT.kBlack)
  tmpRatioHist.Add(mchist,-1)
  tmpRatioHist.Divide(mchist)

  UpDownHists = []

  if mcUPhist.GetEntries() >= 0:
    tmpJESRatioHistup = mcUPhist
    tmpJESRatioHistup.Add( mchist, -1. )
    tmpJESRatioHistup.Divide( mchist )
    tmpJESRatioHistup.SetMarkerColorAlpha( ROOT.kBlue,0.15)
    tmpJESRatioHistup.SetLineColorAlpha( ROOT.kBlue,0.15)
    tmpJESRatioHistup.SetFillColorAlpha( ROOT.kBlue, 0.15)
    tmpJESRatioHistup.SetFillStyle(1001)
    UpDownHists.append(tmpJESRatioHistup) 

  print mcDOWNhist.GetEntries()
  if mcDOWNhist.GetEntries() >= 0:
    tmpJESRatioHistdown = mcDOWNhist.Clone()
    tmpJESRatioHistdown.Add( mchist, -1. )
    tmpJESRatioHistdown.Divide( mchist )
    tmpJESRatioHistdown.SetMarkerColorAlpha( ROOT.kBlue,0.15)
    tmpJESRatioHistdown.SetLineColorAlpha( ROOT.kBlue,0.15)
    tmpJESRatioHistdown.SetFillColorAlpha( ROOT.kBlue, 0.15)
    tmpJESRatioHistdown.SetFillStyle(1001)
    UpDownHists.append(tmpJESRatioHistdown) 

  ## If data is 0 then there should be no ratio drawn
  for iBin in range(1, tmpRatioHist.GetNbinsX()+1):
    if newdatahist.GetBinContent(iBin) == 0:
      tmpRatioHist.SetBinContent(iBin, 0)
      tmpRatioHist.SetBinError(iBin, 0)
  
  outputName = folderextension+"FancyFigure1WithFitLabels_WithMCRatio_BothSignals"+plotextension		
  myPainter.test(newdatahist,newfithist,newbasicSignificancePlot,newresidual,mixedSignalCollection,\
    [],mixedSignalMassCollection,mixedTitleCollection,"m_{jj} [TeV]","Events","#frac{Data-MC}{MC}","#splitline{Significance}{data - fit}",\
    outputName,luminosity,Ecm,firstBin,mixedExtLastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,True,False,False,mixedUserScaleTextCollection,True,bumpHunterPVal,True,fitRange[0],fitRange[1],mchist,tmpRatioHist,UpDownHists[0],UpDownHists[1])

