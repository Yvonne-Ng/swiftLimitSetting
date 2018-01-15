import math
import ROOT
import os

ROOT.gROOT.SetBatch(True)

# Calculate 1 sigma JES uncertainty for gaussians. Use Z' signal and calculate left right shift in peak position (estimated using crystal ball fit). Calculate separately for each JES component, before combining in quadrature for up and down shifts separately. Note: Using 3 sigma shifted JES templates and dividing by 3 in calculation, seems to be more stable than using 1 sigma shifted JES templates and not dividing by 3.
 
# Replace XXX with your code location
runDir = "XXX/StatisticalAnalysis/Bayesian/scripts/CrystalBall/" 

# Uncomment for jjj analysis
inDir = "inDir/jjj/NoMjj/"
plotDir = "./FitPlots_jjj_NoMjj_3Sig"
ext = "jjj_NoMjj_3Sig"
isChopped = False
isjjj = True

# Uncomment for gjj analysis
#inDir = "inDir/gjj/NoMjj/"
#plotDir = "./FitPlots_gjj_NoMjj_3Sig"
#ext = "gjj_NoMjj_3Sig"
#isChopped = False
#isjjj = False

inputFiles = os.listdir(runDir+inDir)

def fitWidth(histoimmutable, mmed, gq, name):
  c=ROOT.TCanvas()
    
  histo = histoimmutable.Clone("hsig")
  massInt = int(mmed)

  #make unit area histogram
  integral = histo.Integral()
  # print " entries: ", str(integral)
  histo.Scale(1/integral)
  # print "mu: %f   rms: %f" % (histo.GetMean(),histo.GetRMS())

  #make function
  # use directly the function in ROOT::MATH note that the parameters definition is different is (alpha, n sigma, mu)
  # auto f2 = new TF1("f2","ROOT::Math::crystalball_function(x, 2, 1, 1, 0)",-5,5);
  # Kate f1 = ROOT.TF1("fcb","[0]*ROOT::Math::crystalball_function(x, [2], [3], [4], [1])",0.5*massInt,1.15*massInt)

  low = 0.5*massInt
  high = 1.15*massInt
  
  #double ROOT::Math::crystalball_function (double x, double alpha, double n, double sigma, double x0 = 0) 	
  f1 = ROOT.TF1("fcb","[0]*ROOT::Math::crystalball_function(x, [2], [3], [4], [1])",low,high)

  #probably parameter init is bogus
  #f1.SetParameters(0.5,massInt,0.3,3,0.05*massInt)#,1000)
  f1.SetParameters(0.5,massInt,0.3,3,0.045*massInt)#,1000)
  f1.SetParLimits(0,0.,1.)
  f1.SetParLimits(1,0.6*massInt,1.4*massInt)
  f1.SetParLimits(2,0.05,3.5)
  f1.SetParLimits(3,0.0001,20)
  f1.SetParLimits(4,0.001*massInt,0.5*massInt)
  #if massInt == 550:
  #  f1.SetParLimits(4,0.001*massInt,0.35*massInt)
  
  result = histo.Fit(f1,"IMRs");
  if not result.IsValid:
      print "fit failed!"
      return 0,0,0
  
  # Calculate "gaussian efficiency" 3sigma/all events
  parameters = result.Parameters()
  sigma=parameters[4]
  mean=parameters[1]
  #detresGeV = mean*detResFunction(mean)
  # print "mean: %6.1f  sigma: %7.3f  detres: %7.3f" % (mean,sigma,detresGeV)

  nwindwidth = 2.9
  #if detresGeV < sigma:
  integration_window = nwindwidth*sigma
  #else:
  #integration_window = nwindwidth*detresGeV

  #print mean,sigma,mean-integration_window,mean+integration_window
  eff = histo.Integral(histo.FindBin(mean-integration_window),histo.FindBin(mean+integration_window))
  #print "Mass|GaussianAcceptance:",massInt,eff
  if True:
    histo.GetXaxis().SetRangeUser(massInt*0.2,massInt*1.8)
    ymax = histo.GetMaximum()
    #line = ROOT.TLine(mean-integration_window,0,mean-integration_window,ymax);
    line = ROOT.TLine(low,0,low,ymax);
    line.SetLineColor(ROOT.kRed);
    histo.Draw()
    line.Draw("same")
    #line = ROOT.TLine(mean+integration_window,0,mean+integration_window,ymax);
    line.DrawLine(high,0,high,ymax);
    f1.Draw("same")
    # make filename
    #outfilename = "widthfit_{0}_{1}_{2}.pdf".format(str(gq*100),str(int(mmed)),ext)
    if not os.path.exists(plotDir):
        os.makedirs(plotDir)
    outfilename = plotDir+"/widthfit_{0}.png".format(name)#str(gq*100),str(int(mmed)),ext)
    c.Print(outfilename)

  print result.Status()
  
  if result.Status()==4:
      # minuit problem
      print "Minuit failure!"
      print name
      return None
    
  return eff, sigma, mean


####### Runs from here #########

widthDict = {}

