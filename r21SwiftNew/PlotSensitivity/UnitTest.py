import ROOT, glob, math, argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gROOT.LoadMacro("RootStyle/atlasstyle-00-03-05/AtlasStyle.C");

ROOT.SetAtlasStyle();

ROOT.gROOT.LoadMacro("RootStyle/atlasstyle-00-03-05/AtlasUtils.C");

from fileNamingTool import *
import os
#--------unit test for
def test_findLabel(tag):
    directory="/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/SensitivityStudies/source/scripts/../results2/searchphase/"
    gaussianMean=500
    windowWidth=12
    try:
        bkgOnlyFileName=findLabelledFileName(directory, tag, gaussianMean,windowWidth)
        print "labelled File!: ",bkgOnlyFileName
    except ValueError:
        print("oops, there is no such file!")




def test_findDirFromFilePath():
    findDirFromFilePath("/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/SensitivityStudies/source/scripts/../results2/searchphase/searchphase.Gauss_width3.500.gev.0p5.ifb.mjj.4.par.0.seed.default_ww12.root")

if __name__=="__main__":
    #---working! first try! woohoo!
    #test_findDirFromFilePath()

    #test_findLabel("JUSTABOVE")
    #test_findLabel("JUSTBELOW")
    test_findLabel("NOSIGNAL")



