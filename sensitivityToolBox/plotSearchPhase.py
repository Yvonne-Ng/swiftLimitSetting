#!/bin/python

#******************************************
#plot serach phase results from Statistical Analysis Bayesian tool
#this is a simplified version of the morisot module

#EXAMPLE python plotSearchPhase.py --bump/--tomo --file path/to/file/searchPhaseResults.root --notes <note1> ... <noteN> --lumi <lumi> --wait

#******************************************
#import stuff
import sys, os, argparse, ROOT
import plotTools

#******************************************
def getAxisRangeFromHist(hist):
    #NOTE function taken from morisot modules
    #axis range should be decided by data hist
    firstBin =0
    while (hist.GetBinContent(firstBin+1)==0 and firstBin < hist.GetNbinsX()) :
        firstBin+=1
    lastBin = hist.GetNbinsX()+1
    while (hist.GetBinContent(lastBin-1)==0 and lastBin > 0) :
        lastBin-=1
    if (firstBin > lastBin):
        firstBin=1
        lastBin = hist.GetNbinsX()
    return firstBin,lastBin

#******************************************
def plotSearchPhase(dataHist,
                    fitHist,
                    significanceHist,
                    xLab,
                    yLab,
                    sigLab,
                    name,
                    luminosity,
                    CME,
                    chi2ndf,
                    BHpval,
                    nPar,
                    userFirstBin=-1,
                    userLastBin=-1,
                    bumpLow=0,
                    bumpHigh=0,
                    bumpFound=False,
                    logx=False,
                    notes=[],
                    wait=False):

    print '\n******************************************'
    print 'plot search phase results'
    
    #set ATLAS style
    if os.path.isfile(os.path.expanduser('~/RootUtils/AtlasStyle.C')):
        ROOT.gROOT.LoadMacro('~/RootUtils/AtlasStyle.C')
        ROOT.SetAtlasStyle()
        ROOT.set_color_env()
    else:
        print '\n***WARNING*** couldn\'t find ATLAS Style'
        #import AtlasStyle
        #AtlasStyle.SetAtlasStyle()
    
    #canvas
    c = ROOT.TCanvas('c', 'c', 100, 50, 800, 600)
    c.SetLogx(logx)
    c.SetLogy(1)

    textSize=20

    #pads
    outpad = ROOT.TPad("extpad","extpad", 0., 0.,   1., 1.)
    pad1   = ROOT.TPad("pad1",  "pad1",   0., 0.33, 1., 1.)
    pad2   = ROOT.TPad("pad2",  "pad2",   0., 0.,   1., 0.33)

    #setup drawing options
    outpad.SetFillStyle(4000)#transparent
    pad1.SetBottomMargin(0.00001)
    pad1.SetBorderMode(0)
    pad1.SetLogy(1)
    pad1.SetLogx(logx)
    pad2.SetTopMargin(0.00001)
    pad2.SetBottomMargin(0.3)
    pad2.SetBorderMode(0)
    pad2.SetLogx(logx)
    pad1.Draw()
    pad2.Draw()
    outpad.Draw()

    #------------------------------------------
    #draw data and fit histograms
    pad1.cd()

    #use bin range within which bkg plot has entries,
    #plus one empty on either side if available
    #print 'userFirstBin, userLastBin = %s, %s'%(userFirstBin,userLastBin)
    firstBin,lastBin = getAxisRangeFromHist(dataHist)
    #print 'firstBin, lastBin = %s, %s'%(firstBin,lastBin)
    if (userFirstBin>0) :
        firstBin=userFirstBin
        #print 'first bin = %s'%firstBin
    if (userLastBin>0 and userLastBin>=firstBin) :
        lastBin = userLastBin
        #print 'last bin  = %s'%LastBin

    #draw fit histogram
    fitHist.SetLineColor(ROOT.kRed)
    fitHist.SetFillStyle(0)
    fitHist.SetLineWidth(2)
    
    fitHist.GetXaxis().SetRange(firstBin,lastBin)
    
    fitHist.GetYaxis().SetTitle(yLab)
    fitHist.GetYaxis().SetTitleFont(43)
    fitHist.GetYaxis().SetTitleSize(textSize)
    #fitHist.GetYaxis().SetTitleOffset(1.0)
    fitHist.GetYaxis().SetLabelFont(43)
    fitHist.GetYaxis().SetLabelSize(textSize)
    #fitHist.GetYaxis().SetRangeUser(0.5,fitHist.GetMaximum()*10.)

    fitHist.Draw('hist ][')
    c.Update()
        
    #draw data histogram
    dataHist.SetMarkerStyle(textSize)
    dataHist.SetMarkerColor(ROOT.kBlack)
    dataHist.SetLineColor(ROOT.kBlack)
    dataHist.GetXaxis().SetRange(firstBin,lastBin)
    
    dataHist.Draw("E same")
    c.Update()
        
    #set y axis range
    if dataHist.GetBinContent(lastBin) <= fitHist.GetBinContent(lastBin):
        ymin = dataHist.GetBinContent(lastBin)
        if ymin == 0.:
            ymin = 0.5
        fitHist.SetMinimum(ymin*0.5)
        c.Update()

    #------------------------------------------
    #draw significance histogram
    pad2.cd()
    
    significanceHist.GetXaxis().SetTitle(xLab)
    significanceHist.GetXaxis().SetTitleFont(43)
    significanceHist.GetXaxis().SetTitleSize(textSize)
    significanceHist.GetXaxis().SetTitleOffset(3.0)
    significanceHist.GetXaxis().SetLabelFont(43)
    significanceHist.GetXaxis().SetLabelSize(textSize)
    significanceHist.GetXaxis().SetRange(firstBin,lastBin)

    significanceHist.GetYaxis().SetTitle(sigLab)
    significanceHist.GetYaxis().SetTitleFont(43)
    significanceHist.GetYaxis().SetTitleSize(textSize)
    #significanceHist.GetYaxis().SetTitleOffset(1.0)
    significanceHist.GetYaxis().SetLabelFont(43)
    significanceHist.GetYaxis().SetLabelSize(textSize)
    #significanceHist.GetYaxis().SetRangeUser(-5.,fitHist.GetMaximum*1.1)

    significanceHist.SetLineColor(ROOT.kBlack)
    significanceHist.SetLineWidth(2)
    significanceHist.SetFillColor(ROOT.kRed)
    significanceHist.SetFillStyle(1001)

    significanceHist.Draw("HIST")
    c.Update()
    
    #------------------------------------------
    #labels
    pad1.cd()

    ax = 0.60
    ay = 0.85
    a = plotTools.getATLAS()
    p = plotTools.getInternal()
    n = plotTools.getNote(textSize)
            
    #ATLAS internal
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'internal')

    #notes
    allNotes = []
    allNotes.append('#sqrt{s} = %s TeV'%CME)
    if float(luminosity) > 0.:
        if float(luminosity) < 0.1:
            allNotes.append('L_{int} = %.0f pb^{-1}'%float(luminosity)*1e3)
        else:
            allNotes.append('L_{int} = %.1f fb^{-1}'%float(luminosity))
    allNotes.append('#chi^{2}/ndf = %.3f'%float(chi2ndf))
    allNotes.append('bump range = %.0f - %.0f GeV'%(float(bumpLow), float(bumpHigh)))
    allNotes.append('BH p-value = %.4f'%float(BHpval))
    if bumpFound:
        allNotes.append('bump range excluded')
    else:
        allNotes.append('bump range not excluded')            
    allNotes.append('%s par. fit func.'%nPar)
    allNotes+=notes
    
    for ii, note in enumerate(allNotes):
        n.DrawLatex(ax,ay-0.05*(ii+1),note)

    c.Update()

    #------------------------------------------
    #draw bump lines
    line = ROOT.TLine()
    if bumpFound:
        line.SetLineColor(ROOT.kGreen+1)
    else:
        line.SetLineColor(ROOT.kBlue)
    line.SetLineWidth(1)
    pad1.cd()
    line.DrawLine( bumpLow, dataHist.GetYaxis().GetXmin(),
                    bumpLow, dataHist.GetBinContent( dataHist.FindBin(bumpLow) ) )
    line.DrawLine( bumpHigh, dataHist.GetYaxis().GetXmin(),
                    bumpHigh, dataHist.GetBinContent( dataHist.FindBin(bumpHigh)-1 ) )
    pad2.cd()
    line.DrawLine( bumpLow, significanceHist.GetMinimum(),
                    bumpLow, 2*significanceHist.GetMaximum() )
    line.DrawLine( bumpHigh, significanceHist.GetMinimum(),
                    bumpHigh, 2*significanceHist.GetMaximum() )
    c.Update()    

    #------------------------------------------
    #save
    c.Update()
    if wait:
        c.WaitPrimitive()
    localdir = os.path.dirname(os.path.realpath(__file__))
    c.SaveAs(localdir+'/figures/bumphunt.'+name+'.pdf')


