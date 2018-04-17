#!/usr/bin/env python

#******************************************
#import stuff
import ROOT, re, sys, os, math

#******************************************
def getEffectiveEntriesHistogram(hist, name = "hee"):
    print("N: ", hist.GetXaxis().GetNbins())
    print("array: ", hist.GetXaxis().GetXbins().GetArray())
    hee = ROOT.TH1D(name,name,hist.GetXaxis().GetNbins(),hist.GetXaxis().GetXbins().GetArray())
    for ii in xrange(1,hist.GetNbinsX()+1):
        if hist.GetBinError(ii) != 0.:
            nee = pow(hist.GetBinContent(ii), 2) /  pow(hist.GetBinError(ii), 2)
        else:
            nee = 0.
        hee.SetBinContent(ii, nee)
        hee.SetBinError(ii, math.sqrt(nee))
    return hee

#******************************************
def getDataLikeHist(eff, scaled, name, seed=10, thresholdMass=1000.):
    dataLike = ROOT.TH1D(name, name, eff.GetXaxis().GetNbins(), eff.GetXaxis().GetXbins().GetArray())
    dataLike.SetDirectory(0)

    #random number generator
    rand3 = ROOT.TRandom3(1986)

    #loop over bins
    for ii in xrange(1,eff.GetNbinsX()+1):

        #enough effective entries?
        #NOTE bin upper edge must be above thresholdMass
        nee = eff.GetBinContent(ii)
        if scaled.GetBinContent(ii) > 0 and nee >= scaled.GetBinContent(ii) and scaled.GetXaxis().GetBinUpEdge(ii) > thresholdMass:

            #set seed
            #NOTE the seed for each bin must be always the same
            binSeed = int( round( eff.GetBinCenter(ii) + seed*1e5))
            rand3.SetSeed(binSeed)

            #get data-like bin content by drawing entries
            #NOTE weights are poissonian by construction
            for jj in xrange( int( round( nee))):
                if rand3.Uniform() < scaled.GetBinContent(ii) / nee :
                    dataLike.Fill(dataLike.GetBinCenter(ii))

    return dataLike

#******************************************
def getSmoothHistogram(hist, name="hs"):
    hs = ROOT.TH1D(name,name,hist.GetXaxis().GetNbins(),hist.GetXaxis().GetXbins().GetArray())
    for ii in xrange(1,hist.GetNbinsX()+1):
        bincontent = int( round( hist.GetBinContent(ii) ) )
        for jj in xrange(bincontent):
            hs.Fill(hs.GetBinCenter(ii))
    return hs

#******************************************
def addPoissonNoiseToHistogram(hist, name="hp", seed=0.):
    #NEW
    #this function is based on getSmoothHistogram
    #print '\nadding Poisson noise to histogram' #TEST

    hp = ROOT.TH1D(name,name,hist.GetXaxis().GetNbins(),hist.GetXaxis().GetXbins().GetArray())

    #random number generator
    rand3 = ROOT.TRandom3(1986)

    for ii in xrange(1,hist.GetNbinsX()+1):

        #get bin content
        bincontent = int( round( hist.GetBinContent(ii) ) )

        #set seed
        #NOTE the seed for each bin must be always the same
        binSeed = int( round( hp.GetBinCenter(ii) + seed*1e5))
        rand3.SetSeed(binSeed)

        #add Poisson noise
        bincontent = int( round( rand3.PoissonD(bincontent)))

        #print '  bin %s\t%s\t%s'%(ii, hist.GetBinContent(ii), bincontent) #TEST

        #fill
        for jj in xrange(bincontent):
            hp.Fill(hp.GetBinCenter(jj))

    return hp

#******************************************
def getRawAxesLabels(hist):
    #given a histogram, get raw labels
    if type(hist) == str:
        histName = hist
    elif 'TH' in str( type(hist)):
        histName = hist.GetName()
    else:
        histName = ''
    return histName.split('_')

