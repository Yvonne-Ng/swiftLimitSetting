#!/usr/bin/env python

#******************************************
import os, argparse

#******************************************
def plotAll(args):

    print '\n******************************************'
    print 'plot sensitivity and luminosity scan results for all given config files'

    #******************************************
    #loop over list of config files
    for configFileName in args.configFileNames:
        print '\n%s'%configFileName
    
        #******************************************
        #options
        options = '--config %s --path %s --tag %s'%(configFileName, args.path, args.tag)
    
        #******************************************
        #plot luminosity scans
        lumiCommand = 'python plotLumiScanResults.py %s'%options
        print '\n%s'%lumiCommand
        os.system(lumiCommand)
        
        #******************************************
        #plot sensitivity scans
        sensitivityCommand = 'python plotSensitivityScan.py %s'%options
        print '\n%s'%sensitivityCommand
        os.system(sensitivityCommand)

#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('--configs', dest='configFileNames', nargs='+', type=str, default=[''], help='list of config files')
    parser.add_argument('--path', dest='path', default='', required=True, help='path to search phase results directory')
    parser.add_argument('--tag', dest='tag', default='default', required=True, help='tag for output files')
    parser.add_argument('--wait', dest='wait', action='store_true', default=False, help='wait?')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    #------------------------------------------
    #plot sensitivity scan results
    plotAll(args)
    print '\n******************************************'
    print 'plotted sensitivity and luminosity scan results'