#******************************************
def plotTomography(tomographyHist,
                    xLab,
                    yLab,
                    name,
                    luminosity,
                    CME,
                    BHpval,
                    nPar,
                    bumpLow=0,
                    bumpHigh=0,
                    bumpFound=False,
                    logx=False,
                    notes=[],
                    wait=False):

    print '\n******************************************'
    print 'plot search phase tomography'
    
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
    #canvas
    c = ROOT.TCanvas('c', 'c', 100, 50, 800, 600)
    c.SetLogx(logx)
    c.SetLogy(1)

    #------------------------------------------
    #draw
    textSize = 20
    
    tomographyHist.SetLineColor(ROOT.kRed)
    tomographyHist.SetTitle("");

    tomographyHist.GetXaxis().SetTitle(xLab)
    tomographyHist.GetXaxis().SetTitleFont(43)
    tomographyHist.GetXaxis().SetTitleSize(textSize)
    #tomographyHist.GetXaxis().SetTitleOffset(3.0)
    tomographyHist.GetXaxis().SetLabelFont(43)
    tomographyHist.GetXaxis().SetLabelSize(textSize)
    #tomographyHist.GetXaxis().SetNdivisions(805,ROOT.kTRUE)
    #tomographyHist.GetXaxis().SetMoreLogLabels()

    tomographyHist.GetYaxis().SetTitle("Poisson p-value")
    tomographyHist.GetYaxis().SetTitleFont(43)
    tomographyHist.GetYaxis().SetTitleSize(textSize)
    #tomographyHist.GetYaxis().SetTitleOffset(1.2)
    tomographyHist.GetYaxis().SetLabelFont(43)
    tomographyHist.GetYaxis().SetLabelSize(textSize)
    #tomographyHist.GetYaxis().SetRangeUser(-5.,fitHist.GetMaximum*1.1)
    #tomographyHist.GetYaxis().SetMoreLogLabels()

    tomographyHist.SetMarkerColor(ROOT.kRed)
    tomographyHist.SetMarkerSize(0.2)
    tomographyHist.Draw("AP");

    #------------------------------------------
    #labels
    c.cd()

    ax = 0.60
    ay = 0.85
    a = plotTools.getATLAS()
    p = plotTools.getInternal()
    n = plotTools.getNote(textSize)
            
    #ATLAS internal
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'internal')

    #notes
    allNotes = []
    allNotes.append('#sqrt{s} = %s TeV'%CME)
    if float(luminosity) > 0.:
        if float(luminosity) < 0.1:
            allNotes.append('L_{int} = %.0f pb^{-1}'%float(luminosity)*1e3)
        else:
            allNotes.append('L_{int} = %.1f fb^{-1}'%float(luminosity))
    allNotes.append('#chi^{2}/ndf = %.3f'%float(chi2ndf))
    allNotes.append('bump range = %.0f - %.0f GeV'%(float(bumpLow), float(bumpHigh)))
    allNotes.append('BH p-value = %.4f'%float(BHpval))
    if bumpFound:
        allNotes.append('bump range excluded')
    else:
        allNotes.append('bump range not excluded')            
    allNotes.append('%s par. fit func.'%nPar)
    allNotes+=notes
    
    for ii, note in enumerate(allNotes):
        n.DrawLatex(ax,ay-0.04*(ii+1),note)

    c.Update()

    #------------------------------------------    
    #save
    c.Update()
    if wait:
        c.WaitPrimitive()
    localdir = os.path.dirname(os.path.realpath(__file__))
    c.SaveAs(localdir+'/figures/tomography.'+name+'.pdf')

    
