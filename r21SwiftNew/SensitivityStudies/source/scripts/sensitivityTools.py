#!/bin/python

#******************************************
#NOTE some of these functions are taken from CommonFunctions.py

#******************************************
#import
import re, sys, os, math, ROOT

#******************************************
#function taken from CommonFunctions.py
#previously named getSample(name)
def getSignalMass(name):
    #print name
    if "ExcitedQ" in name:
        regEx = re.compile("ExcitedQ(.*)Lambda")
    elif "QStar" in name:
        regEx = re.compile("QStar\.(.*)\.GeV")
    elif "BStar" in name:
        regEx = re.compile("BStar\.(.*)\.GeV")
    elif "BlackMax" in name:
        regEx = re.compile("MthMD(.*)\.e2303")
    elif "gq_0p1" in name:
        regEx = re.compile("gq_0p1\.(.*)\.GeV")
#    elif "Gauss" in name:
#        print "Gauss in name"
#        regEx = re.compile("mass(.*)_width")
    elif "width3" in name:
        #print "Gauss_width3 in name"
        regEx = re.compile("mass(.*)_width3")
    elif "width5" in name:
        #print "Gauss_width5 in name"
        regEx = re.compile("mass(.*)_width5")
    elif "width7" in name:
        #print "Gauss_width7 in name"
        regEx = re.compile("mass(.*)_width7")   
    elif "width10" in name:
        #print "Gauss_width10 in name"
        regEx = re.compile("mass(.*)_width10")     
    elif "width15" in name:
        #print "Gauss_width15 in name"
        regEx = re.compile("mass(.*)_width15")    
    elif "width20" in name:
        #print "Gauss_width20 in name"
        regEx = re.compile("mass(.*)_width20") 
    elif "Zprimebb" in name:
        #regEx = re.compile("Zprimebb(.*)\.All")
        regEx = re.compile("Zprimebb\.(.*)\.GeV")
    else:
        regEx = re.compile("_14TeV(.*)_AU2")

    match = regEx.search(name)
    sample = match.group(1)
    return sample

#******************************************
#get Z'->bb cross section times efficiency
def getZprimebbCrossSection(mass):
    localdir = os.path.dirname(os.path.realpath(__file__))
    crossSectionsFileName = localdir+'/../data/Zprimebb.cross.sections.list'
    crossSections = ROOT.TEnv()
    if crossSections.ReadFile(crossSectionsFileName,ROOT.EEnvLevel(0)) != 0:
        raise IOError('could not find Z\'->bb cross sections file: %s'%crossSectionsFileName)
    return float(crossSections.GetValue( str( int(mass)), 0.))
