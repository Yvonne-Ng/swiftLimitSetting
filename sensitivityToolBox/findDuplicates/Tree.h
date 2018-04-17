//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jul 15 14:26:29 2015 by ROOT version 6.02/12
// from TTree outTree/outTree
// found on file: /atlas/data5/userdata/guescini/dijet/inputs/Full_20150710/MC15a/tree/user.jdandoy.mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.AllUp1-0.QCD_20150710_tree.root
//////////////////////////////////////////////////////////

#ifndef Tree_h
#define Tree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "vector"
#include "vector"

class Tree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           runNumber;
   Int_t           eventNumber;
   Int_t           mcEventNumber;
   Int_t           mcChannelNumber;
   Float_t         mcEventWeight;
   Float_t         weight_pileup;
   Int_t           NPV;
   Float_t         actualInteractionsPerCrossing;
   Float_t         averageInteractionsPerCrossing;
   Int_t           lumiBlock;
   Double_t        rhoEM;
   Int_t           pdgId1;
   Int_t           pdgId2;
   Int_t           pdfId1;
   Int_t           pdfId2;
   Float_t         x1;
   Float_t         x2;
   Float_t         xf1;
   Float_t         xf2;
   Float_t         yStar;
   Float_t         yBoost;
   Float_t         mjj;
   Float_t         pTjj;
   Float_t         m3j;
   Float_t         deltaPhi;
   Float_t         Insitu_Segs_response_E;
   Float_t         Insitu_Segs_response_pT;
   Int_t           punch_type_segs;
   Float_t         pTBalance;
   Float_t         MHT;
   Float_t         MHTPhi;
   Float_t         MHTJVT;
   Float_t         MHTJVTPhi;
   Float_t         weight;
   Float_t         weight_xs;
   Float_t         weight_prescale;
   Float_t         weight_resonanceKFactor;
   Int_t           passAny;
   Int_t           passL1;
   Int_t           passHLT;
   Int_t           masterKey;
   Int_t           lvl1PrescaleKey;
   Int_t           hltPrescaleKey;
   vector<string>  *passedTriggers;
   Float_t         metFinal;
   Float_t         metFinalPx;
   Float_t         metFinalPy;
   Float_t         metFinalSumEt;
   Float_t         metFinalPhi;
   Int_t           njets;
   vector<float>   *jet_E;
   vector<float>   *jet_pt;
   vector<float>   *jet_phi;
   vector<float>   *jet_eta;
   vector<float>   *jet_rapidity;
   vector<float>   *jet_Timing;
   vector<float>   *jet_LArQuality;
   vector<float>   *jet_HECQuality;
   vector<float>   *jet_NegativeE;
   vector<float>   *jet_AverageLArQF;
   vector<float>   *jet_BchCorrCell;
   vector<float>   *jet_N90Constituents;
   vector<float>   *jet_LArBadHVEFracnergyFrac;
   vector<int>     *jet_LArBadHVNCell;
   vector<float>   *jet_OotFracClusters5;
   vector<float>   *jet_OotFracClusters10;
   vector<float>   *jet_LeadingClusterPt;
   vector<float>   *jet_LeadingClusterSecondLambda;
   vector<float>   *jet_LeadingClusterCenterLambda;
   vector<float>   *jet_LeadingClusterSecondR;
   vector<int>     *jet_clean_passLooseBad;
   vector<int>     *jet_clean_passLooseBadUgly;
   vector<int>     *jet_clean_passTightBad;
   vector<int>     *jet_clean_passTightBadUgly;
   vector<float>   *jet_HECFrac;
   vector<float>   *jet_EMFrac;
   vector<float>   *jet_CentroidR;
   vector<float>   *jet_FracSamplingMax;
   vector<float>   *jet_FracSamplingMaxIndex;
   vector<float>   *jet_LowEtConstituentsFrac;
   vector<float>   *jet_GhostMuonSegmentCount;
   vector<float>   *jet_Width;
   vector<vector<float> > *jet_EnergyPerSampling;
   vector<int>     *jet_NumTrkPt1000PV;
   vector<float>   *jet_SumPtTrkPt1000PV;
   vector<float>   *jet_TrackWidthPt1000PV;
   vector<int>     *jet_NumTrkPt500PV;
   vector<float>   *jet_SumPtTrkPt500PV;
   vector<float>   *jet_TrackWidthPt500PV;
   vector<float>   *jet_JVFPV;
   vector<float>   *jet_Jvt;
   vector<float>   *jet_JvtJvfcorr;
   vector<float>   *jet_JvtRpt;
   vector<int>     *jet_numConstituents;
   vector<float>   *jet_SV0;
   vector<float>   *jet_SV1;
   vector<float>   *jet_IP3D;
   vector<float>   *jet_SV1IP3D;
   vector<float>   *jet_MV1;
   vector<float>   *jet_MV2c00;
   vector<float>   *jet_MV2c20;
   vector<float>   *jet_GhostArea;
   vector<float>   *jet_ActiveArea;
   vector<float>   *jet_VoronoiArea;
   vector<float>   *jet_ActiveArea4vec_pt;
   vector<float>   *jet_ActiveArea4vec_eta;
   vector<float>   *jet_ActiveArea4vec_phi;
   vector<float>   *jet_ActiveArea4vec_m;
   vector<int>     *jet_ConeTruthLabelID;
   vector<int>     *jet_TruthCount;
   vector<float>   *jet_TruthLabelDeltaR_B;
   vector<float>   *jet_TruthLabelDeltaR_C;
   vector<float>   *jet_TruthLabelDeltaR_T;
   vector<int>     *jet_PartonTruthLabelID;
   vector<float>   *jet_GhostTruthAssociationFraction;
   vector<float>   *jet_truth_E;
   vector<float>   *jet_truth_pt;
   vector<float>   *jet_truth_phi;
   vector<float>   *jet_truth_eta;
   vector<float>   *jet_constitScaleEta;
   vector<float>   *jet_emScaleEta;
   vector<float>   *jet_minDeltaR;
   vector<int>     *jet_numberCloseJets;

   // List of branches
   TBranch        *b_runNumber;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_mcEventNumber;   //!
   TBranch        *b_mcChannelNumber;   //!
   TBranch        *b_mcEventWeight;   //!
   TBranch        *b_weight_pileup;   //!
   TBranch        *b_NPV;   //!
   TBranch        *b_actualInteractionsPerCrossing;   //!
   TBranch        *b_averageInteractionsPerCrossing;   //!
   TBranch        *b_lumiBlock;   //!
   TBranch        *b_rhoEM;   //!
   TBranch        *b_pdgId1;   //!
   TBranch        *b_pdgId2;   //!
   TBranch        *b_pdfId1;   //!
   TBranch        *b_pdfId2;   //!
   TBranch        *b_x1;   //!
   TBranch        *b_x2;   //!
   TBranch        *b_xf1;   //!
   TBranch        *b_xf2;   //!
   TBranch        *b_yStar;   //!
   TBranch        *b_yBoost;   //!
   TBranch        *b_mjj;   //!
   TBranch        *b_pTjj;   //!
   TBranch        *b_m3j;   //!
   TBranch        *b_deltaPhi;   //!
   TBranch        *b_Insitu_Segs_response_E;   //!
   TBranch        *b_Insitu_Segs_response_pT;   //!
   TBranch        *b_punch_type_segs;   //!
   TBranch        *b_pTBalance;   //!
   TBranch        *b_MHT;   //!
   TBranch        *b_MHTPhi;   //!
   TBranch        *b_MHTJVT;   //!
   TBranch        *b_MHTJVTPhi;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_weight_xs;   //!
   TBranch        *b_weight_prescale;   //!
   TBranch        *b_weight_resonanceKFactor;   //!
   TBranch        *b_passAny;   //!
   TBranch        *b_passL1;   //!
   TBranch        *b_passHLT;   //!
   TBranch        *b_masterKey;   //!
   TBranch        *b_lvl1PrescaleKey;   //!
   TBranch        *b_hltPrescaleKey;   //!
   TBranch        *b_passedTriggers;   //!
   TBranch        *b_metFinal;   //!
   TBranch        *b_metFinalPx;   //!
   TBranch        *b_metFinalPy;   //!
   TBranch        *b_metFinalSumEt;   //!
   TBranch        *b_metFinalPhi;   //!
   TBranch        *b_njets;   //!
   TBranch        *b_jet_E;   //!
   TBranch        *b_jet_pt;   //!
   TBranch        *b_jet_phi;   //!
   TBranch        *b_jet_eta;   //!
   TBranch        *b_jet_rapidity;   //!
   TBranch        *b_jet_Timing;   //!
   TBranch        *b_jet_LArQuality;   //!
   TBranch        *b_jet_HECQuality;   //!
   TBranch        *b_jet_NegativeE;   //!
   TBranch        *b_jet_AverageLArQF;   //!
   TBranch        *b_jet_BchCorrCell;   //!
   TBranch        *b_jet_N90Constituents;   //!
   TBranch        *b_jet_LArBadHVEFracnergyFrac;   //!
   TBranch        *b_jet_LArBadHVNCell;   //!
   TBranch        *b_jet_OotFracClusters5;   //!
   TBranch        *b_jet_OotFracClusters10;   //!
   TBranch        *b_jet_LeadingClusterPt;   //!
   TBranch        *b_jet_LeadingClusterSecondLambda;   //!
   TBranch        *b_jet_LeadingClusterCenterLambda;   //!
   TBranch        *b_jet_LeadingClusterSecondR;   //!
   TBranch        *b_jet_clean_passLooseBad;   //!
   TBranch        *b_jet_clean_passLooseBadUgly;   //!
   TBranch        *b_jet_clean_passTightBad;   //!
   TBranch        *b_jet_clean_passTightBadUgly;   //!
   TBranch        *b_jet_HECFrac;   //!
   TBranch        *b_jet_EMFrac;   //!
   TBranch        *b_jet_CentroidR;   //!
   TBranch        *b_jet_FracSamplingMax;   //!
   TBranch        *b_jet_FracSamplingMaxIndex;   //!
   TBranch        *b_jet_LowEtConstituentsFrac;   //!
   TBranch        *b_jet_GhostMuonSegmentCount;   //!
   TBranch        *b_jet_Width;   //!
   TBranch        *b_jet_EnergyPerSampling;   //!
   TBranch        *b_jet_NumTrkPt1000PV;   //!
   TBranch        *b_jet_SumPtTrkPt1000PV;   //!
   TBranch        *b_jet_TrackWidthPt1000PV;   //!
   TBranch        *b_jet_NumTrkPt500PV;   //!
   TBranch        *b_jet_SumPtTrkPt500PV;   //!
   TBranch        *b_jet_TrackWidthPt500PV;   //!
   TBranch        *b_jet_JVFPV;   //!
   TBranch        *b_jet_Jvt;   //!
   TBranch        *b_jet_JvtJvfcorr;   //!
   TBranch        *b_jet_JvtRpt;   //!
   TBranch        *b_jet_numConstituents;   //!
   TBranch        *b_jet_SV0;   //!
   TBranch        *b_jet_SV1;   //!
   TBranch        *b_jet_IP3D;   //!
   TBranch        *b_jet_SV1IP3D;   //!
   TBranch        *b_jet_MV1;   //!
   TBranch        *b_jet_MV2c00;   //!
   TBranch        *b_jet_MV2c20;   //!
   TBranch        *b_jet_GhostArea;   //!
   TBranch        *b_jet_ActiveArea;   //!
   TBranch        *b_jet_VoronoiArea;   //!
   TBranch        *b_jet_ActiveArea4vec_pt;   //!
   TBranch        *b_jet_ActiveArea4vec_eta;   //!
   TBranch        *b_jet_ActiveArea4vec_phi;   //!
   TBranch        *b_jet_ActiveArea4vec_m;   //!
   TBranch        *b_jet_ConeTruthLabelID;   //!
   TBranch        *b_jet_TruthCount;   //!
   TBranch        *b_jet_TruthLabelDeltaR_B;   //!
   TBranch        *b_jet_TruthLabelDeltaR_C;   //!
   TBranch        *b_jet_TruthLabelDeltaR_T;   //!
   TBranch        *b_jet_PartonTruthLabelID;   //!
   TBranch        *b_jet_GhostTruthAssociationFraction;   //!
   TBranch        *b_jet_truth_E;   //!
   TBranch        *b_jet_truth_pt;   //!
   TBranch        *b_jet_truth_phi;   //!
   TBranch        *b_jet_truth_eta;   //!
   TBranch        *b_jet_constitScaleEta;   //!
   TBranch        *b_jet_emScaleEta;   //!
   TBranch        *b_jet_minDeltaR;   //!
   TBranch        *b_jet_numberCloseJets;   //!

   Tree(TTree *tree=0);
   virtual ~Tree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef Tree_cxx