#******************************************
#main
#******************************************
if __name__ == "__main__":

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--bump', action='store_true', default=False, help='plot search phase BumpHunt')
    group.add_argument('--tomo', action='store_true', default=False, help='plot search phase tomography')
    parser.add_argument('--file', dest='inputFileName', default='', required=True, help='input file name')
    parser.add_argument('--lumi', dest='lumi', default=-999., help='luminosity [fb^-1]')
    parser.add_argument('--notes', dest='notes', nargs='+', type=str, default=[''], help='list of notes to be printed on the plot')
    parser.add_argument('--xlabel', dest='xlabel', default='m [GeV]', help='x-axis label')
    parser.add_argument('--tag', dest='tag', default='default', help='tag for output files')
    parser.add_argument('--wait', dest='wait', action='store_true', default=False, help='wait?')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    print '\n******************************************'
    print 'print search phase results'
    
    #------------------------------------------
    #open SearchPhase results file
    if not os.path.isfile(args.inputFileName):
        raise SystemExit('\n***ERROR*** couldn\'t find input search phase file: %s'%args.inputFileName)
    inputFile = ROOT.TFile(args.inputFileName,'READ')
    if not inputFile:
        raise SystemExit('\n***ERROR*** couldn\'t open input search phase file: %s'%args.inputFileName)

    #------------------------------------------
    #first things first
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()

    #------------------------------------------
    #get SearchPhase results
    #histograms
    basicData                  = inputFile.Get("basicData")
    basicBackground            = inputFile.Get("basicBkgFrom4ParamFit")
    residualHist               = inputFile.Get("residualHist")
    #bumpHunterStatHistNullCase = inputFile.Get("bumpHunterStatHistNullCase")

    #vector
    bumpHunterStatOfFitToData = inputFile.Get("bumpHunterStatOfFitToData")
    bumpHunterStatValue = bumpHunterStatOfFitToData[0]
    bumpHunterPValue    = bumpHunterStatOfFitToData[1]
    bumpHunterPValueErr = bumpHunterStatOfFitToData[2]

    #vector
    bumpHunterPLowHigh = inputFile.Get('bumpHunterPLowHigh')
    #bumpHunterStatValue = bumpHunterPLowHigh[0]
    bumpLowEdge         = bumpHunterPLowHigh[1]
    bumpHighEdge        = bumpHunterPLowHigh[2]

    bumpFoundVector = inputFile.Get("bumpFound")
    bumpFound = bumpFoundVector[0]

    #tomography
    tomographyGraph = inputFile.Get('bumpHunterTomographyFromPseudoexperiments')
    
    #print info
    print "\nbump range: %s GeV - %s GeV"%(bumpLowEdge,bumpHighEdge)
    print "bump window excluded? %s"%bool(bumpFound)
    print "BumpHunter stat = %s"%bumpHunterStatValue
    print "BumpHunter p-value = %s +/- %s"%(bumpHunterPValue, bumpHunterPValueErr)

    bumpHunterSigmas = ROOT.Math.normal_quantile(1.-bumpHunterPValue, 1.)
    print "BumpHunter sigmas = %s"%bumpHunterSigmas

    fittedParameters = inputFile.Get('fittedParameters')

    #------------------------------------------
    #fit chi2/ndf
    chi2OfFitToData = inputFile.Get('chi2OfFitToData')
    chi2OfFitToDataValue = chi2OfFitToData[0]
    ndf = inputFile.Get('NDF')
    ndfValue = ndf[0]
    chi2ndf = float(chi2OfFitToDataValue/ndfValue)
    print 'fit chi2/ndf = %.3f'%chi2ndf

    #------------------------------------------
    #define necessary quantities
    nPar = len(fittedParameters)
    name = args.inputFileName.replace('.root', '')
    name = os.path.basename(name)
    if args.tag != '':
        name+='.'+args.tag
        
    #------------------------------------------
    #plot

    if args.bump:
        #bump hunt
        plotSearchPhase(basicData,
                        basicBackground,
                        residualHist,
                        args.xlabel,
                        'events',
                        'significance',
                        name,
                        args.lumi,
                        13,
                        chi2ndf,
                        bumpHunterPValue,
                        nPar,
                        -1,
                        -1,
                        bumpLowEdge,
                        bumpHighEdge,
                        bumpFound,
                        False,
                        args.notes,
                        args.wait)
    if args.tomo:
        #tomography
        plotTomography(tomographyGraph,
                        args.xlabel,
                        'events',
                        name,
                        args.lumi,
                        13,
                        bumpHunterPValue,
                        nPar,
                        bumpLowEdge,
                        bumpHighEdge,
                        bumpFound,
                        False,
                        args.notes,
                        args.wait)

    #------------------------------------------
    inputFile.Close()

    print '\ndone'
    print '******************************************'
