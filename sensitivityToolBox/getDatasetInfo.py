#!/usr/bin/python

import os, sys, argparse
import pyAMI.client
import pyAMI.atlas.api as AtlasAPI

#******************************************
#get dataset info
def getDatasetInfo(dataset, debug=False):
    
    client = pyAMI.client.Client('atlas')
    AtlasAPI.init()
    results = AtlasAPI.get_dataset_info(client, dataset)

    if len(results) != 1:
        raise SystemExit('\n***EXIT*** no valid results for dataset %s'%dataset)

    eff = None
    
    for name, value in results[0].iteritems():
        if name=='totalEvents': 
            nevents = value
        elif name=='crossSection':
            xsec = float(value)*1e6 #xsec is in nb, hence the 1e6 factor to get it in fb
        elif name=='datasetNumber':
            dsid = value
        elif name=='genFiltEff':
            eff = float(value)

    #if geFiltEff is not available, use aprox_GenFiltEff
    if eff is None:
        for name, value in results[0].iteritems():
            if name=='approx_GenFiltEff':
                eff = float(value)
            
    print '%s %e %e %s'%(dsid, xsec, eff, nevents)

    if debug:
        for name, value in results[0].iteritems():
            print '  %s %s'%((name+':').ljust(24),value)
        print ''

    return dsid, xsec, eff, nevents

#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dataset', '-ds', dest='dataset', default='', help='dataset')
    group.add_argument('--list', '-l', dest='datasetListName', default='', help='list of datasets')
    parser.add_argument('--debug', '-d', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    #------------------------------------------
    #loop over dataset list
    if args.datasetListName != '':

        #open dataset file name
        if not os.path.isfile(args.datasetListName):
            raise SystemExit('\n***ERROR*** couldn\'t find dataset file: %s'%args.datasetListName)
        datasetListFile = open(args.datasetListName,'r')

        print '\nDSID xsec.[fb] eff. events'

        #loop over datasets
        for line in iter(datasetListFile):
            if line == '':
                continue
            if '#' in line:
                continue
            line.lstrip()
            line.rstrip()
            getDatasetInfo(line[:-1], args.debug)
            
    #------------------------------------------
    #print dataset info
    if args.dataset != '':
        print '\nDSID xsec.[fb] eff. events'
        getDatasetInfo(args.dataset, args.debug)
