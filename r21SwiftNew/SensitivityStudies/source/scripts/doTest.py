from fileNamingTool import *
from doSensitivityScan_withLumiSteps import removeOldLabelledFile, countFilesInDirWithKeyword

import os


def test_nosignalNameoutput():
    spFileName="/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/SensitivityStudies/source/results2/searchphase/searchphase.Gauss_width3.500.gev.0p1.ifb.mjj.4.par.0.seed.default_ww12.root"
    zeroLumiFN=zeroLumiFileName(spFileName)
    print "does zero lumi exist? ", os.path.isfile(zeroLumiFN)

    nosignalFN=noSignalFileName(zeroLumiFN)
    print("no signal file name: ", nosignalFN)

def test_removeOldLabelledFile():
   fileDir="/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/SensitivityStudies/source/scripts/../results2/searchphase/"
   label= "JUSTABOVE"
   print("# of justabove files afte remove: ", countFilesInDirWithKeyword(fileDir, label))
   mass=500
   window=12
   removeOldLabelledFile(fileDir, label, mass, window)
   print("# of justabove files afte remove: ", countFilesInDirWithKeyword(fileDir, label))

def Test_countFiles():
    count=countFilesInDirWithKeyword("/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21SwiftNew/SensitivityStudies/source/scripts/../results2/searchphase/", "JUSTABOVE")
    print count

if __name__=="__main__":
    test_removeOldLabelledFile()
    #Test_countFiles()
