#!/bin/python

#******************************************
#plot luminosity scan results for each mass point separately
#EXAMPLE python -u plotLumiScanResults.py --path ../results/searchphase/ --config <config file> --tag <tag> --wait

#******************************************
#import stuff
import sys, os, math, argparse, ROOT
import numpy as np
import plotTools

#******************************************
def plotLumiScanResults(args):

    print '\n******************************************'
    print 'plot lumi scan results'

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
    #check input file
    if not os.path.isdir(args.path):
        raise SystemExit('\n***ERROR*** not a valid path: %s'%args.path)
    
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
    
    #------------------------------------------
    #NOTE remove higher lumi values
    #lumiValues = [lumiValue for lumiValue in lumiValues if lumiValue<40.]
    #------------------------------------------

    print '\nmass values [GeV]: %s'%massValues
    print 'luminosity values [fb^-1]: %s'%lumiValues

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #loop over mass points
    for mass in massValues:

        #------------------------------------------
        #NOTE use just one mass value
        #if float(mass) != 1250:
        #    continue
        #------------------------------------------

        print '\n******************************************'
        print '%s m = %s GeV'%(modelLabel, mass)
        print '******************************************'
        glumi = []
        gpval = []
        gpvalerr = []
        glowedge = []
        ghighedge = []

        #------------------------------------------
        #p-values histogram
        hpval = ROOT.TH1D('pvalues','pvalues',20,0.,1.)
        hpval.SetDefaultSumw2(ROOT.kTRUE)
        hpval.SetDirectory(0)
        
        #------------------------------------------
        #loop over luminosity values
        for lumi in lumiValues:

            #luminosity
            print '\nluminosity = %.1f fb^-1'%lumi
            slumi = ('%.1f'% float( str(lumi).replace('p','.'))).replace('.','p')
            discoverlumi = ''
            
            #get SearchPhase result file
            spFileName = ''
            for searchphaseFileName in sorted(searchphaseFileList):
                if '.%s.'%model in searchphaseFileName and '.%i.par.'%nPar in searchphaseFileName and '.%i.seed.'%seed in searchphaseFileName and args.tag in searchphaseFileName and '.%s.GeV.'%int(mass) in searchphaseFileName and '.%s.ifb.'%slumi in searchphaseFileName and '.%s'%histBaseName in searchphaseFileName and '%s'%bTaggingWP in searchphaseFileName:
                    spFileName = searchphaseFileName

            if spFileName != '':
                print spFileName
            else:
                continue
                    
            #------------------------------------------
            #TEST
            #raise SystemExit('\n***TEST*** exit')
            #------------------------------------------
            
            if os.path.isfile(args.path+'/'+spFileName):
                spFile = ROOT.TFile(args.path+'/'+spFileName,'READ')

                bumpHunterStatOfFitToData = spFile.Get("bumpHunterStatOfFitToData")
                bumpHunterStatValue = bumpHunterStatOfFitToData[0]
                bumpHunterPValue    = bumpHunterStatOfFitToData[1]
                bumpHunterPValueErr = bumpHunterStatOfFitToData[2]

                bumpHunterPLowHigh = spFile.Get('bumpHunterPLowHigh')
                #bumpHunterStatValue = bumpHunterPLowHigh[0]
                bumpLowEdge         = bumpHunterPLowHigh[1]
                bumpHighEdge        = bumpHunterPLowHigh[2]

                print "bump range: %s GeV - %s GeV"%(bumpLowEdge,bumpHighEdge)
                print "BumpHunter stat = %s"%bumpHunterStatValue
                print "BumpHunter p-value = %s +/- %s"%(bumpHunterPValue, bumpHunterPValueErr)

                bumpHunterSigmas = ROOT.Math.normal_quantile(1.-bumpHunterPValue, 1.)
                print "BumpHunter sigmas = %s"%bumpHunterSigmas
                                
                gpval.append(bumpHunterPValue)
                gpvalerr.append(bumpHunterPValueErr)

                glowedge.append(bumpLowEdge)
                ghighedge.append(bumpHighEdge)

                glumi.append(float(lumi))

                highestlumi = lumi

                hpval.Fill(float(bumpHunterPValue))
                
        print '\nhighest luminosity tested = %s pb^-1'%highestlumi
    
        #------------------------------------------
        #TEST
        #raise SystemExit('\n***TEST*** exit')
        #------------------------------------------        
        
        #------------------------------------------
        #plot luminosity scan for given mass value
        glumi = np.array(glumi)#/1e3
        glumierr = np.zeros_like(glumi)#/1e3
        gpval = np.array(gpval)
        gpvalerr = np.array(gpvalerr)
        glowedge = np.array(glowedge)#/1e3
        ghighedge = np.array(ghighedge)#/1e3
        #ROOT.gStyle.SetPadTickY(0)
        #ROOT.gStyle.SetPadRightMargin(0.15)

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

        #------------------------------------------
        #pad 1
        #------------------------------------------
        pad1.cd()
        pad1.Clear()
        pad1.SetLogx(1)
        pad1.SetLogy(0)
        
        #..........................................
        #bump band
        gr = ROOT.TGraphAsymmErrors(len(glumi), glumi, (ghighedge+glowedge)/2, np.zeros_like(glumi), np.zeros_like(glumi), (ghighedge-glowedge)/2, (ghighedge-glowedge)/2) #n,x,y,exl,exh,eyl,eyh
        gr.SetTitle('range')
        #gr.GetXaxis().SetTitle('luminosity [fb^{-1}]')
        gr.GetYaxis().SetTitle(axisLabel)
        gr.GetYaxis().SetLabelFont(43)
        gr.GetYaxis().SetLabelSize(textSize)
        gr.GetYaxis().SetTitleFont(43)
        gr.GetYaxis().SetTitleSize(textSize)
        gr.GetYaxis().SetDecimals(True)

        gr.SetMarkerColor(ROOT.kRed)
        gr.SetLineColor(ROOT.kRed)
        gr.SetFillColor(ROOT.kRed)
        gr.SetFillStyle(3003)

        #..........................................
        #draw
        gr.Draw("ape") #draw points
        grb = gr.Clone() 
        grb.Draw("same3") #draw band
        
        c.cd()
        c.Update()

        #------------------------------------------
        #pad 2
        #------------------------------------------
        pad2.cd()
        pad2.Clear()
        pad2.SetLogx(1)
        pad2.SetLogy(1)
        
        #p-value graph
        gpv = ROOT.TGraphErrors(int(len(glumi)), glumi, gpval, glumierr, gpvalerr)
        gpv.SetTitle('p-value')
        gpv.GetXaxis().SetTitle('luminosity [fb^{-1}]')
        gpv.GetXaxis().SetLabelFont(43)
        gpv.GetXaxis().SetLabelSize(textSize)
        gpv.GetXaxis().SetTitleFont(43)
        gpv.GetXaxis().SetTitleSize(textSize)
        gpv.GetYaxis().SetTitle('BumpHunter p-value')
        gpv.GetYaxis().SetLabelFont(43)
        gpv.GetYaxis().SetLabelSize(textSize)
        gpv.GetYaxis().SetTitleFont(43)
        gpv.GetYaxis().SetTitleSize(textSize)
        gpv.GetXaxis().SetTitleOffset(2.5)#this needs to be adjusted depending on yd
        
        gpv.SetFillColor(ROOT.kBlack)
        gpv.SetFillStyle(3002)
        gpv.SetMaximum(2.)
        gpv.SetMinimum(1e-10)

        gpv.SetMinimum(1e-7)
        gpv.Draw("apel") #HERE after SetMinimum()
        #gpv.Draw("same 3") #draw band #NOTE clashes with the line

        #draw sigma reference lines
        s = ROOT.TLatex()
        s.SetNDC(False)
        s.SetTextFont(43)
        s.SetTextColor(ROOT.kRed)
        s.SetTextSize(textSize)
        lxs = ROOT.TLine()
        lxs.SetLineColor(ROOT.kRed)
        lxs.SetLineWidth(2)

        for i in range(6):
            if i<1: continue
            pvalxs = 1. - ROOT.Math.normal_cdf(i)
            lxs.DrawLine(gpv.GetXaxis().GetXmin(), pvalxs, gpv.GetXaxis().GetXmax(), pvalxs)
            s.DrawLatex(gpv.GetXaxis().GetXmax()*1.05,pvalxs,'%0.f#sigma'%i)

        #draw graph (again) on top
        gpv.Draw("same pel") #HERE after SetMinimum()
        #gpv.Draw("same 3") #draw band #NOTE clashes with the line

        #..........................................
        #labels
        #NOTE notes and labels are written from bottom to top
        ax = 0.20
        ay = 0.24
        a = plotTools.getATLAS()
        p = plotTools.getInternal()
        n = plotTools.getNote(textSize)
        spacing = 0.06

        #notes: 13 TeV, model mass, n. par
        allNotes = []
        allNotes.append('#sqrt{s} = 13 TeV')
        if modelLabel != '':
            allNotes.append('m_{%s} = %0.f GeV'%(modelLabel,float(mass)))
        else:
            allNotes.append('m_{%s} = %0.f GeV'%(model,float(mass)))
        allNotes.append('%s par. fit func.'%nPar)
        allNotes+=notes
        allNotes=allNotes[::-1] #reverse the order
        
        for ii, note in enumerate(allNotes):
            n.DrawLatex(ax,ay+spacing*(ii),note)

        #ATLAS internal
        a.DrawLatex(ax,ay+spacing*len(allNotes),'ATLAS')
        p.DrawLatex(ax+0.13,ay+spacing*len(allNotes),'internal')
                
        #..........................................
        c.Update()
        if args.wait:
            c.WaitPrimitive()
        c.SaveAs(localdir+'/../figures/lumiscan.'+model+'.%s'%int(mass)+'.GeV.'+histName+'.%i'%nPar+'.par.%i'%seed+'.seed.'+args.tag+'.pdf')

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
    #plot luminosity scan results
    plotLumiScanResults(args)
    print '\n******************************************'
    print 'plotted lominosity scan results'
