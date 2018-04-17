#!/usr/bin/env python

#******************************************
#import stuff
import ROOT
import math, os, sys, argparse, time
import multiprocessing as mp
import fileTools
from itertools import repeat

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

#******************************************
def fillHistograms(args):

    print '\n******************************************'
    print 'fill histograms'

    #------------------------------------------
    #input parameters
    print '\ninput parameters:'
    argsdict = vars(args)
    for ii in xrange(len(argsdict)):
        print '  %s = %s'%(argsdict.keys()[ii], argsdict.values()[ii],)
    
    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #get directory of this script
    localdir = os.path.dirname(os.path.realpath(__file__))
	
    #------------------------------------------
    #set error sum and overflow
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TH1.StatOverflows()
    ROOT.TH2.SetDefaultSumw2()
    ROOT.TH2.StatOverflows()

    #------------------------------------------
    #get input files
    if args.inputList != "":
        #get files from input list
        inputFileNames = fileTools.getInputFilesFromList(args.inputList, args.inputTags)
    else:
        #get the files in path which match tags
        inputFileNames = fileTools.getMergedTreeFileList(args.pathToTrees, args.inputTags)
    
    #make sure we have found some files
    if len(inputFileNames) == 0:
        raise SystemExit('\n***EXIT*** no files found for tags: %s'%' '.join(args.inputTags))
  
    print '\ninput files (%s):'%len(inputFileNames)
    for fileName in inputFileNames:
        print '  %s'%fileName

    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #clean tmp directory
    print '\ncleaning tmp/ directory'
    print 'deleting file:'
    localdir = os.path.dirname(os.path.realpath(__file__))
    tmpdir=os.path.join(localdir,'tmp')
    for f in os.listdir(tmpdir):
        if os.path.isfile(os.path.join(tmpdir,f)) and 'histograms.' in f and '.root' in f:
            print '  %s'%os.path.join(tmpdir,f)
            os.remove(os.path.join(tmpdir,f))

    print 'remaining files:'
    for f in os.listdir(tmpdir):
        print '  %s'%os.path.join(tmpdir,f)
    
    #------------------------------------------
    #TEST
    #raise SystemExit('\n***TEST*** exit')
    #------------------------------------------

    #------------------------------------------
    #fill histograms using multiple processes
    ncpu=mp.cpu_count()
    print '\nfilling histograms using the %s cores of this computer\n'%ncpu

    #use as many processes as the number of cores
    pool = mp.Pool(processes=ncpu)

    pargs = zip( range(1, len( inputFileNames)+1),
                 repeat(len(inputFileNames)),
                 inputFileNames,
                 repeat(args.outputTag),
                 repeat(args.lumi),
                 repeat(args.isMC),
                 repeat(args.configFileName))
    
    results = pool.map(fillHistogramsProcess, pargs)
    #results = pool.map(fillHistogramsProcessTEST, pargs)#TEST
    pool.close()
    pool.join()
    print '\ngot results of %s/%s processes'%(len(results), len(inputFileNames))
    if len(results) != len(inputFileNames):
        print '  successful processes: %s'%' '.join(results)
        
    #------------------------------------------
    #add results together
    results = [os.path.join(tmpdir,f) for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir,f)) and 'histograms.' in f and '.root' in f]

    print '\nresults:'
    for result in results:
        print '  %s'%result

    if args.merge:
        print '\nhadd-ing results'
        if args.isMC:
            outputFileName = 'results/histograms.mc.'+args.outputTag+'.root'
        else:
            outputFileName = 'results/histograms.data.'+args.outputTag+'.root'
    
        shadd = 'hadd '+outputFileName+' '+' '.join(results)
        #print shadd
        os.system(shadd)
    
#******************************************
def fillHistogramsProcessTEST(pargs):

    #------------------------------------------
    #input parameters
    num, tot = pargs
    time.sleep(num)
    processTag = '[process %s/%s]'%(num, tot)
    print '%s starting'%processTag
    print '%s input parameters:\n%s'%(processTag, pargs)
    print '%s done'%processTag
    return str(num)

#******************************************
def fillHistogramsProcess(pargs):

    #------------------------------------------
    #input parameters
    num, tot, inputFileName, tag, lumi, isMC, configFileName = pargs
    #time.sleep(num)#TEST
    processTag = '[process %s/%s]'%(num, tot)
    print '%s starting fillHistograms'%processTag
    print '%s input parameters:\n%s'%(processTag, pargs,)

    #------------------------------------------
    #run compiled C++
    if isMC:
        commandLine = './fillHistograms --process "'+processTag+'" --file '+inputFileName+' --isMC --name '+tag+' --lumi '+str(lumi)
    else:
        commandLine = './fillHistograms --process "'+processTag+'" --file '+inputFileName+' --isData --name '+tag+' --lumi '+str(lumi)
    
    if configFileName != "":
        commandLine+=' --config '+configFileName

    #NEW
    if args.applyNLO:
        commandLine+=' --applyNLO'

    #NEW
    if args.applyEW:
        commandLine+=' --applyEW'
            
    print '%s %s'%(processTag, commandLine)
    os.system(commandLine)
                
    #------------------------------------------
    print '%s done'%processTag
    return str(num)

#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='C++ code to quickly produce plots')

    input_parser = parser.add_mutually_exclusive_group(required=True)
    input_parser.add_argument('--list', dest='inputList', default='', help='list of input trees')
    input_parser.add_argument('--path', dest='pathToTrees', default='', help='path to the input trees')

    type_parser = parser.add_mutually_exclusive_group(required=True)
    type_parser.add_argument('--isMC', dest='isMC', action='store_true', default=True, help='this is MC')
    type_parser.add_argument('--isData', dest='isMC', action='store_false', default=True, help='this is data')

    parser.add_argument('--applyNLO', dest='applyNLO', action='store_true', default=False, help='apply k-factors for NLO corrections')
    parser.add_argument('--applyEW', dest='applyEW', action='store_true', default=False, help='apply k-factors for EW corrections')
    
    parser.add_argument('--tags', dest='inputTags', nargs='+', type=str, default=['Pythia8', 'jetjet'], help='list of tags to identify the input files')
    parser.add_argument('--outputTag', dest='outputTag', default='results', help='tag for output files')
    parser.add_argument('--lumi', dest='lumi', type=float, default=1.0, help='desired luminosity in fb^-1')

    parser.add_argument('-m', '--merge', dest='merge', action='store_true', default=False, help='merge output results')
    
    parser.add_argument('-b', '--batch', dest='batch', action='store_true', default=False, help='batch mode for PyRoot')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose mode for debugging')
    parser.add_argument('--config', dest='configFileName', default='', help='config file')

    args = parser.parse_args()
    fillHistograms(args)
    print '\n******************************************'
    print 'done'