#******************************************
def getAxisLabel(rawAxisLabel):
    #given a raw axis label, return the axis label

    labelsDict = {}
    labelsDict['pt'] = 'p_{T} [GeV]'
    labelsDict['pT'] = 'p_{T} [GeV]'
    labelsDict['Pt'] = 'p_{T} [GeV]'
    labelsDict['eta'] = '#eta'
    labelsDict['phi'] = '#phi'
    labelsDict['mjj'] = 'm_{jj} [GeV]'
    labelsDict['SumPtTrkPt500PV'] = '#sump_{T}^{track} [GeV]'
    labelsDict['NumTrkPt500PV'] = 'n_{tracks}'
    labelsDict['TrackWidthPt500PV'] = 'track width'
    labelsDict['ptOverSumPtTrkPt500PV'] = 'p_{T} / #sump_{T}^{track}'
    labelsDict['SumPtTrkPt500PVOverPt'] = '#sump_{T}^{track} / p_{T}'
    #labelsDict[''] = ''
    return labelsDict.get(rawAxisLabel, rawAxisLabel)

#******************************************
def getAxisLog(rawAxisLabel):
    #given a raw axis label, return a flag to set axis/axes logarithmic
    #first entry is meant for the x axis distribution
    #second entry is meant for the y axis distibution
    #third entry is meant for the y axis profile

    logDict = {}
    logDict['pt'] = [True, True, True]
    logDict['pT'] = [True, True, True]
    logDict['Pt'] = [True, True, True]
    logDict['eta'] = [False, True, False]
    logDict['phi'] = [False, False, False]
    logDict['mjj'] = [True, True, True]
    logDict['SumPtTrkPt500PV'] = [True, True, True]
    logDict['NumTrkPt500PV'] = [False, True, False]
    logDict['TrackWidthPt500PV'] = [False, True, False]
    logDict['ptOverSumPtTrkPt500PV'] = [True, True, False]
    logDict['SumPtTrkPt500PVOverPt'] = [True, True, False]

    return logDict.get(rawAxisLabel, [False, False, False])

#******************************************
def getXAxisRange(rawAxisLabel):
    #given a raw axis label, return x axis range
    rangeDict = {}
    rangeDict['pt'] = [20., 3.2e3]
    rangeDict['eta'] = [-2.8, 2.8]
    rangeDict['TrackWidthPt500PV'] = [0., 1.]
    rangeDict['ptOverSumPtTrkPt500PV'] = [0., 5.]
    rangeDict['SumPtTrkPt500PVOverPt'] = [0., 5.]
    return rangeDict.get(rawAxisLabel,[])

#******************************************
def getYAxisMin(rawAxisLabel):
    #given a raw axis label, return the minimum y axis range
    minDict = {}
    minDict['pt'] = 0.1
    minDict['pT'] = 0.1
    minDict['Pt'] = 0.1
    minDict['eta'] = -1.
    minDict['phi'] = -1.
    minDict['mjj'] = 0.1
    minDict['SumPtTrkPt500PV'] = -1.
    minDict['NumTrkPt500PV'] = 0.1
    minDict['TrackWidthPt500PV'] = 0.1
    minDict['ptOverSumPtTrkPt500PV'] = 0.1
    minDict['SumPtTrkPt500PVOverPt'] = 0.1
    return minDict.get(rawAxisLabel,-1.)

#******************************************
#def getYAxisProfileRange(rawAxisLabel):
#    #given a raw axis label, return the y axis range for a profile
#    rangeDict = {}
#    rangeDict['pt'] = [2e2, 6e2]
#    rangeDict['pT'] = [2e2, 6e2]
#    rangeDict['Pt'] = [2e2, 6e2]
#    rangeDict['ptOverSumPtTrkPt500PV'] = [0., 1.2]
#    rangeDict['SumPtTrkPt500PVOverPt'] = [0., 1.2]
#    return rangeDict.get(rawAxisLabel,-1.)

