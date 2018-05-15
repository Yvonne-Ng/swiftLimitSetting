#!/cvmfs/atlas.cern.ch/repo/sw/software/21.2/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/bin/python
import sys, os, math, argparse, ROOT

import sensitivityTools
import numpy as np
import os.path
from fileNamingTool import *
import json

if __name__=="__main__":
    #config={"modelRange":["Gauss_width15", "Gauss_width10, "Gauss_width],
    #        "signalMasses": [450, 550, 650, 750, 850, 1050, 1150],
    #        "window":[12, 11, 10, 9, 8]
    #        }
    #config={"modelRange":["Gauss_width15", "Gauss_width10"],
    #        "signalMasses": [450, 550],
    #        "windows":[12, 11]
    #        }

    config={"modelRange":["Gauss_width7"],
            "signalMasses": [400],
            "windows":[12]
            }

    for model in config["modelRange"]:
        for signalMass in config["signalMasses"]:
            for window in  config["windows"]:
                    #command="sbatch  -c 8 -p atlas_all -t 100 doSensitivityScan2_rewrite.py --config configDoSen/width15Configbackground2.json --model %s --window %s --signalMass %s"%(model, window, mass)
                    #os.system("export PYTHONPATH=/lustre/SCRATCH/atlas/ywng/WorkSpace/signalInjection2/20171122_SensitivityScan/toolbox/:$PYTHONPATH")
                command="sbatch -c 8 -p atlas_slow -t 100 ./batchDoSensitivity.sh %s %s %s"%(model, window, signalMass)
                os.system(command)
