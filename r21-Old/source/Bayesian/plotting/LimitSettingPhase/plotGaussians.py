#/usr/bin/env python
import sys
import ROOT
from art.morisot import Morisot

luminosity = 3230 #4000 #80 # ipb. 7 ipb = 0.007 ifb.

# Get input: basic gaussian
ratios = [-1,0.07,0.10,0.15]# Don't include widest gaussian,0.15]#,0.30]

subranges = [[200,400],[400,600],[600,800],[800,1000],[1000,1500]]

folderextension = 'IgnoreNeff_dijetgamma_mc_00-00-05_3p23fb_4Par/'

plotextension = ''#_3p34'

basicInputFileTemplate = "/home/beresford/TriJet/StatisticalAnalysis/Bayesian/results/Step4_GaussianLimits/IgnoreNeff_dijetgamma_mc_00-00-05_3p23fb_4Par/GenericGaussians_3p23_low{0}_high{1}_{2}.root"

inputsForFailedPoints = "/home/beresford/TriJet/StatisticalAnalysis/Bayesian/results/Step4_GaussianLimits/IgnoreNeff_dijetgamma_mc_00-00-05_3p23fb_4Par/GenericGaussians_mass{0}_{1}.root"
failedPoints = []
#failedPoints = [[1350,-1],[1500,-1],[1650,0.15],[1750,0.10]]
#failedPoints = [[1700,0.15]]

	
# Initialize painter
myPainter = Morisot()
myPainter.setLabelType(1) # label

graphs = []
#names = ['#sigma_{G}/m_{G} = 0.15','#sigma_{G}/m_{G} = 0.10','#sigma_{G}/m_{G} = 0.07','#sigma_{G}/m_{G} = Res.']
names = ['#sigma_{G}/m_{G} = Res','#sigma_{G}/m_{G} = 0.07','#sigma_{G}/m_{G} = 0.10.','#sigma_{G}/m_{G} = 0.15.']

results = {}

# Retrieve search phase inputs
for width in sorted(ratios,reverse=True) :

  print "--------------------------------------"
  print "Beginning width",width,":"

  thisobserved = ROOT.TGraph()
  massAndWidths = {}

  if width>0 :
    widthfornames = int(1000*width)
    internalwidth = widthfornames
  else :
    widthfornames = 'resolutionwidth'
    internalwidth = -1000

#  if width == -1 :
#    myrange = subranges2
#  elif width == 0.10 :
#    myrange = subranges3
#  else :
  myrange = subranges

  outindex = 0
  for thisrange in sorted(myrange) :

    print "Using subrange2",thisrange
    outindex = outindex + 1

    # TEMP
    myrangelow = thisrange[0]
    myrangehigh = thisrange[1]
    filename = basicInputFileTemplate.format(thisrange[0],thisrange[1],widthfornames)

    file = ROOT.TFile.Open(filename)
    vectorName = "CLsPerMass_widthToMass{0}".format(internalwidth)
    cls = file.Get(vectorName)

    masses = file.Get("massesUsed")#massPoints")

    index = 0
    
    for i in range(len(masses)) :
      if cls[i]<0 :
        continue
      mass = masses[i]
      print mass,",",cls[i]
      if mass < myrangelow:
        continue
      if mass > 1300: # Don't go too high in mass (For ISR 2015 analysis only, due to fit bias studies)
        continue

      # Replace with a fix-file if this mass point initially failed
      print int(mass),width,failedPoints
      if [int(mass),width] in failedPoints :
        otherfile = ROOT.TFile.Open(inputsForFailedPoints.format(int(mass),widthfornames))
        print "Getting new val out of",inputsForFailedPoints.format(int(mass),widthfornames)
        cl = otherfile.Get("CLOfRealLikelihood")[0]
        massAndWidths[mass] = cl/luminosity

      else :
        massAndWidths[mass] = cls[i]/luminosity

  index = 0
  for mass in sorted(massAndWidths.keys()) :
    thisobserved.SetPoint(index,mass,massAndWidths[mass])
    index = index+1

  print "setting results[",width,"] = ",massAndWidths
  results[width] = massAndWidths
  graphs.append(thisobserved)

