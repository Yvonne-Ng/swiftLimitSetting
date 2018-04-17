#include "TROOT.h"
#include "TObject.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TStopwatch.h"
#include "TMath.h"
#include "TKey.h"
#include "TEnv.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>

#include "TreeClass.h"

using std::cout;
using std::cerr;
using std::endl;
using std::vector;
using std::string;
using std::ofstream;

//******************************************
/*
double getCrossSectionTimesFilterEff(string DSID) {
  //NOTE //FIX move this to a TEnv reading from a text file
  std::map<string,double> DSIDMap;

  //Z'->bb
  DSIDMap["301920"]=13.198      * 1.;
  DSIDMap["301921"]= 4.3098     * 1.;
  DSIDMap["301922"]= 1.7476     * 1.;
  DSIDMap["301923"]= 0.6638     * 1.;
  DSIDMap["301924"]= 0.29113    * 1.;
  DSIDMap["301925"]= 0.13823    * 1.;
  DSIDMap["301926"]= 0.070766   * 1.;
  DSIDMap["301927"]= 0.020788   * 1.;
  DSIDMap["301928"]= 0.007046   * 1.;
  DSIDMap["301929"]= 0.0010493  * 1.;
  DSIDMap["301930"]= 0.00022791 * 1.;

  //b*
  DSIDMap["301931"]= 513.4000     * 1.;
  DSIDMap["301932"]= 124.1300     * 1.;
  DSIDMap["301933"]= 38.90500     * 1.;
  DSIDMap["301934"]= 11.22300     * 1.;
  DSIDMap["301935"]= 3.879800     * 1.;
  DSIDMap["301936"]= 1.469000     * 1.;
  DSIDMap["301937"]= 0.6084800    * 1.;
  DSIDMap["301938"]= 0.1226300    * 1.;
  DSIDMap["301939"]= 0.02838800   * 1.;
  DSIDMap["301940"]= 0.001931800  * 1.;
  DSIDMap["301941"]= 0.0001460300 * 1.;
  
  std::map<string,double>::iterator it;
  it = DSIDMap.find(DSID);
  if (it != DSIDMap.end())
    return DSIDMap.find(DSID)->second*1e3;//NOTE multiply by 1e3 to go from pb to nb
  else
    return 1.;
}
*/

//******************************************
//get NLO weight
//NOTE opening ROOT files is slow: open NLO k-factors file once within the main function
/*
double getNLOKFactor(float mjj, string process) {
  string fileName = "data/NLO.kfactors.root";
  TFile *file=TFile::Open(fileName.c_str(),"READ");
  if(!file) {cerr<<process<<"couldn't open input NLO factors file: "<<fileName<<endl; return 1;}
  string histName = "NLOkfactors";
  TH1D* hist = (TH1D*) file->Get(histName.c_str());
  if(!hist) {cerr<<process<<"couldn't open input NLO factors histogram: "<<histName<<endl; return 1;}
  double kfactor = hist->GetBinContent( hist->FindBin( mjj));
  file->Close();
  delete file;
  return kfactor;
}
*/

//******************************************
//get EW weight
//NOTE opening ROOT files is slow: open EW k-factors file once within the main function
/*
double getEWKFactor(float mjj, string process) {
  string fileName = "data/EW.kfactors.root";
  TFile *file=TFile::Open(fileName.c_str(),"READ");
  if(!file) {cerr<<process<<"couldn't open input EW factors file: "<<fileName<<endl; return 1;}
  string histName = "EWkfactors";
  TH1D* hist = (TH1D*) file->Get(histName.c_str());
  if(!hist) {cerr<<process<<"couldn't open input EW factors histogram: "<<histName<<endl; return 1;}
  double kfactor = hist->GetBinContent( hist->FindBin( mjj));
  file->Close();
  delete file;
  return kfactor;
}
*/

//******************************************
//check if file exists
bool fileExists(string fileName) {
  std::ifstream ifile(fileName.c_str());
  //cout<<"***TEST*** does "<<fileName<<" exist? "<<ifile<<endl;
  return ifile;
}

