#include <iostream>
#include "TH1.h"
#include "TError.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TVectorD.h"
#include "TGraphAsymmErrors.h"
#include <string>
#include <vector>
#include <algorithm>
#include <boost/algorithm/string/replace.hpp>
/*
string& replaceString(string& original, string substring1, string substring2)
{ // 1. 
        boost::replace_all(test, "abc", "hij");
          boost::replace_all(test, "def", "klm");
}
*/

using namespace std;

vector<double> GetCenterAndSigmaDeviations(vector<double> input) 
{
  std::sort(input.begin(),input.end());
  unsigned int nVals = input.size();
  vector<double> statVals;
  double wantEvents;
  int bestEvent;
  double quantiles [5] = {0.02275,0.1587,0.5,0.8413,0.9772};
  for (int i=0; i<5; i++) {
    wantEvents = nVals*quantiles[i];
    bestEvent = (int) wantEvents;
    statVals.push_back(input.at(bestEvent));
  }
  return statVals;
}
//Consturct the file name Template of the run
string initializeFileNameTemplate(string fileNametemplate, string ptCut, string coupling){
    //fileNametemplate.replace("PPP", ptCut);
    boost::replace_all(fileNametemplate, "PPP", ptCut);
    boost::replace_all(fileNametemplate, "CCC", coupling);
    cout<<"filenameTemplate for the run: "<<fileNametemplate<<endl;
    return fileNametemplate;
}

//Construct the file name for the mass
string constructMassFileName(string fileName, string mass){
    boost::replace_all(fileName, "MMM", mass);
    cout<<"filenamefromfucntion: "<<fileName<<endl;
    return fileName;
}

int main(){
    //---------------------Configurations---------------------------//
    string inputDir = "/lustre/SCRATCH/atlas/ywng/r21/r21-Old/oldStep2Results";
//string fileNameTemplate ="Step2_setLimitsOneMassPoint_test2PhPPP_ZprimeCCCMMMM_15p45fb_0.root";
    string fileNameTemplate =inputDir+"/"+"Step2_setLimitsOneMassPoint_JDMPhPPP_ZprimeCCCMMM_15p45fb_0.root";
    //TString fileNameTemplate ="Step2_setLimitsOneMassPoint_test2Ph100_Zprime0p31500_15p45fb_0.root";

    //gSMp02_ph100
    string ptCut = "100";
    string coupling="0p2";
   // int masses[]={250, 350, 450, 550,750};

    vector<int> masses{250, 350, 450, 550,750};
    string fileNameTemplateForRun=initializeFileNameTemplate(fileNameTemplate, ptCut,coupling);



    //---------------------End of Configurations-------------------//
    //
    //------------------------Psuedo-Code------------------------//
    //Declare the observed histogram
    //Declare the Limit histogram

    //Lopp through all the mass points 
    //  find the CLofRealLikelihood
    //  Set the mass points and the CL of the observed graph
    //  loop through psuedo test to make a CLpseudoTest Vector
    //  find the band width 
    //  Calculate the bands
    //  Set the point of the 1 sigma and 2 sigma graph

    //---------------end of Psuedo-Code-----------------------//


//maybe put this into a function 
//
for (int iMassPoint=0; iMassPoint<masses.size(); iMassPoint++){
    int iMass = masses.at(iMassPoint);
    cout<<"MAss: "<<iMass<<endl;
    string iMassFileName=constructMassFileName(fileNameTemplateForRun,to_string(iMass));

// construct TFile f
    TFile f(iMassFileName.c_str(), "READ");
//Get the observed Limit
    //(TVectorD *)


}
    return 0;
}//end of main
