#!/usr/bin/env python
import os
import ROOT,sys
import subprocess # So can use shell scripting in python
from ROOT import *
import glob
import re

# Lydia Beresford

#------------------------------------------
#check input parameters
if len(sys.argv) != 2:
  raise SystemExit(
          '\n***ERROR*** wrong input parameters (%s/%s) \
          \nHOW TO: python RenameHistos.py inname1 inname2 legend1 legend2 outname\n\
	  \'inname1\' first input file name and path\n\
EXAMPLE: python RenameHistos.py /home/Test.root'\
            %(len(sys.argv),7))

#------------------------------------------
# Setup, including getting some inputs from command line
# define input path, extension

# File 1
InputDir=sys.argv[1].strip()
print "First input dir %s"%InputDir
  
#******************************************
if __name__ == '__main__':

  print InputDir
  myglob =  glob.glob(InputDir+"/*.root")
  
  for f in myglob:
    Dir = f.split("hist-user")[0]
    mR = re.search('mRp\d{1,2}',f).group()
    mR = mR.split('mR')[1].replace('p','.')
    mR = str(int(float(mR)*1000))
    gSM = re.search('gSp\d{1,2}',f).group()
    gSM = str(gSM.split('gS')[1].replace('p','0p')+'0')
    newName =Dir+"ZPrimemR"+mR+"gSM"+gSM+".root"
    print "Moving "+f+" to "+newName
    #raise SystemExit('\n***TEST***')
    subprocess.call("mv %s %s"%(f,newName), shell=True) 
  print '\ndone'
