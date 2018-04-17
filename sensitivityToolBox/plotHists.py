#!/usr/bin/env python

#******************************************
#plot histograms from different files all together

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
parser = argparse.ArgumentParser(description='%prog [options]', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--files', dest='inputFileNames', nargs='+', type=str, default=[], required=True, help='input file names')
parser.add_argument('--labels', dest='labels', nargs='+', type=str, default=[], help='input file labels')
parser.add_argument('--hists', dest='inputHistNames', nargs='+', type=str, default=[], required=True, help='input histogram names')
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
def plotHists(args):

    print '\n******************************************'
    print 'plot histograms together'

    #------------------------------------------
    #input parameters
    print '\ninput parameters:'
    argsdict = vars(args)
    for ii in xrange(len(argsdict)):
        print '  %s = %s'%(argsdict.keys()[ii], argsdict.values()[ii],)
    
    #------------------------------------------
    #define useful variables
    lumi = float(args.lumi) #fb^-1
    colors = plotTools.getColors()

    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))
	
    #------------------------------------------
    #set error sum and overflow
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()

    #------------------------------------------
    #check inputs
    if len(args.inputFileNames) == 0:
        raise SystemExit('\n***EXIT*** no files given')

    if len(args.inputHistNames) == 0:
        raise SystemExit('\n***EXIT*** no histograms given')
  
    if len(args.inputHistNames) != len(args.inputFileNames):
        raise SystemExit('\n***EXIT*** number of files and histograms is different: %s files and %s histograms'%(len(args.inputFileNames), len(args.inputHistNames)))

    print '\ninput files and histograms (%s):'%len(args.inputFileNames)
    for fileName, histName in zip(args.inputFileNames, args.inputHistNames):
        print '  %s\t%s'%(fileName,histName)

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #open files and get histograms
    files = []
    hists = []

    for ii in xrange( len(args.inputFileNames)):
        
        #open input file
        if not os.path.isfile(args.inputFileNames[ii]):
            raise SystemExit('\n***ERROR*** couldn\'t find input file: %s'%args.inputFileNames[ii])
        files.append(ROOT.TFile(args.inputFileNames[ii]))
    
        #get input histogram
        if not files[ii].Get(args.inputHistNames[ii]):
            raise SystemExit('\n***ERROR*** couldn\'t find input histogram %s in file %s'%(args.inputHistNames[ii],args.inputHistNames[ii]))
        hists.append(files[ii].Get(args.inputHistNames[ii]))

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
    #line = plotTools.getLine()
    
    #------------------------------------------
    #canvas
    '''
    c = ROOT.TCanvas('c', 'c', 60, 50, 800, 600)
    c.cd()
    c.SetLogx(args.logx)
    c.SetLogy(args.logy)
    c.SetRightMargin(0.05)
    c.Draw()
    '''
    
    c   = ROOT.TCanvas('c', 'c', 50, 50, 800, 600)
    #cp  = ROOT.TPad("cp",  "cp",  0., 0.,   1., 1.)
    cp1 = ROOT.TPad("cp1", "cp1", 0., 0.33, 1., 1.)
    cp2 = ROOT.TPad("cp2", "cp2", 0., 0.,   1., 0.33)

    c.SetRightMargin(0.15)
    c.Draw()

    cp1.SetLogx(args.logx)
    cp1.SetLogy(args.logy)
    cp2.SetLogx(args.logx)
    cp2.SetLogy(False)
    cp1.SetBottomMargin(0.)
    cp1.SetBorderMode(0)
    cp2.SetTopMargin(0.)
    cp2.SetBottomMargin(0.3)
    cp2.SetBorderMode(0)
    cp1.Draw()
    cp2.Draw()

    #cp.SetFillStyle(4000)#transparent
    #cp.Draw()
    
    #------------------------------------------
    #plot distributions
    cp1.Clear()
    cp1.cd()

    #set histograms
    hs = ROOT.THStack('hs','hs')
    hs.Clear()

    for ii,hist in enumerate(hists):
        hist.SetMarkerColor( colors[ ii%len(colors) ] )
        hist.SetLineColor( colors[ ii%len(colors) ] )
        hist.SetMarkerStyle(20)
        hs.Add(hist)
        
    hs.Draw('nostack hist')

    if len(args.xlabel) != 0:        
        hs.GetXaxis().SetTitle(args.xlabel)
    else:
        hs.GetXaxis().SetTitle(args.inputHistNames[0])
    hs.GetXaxis().SetTitleFont(43)
    hs.GetXaxis().SetTitleSize(size)
    hs.GetXaxis().SetTitleOffset(1.5)
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(size)
    #hs.GetXaxis().SetRange(firstBin,lastBin)

    hs.GetYaxis().SetTitle(args.ylabel)
    hs.GetYaxis().SetTitleFont(43)
    hs.GetYaxis().SetTitleSize(size)
    hs.GetYaxis().SetTitleOffset(1.5)
    hs.GetYaxis().SetLabelFont(43)
    hs.GetYaxis().SetLabelSize(size)
    #hs.GetYaxis().SetRangeUser(0.5,hs.GetMaximum()*10.)
    c.Update()

    #------------------------------------------
    #plot ratios
    cp2.Clear()
    cp2.cd()

    rs=[]

    #clone
    for ii in range(len(hists)):
        rs.append(hists[ii].Clone(hists[ii].GetName()+'_ratio'))

    #divide
    for ii in range(len(hists)):
        rs[ii].Divide(hists[0])

    #stack of ratio histograms
    hsr = ROOT.THStack('hsr','hsr')
    #NOTE set y axis range before drawing
    #hsr.SetMinimum(0.)#0.
    #hsr.SetMaximum(2.)#2.

    #set properties
    for ii in range(len(rs)):
        rs[ii].SetMarkerStyle(20)
        rs[ii].SetMarkerColor(colors[ii%len(colors)])
        rs[ii].SetLineColor(colors[ii%len(colors)])
        #if ii!=0: #NOTE skip the first ratio plot
        hsr.Add(rs[ii])

    hsr.Draw('nostack')
    
    #line
    #lowx = rs[0].GetBinLowEdge(1)
    #highx = rs[0].GetBinLowEdge(rs[0].GetNbinsX()+1)
    #print '\ndrawing the line in the range %s - %s'%(lowx,highx)
    #line.DrawLine(lowx,1.0,highx,1.0)
    
    hsr.GetYaxis().SetTitle('ratio')
    hsr.GetYaxis().SetTitleFont(43)
    hsr.GetYaxis().SetTitleSize(size)
    hsr.GetYaxis().SetTitleOffset(1.5)
    hsr.GetYaxis().SetLabelFont(43)
    hsr.GetYaxis().SetLabelSize(size)
        
    hsr.GetXaxis().SetTitle(args.xlabel)
    hsr.GetXaxis().SetTitleFont(43)
    hsr.GetXaxis().SetTitleSize(size)
    hsr.GetXaxis().SetTitleOffset(3.0)
    hsr.GetXaxis().SetLabelFont(43)
    hsr.GetXaxis().SetLabelSize(size)

    hsr.Draw('nostack hist')
    c.Update()

    #------------------------------------------
    #labels
    cp1.cd()

    ax = 0.20#0.65
    ay = 0.32#0.88
    spacing = 0.05#0.04
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'simulation internal')#internal, simualtion internal
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
        c.SaveAs(localdir+'/figures/histograms.%s.pdf'%args.tag)

#******************************************
if __name__ == '__main__':
    args = parser.parse_args()
    plotHists(args)
                
    print '\n******************************************'
    print 'done'
