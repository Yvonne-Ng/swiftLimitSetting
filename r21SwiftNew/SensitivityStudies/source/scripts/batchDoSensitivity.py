#!/cvmfs/atlas.cern.ch/repo/sw/software/21.2/AnalysisBaseExternals/21.2.3/InstallArea/x86_64-slc6-gcc62-opt/bin/python
import sys, os, math, argparse, ROOT

import sensitivityTools
import numpy as np
import os.path
from fileNamingTool import *
import json

def batchRun(config):
    localdir = os.path.dirname(os.path.realpath(__file__))
    json_data = open(config["json"])
    print("config[json]: ", config["json"])
    configJson=json.load(json_data)
    try:
        json_data = open(localdir+"/"+config["json"])
        configJson=json.load(json_data)
    except:
        print("can't open json file. Abort.")
        raise RuntimeError
#----end of opening json config file
    for model in config["modelRange"]:
        for window in  config["windows"]:
            conciseLogDir=localdir+"/log/"+configJson["SeriesName"]
            conciseLogDirModel=conciseLogDir+"/"+model
            conciseLogDirWindow=conciseLogDirModel+"/"+str(window)
            if not os.path.isdir(conciseLogDir):
                os.mkdir(conciseLogDir)
            if not os.path.isdir(conciseLogDirModel):
                os.mkdir(conciseLogDirModel)
            if not os.path.isdir(conciseLogDirWindow):
                os.mkdir(conciseLogDirWindow)
            # creating concise log file
            conciseLogName=makeConciseLogName(localdir, configJson["SeriesName"], model, window)
            conciseLog=open(conciseLogName , 'w+')
            conciseLog.write("model %s\n"%(model))
            conciseLog.write("window %s\n"%(window))
            conciseLog.close()

            configJson["conciseLog"]=conciseLogName

            json_data2 = open(localdir+"/"+config["json"], "w")
            print "configJson: ", configJson
            json.dump(configJson, json_data2)

            for signalMass in config["signalMasses"]:
                folder="%s_Mass%s_ww%s"%(model, signalMass, window)
                commandMKDIR1="mkdir %s/%s"%("outputSlurm",configJson["SeriesName"])
                commandMKDIR2="mkdir %s/%s/%s"%("outputSlurm",configJson["SeriesName"], folder)
                command="sbatch -c 2 -p atlas_all -t 100 -o %s/%s/%s/%s/output.log ./batchDoSensitivity.sh %s %s %s %s"%(localdir,"outputSlurm",configJson["SeriesName"], folder,model, window, signalMass, config["json"])
                #command="sbatch -c 2 -p atlas_slow -t 100 ./batchDoSensitivity.sh %s %s %s"%(model, window, signalMass)
                print(command)
                os.system(commandMKDIR1)
                os.system(commandMKDIR2)
                os.system(command)

if __name__=="__main__":
    #config={"modelRange":["Gauss_width15", "Gauss_width10, "Gauss_width],
    #        "signalMasses": [450, 550, 650, 750, 850, 1050, 1150],
    #        "window":[12, 11, 10, 9, 8]
    #        }
    #config={"modelRange":["Gauss_width15", "Gauss_width10"],
    #        "signalMasses": [450, 550],
    #        "windows":[12, 11]
    #        }

    #config={"modelRange":["Gauss_width7", "Gauss_width10", "Gauss_width15"],
    #        "signalMasses": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
    #        "windows":[12, 11, 10, 9, 8]
    #        }

    configList=[
            #{"modelRange":["Gauss_width15"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_compound_inclusive.json",
            #}
           # {"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
           # "signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
           # "windows":[16, 15, 14, 13, 12, 11, 10],
           # #"seriesname": "trijetinclusiveapril-2"
           # "json":"configDoSen/may2018/photon_compound_inclusive.json",
           # },

           # {"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
           # "signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
           # "windows":[16, 15, 14, 13, 12, 11, 10],
           # #"seriesname": "trijetinclusiveapril-2"
           # "json":"configDoSen/may2018/photon_compound_n2tbagged.json"

           # },

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10, 9],
            ###"seriesname": "trijetinclusiveapril-2"

            #"json":"configDoSen/may2018/photon_single_inclusiveCatDogCheck.json"
            ##"json":"configDoSen/may2018/photon_single_inclusive.json"
            #}
