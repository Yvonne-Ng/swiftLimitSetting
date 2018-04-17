#!/usr/bin/env python

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
parser.add_argument('--ref', dest='reference', default='', help='reference input file')
parser.add_argument('--tags', dest='inputFileTags', nargs='+', type=str, default=[], help='input file tags')
parser.add_argument('--labels', dest='labels', nargs='+', type=str, default=[], help='input file labels')
parser.add_argument('--hist', dest='inputHistName', default='', help='input histogram name')
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
def plotSlices(args):

    print '\n******************************************'
    print 'plot slices'

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
    #colors = []
    ##colors.append(ROOT.kBlack)
    #colors.append(ROOT.kGreen+1)
    #colors.append(ROOT.kCyan+1)
    #colors.append(ROOT.kBlue+1)
    #colors.append(ROOT.kMagenta+1)
    #colors.append(ROOT.kRed+1)
    #colors.append(ROOT.kYellow+1)
    #colors.append(ROOT.kSpring+1)
    #colors.append(ROOT.kTeal+1)
    #colors.append(ROOT.kAzure+1) 
    #colors.append(ROOT.kViolet+1)
    #colors.append(ROOT.kPink+1)
    #colors.append(ROOT.kOrange+1)

    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))
	
    #------------------------------------------
    #set error sum and overflow
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()

    #------------------------------------------
    #get input files
    inputFileNames = [inputFileName for inputFileName in args.inputFileNames if (all(tag in inputFileName for tag in args.inputFileTags) and '.root' in inputFileName)]
    inputFileNames = list( set(inputFileNames))
    inputFileNames.sort()
    
    #make sure we have found some files
    if len(inputFileNames) == 0:
        raise SystemExit('\n***EXIT*** no files found for tags: %s'%' '.join(args.inputFileTags))
  
    print '\ninput files (%s):'%str(len(inputFileNames)+len([args.reference]))
    if len(args.reference) != 0:
        print '  %s\t(reference)'%args.reference
    
    for fileName in inputFileNames:
        print '  %s'%fileName

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #open files and get histograms
    if len(args.reference) != 0:

        #open reference input file
        if not os.path.isfile(args.reference):
            raise SystemExit('\n***ERROR*** couldn\'t find reference input file')
        rf = ROOT.TFile(args.reference)
    
        #get input histograms
        if len(args.inputHistName) == 0:
            raise SystemExit('\n***ERROR*** no input histogram name')
        if not rf.Get(args.inputHistName):
            raise SystemExit('\n***ERROR*** couldn\'t find reference input histogram: %s'%args.inputHistName)
        rh = rf.Get(args.inputHistName)
    
    files = []
    hists = []

    for ii,inputFileName in enumerate(inputFileNames):
        
        #open input file
        if len(inputFileName) == 0:
            raise SystemExit('\n***ERROR*** no input file name')
        if not os.path.isfile(inputFileName):
            raise SystemExit('\n***ERROR*** couldn\'t find input file')
        files.append(ROOT.TFile(inputFileName))
    
        #get input histograms
        if len(args.inputHistName) == 0:
            raise SystemExit('\n***ERROR*** no input histogram name')
        if not files[ii].Get(args.inputHistName):
            raise SystemExit('\n***ERROR*** couldn\'t find input histogram: %s'%args.inputHistName)
        hists.append(files[ii].Get(args.inputHistName))

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

    #------------------------------------------
    #canvase
    c = ROOT.TCanvas('c', 'c', 60, 50, 800, 600)
    c.cd()
    c.SetLogx(args.logx)
    c.SetLogy(args.logy)
    c.SetRightMargin(0.05)
    c.Draw()

    #------------------------------------------
    #plot

    #set histograms
    hs = ROOT.THStack('hs','hs')
    hs.Clear()

    if len(args.reference) != 0:
        if rh is not None:
            rh.SetMarkerColor(ROOT.kBlack)
            rh.SetLineColor(ROOT.kBlack)
            rh.SetMarkerStyle(20)
            hs.Add(rh)
    
    for ii,hist in enumerate(hists):
        hist.SetMarkerColor( colors[ ii%len(colors) ] )
        hist.SetLineColor( colors[ ii%len(colors) ] )
        hist.SetMarkerStyle(20)
        hs.Add(hist)
        
    hs.Draw('nostack')

    if len(args.xlabel) != 0:        
        hs.GetXaxis().SetTitle(args.xlabel)
    else:
        hs.GetXaxis().SetTitle(args.inputHistName)
    hs.GetXaxis().SetTitleFont(43)
    hs.GetXaxis().SetTitleSize(20)
    hs.GetXaxis().SetTitleOffset(1.5)
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(20)
    #hs.GetXaxis().SetRange(firstBin,lastBin)

    hs.GetYaxis().SetTitle(args.ylabel)
    hs.GetYaxis().SetTitleFont(43)
    hs.GetYaxis().SetTitleSize(20)
    hs.GetYaxis().SetTitleOffset(1.5)
    hs.GetYaxis().SetLabelFont(43)
    hs.GetYaxis().SetLabelSize(size)
    #hs.GetYaxis().SetRangeUser(0.5,hs.GetMaximum()*10.)
    c.Update()

    #labels
    ax = 0.65
    ay = 0.88
    a.DrawLatex(ax,ay,'ATLAS')
    p.DrawLatex(ax+0.13,ay,'internal')
    c.Update()
        
    #notes
    print '\nnotes:'
    notes = []
    notes.append('#sqrt{s} = 13 TeV')
    if float(lumi) > 0.:
        notes.append('L_{int} = %s fb^{-1}'%lumi)
    notes+=args.notes
    for ii, note in enumerate(notes):
        n.DrawLatex(ax,ay-0.04*(ii+1),note)
        print '  %s'%note
    c.Update()
    
    #legend
    l.Clear()
    l.SetTextSize(20)
    if len(args.reference) != 0:
        if rh is not None:
            l.AddEntry(rh, 'total', 'pl')

    for ii,hist in enumerate(hists):
        if len(args.labels) == len(hists):
            l.AddEntry(hists[ii], args.labels[ii], 'pl')
        else:
            l.AddEntry(hists[ii], os.path.basename(hists[ii].GetDirectory().GetFile().GetName()), 'pl')
    l.SetX1(ax)
    l.SetY1(ay-0.04*(len(notes)+1)-0.03*l.GetNRows())
    l.SetX2(ax+0.15)
    l.SetY2(ay-0.04*(len(notes)+1))
    l.Draw()
    c.Update()

    if args.wait:
        c.WaitPrimitive()
    if args.save:
        c.SaveAs(localdir+'/figures/MCSlices.%s.%s.pdf'%(args.inputHistName,args.tag))

#******************************************
if __name__ == '__main__':
    args = parser.parse_args()
    plotSlices(args)
                
    print '\n******************************************'
    print 'done'
