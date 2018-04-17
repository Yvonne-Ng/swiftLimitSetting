#!/bin/python

#******************************************
#plot sensitivity scan by looping over all masses on a range of luminosity values
#EXAMPLE python plotSensitivityScan.py --path ../results/searchphase/ --config <config file> --tag <tag> --wait

#******************************************
#import stuff
import sys, os, math, argparse, ROOT
import numpy as np
import plotTools

#******************************************
def plotSensitivityScanResults(args):

    print '\n******************************************'
    print 'plot sensitivity scan results'

    #******************************************
    #set ATLAS style
    if os.path.isfile(os.path.expanduser('~/RootUtils/AtlasStyle.C')):
        ROOT.gROOT.LoadMacro('~/RootUtils/AtlasStyle.C')
        ROOT.SetAtlasStyle()
        ROOT.set_color_env()
    else:
        print '\n***WARNING*** couldn\'t find ATLAS Style'
        #import AtlasStyle
        #AtlasStyle.SetAtlasStyle()

    #------------------------------------------
    #set error sum and overflow
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()
    ROOT.TH2.SetDefaultSumw2()
    ROOT.TH2.StatOverflows()
    
    #------------------------------------------
    #input parameters
    print '\ninput parameters:'
    argsdict = vars(args)
    for ii in xrange(len(argsdict)):
        print '  %s = %s'%(argsdict.keys()[ii], argsdict.values()[ii],)
    
    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))
	    
    #------------------------------------------
    #get settings
    print '\nconfig settings:'
    settings = ROOT.TEnv()
    if settings.ReadFile(args.configFileName,ROOT.EEnvLevel(0)) != 0:
        raise SystemExit('***ERROR*** could not find sensitivity scan config file: %s'%args.configFileName)

    model = settings.GetValue('signalModel','')
    print '  signal model = %s'%model

    modelLabel = settings.GetValue('signalModelLabel','').replace('"','')
    print '  signal model label = %s'%modelLabel

    massValuesConfig = settings.GetValue('signalMasses','2000,3000,4000').split(',')
    massValuesConfig = [float(m) for m in massValuesConfig]
    print '  signal masses [GeV] = %s'%massValuesConfig

    lumiMin = float(settings.GetValue('luminosityMin','0.1'))
    if lumiMin < 0.1: #fb^-1
        lumiMin = 0.1 #fb^-1
    print '  minimum luminosity = %s'%lumiMin

    lumiMax = float(settings.GetValue('luminosityMax','10.'))
    print '  maximum luminosity = %s'%lumiMax
    if lumiMax > 100.: #fb^-1
        lumiMax = 100. #fb^-1
    
    histBaseName = settings.GetValue('histBaseName','mjj')
    print '  hist base name = %s'%histBaseName

    bTaggingWP = settings.GetValue('bTaggingWP','') #fix_8585
    print '  b-tagging WP = %s'%bTaggingWP

    axisLabel = settings.GetValue('axisLabel','m [GeV]')
    print '  hist x-axis label = %s'%axisLabel

    nPar = int(settings.GetValue('nFitParameters','3'))
    print '  n fit parameters = %s'%nPar

    seed = float(settings.GetValue('randomSeed','0'))
    print '  random seed = %s'%seed

    notes = settings.GetValue('notes','').split(',')
    print '  notes = %s'%notes

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #set variables
    histName = histBaseName
    if bTaggingWP != '':
        histName+='_'+bTaggingWP
    if args.debug:
        print '\nhist name = %s'%histName

    textSize = 20

    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))

    #------------------------------------------
    #get list of available mass and lumi points
    massValuesAvailable = []
    lumiValues = []
    searchphaseFileList=os.listdir(args.path)

    for searchphaseFileName in sorted(searchphaseFileList):
        if '.%s.'%model in searchphaseFileName and '.%i.par.'%nPar in searchphaseFileName and '.%i.seed.'%seed in searchphaseFileName and args.tag in searchphaseFileName:

            fields = searchphaseFileName.split('.')
            for ii,field in enumerate(fields):
                if field == 'GeV':
                    massValuesAvailable.append( int(fields[ii-1]))
                if field == 'ifb':
                    lumiValues.append( float(fields[ii-1].replace('p','.')))


    massValues = list( set(massValuesConfig) & set(massValuesAvailable) )
    massValues.sort(key=float)
    lumiValues = list( set(lumiValues))
    lumiValues.sort(key=float)
    print '\navailable values'
    print '  mass [GeV]: %s'%massValues
    print '  luminosity [fb^-1]: %s'%lumiValues

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------
    
    #------------------------------------------
    #arrays for sensitivity scan graphs
    gmass = np.array(massValues,dtype=np.float64)
    glumi = np.zeros_like(gmass,dtype=np.float64)
    glowedge = np.zeros_like(gmass,dtype=np.float64)
    ghighedge = np.zeros_like(gmass,dtype=np.float64)
    
    #------------------------------------------
    #loop over luminosity values
    for lumi in lumiValues:
        
        #------------------------------------------
        if args.debug:
            print '\n\n******************************************'
            print '******************************************'
            print 'luminosity = %s ^pb-1'%lumi
            print 'available mass values [GeV]: %s'%massValues
            print '******************************************'
            print '******************************************\n'

        slumi = ('%.1f'% float( str(lumi).replace('p','.'))).replace('.','p')
        
        #------------------------------------------
        #loop over signal mass values
        removeMassValues = []
        for mass in massValues:

            #------------------------------------------
            #check SearchPhase results
            if args.debug:
                print '******************************************\nSearchPhase results\n'
                print '%s mass = %s GeV'%(model, mass)
                print 'lumi = %s fb^-1'%lumi
            
            #get SearchPhase result file
            spFileName = ''
            for searchphaseFileName in sorted(searchphaseFileList):
                #if '.%s.'%model in searchphaseFileName and '.%i.par.'%nPar in searchphaseFileName and '.%i.seed.'%seed in searchphaseFileName and args.tag in searchphaseFileName and '.%s.GeV.'%int(mass) in searchphaseFileName and '.%s.ifb.'%slumi in searchphaseFileName:
                if '.%s.'%model in searchphaseFileName and '.%i.par.'%nPar in searchphaseFileName and '.%i.seed.'%seed in searchphaseFileName and args.tag in searchphaseFileName and '.%s.GeV.'%int(mass) in searchphaseFileName and '.%s.ifb.'%slumi in searchphaseFileName and '.%s'%histBaseName in searchphaseFileName and '%s'%bTaggingWP in searchphaseFileName:
                    spFileName = searchphaseFileName

            spFileName = args.path+'/'+spFileName
                    
            if spFileName != '':
                if args.debug:
                    print 'file = %s'%spFileName
            else:
                continue            
            
            if os.path.isfile(spFileName):
                spFile = ROOT.TFile(spFileName,'READ')
                if not spFile:
                    raise SystemExit('\n***ERROR*** couldn\'t open search pahse output file: %s'%spFileName)

                #------------------------------------------
                #fill sensitivity scan graph and remove discovered signal mass values from the list
                bumpHunterStatOfFitToData = spFile.Get("bumpHunterStatOfFitToData")
                bumpHunterStatValue = bumpHunterStatOfFitToData[0]
                bumpHunterPValue    = bumpHunterStatOfFitToData[1]
                bumpHunterPValueErr = bumpHunterStatOfFitToData[2]

                bumpHunterPLowHigh = spFile.Get('bumpHunterPLowHigh')
                #bumpHunterStatValue = bumpHunterPLowHigh[0]
                bumpLowEdge         = bumpHunterPLowHigh[1]
                bumpHighEdge        = bumpHunterPLowHigh[2]

                if args.debug:
                    print "bump range: %s GeV - %s GeV"%(bumpLowEdge,bumpHighEdge)
                    print "BumpHunter stat = %s"%bumpHunterStatValue
                    print "BumpHunter p-value = %s +/- %s"%(bumpHunterPValue, bumpHunterPValueErr)

                bumpHunterSigmas = ROOT.Math.normal_quantile(1.-bumpHunterPValue, 1.)
                if args.debug:
                    print "BumpHunter sigmas = %s"%bumpHunterSigmas
                                
                if bumpHunterSigmas > 5.:
                    massIndex = np.where(gmass == mass)

                    #------------------------------------------
                    #NOTE remove some points
                    #if float(mass) <= 6000. or float(mass) >= 11000.:
                    #    glumi[massIndex] = 0.
                    #else:
                    glumi[massIndex] = lumi #NOTE always keep this uncommented
                    glowedge[massIndex] = bumpLowEdge #NOTE always keep this uncommented
                    ghighedge[massIndex] = bumpHighEdge #NOTE always keep this uncommented
                    #------------------------------------------
                    
                    removeMassValues.append(mass)

                #------------------------------------------

            else:
                print 'BumpHunter results not available for %s GeV %s: %s'%(mass,model, spFileName)

            #------------------------------------------
            #TEST
            #raise SystemExit('\n***TEST*** exit')
            #------------------------------------------

        #------------------------------------------
        #remove mass points discovered
        for removeMass in removeMassValues:
            massValues.remove(removeMass)
        if args.debug:
            print '\n******************************************'
            print 'available mass values [GeV]: %s'%massValues
            print '******************************************'
                
    #------------------------------------------
    #print sensitivity scan results
    print '\nsensitivity scan results'
    print '  mass [GeV] = %s'%gmass
    print '  luminosity [fb^-1] = %s'%glumi

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #plot

    #------------------------------------------
    #canvas and pads
    c = ROOT.TCanvas('c', 'c', 100, 50, 800, 600)
    yd = 0.5 #bottom pad height (pad2)
    pad1 = ROOT.TPad("pad1","pad1",0, yd, 1, 1)#top
    pad2 = ROOT.TPad("pad2","pad2",0, 0, 1, yd)#bottom

    pad1.SetTopMargin(0.08)
    pad1.SetBottomMargin(0.0)
    #pad1.SetBorderMode(0)
    pad1.Draw()

    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.2)
    #pad2.SetBorderMode(0)
    pad2.Draw()

    #..........................................
    #labels
    ax = 0.65 #0.20
    ay = 0.80 #0.88
    a = plotTools.getATLAS()
    p = plotTools.getInternal()
    n = plotTools.getNote(textSize)
    spacing = 0.06 #0.04
    textSize = 20

    #------------------------------------------
    #pad 1
    #------------------------------------------
    pad1.cd()
    pad1.Clear()
    pad1.SetLogx(0)
    pad1.SetLogy(1)
    
    #..........................................
    #graph
    g = ROOT.TGraph(len(gmass), gmass, glumi)
    g.SetTitle('sensitivity studies')

    g.GetXaxis().SetTitle('m_{%s} [GeV]'%modelLabel)
    g.GetXaxis().SetLabelFont(43)
    g.GetXaxis().SetLabelSize(textSize)
    g.GetXaxis().SetTitleFont(43)
    g.GetXaxis().SetTitleSize(textSize)
    dx = gmass[0]*0.1
    g.GetXaxis().SetLimits(gmass[0]-dx, gmass[-1]+dx)

    g.GetYaxis().SetTitle('discovery luminosity [fb^{-1}]')
    g.GetYaxis().SetLabelFont(43)
    g.GetYaxis().SetLabelSize(textSize)
    g.GetYaxis().SetTitleFont(43)
    g.GetYaxis().SetTitleSize(textSize)

    glumiMin = max(glumi[0], glumi.min()) #NOTE can not use 0. in log scale
    g.SetMinimum(glumiMin*0.5) #HERE before Draw()
    g.SetMaximum(glumi.max()*2.) #HERE before Draw()

    g.Draw("ap")

    #..........................................
    #luminosity lines
    llumi = ROOT.TLine()
    llumi.SetLineColor(ROOT.kRed)
    llumi.SetLineWidth(2)
    #llumi.DrawLine(g.GetXaxis().GetXmin(), 1., g.GetXaxis().GetXmax(), 1.)
    
    #draw graph (again but) on top of the lines
    g.Draw("same p")

    #..........................................
    #ATLAS internal
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'internal')

    #notes
    allNotes=[]
    allNotes.append('#sqrt{s} = 13 TeV')
    allNotes.append('%s sensitivity scan'%modelLabel)
    allNotes.append('%s parameter fit'%nPar)
    allNotes+=notes
    
    for ii, note in enumerate(allNotes):
        n.DrawLatex(ax,ay-spacing*(ii+1),note)

    #..........................................
    c.cd()
    c.Update()

    #------------------------------------------
    #pad 2
    #------------------------------------------
    pad2.cd()
    pad2.Clear()
    pad2.SetLogx(0)
    pad2.SetLogy(0)
    pad2.SetGridx(1)
    pad2.SetGridy(1)

    #..........................................
    #bump band
    gb = ROOT.TGraphAsymmErrors(len(glumi), gmass, (ghighedge+glowedge)/2, np.zeros_like(glumi), np.zeros_like(glumi), (ghighedge-glowedge)/2, (ghighedge-glowedge)/2) #n,x,y,exl,exh,eyl,eyh
    gb.SetTitle('bump range')

    gb.GetXaxis().SetTitle('m_{%s} Q[GeV]'%modelLabel)
    gb.GetXaxis().SetLabelFont(43)
    gb.GetXaxis().SetLabelSize(textSize)
    gb.GetXaxis().SetTitleFont(43)
    gb.GetXaxis().SetTitleSize(textSize)
    gb.GetXaxis().SetLimits(gmass[0]-dx, gmass[-1]+dx)
    gb.GetXaxis().SetTitleOffset(2.5)#this needs to be adjusted depending on yd

    gb.GetYaxis().SetTitle('m_{%s} Q[GeV]'%modelLabel)
    gb.GetYaxis().SetTitle(axisLabel)
    gb.GetYaxis().SetLabelFont(43)
    gb.GetYaxis().SetLabelSize(textSize)
    gb.GetYaxis().SetTitleFont(43)
    gb.GetYaxis().SetTitleSize(textSize)
    gb.GetYaxis().SetDecimals(True)

    gb.SetMarkerColor(ROOT.kRed)
    gb.SetLineColor(ROOT.kRed)
    gb.SetFillColor(ROOT.kRed)
    gb.SetFillStyle(3003)

    #..........................................
    #draw
    gb.Draw("ape") #draw points
    #gbb = gb.Clone() 
    #gbb.Draw("same3") #draw band
        
    #..........................................
    c.cd()
    c.Update()
    
    #..........................................
    c.Update()
    if args.wait:
        c.WaitPrimitive()
    c.SaveAs(localdir+'/../figures/sensitivityscan.'+model+'.'+histName+'.%i'%nPar+'.par.%i'%seed+'.seed.'+args.tag+'.pdf')

#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('--config', dest='configFileName', default='', required=True, help='sensitivity scan config file')
    parser.add_argument('--path', dest='path', default='', required=True, help='path to search phase results directory')
    parser.add_argument('--tag', dest='tag', default='default', required=True, help='tag for output files')
    parser.add_argument('--wait', dest='wait', action='store_true', default=False, help='wait?')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    #------------------------------------------
    #plot sensitivity scan results
    plotSensitivityScanResults(args)
    print '\n******************************************'
    print 'plotted sensitivity scan results'
