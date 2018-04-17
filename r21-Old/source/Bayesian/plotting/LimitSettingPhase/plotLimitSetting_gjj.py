#!/usr/bin/env python

import ROOT
import os,sys
from art.morisot_gjj import Morisot_gjj
from array import array
from pprint import pprint
from decimal import Decimal

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence) 
  return new.join(li)

# Get input
xseceffInputFile = ROOT.TFile('./inputs/xsecandacceptance/TheoryCurves_gjj.root')
templateInputFile = ROOT.TFile('./inputs/xsecandacceptance/ZPrime_gjj.root')

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
myPainter = Morisot_gjj()
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

# Setup signal info

masses = {} # Define mass points for signals

masses["ZPrime0p16"]    = ["300","400","500","600","700","800","900","1000"]
# XXX FIXME TODO masses["ZPrime0p10"]    = ["250","350","450","550"]#,"600","700","800","900","1000"]
masses["ZPrime0p10"]    = ["250","350","550"]#,"600","700","800","900","1000"]
masses["ZPrime0p20"]    = ["250","350","450","550","750"]#,"800","900","1000"]
masses["ZPrime0p30"]    = ["200","250","300","350","400","450","500","550","750","950"] 
masses["ZPrime0p40"]    = ["750"]#300","400","500","600","700","800","900","1000"]

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
#yranges['ZPrime0p16'] = [5E-3,15]
#yranges['ZPrime0p10'] = [5E-3,15]
#yranges['ZPrime0p20'] = [5E-3,15]
#yranges['ZPrime0p30'] = [5E-3,15]
#yranges['ZPrime0p40'] = [5E-3,15]

