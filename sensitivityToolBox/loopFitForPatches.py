#!/usr/bin/env python

#******************************************
import os, itertools

#******************************************
if __name__ == '__main__':

    nPars = [3, 4]
    hists = ['mbj', 'mbb']
    btags = ['fix_8585', 'flt_8585', 'fix_7777', 'flt_7777']
    items = list(itertools.product(nPars, hists, btags) )
    slumi = '20p0'

    for item in items:
        nPar = str(item[0])
        hist = item[1]
        btag = item[2]
        command = 'time python runSearchPhase.py ../trantor/SensitivityStudies/results/datalikeQCD/datalikeQCD.'+slumi+'.ifb.'+hist+'_'+btag+'.0.seed.QCD.root "" '+hist+'_'+btag+'_smooth 20 '+nPar+' patch.QCD.'+slumi+'.ifb.'+hist+'_'+btag+'_smooth.0.seed.'+nPar+'.par'
        print '\n%s'%command
        os.system(command)
