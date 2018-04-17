//Francesco Guescini
#include "TFile.h"
#include "TTree.h"
#include "TStopwatch.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using std::cout;
using std::endl;
using std::vector;
using std::string;
using std::istringstream;
using std::ofstream;

int main(int argc, char *argv[]) {

  //******************************************
  TStopwatch time;
  time.Start();

  //******************************************
  //get parameters
  string fileListName="";
  string name="ntuple";
  bool isMC=false;
  bool bool_help=false;
  int ip=1;
  while (ip<argc) {

    if (string(argv[ip]).substr(0,2)=="--") {

      //help
      if (string(argv[ip])=="--help") {
	bool_help=true; break;
      }
      
      //file list
      else if (string(argv[ip])=="--list") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  fileListName=argv[ip+1];
	  ip+=2;
	} else {cout<<"\nno file list name inserted"<<endl; bool_help=true; break;}
      }
      
      //name
      else if (string(argv[ip])=="--name") {
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
	  name=argv[ip+1];
	  ip+=2;
	} else {cout<<"\nno name inserted"<<endl; bool_help=true; break;}
      }

      //MC
      else if (string(argv[ip])=="--isMC") {
        isMC = true;
        ip+=1;
      }

      //unknown command
      else {
	cout<<"\ncommand '"<<string(argv[ip])<<"' unknown"<<endl;
	bool_help=true;
	if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") ip+=2;
	else ip+=1;
      }
      
    }//end if "--command"
    
    else { //if command does not start with "--"
      cout << "\ncommand '"<<string(argv[ip])<<"' unknown"<<endl;
      bool_help=true;
      break;
    }//end if "--"
    
  }//end while loop
  
  //after reading the input parameters, call the functions
  if (bool_help || fileListName=="") {
    cout<<"\ndoEventsList"<<endl;
    cout<<"HOW TO: doEventsList --list <file list> --name <name> --isMC"<<endl;
    cout<<"HELP:   doEventsList --help"<<endl;
    return 1;
  }

  //******************************************
  ofstream fout1;
  if (isMC) {
    fout1.open(("eventList/"+name+".mcChannelNumber-runNumber-eventNumber.list").c_str());
  } else {
    fout1.open(("eventList/"+name+".runNumber-eventNumber-lumiBlock.list").c_str());
  }
  //  //  ofstream fout2((name+".RunNumber-file-EventNumber.list").c_str());
  ofstream fout3(("list/"+name+".runNumber-file-nEvents.list").c_str());
  //  ofstream fout4((name+".RunNumber-nEvents.list").c_str());
  
  UInt_t nEvents=0;
  //  UInt_t currentRunNumber=999;
  //  UInt_t nEventsRunNumber=0;
  UInt_t nEventsFile=0;

  //******************************************
  //set file list
  vector<string> fileList;
  std::ifstream ifs(fileListName.c_str());
  while(ifs) {
    string s;
    if (!getline(ifs,s)) break;
    istringstream iss(s);
    while (iss) {
      string s1;
      if (!getline(iss,s1,',')) break;
      fileList.push_back(s1);
      //	std::cout<<"  "<<s1<<std::endl;
    }
  }
  cout<<"input file list: "<<fileListName<<endl;
  cout<<fileList.size()<<" files in the list"<<endl;
  
  //******************************************
  //set iterators to run over file list
  std::vector<std::string>::const_iterator fileList_itr;
  std::vector<std::string>::const_iterator fileList_end;
  fileList_itr=fileList.begin();
  fileList_end=fileList.end();
  
  //******************************************
  //loop over files in the list
  for(;fileList_itr!=fileList_end;++(fileList_itr)) {
    
    //open the file and access its tree
    cout<<"\n"<<fileList_itr->c_str()<<endl;

    //------------------------------------------
    //open files in a while loop
    UInt_t openFileCounter=0;
    TFile *file=0;
    while(!file && openFileCounter<10){
      file=TFile::Open(fileList_itr->c_str(),"READ");
      if(!file) sleep(3);
      openFileCounter++;
      cout<<"  reading try number "<<openFileCounter<<endl;
    }
    //------------------------------------------

    if(!file) {std::cerr<<"couldn't open input file: "<<*fileList_itr<<std::endl; return 1;}
    TTree *tree;
    tree=dynamic_cast<TTree*>(file->Get("physics"));
    if(!tree) tree=dynamic_cast<TTree*>(file->Get("qcd"));
    if(!tree) tree=dynamic_cast<TTree*>(file->Get("susy"));
    if(!tree) tree=dynamic_cast<TTree*>(file->Get("outTree"));
    if(!tree) {std::cerr<<"File '"<<*fileList_itr<<"' doesn't container TTree 'physics' or 'qcd' or 'susy' or 'outTree'"<<std::endl; delete file; return 1;}
  
    //******************************************
    //set branches
    Int_t          runNumber;
    Int_t          eventNumber;
    Int_t          lumiBlock;
    //Int_t          mcEventNumber;
    Int_t          mcChannelNumber;
    Float_t        mjj;
    
    TBranch        *b_runNumber;   //!
    TBranch        *b_eventNumber;   //!
    TBranch        *b_lumiBlock;   //!
    //TBranch        *b_mcEventNumber;   //!
    TBranch        *b_mcChannelNumber;   //!
    TBranch        *b_mjj;   //!

    tree->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
    tree->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
    tree->SetBranchAddress("mjj", &mjj, &b_mjj);
   
    if (isMC) {
      //tree->SetBranchAddress("mcEventNumber", &mcEventNumber, &b_mcEventNumber);
      tree->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
    } else {
      tree->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
    }
    
    //******************************************
    //loop over tree entries
    nEventsFile=0;
    for(UInt_t jj=0;jj<tree->GetEntries();jj++) {
      nEvents++;
      nEventsFile++;
      b_runNumber->GetEntry(jj);
      b_eventNumber->GetEntry(jj);
      b_mjj->GetEntry(jj);
      
      if (isMC) {
	//b_mcEventNumber->GetEntry(jj);
	b_mcChannelNumber->GetEntry(jj);	
      } else {
	b_lumiBlock->GetEntry(jj);
      }

      if (isMC) {
	fout1<<mcChannelNumber<<" "<<runNumber<<" "<<eventNumber<<" "<<mjj<<endl;
      } else {
	fout1<<runNumber<<" "<<eventNumber<<" "<<lumiBlock<<" "<<mjj<<endl;
      }

      //fout1 is enough, no need for fout2
      /*
      fout2<<runNumber<<" "<<file->GetName()<<" "<<eventNumber<<endl;
      if (currentRunNumber!=runNumber) {
	if (currentRunNumber!=999) fout4<<currentRunNumber<<" "<<nEventsRunNumber<<endl;
	currentRunNumber=runNumber;
	nEventsRunNumber=0;
      }
      nEventsRunNumber++;
      */
    }
    fout3<<runNumber<<" "<<file->GetName()<<" "<<nEventsFile<<endl;

    //******************************************
    delete tree;
    file->Close();
    delete file;    
    fout1.flush();
    //    fout2.flush();
    fout3.flush();
  }
  //  fout4<<currentRunNumber<<" "<<nEventsRunNumber<<endl;

  //******************************************
  fout1.close();
  //  fout2.close();
  fout3.close();
  //  fout4.close();
  time.Stop();
  std::cout<<"\nran over "<<nEvents<<" events in "<<fileList.size()<<" files in "<<time.CpuTime()<<" seconds"<<std::endl;
  return 0;
}
