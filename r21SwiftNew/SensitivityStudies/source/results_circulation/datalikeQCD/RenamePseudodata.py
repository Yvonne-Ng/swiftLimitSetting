#!/bin/python
from ROOT import *

fin = TFile.Open("Pseudodata_from_DSJ100yStar06_TriggerJets_J100_yStar06_mjj_2016binning_TLArange_data_4param_G_upTo4000.29p7.ifb.root", "UPDATE")

h=fin.Get("Pseudodata")
h.Clone()
h.Write("mjj_Gauss_DL")
