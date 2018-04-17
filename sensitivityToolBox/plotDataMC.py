#!/bin/python

#******************************************
#import stuff
import ROOT, math, os, sys, argparse, time
import plotTools

#******************************************
#set ATLAS style
if os.path.isfile(os.path.expanduser('~/RootUtils/AtlasStyle.C')):
    ROOT.gROOT.LoadMacro('~/RootUtils/AtlasStyle.C')
    ROOT.SetAtlasStyle()
    ROOT.set_color_env()
else:
    #print '\n***WARNING*** couldn\'t find ATLAS Style'
    import AtlasStyle
    AtlasStyle.SetAtlasStyle()

#******************************************
#parse input arguments
parser = argparse.ArgumentParser(description='%prog [options]')#, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--datafile', dest='dataFileName', default='', required=True, help='data file name')
parser.add_argument('--MCfiles', dest='MCFileNames', nargs='+', type=str, default=[], required=True, help='MC file names')
parser.add_argument('--hist', dest='histName', default='', required=True, help='input histogram name')
parser.add_argument('--outputTag', dest='outputTag', default='results', help='tag for output files')
parser.add_argument('--labels', dest='labels', nargs='+', type=str, default=[], help='input file labels')
parser.add_argument('--xlabel', dest='xlabel', default='', help='x axis label')
parser.add_argument('--ylabel', dest='ylabel', default='events', help='y axis label')
parser.add_argument('--logx', dest='logx', action='store_true', default=False, help='x axis log scale?')
parser.add_argument('--logy', dest='logy', action='store_true', default=True, help='y axis log scale?')
parser.add_argument('--tag', dest='tag', default='standard', help='tag for output files')
parser.add_argument('--lumi', dest='lumi', type=float, default=-1.0, help='desired luminosity in fb^-1')
parser.add_argument('--notes', dest='notes', nargs='+', type=str, default=[], help='list of notes to add to the plots')
parser.add_argument('--wait', dest='wait', action='store_true', default=False, help='wait?')
parser.add_argument('--save', dest='save', action='store_true', default=False, help='save plots?')
parser.add_argument('-b', '--batch', dest='batch', action='store_true', default=False, help='batch mode for PyRoot')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose mode for debugging')

