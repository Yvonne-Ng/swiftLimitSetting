import os
import SigRemovalRatios_CD

if __name__=="__main__":

    configList=[
            #{"modelRange":["Gauss_width15"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_compound_inclusive.json",
            #}
            #{"modelRange":["Gauss_width15", "Gauss_width10"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_compound_n2tbagged.json",
            #"outputpdfDir": "perMassPdf/"
            #}
#last fit
            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"

            #"json":"configDoSen/may2018/photon_single_inclusive.json",
            #"outputpdfDir": "perMassPdf/"
            #}

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_compound_inclusive.json",
            #"outputpdfDir": "perMassPdf/"
            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_compound_n2tbagged.json",
            #"outputpdfDir": "perMassPdf/"
            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/photon_single_inclusive.json",
            #"outputpdfDir": "perMassPdf/"
            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"

            #"json":"configDoSen/may2018/photon_single_n2tbagged.json",
            #"outputpdfDir": "perMassPdf/"
            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/trijetInclusive.json",
            #"outputpdfDir": "perMassPdf/"

            #},

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            ##"seriesname": "trijetinclusiveapril-2"
            #"json":"configDoSen/may2018/trijetn2tbagged.json",
            #"outputpdfDir": "perMassPdf/"
            #}

            #{"modelRange":["Gauss_width15"],
            #"signalMasses": [1000],
            #"windows":[16, 15],
            #"json":"configDoSen/may2018/photon_single_inclusiveCatDogCheck.json",
            #"outputpdfDir": "perMassPdf/"
            #}

            #{"modelRange":["Gauss_width15", "Gauss_width10", "Gauss_width7"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[16, 15, 14, 13, 12, 11, 10],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/photon_single_inclusive.json"
            #}

            #{"modelRange":["Gauss_width7","Gauss_width10", "Gauss_width15"],
            #"signalMasses": [450, 550, 650, 750,850, 950,1000, 1100, 1200],
            #"windows":[23, 21, 19, 17, 15, 13,  10, 8],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/photon_single_inclusiveCatDogCheck.json"
            #}
#cat dog fri test
            #{"modelRange":["Gauss_width1"],
            #"signalMasses": [450],
            #"windows":[23],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/photon_single_inclusive.json"
            #},

            #{"modelRange":["Gauss_width7"],
            #"signalMasses": [450],
            #"windows":[23],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/photon_compound_inclusive.json"
            #},

            #{"modelRange":["Gauss_width7"],
            #"signalMasses": [450],
            #"windows":[23],
            #"outputpdfDir": "perMassPdf/",
            #"json":"configDoSen/may2018/fiveParams/trijetInclusive.json"
            #}

            {"modelRange":["Gauss_width10"],
            "signalMasses": [450],
            "windows":[23],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/photon_single_inclusive.json"
            },

            {"modelRange":["Gauss_width10"],
            "signalMasses": [450],
            "windows":[23],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/photon_compound_inclusive.json"
            },

            {"modelRange":["Gauss_width10"],
            "signalMasses": [450],
            "windows":[15],
            "outputpdfDir": "perMassPdf/",
            "json":"configDoSen/may2018/fiveParams/trijetInclusive.json"
            }

            ]

    for config in configList:
        #os.system("python ../../../PlotSensitivity/SigRemovalRatios_CD.py --config %s "%config)
        SigRemovalRatios_CD.plotSignalInjectionMassPoint(config)