#******************************************
#get ATLAS label
def getATLAS():
    a = ROOT.TLatex()
    a.SetNDC()
    a.SetTextFont(73)
    a.SetTextColor(1)
    a.SetTextSize(30)
    return a

#******************************************
#get internal label
def getInternal():
    p = ROOT.TLatex()
    p.SetNDC()
    p.SetTextFont(43)
    p.SetTextColor(1)
    p.SetTextSize(30)
    return p

#******************************************
#get note
def getNote(size=15):
    n = ROOT.TLatex()
    n.SetNDC()
    n.SetTextFont(43)
    n.SetTextColor(1)
    n.SetTextSize(size)
    return n

#******************************************
#get legend
def getLegend(ax=65, ay=90, size=15):
    l = ROOT.TLegend(ax, ay, ax+0.15, ay-0.12)
    l.SetFillStyle(0)
    l.SetFillColor(0)
    l.SetLineColor(0)
    l.SetTextFont(43)
    l.SetBorderSize(0)
    l.SetTextSize(size)
    return l

#******************************************
#get line
def getLine():
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(1)
    line.SetLineStyle(7)
    return line

#******************************************
def getColors():
    colors = []
    #colors.append(ROOT.kBlack)
    colors.append(ROOT.kGreen+1)
    colors.append(ROOT.kCyan+1)
    colors.append(ROOT.kBlue+1)
    colors.append(ROOT.kMagenta+1)
    colors.append(ROOT.kRed+1)
    colors.append(ROOT.kYellow+1)
    colors.append(ROOT.kSpring+1)
    colors.append(ROOT.kTeal+1)
    colors.append(ROOT.kAzure+1)
    colors.append(ROOT.kViolet+1)
    colors.append(ROOT.kPink+1)
    colors.append(ROOT.kOrange+1)
    return colors

#******************************************
def getMarkers():
    markers = []
    markers.append(20)
    markers.append(22)
    markers.append(21)
    markers.append(23)
    return markers

#******************************************
#TEST #CHECK
def getCanvasWithRatioPad():
    c   = ROOT.TCanvas('c', 'c', 50, 50, 800, 600)
    cp  = ROOT.TPad("cp",  "cp",  0., 0.,   1., 1.)
    cp1 = ROOT.TPad("cp1", "cp1", 0., 0.33, 1., 1.)
    cp2 = ROOT.TPad("cp2", "cp2", 0., 0.,   1., 0.33)

    c.SetRightMargin(0.15)
    #c.Draw()

    cp1.SetLogx(logs[0])
    cp1.SetLogy(True)
    cp1.SetBottomMargin(0.)
    cp1.SetBorderMode(0)
    #cp1.Draw()

    cp2.SetLogx(logs[0])
    cp2.SetLogy(False)
    cp2.SetTopMargin(0.)
    cp2.SetBottomMargin(0.3)
    cp2.SetBorderMode(0)
    #cp2.Draw()

    cp.SetFillStyle(4000)#transparent
    #cp.Draw()

    return c, cp1, cp2, cp

#******************************************
#DEPRACATED
#******************************************