#******************************************
def plotDataMC(args):

    print '\n******************************************'
    print 'plotting data and MC distributions together'

    #------------------------------------------
    #input parameters
    print '\ninput parameters:'
    argsdict = vars(args)
    for ii in xrange(len(argsdict)):
        print '  %s = %s'%(argsdict.keys()[ii], argsdict.values()[ii],)

    #------------------------------------------
    #define useful variables
    lumi = float(args.lumi) #fb^-1
    #colors = plotTools.getColors()
    colors = []
    colors.append(ROOT.kRed+1)
    colors.append(ROOT.kBlue+1)
    colors.append(ROOT.kGreen+1)

    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))

    #------------------------------------------
    #first things first
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()
    ROOT.TH2.SetDefaultSumw2()
    ROOT.TH2.StatOverflows()

    #------------------------------------------
    #check inputs
    if args.dataFileName == '':
        raise SystemExit('\n***EXIT*** no data file given')

    if len(args.MCFileNames) == 0:
        raise SystemExit('\n***EXIT*** no MC files given')

    if len(args.histName) == 0:
        raise SystemExit('\n***EXIT*** no histogram name given')

    inputFileNames = []
    inputFileNames.append(args.dataFileName)
    inputFileNames += args.MCFileNames
    #print inputFileNames#DEBUG
      
    if len(inputFileNames) != len(args.labels):
        raise SystemExit('\n***EXIT*** number of files and labels is different: %s files and %s labels'%( len(inputFileNames), len(args.labels)))

    #------------------------------------------
    #open files and get histograms
    files = []
    hists = []

    for ii in xrange( len(inputFileNames)):
        
        #open input file
        if not os.path.isfile(inputFileNames[ii]):
            raise SystemExit('\n***ERROR*** couldn\'t find input file: %s'%inputFileNames[ii])
        files.append(ROOT.TFile(inputFileNames[ii]))
    
        #get input histogram
        if not files[ii].Get(args.histName):
            raise SystemExit('\n***ERROR*** couldn\'t find input histogram %s in file %s'%(args.histName,args.histName))
        hists.append(files[ii].Get(args.histName))

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #scale MC to data
    print '\nscaling MC distributions to data integral'

    print 'before'
    for ii, hist in enumerate(hists):
        print '  %s\t%s\t%s\t%s'%(ii, hist.Integral(), hist.Integral('width'), hist.GetEntries())


    for ii in xrange( len(hists)):
        if ii==0: continue #skip data file
        hists[ii].Scale(hists[0].Integral()/hists[ii].Integral())

    print 'after'
    for ii, hist in enumerate(hists):
        print '  %s\t%s\t%s\t%s'%(ii, hist.Integral(), hist.Integral('width'), hist.GetEntries())
    
    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #labels and legends
    ax = 0.65
    ay = 0.85
    size=20
    a = plotTools.getATLAS()
    p = plotTools.getInternal()
    n = plotTools.getNote(size)
    l = plotTools.getLegend(ax,ay,size)
    line = plotTools.getLine()
    
    #------------------------------------------
    #canvas and pads
    c = ROOT.TCanvas('c', 'c', 400, 50, 800, 600)
    pad1 = ROOT.TPad("pad1","pad1",0, 0.5, 1, 1.0)#top
    pad2 = ROOT.TPad("pad2","pad2",0, 0.3, 1, 0.5)#central
    pad3 = ROOT.TPad("pad3","pad3",0, 0.0, 1, 0.3)#bottom
    
    pad1.SetTopMargin(0.08)
    pad1.SetBottomMargin(0.0)
    pad1.SetBorderMode(0)
    pad1.Draw()

    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.0)
    pad2.SetBorderMode(0)
    pad2.Draw()

    pad3.SetTopMargin(0.0)
    pad3.SetBottomMargin(1./3.)
    pad3.SetBorderMode(0)
    pad3.Draw()
    
    #------------------------------------------
    #draw histograms
    pad1.cd()
    pad1.SetLogx(args.logx)
    pad1.SetLogy(1)
    pad1.SetGrid(1,1)

    #data histogram
    hists[0].SetMarkerStyle(20)
    hists[0].SetMarkerColor(ROOT.kBlack)
    hists[0].SetLineColor(ROOT.kBlack)
    hists[0].SetFillStyle(0)
    hists[0].SetLineWidth(2)
    ymax = ROOT.gPad.GetFrame().GetY2()

    #MC histograms
    for ii in xrange( len(hists)):
        if ii == 0: continue
        hists[ii].SetMarkerStyle(0)
        hists[ii].SetMarkerColor(colors[ (ii-1)%len(colors) ] )
        hists[ii].SetLineColor(colors[ (ii-1)%len(colors) ] )
        hists[ii].SetFillStyle(0)
        hists[ii].SetLineWidth(2)
        hists[ii].GetYaxis().SetRangeUser(0.1,ymax)
    
    hs = ROOT.THStack('hs','hs')
    for ii in xrange( len(hists)):
        hs.Add(hists[ii])
    hs.Draw('nostack')

    hs.GetYaxis().SetTitle("events/bin")
    hs.GetYaxis().SetTitleFont(43)
    hs.GetYaxis().SetTitleSize(size)
    hs.GetYaxis().SetLabelFont(43)
    hs.GetYaxis().SetLabelSize(size)
    
    hs.GetXaxis().SetTitle(args.xlabel)
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(size)
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(size)

    hs.Draw('nostack')
    c.Update()

    #------------------------------------------
    #draw ratios
    pad2.cd()
    pad2.SetLogx(args.logx)
    pad2.SetLogy(0)
    pad2.SetGrid(1,1)

    ratios = []
    
    for ii in xrange( len(hists)):
        if ii == 0: continue
        ratio = hists[0].Clone()
        ratio.Divide(hists[ii])
        ratio.SetName('ratio_%s'%str(ii))
        ratio.SetTitle('ratio_%s'%str(ii))

        ratio.SetMarkerStyle(0)
        ratio.SetMarkerColor(colors[ (ii-1)%len(colors) ] )
        ratio.SetLineColor(colors[ (ii-1)%len(colors) ] )
        ratio.SetFillStyle(0)
        ratio.SetLineWidth(2)

        ratio.GetYaxis().SetRangeUser(0.,2.)#TEST

        ratios.append(ratio)
        
    hsr = ROOT.THStack('hsr','hsr')
    for ii in xrange( len(ratios)):
        hsr.Add(ratios[ii])
    hsr.Draw('nostack')
    
    hsr.GetYaxis().SetTitle('data/MC')
    hsr.GetYaxis().SetTitleFont(43)
    hsr.GetYaxis().SetTitleSize(size)
    hsr.GetYaxis().SetLabelFont(43)
    hsr.GetYaxis().SetLabelSize(size)
    
    hsr.GetXaxis().SetTitle(args.xlabel)
    hsr.GetXaxis().SetTitleFont(43)
    hsr.GetXaxis().SetTitleSize(size)
    hsr.GetXaxis().SetTitleOffset(4.0)
    hsr.GetXaxis().SetLabelFont(43)
    hsr.GetXaxis().SetLabelSize(size)
    hsr.GetYaxis().SetMoreLogLabels(1)
    
    #lowx = ratios[0].GetBinLowEdge(1)
    #highx = ratios[0].GetBinLowEdge(ratios[0].GetNbinsX()+1)
    #line.DrawLine(lowx,1.,highx,1.)

    hsr.Draw('nostack')
    c.Update()

    #------------------------------------------
    #draw differences
    pad3.cd()
    pad3.SetLogx(args.logx)
    pad3.SetLogy(0)
    pad3.SetGrid(1,1)

    diffs = []
    
    for ii in xrange( len(hists)):
        if ii == 0: continue
        diff = hists[0].Clone()
        diff.Add(hists[ii], -1)
        diff.SetName('diff_%s'%str(ii))
        diff.SetTitle('diff_%s'%str(ii))

        diff.SetMarkerStyle(0)
        diff.SetMarkerColor(colors[ (ii-1)%len(colors) ] )
        diff.SetLineColor(colors[ (ii-1)%len(colors) ] )
        diff.SetFillStyle(0)
        diff.SetLineWidth(2)

        diff.GetYaxis().SetRangeUser(-1e3,1e3)#TEST
        
        diffs.append(diff)
        
    hsd = ROOT.THStack('hsd','hsd')
    for ii in xrange( len(diffs)):
        hsd.Add(diffs[ii])
    hsd.Draw('nostack')
    
    hsd.GetYaxis().SetTitle('data-MC')
    hsd.GetYaxis().SetTitleFont(43)
    hsd.GetYaxis().SetTitleSize(size)
    hsd.GetYaxis().SetLabelFont(43)
    hsd.GetYaxis().SetLabelSize(size)
    
    hsd.GetXaxis().SetTitle(args.xlabel)
    hsd.GetXaxis().SetTitleFont(43)
    hsd.GetXaxis().SetTitleSize(size)
    hsd.GetXaxis().SetTitleOffset(4.0)
    hsd.GetXaxis().SetLabelFont(43)
    hsd.GetXaxis().SetLabelSize(size)
    hsd.GetYaxis().SetMoreLogLabels(1)
    
    #lowx = diffs[0].GetBinLowEdge(1)
    #highx = diffs[0].GetBinLowEdge(diffs[0].GetNbinsX()+1)
    #line.DrawLine(lowx,1.,highx,1.)

    hsd.Draw('nostack')
    c.Update()

    #------------------------------------------
    #draw labels and legend
    pad1.cd()

    ax = 0.65
    ay = 0.80
    spacing = 0.08
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'internal')#internal, simualtion internal
    c.Update()
        
    #notes
    print '\nnotes:'
    notes = []
    notes.append('#sqrt{s} = 13 TeV')
    if float(lumi) > 0.:
        notes.append('L_{int} = %s fb^{-1}'%lumi)
    notes+=args.notes
    for ii, note in enumerate(notes):
        n.DrawLatex(ax,ay-spacing*(ii+1),note)
        print '  %s'%note
    c.Update()
    
    #legend
    l.Clear()
    l.SetTextSize(20)
    for ii,hist in enumerate(hists):
        if len(args.labels) == len(hists):
            l.AddEntry(hists[ii], args.labels[ii], 'pl')
        else:
            l.AddEntry(hists[ii], os.path.basename(hists[ii].GetDirectory().GetFile().GetName()), 'pl')
    l.SetX1(ax)
    l.SetY1(ay-spacing*(len(notes)+1)-spacing*l.GetNRows())
    l.SetX2(ax+0.15)
    l.SetY2(ay-spacing*(len(notes)+1))
    l.Draw()
    c.Update()

    if args.wait:
        c.WaitPrimitive()
    if args.save:
        c.SaveAs(localdir+'/figures/dataMC.%s.pdf'%args.tag)
    del c

#******************************************
if __name__ == "__main__":
    args = parser.parse_args()
    plotDataMC(args)
    print '\n******************************************'
    print 'done'
