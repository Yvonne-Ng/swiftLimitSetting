#!/usr/bin/env python

#******************************************
#import stuff
import ROOT, re, sys, os, math

#******************************************
def getMergedTreeFileList(path, tags):
    #NOTE given a path and tags (to identify the right dataset),
    #return the list of all the merged 'tree' files
    #NOTE 'path' should be the path to the gridOutput directory

    #tags.append(".root")
    
    path+='/'
    fileList = []
    for f in os.listdir(path):
        if not os.path.isfile( os.path.join(path,f) ): continue

        passed = True
        for tag in tags:
            if '=' in tag:
                if not any(splitTag in f for splitTag in list(tag.split('='))):
                    passed = False
            else:
                if not tag in f:
                    passed = False

        if passed and '.root' in f:
            fileList.append( os.path.join(path,f) )

    fileList.sort()
    return fileList

#******************************************
def getInputFilesFromList(list, tags):

    fileList = []

    with open(list) as inputList:
        for f in inputList:
            if all(tag in f for tag in tags) and '.root' in f:
                fileList.append(f.strip())

    fileList.sort()
    return fileList

#******************************************
#******************************************
