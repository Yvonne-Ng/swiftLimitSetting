#!/usr/bin/env python

#******************************************
#collection of handy tools when dealing with fits and search pahse

#******************************************
#import stuff
import sys, os, math, ROOT

#******************************************
def simpleFit(fileName, histDir, histName, hmin=1100., hmax=13000., nPar=3, draw=False):

    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()

    file = ROOT.TFile(fileName)
    if not file:
        raise SystemExit('\n***ERROR*** couldn\'t find file: %s'%fileName)

    if histDir != '':
        hist = file.GetDirectory(histDir).Get(histName)
    else:
        hist = file.Get(histName)
    if not hist:
        raise SystemExit('\n***ERROR*** couldn\'t find hist: %s'%histName)

    hist.Scale(1.,'width')

    hist.GetXaxis().SetTitle('m [GeV]');
    hist.GetYaxis().SetTitle('entries/GeV');#NOTE it's scaled
    hist.SetMarkerColor(1);
    hist.SetLineColor(1);

    if draw is True:
        c1 = ROOT.TCanvas('c1', 'c1', 100, 50, 800, 600)
        c1.SetLogy(1)
        c1.SetLogx(1)
        hist.Draw();

    if nPar == 5:
        func = ROOT.TF1('mjjpar5function','[0] * pow(1-(x/13e3), [1]) * pow((x/13e3), [2]+[3]*log(x/13e3)+[4]*pow(log(x/13e3), 2))', hmin, hmax); #5 par
    elif nPar == 4:
        func = ROOT.TF1('mjj4parfunction','[0] * pow(1-(x/13e3), [1]) * pow((x/13e3), [2]+[3]*log(x/13e3))', hmin, hmax) #4 par
    else:
        func = ROOT.TF1('mjj4parfunction','[0] * pow(1-(x/13e3), [1]) * pow((x/13e3), [2])', hmin, hmax) #3 par
        
    func.SetLineColor(2);

    #dummy fit parameter values
    func.SetParameter(0,0.000001)
    func.SetParameter(1,0.94)
    func.SetParameter(2,8.7)
    if nPar == 4:
        func.SetParameter(3,0.46)
    if nPar == 5:
        func.SetParameter(4,0.)

    #fit twice
    hist.Fit(func,'NMR')
    hist.Fit(func,'NMR')

    if draw is True:
        func.Draw('same')
        c1.Update()
        c1.WaitPrimitive()

    pars=[]
    pars.append(func.GetParameter(0))
    pars.append(func.GetParameter(1))
    pars.append(func.GetParameter(2))
    if nPar == 4:
        pars.append(func.GetParameter(3))
    if nPar == 5:
        pars.append(func.GetParameter(4))
        
    return pars

#******************************************