for inputFile in inputFiles:

  if isChopped:
    MCSampleTag=inputFile.split("_")[1].split(".root")[0]
  else:
    MCSampleTag=inputFile.split(".root")[0]
  mmed = MCSampleTag.split("mR")[1].split("gSM")[0]
  gq = float(MCSampleTag.split("gSM")[1].replace("p","."))

  histList = {"Nominal"        : ["mjj_{0}_1fb_Nominal",],
              "EtaIntercal_p1" : ["mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure__3up",],
              "EtaIntercal_d1" : ["mjj_{0}_1fb_JET_EtaIntercalibration_NonClosure__3down",],
              "Grouped1_p1"    : ["mjj_{0}_1fb_JET_GroupedNP_1__3up",],
              "Grouped1_d1"    : ["mjj_{0}_1fb_JET_GroupedNP_1__3down",],
              "Grouped2_p1"    : ["mjj_{0}_1fb_JET_GroupedNP_2__3up",],
              "Grouped2_d1"    : ["mjj_{0}_1fb_JET_GroupedNP_2__3down",],
              "Grouped3_p1"    : ["mjj_{0}_1fb_JET_GroupedNP_3__3up",],
              "Grouped3_d1"    : ["mjj_{0}_1fb_JET_GroupedNP_3__3down",]}

  readfile = ROOT.TFile(runDir+inDir+inputFile,'r')
  print "Opening",inputFile
  for val in histList.keys() :
    name = histList[val][0].format(MCSampleTag)
    print "Getting",name
    hist = readfile.Get(name)
    fitresult = fitWidth(hist, mmed, gq, name)
    eff, sigma, mean = fitresult
    histList[val].append(mean)

  # Now compute up and down variations here
  # Up
  u1 = (histList["EtaIntercal_p1"][1] - histList["Nominal"][1])/3
  u2 = (histList["Grouped1_p1"][1] - histList["Nominal"][1])/3
  u3 = (histList["Grouped2_p1"][1] - histList["Nominal"][1])/3
  u4 = (histList["Grouped3_p1"][1] - histList["Nominal"][1])/3
  totalUp = math.sqrt(u1*u1 + u2*u2 + u3*u3 + u4*u4)
  percentUp = totalUp/histList["Nominal"][1]

  # Down
  d1 = (histList["EtaIntercal_d1"][1] - histList["Nominal"][1])/3
  d2 = (histList["Grouped1_d1"][1] - histList["Nominal"][1])/3
  d3 = (histList["Grouped2_d1"][1] - histList["Nominal"][1])/3
  d4 = (histList["Grouped3_d1"][1] - histList["Nominal"][1])/3
  totalDown = math.sqrt(d1*d1 + d2*d2 + d3*d3 + d4*d4 )
  percentDown = totalDown/histList["Nominal"][1]

  # Values we need are percentages
  if not gq in widthDict.keys() :
    widthDict[gq] = {}
  widthDict[gq][mmed] = [percentUp,percentDown]

# Make a histogram to match the old inputs I had from Lydia
outfile = ROOT.TFile("outWidths{0}.root".format(ext),"RECREATE")
for width in widthDict.keys() :
  histUp = ROOT.TH1D("ZPrime_width{0}_JESUp".format(width).replace(".","p"),"ZPrime_width{0}_JESUp".format(width).replace(".","p"),10,0,10)
  histDown = ROOT.TH1D("ZPrime_width{0}_JESDown".format(width).replace(".","p"),"ZPrime_width{0}_JESDown".format(width).replace(".","p"),10,0,10)
  index = 0
  for mass in sorted(widthDict[width].keys()) :
    index = index+1
    histUp.SetBinContent(index,widthDict[width][mass][0])
    histUp.GetXaxis().SetBinLabel(index,"{0}".format(mass))
    histUp.GetYaxis().SetRangeUser(0,0.05)
    histDown.SetBinContent(index,widthDict[width][mass][1])
    histDown.GetXaxis().SetBinLabel(index,"{0}".format(mass))
    histDown.GetYaxis().SetRangeUser(0,0.05)

  c=ROOT.TCanvas()

  XName = "Mass Point [GeV]"
  YName = "Relative uncertainty"
  Offset = 1.5

  leg = ROOT.TLegend(0.60,0.65,0.80,0.85)
  leg.AddEntry(histDown, "JES, 1 #sigma down ", "l")
  leg.AddEntry(histUp, "JES, 1 #sigma up ", "l")

  outfilename = plotDir+"/ZPrimegSM0p30_JESShifts1fb_Quadrature_1Sigma.pdf".format(name)#str(gq*100),str(int(mmed)),ext)
  histUp.SetLineStyle(2)

  histUp.SetStats(0)
  histDown.SetStats(0)
  histUp.SetTitle("")
  histDown.SetTitle("")

  histUp.GetXaxis().SetTitle(XName)
  histUp.GetYaxis().SetTitle(YName)
  histUp.GetYaxis().SetTitleOffset(Offset)
  histDown.GetXaxis().SetTitle(XName)
  histDown.GetYaxis().SetTitle(YName)
  histDown.GetYaxis().SetTitleOffset(Offset)

  histUp.Draw("HIST")
  histDown.Draw("HIST same")
  leg.Draw() 
  c.Print(outfilename)

  histUp.Write()
  histDown.Write()

outfile.Close()