#******************************************
def getAxesLabels(hist):
    #given a histogram name using the convention 'x_y_z_anything_else', retrieve axes labels
    #FIX return raw labels if no labal is available from the dictionary
    #NOTE this is becoming deprecated, use getAxisLabel instead

    #define labels dictionary
    labelsDict = {}
    labelsDict['pt'] = 'p_{T} [GeV]'
    labelsDict['pT'] = 'p_{T} [GeV]'
    labelsDict['Pt'] = 'p_{T} [GeV]'
    labelsDict['eta'] = '#eta'
    labelsDict['phi'] = '#phi'
    labelsDict['mjj'] = 'm_{jj} [GeV]'
    labelsDict['SumPtTrkPt500PV'] = '#sump_{T}^{track} [GeV]'
    labelsDict['NumTrkPt500PV'] = 'n_{tracks}'
    labelsDict['TrackWidthPt500PV'] = 'track width'
    labelsDict['ptOverSumPtTrkPt500PV'] = 'p_{T} / #sump_{T}^{track}'
    labelsDict['SumPtTrkPt500PVOverPt'] = '#sump_{T}^{track} / p_{T}'
    #labelsDict[''] = ''

    #get raw labels
    rawLabels = getRawAxesLabels(hist)

    #get labels
    if 'TH1' in str( type(hist) ):
        labels = ['']
        if len(rawLabels) >= 1:
            labels[0] = labelsDict.get(rawLabels[0],'')

    elif 'TH2' in str( type(hist) ):
        labels = ['', '']
        if len(rawLabels) >= 2:
            labels[0] = labelsDict.get(rawLabels[0],'')
            labels[1] = labelsDict.get(rawLabels[1],'')

    elif 'TH3' in str( type(hist) ):
        labels = ['', '', '']
        if len(rawLabels) >= 3:
            labels[0] = labelsDict.get(rawLabels[0],'')
            labels[1] = labelsDict.get(rawLabels[1],'')
            labels[2] = labelsDict.get(rawLabels[2],'')

    else:
        print '\n***WARNING*** \'%s\' format is not supported (%s)'%(type(hist), histName)
        return rawLabels #NOTE risky

    #check labels
    #replace empty labels with raw labels
    for ii in range( len(labels) ):
        if len(labels[ii]) <= 0:
            print '\n***WARNING*** could not find label for \'%s\' in %s histogram, using label from histogram name instead: \'%s\''%(rawLabels[ii], histName, rawLabels[ii])
            labels[ii] = rawLabels[ii]

    return labels

#******************************************
def getAxesLogs(rawAxisLabel):
    #given an histogram, return a flag to set axis/axes logarithmic
    #NOTE this is becoming deprecated, use getAxisLog instead

    #define logs dictionaries

    #x axis
    logXDict = {}
    logXDict['pt'] = False
    logXDict['pT'] = False
    logXDict['Pt'] = False
    logXDict['eta'] = False
    logXDict['phi'] = False
    logXDict['mjj'] = True
    logXDict['SumPtTrkPt500PV'] = True
    logXDict['NumTrkPt500PV'] = False
    logXDict['TrackWidthPt500PV'] = False
    logXDict['ptOverSumPtTrkPt500PV'] = True
    logXDict['SumPtTrkPt500PVOverPt'] = True

    #yaxis
    logYDict = {}
    logYDict['pt'] = False
    logYDict['pT'] = False
    logYDict['Pt'] = False
    logYDict['eta'] = False
    logYDict['phi'] = False
    logYDict['mjj'] = True
    logYDict['SumPtTrkPt500PV'] = True
    logYDict['NumTrkPt500PV'] = False
    logYDict['TrackWidthPt500PV'] = False
    logYDict['ptOverSumPtTrkPt500PV'] = True
    logYDict['SumPtTrkPt500PVOverPt'] = True


    #get raw labels
    rawLabels = getRawAxesLabels(hist)

    #get logs
    logs = []
    if 'TH1' in str( type(hist) ):
        logs = [False]
        if len(rawLabels) >= 1:
            logs[0] = logXDict.get(rawLabels[0],False)

    elif 'TH2' in str( type(hist) ):
        logs = [False, False]
        if len(rawLabels) >= 2:
            logs[0] = logXDict.get(rawLabels[0],False)
            logs[1] = logYDict.get(rawLabels[1],False)

    elif 'TH3' in str( type(hist) ):
        logs = [False, False, False]
        if len(rawLabels) >= 3:
            logs[0] = logXDict.get(rawLabels[0],False)
            logs[1] = logYDict.get(rawLabels[1],False)
            logs[2] = logYDict.get(rawLabels[2],False)

    else:
        print '\n***WARNING*** \'%s\' format is not supported (%s)'%(type(hist), histName)
        return []

    return logs

#******************************************
#******************************************
