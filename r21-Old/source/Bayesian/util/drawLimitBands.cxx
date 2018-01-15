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
#include "TGraphErrors.h"
#include <fstream>
/*
string& replaceString(string& original, string substring1, string substring2)
{ // 1. 
        boost::replace_all(test, "abc", "hij");
          boost::replace_all(test, "def", "klm");
}
*/

using namespace std;

bool does_file_exist(const char *fileName)
{
    ifstream infile(fileName);
    return infile.good();

}
vector<double> GetCenterAndSigmaDeviations(vector<double> input) 
{
  std::sort(input.begin(),input.end());
//for ( int i =0; i< input.size(); ++i){
//    cout<<"pseudo tests:" <<input.at(i)/35.1<<endl;
//  }
  unsigned int nVals = input.size();
  vector<double> statVals;
  double wantEvents;
  int bestEvent;
  double quantiles [5] = {0.02275,0.1587,0.5,0.8413,0.9772};
  for (int i=0; i<5; i++) {
    wantEvents = nVals*quantiles[i];
    bestEvent = (int) wantEvents;
    statVals.push_back(input.at(bestEvent));
    cout<<"quantile: "<<quantiles[i]<<" pseudoTestValue: "<<input.at(bestEvent)/35.1<<endl;
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
    cout<<"Configuration"<<endl;
    //---------------------Configurations---------------------------//
    //------r21-Old config---///
    string inputDir = "/lustre/SCRATCH/atlas/ywng/WorkSpace/r21/r21-Old/source/Bayesian/results/Step2_setLimitsOneMassPoint/test";
    string fileNameTemplate =inputDir+"/"+"Step2_setLimitsOneMassPoint_JDMPhPPP_ZprimeCCCMMM_35p45fb_0.root";
    string outputFileNamePrefix="testLimitPlot";
    string outputFileName;
    //----end of r21-Old config---//
    //-------r21SwiftBunny----///
    //string inputDir = "/lustre/SCRATCH/atlas/ywng/r21/r21SwiftNew/r21StatisticalAnalysis/source/results/Step2_setLimitsOneMassPoint/svnCodebkgndFit";
    //string fileNameTemplate = inputDir+"/"+"Step2_setLimitsOneMassPoint_JDMPhPPP_ZprimeCCCMMM_35p45fb_0_seedMMM.root";
    ////string fileNameTemplate =inputDir+"/"+"Step2_setLimitsOneMassPoint_JDMPhPPP_ZprimeCCCMMM_35p45fb_0.root";
    //string outputFileName="testLimitr21SwiftPlot.root";

    double luminosity=35100;
    //gSMp02_ph100
    vector<string> ptCutList={"50","100"};
    vector<string> couplingList={"0p1","0p2", "0p3", "0p4"};
    
    //string ptCut = "100";
    //string coupling="0p3";
   // int masses[]={250, 350, 450, 550,750};
    

    vector<int> masses{300, 350,400, 450,500, 550,750, 950,1500};
//for each pt cut for each coupling for each mass, if file exist then do blah

    cout<<"end of configuration"<<endl;
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
//for (vector<char>::iterator ptCut = ptCutList.begin(); ptCut != ptCutList.end(); ++ptCut){
//for (vector<char>::iterator coupling = couplingList.begin(); coupling = couplingList.end(); ++coupling){
for (auto ptCut: ptCutList){
for (auto coupling: couplingList){

    string fileNameTemplateForRun=initializeFileNameTemplate(fileNameTemplate, ptCut,coupling);
    outputFileName= outputFileNamePrefix+ string("_") +string(ptCut)+string("_")+string(coupling)+string(".root");
    cout<<"coupling: "<<coupling<<" ptCut: "<<ptCut<<endl;
    int iMassExist =0; //iMassCounter that exists

    cout<<"creating makeing histogram"<<endl; //declaring the histograms here 
    TGraphErrors * observed = new TGraphErrors();
    TGraphAsymmErrors * expectedWithOneSigma = new TGraphAsymmErrors();
    TGraphAsymmErrors * expectedWithTwoSigma = new TGraphAsymmErrors();
for (int iMassPoint=0; iMassPoint<masses.size(); iMassPoint++){//This mass point loop through the mass points that are in the list (does not always exists)
    int iMass = masses.at(iMassPoint);
    cout<<"MAss: "<<iMass<<endl;
    string iMassFileName=constructMassFileName(fileNameTemplateForRun,to_string(iMass));
    if (does_file_exist(iMassFileName.c_str())) {
        vector<double> CLPseudo;
        double CLObserved = -1;


    //cout<<"opening file "<<iMassFileName<<endl;
// construct TFile f
    TFile f(iMassFileName.c_str(), "READ");
//Get the observed Limit
///
    //cout<<"getting CLOfRealLikelihood"<<endl;
    TVectorD * CLFromFile = (TVectorD*) f.Get("CLOfRealLikelihood");
    CLObserved = (*CLFromFile)[0]/luminosity;
//#cout<<"CLObserved: "<<CLObserved<<endl;
    
    //Set points for the theory line
    observed->SetPoint(iMassExist, iMass, CLObserved);

    cout<<"pt #: "<<iMassExist <<" mass: "<<iMass<<" CLObserved: "<<CLObserved<<endl;
    observed->SetPointError(iMassExist, 0, 0);

    // Read tree from file
    //cout<<"getting ensemble test"<<endl;
    TTree * tree = (TTree*) f.Get("ensemble_test");
    double CL;

    //cout<<"getting 95quantile_marginalized_2"<<endl;
    tree->SetBranchAddress("95quantile_marginalized_1", &CL);
    for (int i = 0; i<tree->GetEntries(); i++) {
      tree->GetEvent(i);
      CLPseudo.push_back(CL);
      //std::cout << "individual pseudo CL = " << CL << "/" << luminosity << " = " << CL/luminosity << std::endl;
    }
    f.Close();

      vector<double> bandLimits = GetCenterAndSigmaDeviations(CLPseudo);

      for(std::vector<double>::size_type p=0; p!=bandLimits.size(); ++p) bandLimits[p] /= luminosity;

      for(std::vector<double>::size_type p=0; p!=bandLimits.size(); ++p)  cout<<"bandLimits: "<<bandLimits[p]<<endl;

      // Set points in expected graphs
      expectedWithOneSigma->SetPoint(iMassExist, iMass, bandLimits.at(2));
      expectedWithOneSigma->SetPointError(iMassExist, 0, 0, (bandLimits.at(2)-bandLimits.at(1)),
                               (bandLimits.at(3)-bandLimits.at(2)));
      expectedWithTwoSigma->SetPoint(iMassExist, iMass, bandLimits.at(2));
      expectedWithTwoSigma->SetPointError(iMassExist, 0, 0, (bandLimits.at(2)-bandLimits.at(0)),
                               (bandLimits.at(4)-bandLimits.at(2)));

      std::cout << "Center of expected, observed: " << bandLimits.at(2) << " " << CLObserved << std::endl;
      iMassExist++;  
    }// if does file exist
} //loop for imass
  std::cout << "Writing output file " << outputFileName  << std::endl;

  TFile outfile(outputFileName.c_str(),"RECREATE");
  outfile.cd();

  observed->SetName("observedXSecAccVersusMass");
  observed->Print();
  observed->Write();
  expectedWithOneSigma->SetName("expectedXSecAccVersusMass_oneSigma");
  expectedWithOneSigma->Print();
  expectedWithOneSigma->Write();
  expectedWithTwoSigma->SetName("expectedXSecAccVersusMass_twoSigma");
  expectedWithTwoSigma->Print();
  expectedWithTwoSigma->Write();

  outfile.Close();
  delete observed;
  delete expectedWithOneSigma;
  delete expectedWithTwoSigma;
} //loop for ptCu
}// loop for coupling 

  return 0;
}//end of main