#yvonne
            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10, 9, 8],
            ##"seriesname": "trijetinclusiveapril-2"

            #"json":"configDoSen/may2018/photon_single_n2tbagged.json"
            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10, 9, 8],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/trijetInclusive.json"

            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10, 9, 8],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/trijetn2tbagged.json"
            #}
#catdog check

            #{"modelRange":["Gauss_width7", "Gauss_width15"],
            #"signalMasses": [1000],
            #"windows":[23],

            #"json":"configDoSen/may2018/photon_single_inclusiveCatDogCheck.json"
            #}

            #{"modelRange":["Gauss_width7","Gauss_width10", "Gauss_width15"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[23, 21, 19, 17, 15, 13,  10, 8],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/photon_single_inclusiveCatDogCheck.json"
            #}

            #{"modelRange":["Gauss_width7","Gauss_width10", "Gauss_width15"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[23, 21, 19, 17, 15, 13,  10, 8],

            {"modelRange":["Gauss_width10"],
            #"signalMasses": [400],
            #"windows":[22, 21, 20, 19],
            "windows":[23, 21, 19, 17, 15, 13,  10, 8],
            "signalMasses": [450, 550, 650, 750,850, 950,1000, 1100],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/photon_single_inclusive.json"
            },

            {"modelRange":["Gauss_width10"],
            #"signalMasses": [400],#
            "signalMasses": [450, 550, 650, 750,850, 950,1000, 1100],
            #"windows":[23],
            "windows":[23, 21, 19, 17, 15, 13,  10, 8],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/photon_compound_inclusive.json"
            },

            {"modelRange":["Gauss_width10"],
            #"signalMasses": [400],
            "signalMasses": [450, 550, 650, 750,850, 950,1000, 1100],
            #"windows":[15],
            "windows":[23, 21, 19, 17, 15, 13,  10, 8],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/trijetInclusive.json"
            }

# config generation:
            #{"modelRange":["Gauss_width10"],
            #"signalMasses": [250, 300, 350, 450, 550, 650, 750,850, 950,1000, 1100],
            #"windows":[23,22,  21, 20, 19,18, 17,16, 15, 14, 13,12, 11,   10,9,  8],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/photon_single_inclusive.json"
            #}
            #{"modelRange":["Gauss_width10"],
            #"signalMasses": [350,400, 450, 550, 650, 750,850, 950,1000, 1100],
            ##"windows":[23, 21, 19, 17, 15, 13,  10, 8],
            #"windows":[23,22,  21, 20, 19,18, 17,16, 15, 14, 13,12, 11,   10,9,  8],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/trijetInclusive.json"
            #},

            #{"modelRange":["Gauss_width10"],
            #"signalMasses": [350, 400, 450, 550, 650, 750,850, 950,1000, 1100],
            #"windows":[23,22,  21, 20, 19,18, 17,16, 15, 14, 13,12, 11,   10,9,  8],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/photon_compound_inclusive.json"
            #}

            #{"modelRange":["Gauss_width15"],
            #"signalMasses": [450],
            #"windows":[16],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/trijetn2tbagged.json"
            #}
# cat dof
         #   {"modelrange":["gauss_width15"],
         #   "signalmasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
         #   "windows":[10],
         #   #"seriesname": "trijetinclusiveapril-2"
         #   "json":"configdosen/width15configbackground2.json"
         #   },

         #   {"modelrange":["gauss_width15"],
         #   "signalmasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
         #   "windows":[10],
         #   #"seriesname": "trijetinclusiveapril-2"
         #   "json":"configdosen/width15configbackground2.json"
         #   },

         #   {"modelrange":["gauss_width15"],
         #   "signalmasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
         #   "windows":[10],
         #   #"seriesname": "trijetinclusiveapril-2"
         #   "json":"configdosen/width15configbackground2.json"
         #   },

         #   {"modelrange":["gauss_width15"],
         #   "signalmasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
         #   "windows":[10],
         #   #"seriesname": "trijetinclusiveapril-2"
         #   "json":"configdosen/width15configbackground2.json"
         #   },
         ]

    for config in configList:
        batchRun(config)

