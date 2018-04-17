#!/usr/bin/env python

#******************************************
#import stuff
import math, os, sys, ROOT

#******************************************
def runSearchPhase(inputFileName, inputHistDir, inputHistName, lumi, nPar, tag):

    print '\n******************************************'
    print 'run search phase'
    
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

    lumi = float(lumi)
    nPar = int(nPar)
    
    print '\nparameters:'
    print '  input file name: %s'%inputFileName
    print '  input hist dir:  %s'%inputHistDir
    print '  input hist name: %s'%inputHistName
    print '  lumi [ifb]:      %s'%lumi
    print '  n par.:          %s'%nPar
    print '  tag:             %s'%tag
    
    #------------------------------------------
    #prepare config file
    localdir = os.path.dirname(os.path.realpath(__file__))
    configFileName    = localdir+'/data/searchPhase.config'
    newConfigFileName = localdir+'/configs/searchPhase.'+tag+'.config'
    #print configFileName
    #print newConfigFileName
    searchPhaseOutputFileName = localdir+'/results/searchPhase.'+tag+'.root'
    
    #starting parameters
    #3 par, 1/fb:   0.180377, 8.1554,  -5.25718
    #4 par, 1/fb:   4.28171, 10.814,   -2.72612,  0.577889
    #4 par, 30/fb: 59.28,    12.85,    -0.5871,   1.069
    #5 par, 1/fb: 0.426909,   9.45062, -5.49925, -0.759262, -0.240173

    if nPar == 3:
        pars = [0.180377, 8.1554, -5.25718]
    elif nPar == 5:
        pars = [0.426909, 9.45062, -5.49925, -0.759262, -0.240173]
    elif nPar == 6:
        pars = [0.756961, 21.0028, -5.18678, -1.25474, -0.326143, 19998.6]
    else:
        nPar = 4 #DEFAULT
        pars = [4.28171, 10.814, -2.72612, 0.577889]
        if float(str(lumi).replace('p','.')) > 10.0:
            pars = [59.28,    12.85,  -0.5871,  1.069]

    with open(configFileName,'r') as configFile:
        with open(newConfigFileName,'w') as newConfigFile:
            for line in configFile:
                newLine = line
                newLine = newLine.replace('dummyInputFileName', inputFileName)
                if len(inputHistDir)>0:
                    newLine = newLine.replace('#inputHistDir', 'inputHistDir\t\t'+inputHistDir)
                newLine = newLine.replace('dummyHistName', inputHistName)
                newLine = newLine.replace('dummyOutputFileName', searchPhaseOutputFileName)

                #3 parameters
                if nPar == 3:
                    newLine = newLine.replace('dummyFuncCode', str(9))
                    newLine = newLine.replace('dummyNPar', str(3))
                    newLine = newLine.replace('dummyP1', str(pars[0]))
                    newLine = newLine.replace('dummyP2', str(pars[1]))
                    newLine = newLine.replace('dummyP3', str(pars[2]))

                #4 parameters
                elif nPar == 4:
                    newLine = newLine.replace('dummyFuncCode', str(4))
                    newLine = newLine.replace('dummyNPar', str(4))
                    newLine = newLine.replace('dummyP1', str(pars[0]))
                    newLine = newLine.replace('dummyP2', str(pars[1]))
                    newLine = newLine.replace('dummyP3', str(pars[2]))
                    newLine = newLine.replace('#parameter4', 'parameter4\t\t'+str(pars[3]))

                #5 parameters
                elif nPar == 5:
                    newLine = newLine.replace('dummyFuncCode', str(7))
                    newLine = newLine.replace('dummyNPar', str(5))
                    newLine = newLine.replace('dummyP1', str(pars[0]))
                    newLine = newLine.replace('dummyP2', str(pars[1]))
                    newLine = newLine.replace('dummyP3', str(pars[2]))
                    newLine = newLine.replace('#parameter4', 'parameter4\t\t'+str(pars[3]))
                    newLine = newLine.replace('#parameter5', 'parameter5\t\t'+str(pars[4]))

                #6 parameters
                elif nPar == 6:
                    newLine = newLine.replace('dummyFuncCode', str(8))
                    newLine = newLine.replace('dummyNPar', str(6))
                    newLine = newLine.replace('dummyP1', str(pars[0]))
                    newLine = newLine.replace('dummyP2', str(pars[1]))
                    newLine = newLine.replace('dummyP3', str(pars[2]))
                    newLine = newLine.replace('#parameter4', 'parameter4\t\t'+str(pars[3]))
                    newLine = newLine.replace('#parameter5', 'parameter5\t\t'+str(1.000))
                    newLine = newLine.replace('#parameter6', 'parameter6\t\t'+str(1.000))

                newConfigFile.write(newLine)

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #search phase
    print '\n******************************************'
    print 'runnning SearchPhase'
    os.system('SearchPhase --config %s --noDE'%newConfigFileName)
    
    #------------------------------------------
    #get BH p-value
    #open SearchPhase results file
    if not os.path.isfile(searchPhaseOutputFileName):
        raise SystemExit('\n***ERROR*** couldn\'t find SearchPhase output file')
    searchPhaseOutputFile = ROOT.TFile(searchPhaseOutputFileName)

    #get SearchPhase results
    #histograms
    basicData                  = searchPhaseOutputFile.Get("basicData")
    basicBackground            = searchPhaseOutputFile.Get("basicBkgFrom4ParamFit")
    residualHist               = searchPhaseOutputFile.Get("residualHist")
    #bumpHunterStatHistNullCase = searchPhaseOutputFile.Get("bumpHunterStatHistNullCase")
    #print 'basicBackground entries = %s'%basicBackground.GetEntries()

    #initial BH p-value
    bumpHunterStatOfFitToDataInitial = searchPhaseOutputFile.Get("bumpHunterStatOfFitToDataInitial")
    #bumpHunterStatValueInitial = bumpHunterStatOfFitToDataInitial[0]
    bumpHunterPValueInitial    = bumpHunterStatOfFitToDataInitial[1]
    bumpHunterPValueErrInitial = bumpHunterStatOfFitToDataInitial[2]

    #vector
    bumpHunterStatOfFitToData = searchPhaseOutputFile.Get("bumpHunterStatOfFitToData")
    if not bumpHunterStatOfFitToData:
        raise SystemExit('\n***ERROR*** couldn\'t find bumpHunterStatOfFitToData vector')
    
    bumpHunterStatValue = bumpHunterStatOfFitToData[0]
    bumpHunterPValue    = bumpHunterStatOfFitToData[1]
    bumpHunterPValueErr = bumpHunterStatOfFitToData[2]

    #vector
    bumpHunterPLowHigh = searchPhaseOutputFile.Get('bumpHunterPLowHigh')
    #bumpHunterStatValue = bumpHunterPLowHigh[0]
    bumpLowEdge         = bumpHunterPLowHigh[1]
    bumpHighEdge        = bumpHunterPLowHigh[2]

    #vector
    bumpFoundVector = searchPhaseOutputFile.Get("bumpFound")
    bumpFound = bool(bumpFoundVector[0])

    #print
    print "\nbump range: %s GeV - %s GeV"%(bumpLowEdge,bumpLowEdge)
    print "BumpHunter stat = %s"%bumpHunterStatValue
    print "initial BumpHunter p-value = %s +/- %s"%(bumpHunterPValueInitial, bumpHunterPValueErrInitial)
    print "final BumpHunter p-value =   %s +/- %s"%(bumpHunterPValue, bumpHunterPValueErr)
    bumpHunterSigmas = ROOT.Math.normal_quantile(1.-bumpHunterPValue, 1.)
    print "BumpHunter sigmas = %s"%bumpHunterSigmas
    print 'bump found? %s'%bumpFound

    #fit chi2/ndf
    chi2OfFitToData = searchPhaseOutputFile.Get('chi2OfFitToData')
    chi2OfFitToDataValue = chi2OfFitToData[0]
    ndf = searchPhaseOutputFile.Get('NDF')
    ndfValue = ndf[0]
    chi2ndf = float(chi2OfFitToDataValue/ndfValue)
    print '\nfit chi2/ndf = %.3f'%chi2ndf

    #log likelihood
    logL = searchPhaseOutputFile.Get('logLOfFitToData')
    logLValue = logL[0]
    
    #------------------------------------------
    return searchPhaseOutputFileName, bumpHunterPValueInitial, bumpHunterPValue, bumpFound, chi2ndf, logLValue, bumpLowEdge, bumpHighEdge

#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #check input parameters
    if len(sys.argv) != 7:
        raise SystemExit(
            '\n***ERROR*** wrong input parameters (%s/%s) \
            \nHOW TO: time python -u runSearchPhase.py inputFileName inputHistDir inputHistName lumi nPar tag'\
            %(len(sys.argv),7))

    #------------------------------------------
    #get input parameters and run
    inputFileName = sys.argv[1].strip()
    inputHistDir = sys.argv[2].strip()
    inputHistName = sys.argv[3].strip()
    lumi = sys.argv[4].strip()
    nPar = sys.argv[5].strip()
    tag = sys.argv[6].strip()

    output = runSearchPhase(inputFileName, inputHistDir, inputHistName, lumi, nPar, tag)
    
    #------------------------------------------
    print '\ndone: %s'%list(output)