#myPainter.drawSeveralObservedLimits(graphs,names,folderextension+"GenericGaussians_GeV","m_{G} [GeV]","#sigma #times #it{A} #times BR [pb]",luminosity,13,1000,6500,1E-3,50,["#sigma_{G}/m_{G}"])

# Make everything shifted by 1000 for TeV plots
shiftedgraphs = []
d1, d2 = ROOT.Double(0), ROOT.Double(0)
findMaxRange = 0
for graph in graphs :
  newgraph = graph.Clone()
  newgraph.SetName(graph.GetName()+"_scaled")
  for np in range(newgraph.GetN()) :
    newgraph.GetPoint(np,d1,d2)
    #newgraph.SetPoint(np,d1/1000.0,d2/0.82) # Dividing by 0.82 to divide out efficiency NOTE
    # FIXME newgraph.SetPoint(np,d1,d2/0.82) # Dividing by 0.82 to divide out efficiency NOTE No divide by 1000, as want GeV
    newgraph.SetPoint(np,d1,d2) # Dividing by 0.82 to divide out efficiency NOTE No divide by 1000, as want GeV
    #if d1/1000 > findMaxRange :
    #  findMaxRange = d1/1000
    if d1 > findMaxRange :
      findMaxRange = d1
  shiftedgraphs.append(newgraph)

trueMaxRange = round(findMaxRange * 2) / 2 + 100
#trueMaxRange = round(findMaxRange * 2) / 2 + 0.5
# Lydia myPainter.drawSeveralObservedLimits(shiftedgraphs,names,folderextension+"GenericGaussians"+plotextension,"m_{G} [TeV]",\
#     "#sigma #times #it{A} #times BR [pb]",luminosity,13,1,trueMaxRange,0.004,5,[])
myPainter.drawSeveralObservedLimits(shiftedgraphs,names,folderextension+"GenericGaussians"+plotextension,"m_{G} [GeV]",\
     "#sigma #times #it{A} #times BR [pb]",luminosity,13,203,trueMaxRange,1E-2,10,names)

print "For table in note:"
mostMasses = results[sorted(results.keys())[0]]
for mass in sorted(mostMasses) :

   sys.stdout.write("{0}".format(int(mass)))
   sys.stdout.write(" & ")
   for width in sorted(results.keys()) :
     if mass in results[width].keys() :
       #sys.stdout.write('{0}'.format(round(results[width][mass]/0.82,3)))# Dividing by 0.82 to divide out efficiency NOTE 
       # FIXME sys.stdout.write('{0}'.format(float('%.2g' % (results[width][mass]/0.82)))) # Dividing by 0.82 to divide out efficiency NOTE 
       sys.stdout.write('{0}'.format(float('%.2g' % (results[width][mass])))) # Dividing by 0.82 to divide out efficiency NOTE 
       #sys.stdout.write("{0}".format(results[width][mass]))
     else :
       sys.stdout.write("-")
     if sorted(results.keys())[-1]!=width :
       sys.stdout.write(" & ")
     else :
       sys.stdout.write(" \\\\ ")

   sys.stdout.write("  \n")
print
print "For Antonio (Same but more dps):"

print 
mostMasses = results[sorted(results.keys())[0]]
for mass in sorted(mostMasses) :

   sys.stdout.write("{0}".format(int(mass)))
   sys.stdout.write(" & ")
   for width in sorted(results.keys()) :
     if mass in results[width].keys() :
       # FIXME sys.stdout.write('{0}'.format(float('%.5g' % (results[width][mass]/0.82)))) # Dividing by 0.82 to divide out efficiency NOTE 
       sys.stdout.write('{0}'.format(float('%.5g' % (results[width][mass])))) # Dividing by 0.82 to divide out efficiency NOTE 
       #sys.stdout.write("{0}".format(results[width][mass]))
     else :
       sys.stdout.write("-")
     if sorted(results.keys())[-1]!=width :
       sys.stdout.write(" & ")
     else :
       sys.stdout.write(" \\\\ ")

   sys.stdout.write("  \n")