yranges['ZPrime0p16'] = [5E-4,5]
yranges['ZPrime0p10'] = [5E-4,5]
yranges['ZPrime0p20'] = [5E-4,5]
yranges['ZPrime0p30'] = [5E-4,5]
yranges['ZPrime0p40'] = [5E-4,5]

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
EffDict = {0.1: {250.0: {'acc': 0.2045000046491623,
               'acceff': 0.16750000417232513,
               'eff': 0.8190709064270492},
       350.0: {'acc': 0.2320999950170517,
               'acceff': 0.19169999659061432,
               'eff': 0.825937099122},
       550.0: {'acc': 0.271450012922287,
               'acceff': 0.2236499935388565,
               'eff': 0.8239085757674468}},
 0.2: {250.0: {'acc': 0.20250000059604645,
               'acceff': 0.16473683714866638,
               'eff': 0.8135152427840667},
       350.0: {'acc': 0.23929999768733978,
               'acceff': 0.19629999995231628,
               'eff': 0.8203092429979643},
       450.0: {'acc': 0.258899986743927,
               'acceff': 0.21244999766349792,
               'eff': 0.8205871322567048},
       550.0: {'acc': 0.2805500030517578,
               'acceff': 0.22290000319480896,
               'eff': 0.7945107851368899},
       750.0: {'acc': 0.31040000915527344,
               'acceff': 0.2443999946117401,
               'eff': 0.787371093437959}},
 0.3: {100.0: {'acc': 0.0182499997317791,
               'acceff': 0.016499999910593033,
               'eff': 0.904109597429815},
       200.0: {'acc': 0.16189999878406525,
               'acceff': 0.1340000033378601,
               'eff': 0.8276714289330115},
       250.0: {'acc': 0.19939999282360077,
               'acceff': 0.16183333098888397,
               'eff': 0.8116014885318971},
       300.0: {'acc': 0.2180500030517578,
               'acceff': 0.1783333271741867,
               'eff': 0.8178551922875062},
       350.0: {'acc': 0.24009999632835388,
               'acceff': 0.19535000622272491,
               'eff': 0.8136193636403469},
       400.0: {'acc': 0.2500999867916107,
               'acceff': 0.20264999568462372,
               'eff': 0.8102759151821809},
       450.0: {'acc': 0.26660001277923584,
               'acceff': 0.2147500067949295,
               'eff': 0.8055138653453783},
       500.0: {'acc': 0.2750000059604645,
               'acceff': 0.22155000269412994,
               'eff': 0.8056363559715021},
       550.0: {'acc': 0.2671999931335449,
               'acceff': 0.22169999778270721,
               'eff': 0.8297155818858981},
       750.0: {'acc': 0.2973000109195709,
               'acceff': 0.2353000044822693,
               'eff': 0.7914564273121584},
       950.0: {'acc': 0.3154999911785126,
               'acceff': 0.24300000071525574,
               'eff': 0.7702060459892827},
       1500.0: {'acc': 0.3492000102996826,
                'acceff': 0.2524999976158142,
                'eff': 0.7230813005965243}},
 0.4: {750.0: {'acc': 0.2992500066757202,
               'acceff': 0.23589473962783813,
               'eff': 0.7882864974618481},
       1500.0: {'acc': 0.3501499891281128,
                'acceff': 0.25922220945358276,
                'eff': 0.7403176281657362}}}

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
      # Without efficiency divided out
      #print "Lydia removing first point in graph!" # FIXME
      #if ((graph.GetName() == "ZPrime03_graph") and (np ==0)): continue
      #newgraph.SetPoint(np,d1,d2)
      # With efficiency divided out
      print "EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
      print signal
      gSM_EffDict = float(signal.split("ZPrime")[1].replace("p","."))
      print gSM_EffDict
      eff = EffDict[gSM_EffDict][d1]['eff']
      print eff
      newgraph.SetPoint(np,d1,d2/eff) # Dividing by efficiency from dict NOTE
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
                "ZPrime0p10" : [550],
                "ZPrime0p20" : [350],
                "ZPrime0p30" : [350],
                "ZPrime0p40" : [750],
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
        #sigplotforratio.Divide(fithist)
        #signalPlots.append(sigplotforfitplusbkg)
        #sigratioPlots.append(sigplotforratio)
        #thistitle = SignalLegends[signal] + ", %s= %d GeV" % (SignalAxes[signal]["X"].split("[GeV]")[0].replace("M","m"),mass)
        #legendlist.append(thistitle)
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
     outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,doRightLeg,labellist,True,bumpHunterPVal,False,-999,-999,None,5E1,5E5)

  outputName = folderextension+"FancyFigure1WithFitLabels_"+signal+plotextension
  myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,signalPlots,\
     sigratioPlots,signalMasses,legendlist,"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
     outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,doRightLeg,labellist,True,bumpHunterPVal,True,fitRange[0],fitRange[1],None,5E1,5E5)


  ##################################################
  # Systematics x-check plots
  ##################################################

  if (doSyst) :


    # Cross-check plots
    systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity","JER":"JER", "PDFAcc":"PDF acceptance", "ISRAcc":"ISR acceptance","mjj_{0}_1fb_JET_GroupedNP_1":"Grouped NP 1","mjj_{0}_1fb_JET_GroupedNP_2":"Grouped NP 2","mjj_{0}_1fb_JET_GroupedNP_3":"Grouped NP 3","mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure":"#eta intercalibration non-closure"}
    #systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity","JER":"JER", "PDFAcc":"PDF acceptance","mjj_{0}_1fb_JET_GroupedNP_1":"Grouped NP 1","mjj_{0}_1fb_JET_GroupedNP_2":"Grouped NP 2","mjj_{0}_1fb_JET_GroupedNP_3":"Grouped NP 3","mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure":"#eta intercalibration non-closure"}
    #systDict = {"BKG_normalisation": "Fit quality", "FUNCCHOICE": "Function choice", "LUMI":"Luminosity", "PDFAcc":"PDF acceptance"}
    for mass in masses[signal]:

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
	#firstBin,lastBin-1,False,0,0,True,False,False,11,-1,True,["Nominal","Best Fit"],5E1,5E5)

      myPainter.drawMultipleFitsAndResiduals(datahist,[fithist,fit2],[residual,residual2],["Nominal fit","Best fit"],\
	"m_{jj} [GeV]","Events",[" Significance","Significance   "],outputName,luminosity,Ecm,\
	firstBin,lastBin-1,False,0,0,True,False,False,11,-1,True,["Nominal","Best Fit"],5E1,5E5)
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
  outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,False,"",False,-999,False,-999,-999,None,5E1,5E5)

outputName = folderextension+"FancyFigure1WithFitLabels_NoSignals"+plotextension
myPainter.drawDataAndFitWithSignalsOverSignificances(datahist,fithist,basicSignificancePlot,residual,[],\
  [],[],[],"m_{jj} [GeV]","Events","[data-fit]/fit","Significance ",\
  outputName,luminosity,Ecm,firstBin,lastBin-1,True,bumpLowEdge,bumpHighEdge,True,False,False,"",True,bumpHunterPVal,True,fitRange[0],fitRange[1],None,5E1,5E5)

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