//******************************************
int main(int argc, char *argv[]) {

  //******************************************
  TStopwatch time;
  time.Start();

  //******************************************
  //get parameters
  string process="[test] ";
  string configFileName="";
  string inputFileName="";
  string name="results";
  bool isMC=false;
  bool applyNLO=false;
  bool applyEW=false;
  double lumi=1.;
  bool bool_help=false;
  int ip=1;

  //cout<<"looping over input praameters"<<endl;
  
  while (ip<argc) {

    //cout<<"  "<<ip<<"  "<<argv[ip]<<endl;
    
    if (string(argv[ip]).substr(0,2)=="--") {

      //------------------------------------------
      //help
      if (string(argv[ip])=="--help") {
	bool_help=true; break;
      }

      //------------------------------------------
      //process
      //NOTE this is a tag to identify the process when running in parallel
      else if (string(argv[ip])=="--process") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  process=argv[ip+1];
	  process+=" ";
	  ip+=2;
	} else {cout<<"\n"<<process<<"no process ID"<<endl; bool_help=true; break;}
      }
      
      //------------------------------------------
      //config file
      else if (string(argv[ip])=="--config") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  configFileName=argv[ip+1];
	  ip+=2;
	} else {cout<<"\n"<<process<<"no config file name given"<<endl; bool_help=true; break;}
      }
      
      //------------------------------------------
      //input file name
      else if (string(argv[ip])=="--file") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  inputFileName=argv[ip+1];
	  ip+=2;
	} else {cout<<"\n"<<process<<"no input file name given"<<endl; bool_help=true; break;}
      }
      
      //------------------------------------------
      //name
      else if (string(argv[ip])=="--name") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  name=argv[ip+1];
	  ip+=2;
	} else {cout<<"\n"<<process<<"no name given"<<endl; bool_help=true; break;}
      }
      
      //------------------------------------------
      //is it MC?
      else if (string(argv[ip])=="--isMC") {
	isMC=true;
	ip+=1;
      }

      //------------------------------------------
      //is it data?
      else if (string(argv[ip])=="--isData") {
	isMC=false;
	ip+=1;
      }
      
      //------------------------------------------
      //luminosity
      else if (string(argv[ip])=="--lumi") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  lumi=atof(argv[ip+1]);
	  ip+=2;
	} else {cout<<"\n"<<process<<"no luminosity value given"<<endl; bool_help=true; break;}
      }
      
      //------------------------------------------
      //apply NLO correction
      else if (string(argv[ip])=="--applyNLO") {
	applyNLO=true;
	ip+=1;
      }

      //------------------------------------------
      //apply EW correction
      else if (string(argv[ip])=="--applyEW") {
	applyEW=true;
	ip+=1;
      }

      //------------------------------------------
      //unknown command
      else {
	cout<<"\n"<<process<<"fillHistograms: command '"<<string(argv[ip])<<"' unknown"<<endl;
	bool_help=true;
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") ip+=2;
	else ip+=1;
      }
      
    }//end if "--command"
    
    //------------------------------------------
    else { //if command does not start with "--"
      cout<<"\n"<<process<<"fillHistograms: command '"<<string(argv[ip])<<"' unknown"<<endl;
      bool_help=true;
      break;
    }//end if "--"
    
  }//end while loop
  
  //------------------------------------------
  //after reading the input parameters, call the functions
  if (bool_help || inputFileName=="") {
    cout<<"\n"<<process<<"fillHistograms"<<endl;
    cout<<process<<"HOW TO: fillHistograms --process <process name> --config <config file> --file <file name> --name <name>  --isMC/--isData --lumi <luminosity [fb^-1]>"<<endl;
    cout<<process<<"HELP:   fillHistograms --help"<<endl;
    return 1;
  }

  //******************************************
  //read settings from config file
  TEnv *settings=new TEnv();
  if (configFileName != "") {
    cout<<process<<"config file = "<<configFileName<<endl;
    int status=settings->ReadFile(configFileName.c_str(),EEnvLevel(0));
    if (status!=0) {
      cout<<process<<"couldn't read config file"<<endl;
      std::exit(1);
    }
  }
  
  double mjjCut=settings->GetValue("mjjCut",-1.);//1100.
  cout<<process<<"mjjCut = "<<mjjCut<<endl;

  double leadJetpTCut=settings->GetValue("leadJetpTCut",410.);
  cout<<process<<"leadJetpTCut [GeV] = "<<leadJetpTCut<<endl;

  double sublJetpTCut=settings->GetValue("sublJetpTCut",0.);
  cout<<process<<"sublJetpTCut [GeV] = "<<sublJetpTCut<<endl;

  double yStarCut=settings->GetValue("yStarCut",-1.);//0.6
  cout<<process<<"yStarCut = "<<yStarCut<<endl;

  double etaCut=settings->GetValue("etaCut",-1.);//2.1
  cout<<process<<"etaCut = "<<etaCut<<endl;
  
  //******************************************
  if (isMC) cout<<process<<"this is MC"<<endl;
  else cout<<process<<"this is data"<<endl;
  if (lumi) cout<<process<<"lumi = "<<lumi<<" fb^-1"<<endl;
  if (applyNLO) cout<<process<<"applying NLO k-factors"<<endl;
  if (applyEW) cout<<process<<"applying EW k-factors"<<endl;

  //******************************************
  //open input file
  cout<<process<<"input file name: "<<inputFileName<<endl;
  UInt_t openFileCounter=0;
  TFile *file=0;
  while(!file && openFileCounter<10){
    file=TFile::Open(inputFileName.c_str(),"READ");
    if(!file) sleep(2);
    openFileCounter++;
    //cout<<process<<"  reading try number "<<openFileCounter<<endl;
  }
  
  //******************************************
  //get input tree
  if(!file) {cerr<<process<<"couldn't open input file: "<<inputFileName<<endl; return 1;}
  TTree *tree;
  tree = dynamic_cast<TTree*>(file->Get("physics"));
  if(!tree) tree = dynamic_cast<TTree*>(file->Get("outTree"));
  if(!tree) {
    cerr<<"\n"<<process<<"file '"<<inputFileName<<"' doesn't contain TTree 'physics' or 'outTree'"<<endl;
    delete file;
    return 1;
  }

  //******************************************
  //instantiate TreeClass object
  TreeClass *tc = new TreeClass(tree, isMC);
  if (tc->fChain == 0) {
    cerr<<process<<"couldn't find chain"<<endl;
    return 1;
  }

  tc->setProcess(process);//set process ID
  tc->readWhatYouNeed(0);//read first entry already

  //******************************************
  //get DSID (MC) or run number (data)
  string snumber="";
  if (isMC) {
    snumber = std::to_string(tc->mcChannelNumber);
    cout<<process<<"DSID = "<<snumber<<endl;
  } else {
    snumber = std::to_string(tc->runNumber);
    cout<<process<<"run number = "<<snumber<<endl;
  }

  //******************************************
  //get number of MC events for normalization
  double totalSliceEvents=1.;
  if (isMC) {
    TIter next(file->GetListOfKeys());
    TKey *key;
    TString keyName;
    while ((key = (TKey*)next())) {
      keyName = key->GetName();
      //cout<<process<<"  "<<keyName<<endl;
      if (keyName.Contains("cutflow") && !keyName.Contains("weighted")) {
	totalSliceEvents = ((TH1D*) key->ReadObj())->GetBinContent(1);
      }
    }
    cout<<process<<"total slice events = "<<totalSliceEvents<<endl;
  }

  //******************************************
  // open NLO and EW k-factor files
  string NLOFileName = "data/NLO.kfactors.root";
  TFile *NLOFile=TFile::Open(NLOFileName.c_str(),"READ");
  if(!NLOFile) {cerr<<process<<"couldn't open input NLO factors file: "<<NLOFileName<<endl; return 1;}
  string NLOHistName = "NLOkfactors";
  TH1D* NLOHist = (TH1D*) NLOFile->Get(NLOHistName.c_str());
  if(!NLOHist) {cerr<<process<<"couldn't open input NLO factors histogram: "<<NLOHistName<<endl; return 1;}

  string EWFileName = "data/EW.kfactors.root";
  TFile *EWFile=TFile::Open(EWFileName.c_str(),"READ");
  if(!EWFile) {cerr<<process<<"couldn't open input EW factors file: "<<EWFileName<<endl; return 1;}
  string EWHistName = "EWkfactors";
  TH1D* EWHist = (TH1D*) EWFile->Get(EWHistName.c_str());
  if(!EWHist) {cerr<<process<<"couldn't open input EW factors histogram: "<<EWHistName<<endl; return 1;}

  //******************************************
  //set defaults
  TH1::SetDefaultSumw2(kTRUE);
  TH1::StatOverflows(kTRUE);
  TH2::SetDefaultSumw2(kTRUE);
  TH2::StatOverflows(kTRUE);

  //******************************************
  //binning
  double mjjBins[] = { 946, 976, 1006, 1037, 1068, 1100, 1133, 1166, 1200, 1234, 1269, 1305, 1341, 1378, 1416, 1454, 1493, 1533, 1573, 1614, 1656, 1698, 1741, 1785, 1830, 1875, 1921, 1968, 2016, 2065, 2114, 2164, 2215, 2267, 2320, 2374, 2429, 2485, 2542, 2600, 2659, 2719, 2780, 2842, 2905, 2969, 3034, 3100, 3167, 3235, 3305, 3376, 3448, 3521, 3596, 3672, 3749, 3827, 3907, 3988, 4070, 4154, 4239, 4326, 4414, 4504, 4595, 4688, 4782, 4878, 4975, 5074, 5175, 5277, 5381, 5487, 5595, 5705, 5817, 5931, 6047, 6165, 6285, 6407, 6531, 6658, 6787, 6918, 7052, 7188, 7326, 7467, 7610, 7756, 7904, 8055, 8208, 8364, 8523, 8685, 8850, 9019, 9191, 9366, 9544, 9726, 9911, 10100, 10292, 10488, 10688, 10892, 11100, 11312, 11528, 11748, 11972, 12200, 12432, 12669, 12910, 13156 };
  UInt_t nMjjBins=sizeof(mjjBins)/sizeof(double)-1;

  double pTBins[] = { 15. ,20. ,25. ,35. ,45. ,55. ,70. ,85. ,100. ,116. ,134. ,152. ,172. ,194. ,216. ,240. ,264. ,290. ,318. ,346.,376.,408.,442.,478.,516.,556.,598.,642.,688.,736.,786.,838.,894.,952.,1012.,1076.,1162.,1310.,1530.,1992.,2500.,3200. };
  UInt_t npTBins=sizeof(pTBins)/sizeof(double)-1;

  //NOTE pT bins go from 0. to tightpTRange
  //UInt_t nTightpTBins=325; double tightpTRange=6500.; double tightpTBins[nTightpTBins+1];
  //for (UInt_t ii=0;ii<=nTightpTBins;ii++) {tightpTBins[ii]=tightpTRange*ii/nTightpTBins;}

  //NOTE eta bins go from -etaRange to +etaRange
  UInt_t nEtaBins=80; double etaRange=4.; double *etaBins = new double[nEtaBins+1];
  for (UInt_t ii=0;ii<=nEtaBins;ii++) {etaBins[ii]=etaRange*(2.*ii/nEtaBins-1.);}

  //NOTE eta bins go from -phiRange to +phiRange
  UInt_t nPhiBins=100; double phiRange=TMath::Pi(); double *phiBins=new double[nPhiBins+1];
  for (UInt_t ii=0;ii<=nPhiBins;ii++) {phiBins[ii]=phiRange*(2.*ii/nPhiBins-1.);}
  
  UInt_t nNumTrkBins=40;/*200*/; double numTrkRange=200.; double *numTrkBins=new double[nNumTrkBins+1];
  for (UInt_t ii=0;ii<=nNumTrkBins;ii++) {numTrkBins[ii]=numTrkRange*ii/nNumTrkBins;}

  UInt_t nTrackWidthBins=200; double trackWidthRange=1.; double *trackWidthBins=new double[nTrackWidthBins+1];
  for (UInt_t ii=0;ii<=nTrackWidthBins;ii++) {trackWidthBins[ii]=trackWidthRange*(2.*ii/nTrackWidthBins-1.);}

  UInt_t nRatioBins=10000; double ratioRange=1000.; double *ratioBins = new double[nRatioBins+1];
  for (UInt_t ii=0;ii<=nRatioBins;ii++) {ratioBins[ii]=ratioRange*ii/nRatioBins;}

  UInt_t nShortRatioBins=200; double shortRatioRange=1000.; double *shortRatioBins=new double[nShortRatioBins+1];
  for (UInt_t ii=0;ii<=nShortRatioBins;ii++) {shortRatioBins[ii]=shortRatioRange*ii/nShortRatioBins;}
  
  //******************************************
  //coarse binning
  /*
  //double coarseEtaBins[]={-4.9,-3.1,-2.8,-2.1,-1.8,-1.5,-1.2,-0.8,0,0.8,1.2,1.5,1.8,2.1,2.8,3.1,4.9};//negative to positive eta
  double coarseEtaBins[]={0.,0.8,1.2,1.5,1.8,2.1,2.8,3.1,4.9};//absolute eta
  UInt_t nCoarseEtaBins=sizeof(coarseEtaBins)/sizeof(double)-1;

  //double coarsepTBins[]={50., 100., 152., 240., 408., 598., 1012., 2500., 3200.};
  double coarsepTBins[]={20., 50., 100., 152., 240., 408., 598., 1012., 2500., 3200.};//TEST
  UInt_t nCoarsepTBins=sizeof(coarsepTBins)/sizeof(double)-1;

  //double coarseMjjBins[]={0.4e3, 0.6e3, 0.9e3, 1.2e3, 1.6e3, 1.8e3, 2e3, 2.25e3, 2.5e3, 2.8e3, 3.1e3, 3.4e3, 3.7e3, 4e3, 4.3e3, 4.6e3, 4.9e3, 5.4e3, 6.5e3, 8e3, 10e3, 13e3};
  //UInt_t nCoarseMjjBins=sizeof(coarseMjjBins)/sizeof(double)-1;
  */
  
  //******************************************
  //histograms

  //default histogras
  TH1D* h_mjj=new TH1D("mjj","mjj",nMjjBins,mjjBins);
  TH1D* h_mbb_fix_8585=new TH1D("mbb_fix_8585","mjj_fix_8585",nMjjBins,mjjBins);
  TH1D* h_mbb_flt_8585=new TH1D("mbb_flt_8585","mjj_flt_8585",nMjjBins,mjjBins);
  TH1D* h_mbb_fix_7777=new TH1D("mbb_fix_7777","mjj_fix_7777",nMjjBins,mjjBins);
  TH1D* h_mbb_flt_7777=new TH1D("mbb_flt_7777","mjj_flt_7777",nMjjBins,mjjBins);
  TH1D* h_pt=new TH1D("pt","pt",npTBins,pTBins);
  TH1D* h_eta=new TH1D("eta","eta",nEtaBins,etaBins);
  TH1D* h_phi=new TH1D("phi","phi",nPhiBins,phiBins);
  TH2D* h_eta_phi=new TH2D("eta_phi","eta_phi",nEtaBins,etaBins,nPhiBins,phiBins);
  TH2D* h_eta_pt=new TH2D("eta_pt","eta_pt",nEtaBins,etaBins,npTBins,pTBins);
  
  //******************************************
  //TEST
  //std::exit(0);
  //******************************************

  //******************************************
  //loop over tree entries
  Long64_t nentries=tc->fChain->GetEntriesFast();
  //nentries=10;//DEBUG
  UInt_t allevents=0;
  UInt_t goodevents=0;
  double weight=1.;

  //------------------------------------------
  //loop
  for (Long64_t ii=0; ii<nentries; ii++) {

    //------------------------------------------
    //load entry
    //cout<<process<<"entry = "<<ii<<endl;//DEBUG
    tc->readWhatYouNeed(ii);//NOTE this is way faster than tc->GetEntry(ii)
    allevents++;

    //------------------------------------------
    //DEBUG
    //cout<<process<<" leding jet reco pT =  "<<(*tc->jet_pt)[0]<<" GeV"<<endl;//DEBUG
    //cout<<process<<" leding jet truth pT = "<<(*tc->jet_truth_pt)[0]<<" GeV"<<endl;//DEBUG
    //cout<<process<<" mjj =           "<<tc->mjj<<" GeV"<<endl;//DEBUG
    
    //------------------------------------------
    //event selection
    //number of jets
    if ((*tc->jet_pt).size() < 2)
      continue;

    //mjj
    if (mjjCut > 0.) {
      if (fabs(tc->mjj) < mjjCut)
	continue;
    }
    
    //leading jets pT
    if ((*tc->jet_pt)[0] < leadJetpTCut)
      continue;
    if ((*tc->jet_pt)[1] < sublJetpTCut)
      continue;

    //y*
    if (yStarCut > 0.) {
      if (fabs(tc->yStar) > yStarCut)
	continue;
    }

    //eta
    if (etaCut > 0.) {
      if (fabs((*tc->jet_eta)[0]) > etaCut)
	continue;
      if (fabs((*tc->jet_eta)[1]) > etaCut)
	continue;
    }
    
    goodevents++;
    
    //------------------------------------------
    //compute weight
    weight = 1.;
    if (isMC && totalSliceEvents > 0.) {
      //if (tc->weight>0.)
      weight = 1. * tc->weight * lumi / totalSliceEvents;
      //else //NOTE apply if cross section is not available in the ntuples
      //weight = 1. * getCrossSectionTimesFilterEff(snumber) * lumi / totalSliceEvents;
      if (applyNLO) weight *= NLOHist->GetBinContent( NLOHist->FindBin(tc->mjj));
      if (applyEW) weight *= EWHist->GetBinContent( EWHist->FindBin(tc->mjj));
    }

    //DEBUG
    //cout<<process<<"  weight = "<<tc->weight<<endl;
    //cout<<process<<"  NLO weight = "<<NLOHist->GetBinContent( NLOHist->FindBin(tc->mjj))<<endl;
    //cout<<process<<"  EW weight  = "<<EWHist->GetBinContent( EWHist->FindBin(tc->mjj))<<endl;
    //cout<<process<<"  lumi = "<<lumi<<endl;
    //cout<<process<<"  totalSliceEvents = "<<totalSliceEvents<<endl;
    //cout<<process<<"  final weight = "<<weight<<endl;
    
    //------------------------------------------
    //fill histograms

    //default histograms
    h_mjj->Fill(tc->mjj, weight);
    h_mbb_fix_8585->Fill(tc->mbb_fix_8585, weight);
    h_mbb_flt_8585->Fill(tc->mbb_flt_8585, weight);
    h_mbb_fix_7777->Fill(tc->mbb_fix_7777, weight);
    h_mbb_flt_7777->Fill(tc->mbb_flt_7777, weight);
    h_pt->Fill((*tc->jet_pt)[0], weight);
    h_pt->Fill((*tc->jet_pt)[1], weight);
    h_eta->Fill((*tc->jet_eta)[0], weight);
    h_eta->Fill((*tc->jet_eta)[1], weight);
    h_phi->Fill((*tc->jet_phi)[0], weight);
    h_phi->Fill((*tc->jet_phi)[1], weight);
    h_eta_phi->Fill((*tc->jet_eta)[0],(*tc->jet_phi)[0], weight);
    h_eta_phi->Fill((*tc->jet_eta)[1],(*tc->jet_phi)[1], weight);
    h_eta_pt->Fill((*tc->jet_eta)[0],(*tc->jet_pt)[0], weight);
    h_eta_pt->Fill((*tc->jet_eta)[1],(*tc->jet_pt)[1], weight);
    
  }
  
  //******************************************
  //save results to output file
  string outputFileName="";
  if (isMC) {
    outputFileName = "tmp/histograms.mc."+snumber+"."+name;
  } else {
    outputFileName = "tmp/histograms.data."+snumber+"."+name;
  }
  int ii = 0;
  while (fileExists(outputFileName+'.'+std::to_string(ii)+".root"))
    ii++;
  TFile *outputFile=new TFile((outputFileName+'.'+std::to_string(ii)+".root").c_str(),"recreate");
  
  h_mjj->Write();
  h_mbb_fix_8585->Write();
  h_mbb_flt_8585->Write();
  h_mbb_fix_7777->Write();
  h_mbb_flt_7777->Write();
  h_pt->Write();
  h_eta->Write();
  h_phi->Write();
  h_eta_phi->Write();
  h_eta_pt->Write();
    
  outputFile->Write();
  outputFile->Close();
  delete outputFile;
  
  //******************************************
  delete tree;
  file->Close();
  delete file;
  NLOFile->Close();
  delete NLOFile;
  EWFile->Close();
  delete EWFile;
  
  //******************************************
  time.Stop();
  cout<<process<<"ran over "<<goodevents<<" good events out of "<<allevents<<" ("<<nentries<<") events in "<<time.CpuTime()<<" seconds"<<endl;
  return 0;
}

//******************************************