Tree::Tree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/atlas/data5/userdata/guescini/dijet/inputs/Full_20150710/MC15a/tree/user.jdandoy.mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.AllUp1-0.QCD_20150710_tree.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/atlas/data5/userdata/guescini/dijet/inputs/Full_20150710/MC15a/tree/user.jdandoy.mc15_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.AllUp1-0.QCD_20150710_tree.root");
      }
      f->GetObject("outTree",tree);

   }
   Init(tree);
}

Tree::~Tree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t Tree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t Tree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void Tree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   passedTriggers = 0;
   jet_E = 0;
   jet_pt = 0;
   jet_phi = 0;
   jet_eta = 0;
   jet_rapidity = 0;
   jet_Timing = 0;
   jet_LArQuality = 0;
   jet_HECQuality = 0;
   jet_NegativeE = 0;
   jet_AverageLArQF = 0;
   jet_BchCorrCell = 0;
   jet_N90Constituents = 0;
   jet_LArBadHVEFracnergyFrac = 0;
   jet_LArBadHVNCell = 0;
   jet_OotFracClusters5 = 0;
   jet_OotFracClusters10 = 0;
   jet_LeadingClusterPt = 0;
   jet_LeadingClusterSecondLambda = 0;
   jet_LeadingClusterCenterLambda = 0;
   jet_LeadingClusterSecondR = 0;
   jet_clean_passLooseBad = 0;
   jet_clean_passLooseBadUgly = 0;
   jet_clean_passTightBad = 0;
   jet_clean_passTightBadUgly = 0;
   jet_HECFrac = 0;
   jet_EMFrac = 0;
   jet_CentroidR = 0;
   jet_FracSamplingMax = 0;
   jet_FracSamplingMaxIndex = 0;
   jet_LowEtConstituentsFrac = 0;
   jet_GhostMuonSegmentCount = 0;
   jet_Width = 0;
   jet_EnergyPerSampling = 0;
   jet_NumTrkPt1000PV = 0;
   jet_SumPtTrkPt1000PV = 0;
   jet_TrackWidthPt1000PV = 0;
   jet_NumTrkPt500PV = 0;
   jet_SumPtTrkPt500PV = 0;
   jet_TrackWidthPt500PV = 0;
   jet_JVFPV = 0;
   jet_Jvt = 0;
   jet_JvtJvfcorr = 0;
   jet_JvtRpt = 0;
   jet_numConstituents = 0;
   jet_SV0 = 0;
   jet_SV1 = 0;
   jet_IP3D = 0;
   jet_SV1IP3D = 0;
   jet_MV1 = 0;
   jet_MV2c00 = 0;
   jet_MV2c20 = 0;
   jet_GhostArea = 0;
   jet_ActiveArea = 0;
   jet_VoronoiArea = 0;
   jet_ActiveArea4vec_pt = 0;
   jet_ActiveArea4vec_eta = 0;
   jet_ActiveArea4vec_phi = 0;
   jet_ActiveArea4vec_m = 0;
   jet_ConeTruthLabelID = 0;
   jet_TruthCount = 0;
   jet_TruthLabelDeltaR_B = 0;
   jet_TruthLabelDeltaR_C = 0;
   jet_TruthLabelDeltaR_T = 0;
   jet_PartonTruthLabelID = 0;
   jet_GhostTruthAssociationFraction = 0;
   jet_truth_E = 0;
   jet_truth_pt = 0;
   jet_truth_phi = 0;
   jet_truth_eta = 0;
   jet_constitScaleEta = 0;
   jet_emScaleEta = 0;
   jet_minDeltaR = 0;
   jet_numberCloseJets = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("mcEventNumber", &mcEventNumber, &b_mcEventNumber);
   fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
   fChain->SetBranchAddress("mcEventWeight", &mcEventWeight, &b_mcEventWeight);
   fChain->SetBranchAddress("weight_pileup", &weight_pileup, &b_weight_pileup);
   fChain->SetBranchAddress("NPV", &NPV, &b_NPV);
   fChain->SetBranchAddress("actualInteractionsPerCrossing", &actualInteractionsPerCrossing, &b_actualInteractionsPerCrossing);
   fChain->SetBranchAddress("averageInteractionsPerCrossing", &averageInteractionsPerCrossing, &b_averageInteractionsPerCrossing);
   fChain->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
   fChain->SetBranchAddress("rhoEM", &rhoEM, &b_rhoEM);
   fChain->SetBranchAddress("pdgId1", &pdgId1, &b_pdgId1);
   fChain->SetBranchAddress("pdgId2", &pdgId2, &b_pdgId2);
   fChain->SetBranchAddress("pdfId1", &pdfId1, &b_pdfId1);
   fChain->SetBranchAddress("pdfId2", &pdfId2, &b_pdfId2);
   fChain->SetBranchAddress("x1", &x1, &b_x1);
   fChain->SetBranchAddress("x2", &x2, &b_x2);
   fChain->SetBranchAddress("xf1", &xf1, &b_xf1);
   fChain->SetBranchAddress("xf2", &xf2, &b_xf2);
   fChain->SetBranchAddress("yStar", &yStar, &b_yStar);
   fChain->SetBranchAddress("yBoost", &yBoost, &b_yBoost);
   fChain->SetBranchAddress("mjj", &mjj, &b_mjj);
   fChain->SetBranchAddress("pTjj", &pTjj, &b_pTjj);
   fChain->SetBranchAddress("m3j", &m3j, &b_m3j);
   fChain->SetBranchAddress("deltaPhi", &deltaPhi, &b_deltaPhi);
   fChain->SetBranchAddress("Insitu_Segs_response_E", &Insitu_Segs_response_E, &b_Insitu_Segs_response_E);
   fChain->SetBranchAddress("Insitu_Segs_response_pT", &Insitu_Segs_response_pT, &b_Insitu_Segs_response_pT);
   fChain->SetBranchAddress("punch_type_segs", &punch_type_segs, &b_punch_type_segs);
   fChain->SetBranchAddress("pTBalance", &pTBalance, &b_pTBalance);
   fChain->SetBranchAddress("MHT", &MHT, &b_MHT);
   fChain->SetBranchAddress("MHTPhi", &MHTPhi, &b_MHTPhi);
   fChain->SetBranchAddress("MHTJVT", &MHTJVT, &b_MHTJVT);
   fChain->SetBranchAddress("MHTJVTPhi", &MHTJVTPhi, &b_MHTJVTPhi);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("weight_xs", &weight_xs, &b_weight_xs);
   fChain->SetBranchAddress("weight_prescale", &weight_prescale, &b_weight_prescale);
   fChain->SetBranchAddress("weight_resonanceKFactor", &weight_resonanceKFactor, &b_weight_resonanceKFactor);
   fChain->SetBranchAddress("passAny", &passAny, &b_passAny);
   fChain->SetBranchAddress("passL1", &passL1, &b_passL1);
   fChain->SetBranchAddress("passHLT", &passHLT, &b_passHLT);
   fChain->SetBranchAddress("masterKey", &masterKey, &b_masterKey);
   fChain->SetBranchAddress("lvl1PrescaleKey", &lvl1PrescaleKey, &b_lvl1PrescaleKey);
   fChain->SetBranchAddress("hltPrescaleKey", &hltPrescaleKey, &b_hltPrescaleKey);
   fChain->SetBranchAddress("passedTriggers", &passedTriggers, &b_passedTriggers);
   fChain->SetBranchAddress("metFinal", &metFinal, &b_metFinal);
   fChain->SetBranchAddress("metFinalPx", &metFinalPx, &b_metFinalPx);
   fChain->SetBranchAddress("metFinalPy", &metFinalPy, &b_metFinalPy);
   fChain->SetBranchAddress("metFinalSumEt", &metFinalSumEt, &b_metFinalSumEt);
   fChain->SetBranchAddress("metFinalPhi", &metFinalPhi, &b_metFinalPhi);
   fChain->SetBranchAddress("njets", &njets, &b_njets);
   fChain->SetBranchAddress("jet_E", &jet_E, &b_jet_E);
   fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   fChain->SetBranchAddress("jet_rapidity", &jet_rapidity, &b_jet_rapidity);
   fChain->SetBranchAddress("jet_Timing", &jet_Timing, &b_jet_Timing);
   fChain->SetBranchAddress("jet_LArQuality", &jet_LArQuality, &b_jet_LArQuality);
   fChain->SetBranchAddress("jet_HECQuality", &jet_HECQuality, &b_jet_HECQuality);
   fChain->SetBranchAddress("jet_NegativeE", &jet_NegativeE, &b_jet_NegativeE);
   fChain->SetBranchAddress("jet_AverageLArQF", &jet_AverageLArQF, &b_jet_AverageLArQF);
   fChain->SetBranchAddress("jet_BchCorrCell", &jet_BchCorrCell, &b_jet_BchCorrCell);
   fChain->SetBranchAddress("jet_N90Constituents", &jet_N90Constituents, &b_jet_N90Constituents);
   fChain->SetBranchAddress("jet_LArBadHVEFracnergyFrac", &jet_LArBadHVEFracnergyFrac, &b_jet_LArBadHVEFracnergyFrac);
   fChain->SetBranchAddress("jet_LArBadHVNCell", &jet_LArBadHVNCell, &b_jet_LArBadHVNCell);
   fChain->SetBranchAddress("jet_OotFracClusters5", &jet_OotFracClusters5, &b_jet_OotFracClusters5);
   fChain->SetBranchAddress("jet_OotFracClusters10", &jet_OotFracClusters10, &b_jet_OotFracClusters10);
   fChain->SetBranchAddress("jet_LeadingClusterPt", &jet_LeadingClusterPt, &b_jet_LeadingClusterPt);
   fChain->SetBranchAddress("jet_LeadingClusterSecondLambda", &jet_LeadingClusterSecondLambda, &b_jet_LeadingClusterSecondLambda);
   fChain->SetBranchAddress("jet_LeadingClusterCenterLambda", &jet_LeadingClusterCenterLambda, &b_jet_LeadingClusterCenterLambda);
   fChain->SetBranchAddress("jet_LeadingClusterSecondR", &jet_LeadingClusterSecondR, &b_jet_LeadingClusterSecondR);
   fChain->SetBranchAddress("jet_clean_passLooseBad", &jet_clean_passLooseBad, &b_jet_clean_passLooseBad);
   fChain->SetBranchAddress("jet_clean_passLooseBadUgly", &jet_clean_passLooseBadUgly, &b_jet_clean_passLooseBadUgly);
   fChain->SetBranchAddress("jet_clean_passTightBad", &jet_clean_passTightBad, &b_jet_clean_passTightBad);
   fChain->SetBranchAddress("jet_clean_passTightBadUgly", &jet_clean_passTightBadUgly, &b_jet_clean_passTightBadUgly);
   fChain->SetBranchAddress("jet_HECFrac", &jet_HECFrac, &b_jet_HECFrac);
   fChain->SetBranchAddress("jet_EMFrac", &jet_EMFrac, &b_jet_EMFrac);
   fChain->SetBranchAddress("jet_CentroidR", &jet_CentroidR, &b_jet_CentroidR);
   fChain->SetBranchAddress("jet_FracSamplingMax", &jet_FracSamplingMax, &b_jet_FracSamplingMax);
   fChain->SetBranchAddress("jet_FracSamplingMaxIndex", &jet_FracSamplingMaxIndex, &b_jet_FracSamplingMaxIndex);
   fChain->SetBranchAddress("jet_LowEtConstituentsFrac", &jet_LowEtConstituentsFrac, &b_jet_LowEtConstituentsFrac);
   fChain->SetBranchAddress("jet_GhostMuonSegmentCount", &jet_GhostMuonSegmentCount, &b_jet_GhostMuonSegmentCount);
   fChain->SetBranchAddress("jet_Width", &jet_Width, &b_jet_Width);
   fChain->SetBranchAddress("jet_EnergyPerSampling", &jet_EnergyPerSampling, &b_jet_EnergyPerSampling);
   fChain->SetBranchAddress("jet_NumTrkPt1000PV", &jet_NumTrkPt1000PV, &b_jet_NumTrkPt1000PV);
   fChain->SetBranchAddress("jet_SumPtTrkPt1000PV", &jet_SumPtTrkPt1000PV, &b_jet_SumPtTrkPt1000PV);
   fChain->SetBranchAddress("jet_TrackWidthPt1000PV", &jet_TrackWidthPt1000PV, &b_jet_TrackWidthPt1000PV);
   fChain->SetBranchAddress("jet_NumTrkPt500PV", &jet_NumTrkPt500PV, &b_jet_NumTrkPt500PV);
   fChain->SetBranchAddress("jet_SumPtTrkPt500PV", &jet_SumPtTrkPt500PV, &b_jet_SumPtTrkPt500PV);
   fChain->SetBranchAddress("jet_TrackWidthPt500PV", &jet_TrackWidthPt500PV, &b_jet_TrackWidthPt500PV);
   fChain->SetBranchAddress("jet_JVFPV", &jet_JVFPV, &b_jet_JVFPV);
   fChain->SetBranchAddress("jet_Jvt", &jet_Jvt, &b_jet_Jvt);
   fChain->SetBranchAddress("jet_JvtJvfcorr", &jet_JvtJvfcorr, &b_jet_JvtJvfcorr);
   fChain->SetBranchAddress("jet_JvtRpt", &jet_JvtRpt, &b_jet_JvtRpt);
   fChain->SetBranchAddress("jet_numConstituents", &jet_numConstituents, &b_jet_numConstituents);
   fChain->SetBranchAddress("jet_SV0", &jet_SV0, &b_jet_SV0);
   fChain->SetBranchAddress("jet_SV1", &jet_SV1, &b_jet_SV1);
   fChain->SetBranchAddress("jet_IP3D", &jet_IP3D, &b_jet_IP3D);
   fChain->SetBranchAddress("jet_SV1IP3D", &jet_SV1IP3D, &b_jet_SV1IP3D);
   fChain->SetBranchAddress("jet_MV1", &jet_MV1, &b_jet_MV1);
   fChain->SetBranchAddress("jet_MV2c00", &jet_MV2c00, &b_jet_MV2c00);
   fChain->SetBranchAddress("jet_MV2c20", &jet_MV2c20, &b_jet_MV2c20);
   fChain->SetBranchAddress("jet_GhostArea", &jet_GhostArea, &b_jet_GhostArea);
   fChain->SetBranchAddress("jet_ActiveArea", &jet_ActiveArea, &b_jet_ActiveArea);
   fChain->SetBranchAddress("jet_VoronoiArea", &jet_VoronoiArea, &b_jet_VoronoiArea);
   fChain->SetBranchAddress("jet_ActiveArea4vec_pt", &jet_ActiveArea4vec_pt, &b_jet_ActiveArea4vec_pt);
   fChain->SetBranchAddress("jet_ActiveArea4vec_eta", &jet_ActiveArea4vec_eta, &b_jet_ActiveArea4vec_eta);
   fChain->SetBranchAddress("jet_ActiveArea4vec_phi", &jet_ActiveArea4vec_phi, &b_jet_ActiveArea4vec_phi);
   fChain->SetBranchAddress("jet_ActiveArea4vec_m", &jet_ActiveArea4vec_m, &b_jet_ActiveArea4vec_m);
   fChain->SetBranchAddress("jet_ConeTruthLabelID", &jet_ConeTruthLabelID, &b_jet_ConeTruthLabelID);
   fChain->SetBranchAddress("jet_TruthCount", &jet_TruthCount, &b_jet_TruthCount);
   fChain->SetBranchAddress("jet_TruthLabelDeltaR_B", &jet_TruthLabelDeltaR_B, &b_jet_TruthLabelDeltaR_B);
   fChain->SetBranchAddress("jet_TruthLabelDeltaR_C", &jet_TruthLabelDeltaR_C, &b_jet_TruthLabelDeltaR_C);
   fChain->SetBranchAddress("jet_TruthLabelDeltaR_T", &jet_TruthLabelDeltaR_T, &b_jet_TruthLabelDeltaR_T);
   fChain->SetBranchAddress("jet_PartonTruthLabelID", &jet_PartonTruthLabelID, &b_jet_PartonTruthLabelID);
   fChain->SetBranchAddress("jet_GhostTruthAssociationFraction", &jet_GhostTruthAssociationFraction, &b_jet_GhostTruthAssociationFraction);
   fChain->SetBranchAddress("jet_truth_E", &jet_truth_E, &b_jet_truth_E);
   fChain->SetBranchAddress("jet_truth_pt", &jet_truth_pt, &b_jet_truth_pt);
   fChain->SetBranchAddress("jet_truth_phi", &jet_truth_phi, &b_jet_truth_phi);
   fChain->SetBranchAddress("jet_truth_eta", &jet_truth_eta, &b_jet_truth_eta);
   fChain->SetBranchAddress("jet_constitScaleEta", &jet_constitScaleEta, &b_jet_constitScaleEta);
   fChain->SetBranchAddress("jet_emScaleEta", &jet_emScaleEta, &b_jet_emScaleEta);
   fChain->SetBranchAddress("jet_minDeltaR", &jet_minDeltaR, &b_jet_minDeltaR);
   fChain->SetBranchAddress("jet_numberCloseJets", &jet_numberCloseJets, &b_jet_numberCloseJets);
   Notify();
}

Bool_t Tree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void Tree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t Tree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef Tree_cxx
