// ***************************************************************
// This file was created using the CreateProject.sh script
// for project MjjProject.
// CreateProject.sh is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://www.mppmu.mpg.de/bat
// ***************************************************************

#include "TH1.h"
#include <iostream>
#include "TEnv.h"
#include "TError.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "TVectorD.h"
#include "TStopwatch.h"
#include "TKey.h"
#include "TDirectory.h"
#include "TClass.h"

#include "Bayesian/MjjFitter.h"
#include "Bayesian/MjjHistogram.h"
#include "Bayesian/MjjFitFunction.h"
#include "Bayesian/MjjStatisticalTest.h"
#include "Bayesian/MjjChi2Test.h"
#include "Bayesian/MjjPseudoExperimenter.h"
#include "Bayesian/MjjStatisticsBundle.h"
#include "Bayesian/MjjSignificanceTests.h"
#include "Bayesian/MjjBumpHunter.h"
#include "Bayesian/BonusFitFunctions.h"

#include <BAT/BCLog.h>
#include <BAT/BCAux.h>
#include <BAT/BCSummaryTool.h>
#include <BAT/BCH1D.h>

#include "Bayesian/MjjBATModel.h"
#include "Bayesian/MjjBATProcess.h"
#include "Bayesian/MjjBATShapeChangingSyst.h"
#include "Bayesian/MjjBATScaleChangingSyst.h"
#include "Bayesian/MjjBATTemplateSyst.h"

void UsagedoGaussianLimits(){
  std::cout << "Usage: " << std::endl;
  std::cout << " --ratio     : width to mass ratio, 0.10 -> 10% width, 0 uses variable resolution" << std::endl;
  std::cout << " --config    : config file to read details from (filenames, JES)" << std::endl;
  std::cout << " --infile    : Gaussian sample input file" << std::endl;
  std::cout << " --useweight : " << std::endl;
  std::cout << "Examples: " << std::endl;
  std::cout << " Fixed Gaussians 10% width: \n"
	    << "  doGaussianLimits --ratio 0.10 --config configurations/GenericGaussians.config" 
	    << std::endl;
  std::cout << " Variable resolution width, from sample file, apply PDF and acceptance weights: \n"
	    << "  doGaussianLimits --ratio 0.0 --config configurations/GenericGaussiansAK.config --infile mtestpdf43_8000_w7.root --useweight"
	    << std::endl;
}

double interpretJESFile(TH1D* theHist, double massGeV) {
  int inbin;
  double frac;
  if (massGeV < 2500) {inbin = 1; if (massGeV < 2000) frac = 0.0; else frac = (massGeV-2000.0)/500.0;} //return theHist->GetBinContent(1);
  else if (massGeV >= 2500 && massGeV < 3000) {inbin = 2; frac = (massGeV-2500)/500.0;} //return theHist->GetBinContent(2);
  else if (massGeV >= 3000 && massGeV < 3500) {inbin = 3; frac = (massGeV-3000)/500.0;} //return theHist->GetBinContent(3);
  else if (massGeV >= 3500 && massGeV < 4000) {inbin = 4; frac = (massGeV-3500)/500.0;} //no equivalent!
  else if (massGeV >= 4000 && massGeV < 4500) {inbin = 5; frac = (massGeV-4000)/500.0;} //return theHist->GetBinContent(4);
  else if (massGeV >= 4500 && massGeV < 5000) {inbin = 6; frac = (massGeV-4500)/500.0;} //return theHist->GetBinContent(5);
  else if (massGeV >= 5000 && massGeV < 5500) {inbin = 7; frac = (massGeV-5000)/500.0;} //return theHist->GetBinContent(6);
  else if (massGeV >= 5500 && massGeV < 6000) {inbin = 8; frac = (massGeV-5500)/500.0;} //return theHist->GetBinContent(7);
  else if (massGeV >= 6000 && massGeV < 6500) {inbin = 9; frac = (massGeV-6000)/500.0;}//return theHist->GetBinContent(8);
  else if (massGeV >= 6500) {inbin = 10; frac = 1.0;}//return theHist->GetBinContent(9);
  else {
    std::cout << "Unexpected result!" << std::endl;
    return -1.0;
  }
  
  double val;
  if (inbin==10) val = theHist->GetBinContent(inbin);
  else val = (theHist->GetBinContent(inbin+1) - theHist->GetBinContent(inbin))*frac + theHist->GetBinContent(inbin);
  std::cout << "Assigning val " << val << " for a mass " << massGeV << std::endl;
  return val;
  
}

int main(int argc,char **argv)
{

  ////////////////////////////////////////////////////////////
  // Initialisation: this part should be user-modified

  // Start counting time
  TStopwatch totaltime;
  totaltime.Start();

  // Start reading input configuration
  TString configFile;
  double thisRatio = -1;
  bool useResolutionWidth = false;
  bool useSubRange = false;
  double rangeLow = 0;
  double rangeHigh = -1;
  float ISRAccErr = 0.;
  bool doISRAccError = false;
  int ip=1;
  while (ip<argc) {

    if (string(argv[ip]).substr(0,2)=="--") {

      //config file
      if (string(argv[ip])=="--config") {
        if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
          configFile=argv[ip+1];
          ip+=2;
        } else {std::cout<<"\nno config file inserted"<<std::endl; break;}
      }

      //number of chains to run
      else if (string(argv[ip])=="--ratio") {
        if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
          sscanf(argv[ip+1],"%lf",&thisRatio);
          ip+=2;
        } else {std::cout<<"\nno ratio specified"<<std::endl; break;}
      }

      //use resolution width
      else if (string(argv[ip])=="--useresolutionwidth") {
          useResolutionWidth = true;
          ip+=1;
      }

      // do only subrange of masses
      else if (string(argv[ip])=="--rangelow") {
        if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
          sscanf(argv[ip+1],"%lf",&rangeLow);
          useSubRange = true;
          ip+=2;
        } else {std::cout<<"\nno ratio specified"<<std::endl; break;}
      }

      else if (string(argv[ip])=="--rangehigh") {
        if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") {
          sscanf(argv[ip+1],"%lf",&rangeHigh);
          useSubRange = true;
          ip+=2;
        } else {std::cout<<"\nno ratio specified"<<std::endl; break;}
      }

      // acceptance uncertainty due to ISR
      else if (string(argv[ip]) == "--ISRAccErr") {
	if (ip+1<argc) {
	  sscanf(argv[ip+1],"%f",&ISRAccErr);
	  ip+=2;
	  std::cout << "ISR acceptance uncertainty: " << ISRAccErr << std::endl;
	  doISRAccError = true;
	} else {std::cout<<"\nno ISR acceptance uncertainty specified"<<std::endl; break;}
      }

      //unknown command
      else {
        std::cout<<"\n" << string(argv[0]) <<": command '"<<string(argv[ip])<<"' unknown"<<std::endl;
        if (ip+1<argc && string(argv[ip+1]).substr(0,2)!="--") ip+=2;
        else ip+=1;
	UsagedoGaussianLimits();
      } }//end if "--command"

    else { //if command does not start with "--"
      std::cout << "\n" << string(argv[0]) << ": command '"<<string(argv[ip])<<"' unknown"<<std::endl;
      UsagedoGaussianLimits();
      break;
    }//end if "--"

  }//end while loop

  std::cout << "got to end of reading inputs." << std::endl;

  int ratioForNames = int(1000*thisRatio);
  int internalRatio = int(100*thisRatio);

  // Get config file
  TEnv * settings = new TEnv();
  int status = settings->ReadFile(configFile.Data(),EEnvLevel(0));
  if (status!=0) {
    std::cout<<"cannot read config file"<<std::endl;
    std::cout<<"******************************************\n"<<std::endl;
    return 1;
  }

  // Specify files
  string inputFileName = settings->GetValue("inputFileName","");
  string outputFileName = settings->GetValue("outputFileName","");

  // Get data
  TString dataMjjHistoName = settings->GetValue("dataHist","");
 
  // Do we use extended region for fit?
  bool doExtendedRange = settings->GetValue("doExtendedRange",true);

  // Get center of mass energy
  double Ecm = settings->GetValue("Ecm",13000.0);
  if (rangeHigh<0) rangeHigh = Ecm;

  // PDF information
  bool readFromFile = settings->GetValue("useBW",false);
  TString inFileFormat = settings->GetValue("BWFileFormat","");
  string PDF = settings->GetValue("PDF","");

  // Resolution file name
  string resfilename = settings->GetValue("resolutionFile","");
  vector<double> respars;
  bool useFile = (useResolutionWidth && resfilename != "");
  bool useFunc = false;
  if (useResolutionWidth && resfilename == "") {
    useFunc = true;
    for (int i = 1; i < 8; i++) {
      string title = Form("respar%i",i);
      double param = settings->GetValue(title.c_str(),1.0);
      respars.push_back(param);
    }
  }

  // JES size file name
  bool doVarJES = settings->GetValue("doVarJES",true);
  TString JESfilename = settings->GetValue("JESFile","./inputs/JESshifts/QStarJESShifts1invfbJES1Component3Down.root");
  bool useJESFile = (doVarJES && JESfilename != "");
  TH1D JESVariationHist;
  if (useJESFile) {
    TFile infileJES(JESfilename);
    infileJES.ls();
    JESVariationHist = *(TH1D*)infileJES.Get("CompDown3");
  }
  std::cout << "\nThis is the JES variation hist:" << std::endl;
  JESVariationHist.Print("all");
  // Store them for later
  vector<double> JESShiftsUsed;

  // Open files
  TFile * infile = TFile::Open(inputFileName.c_str(), "READ");
  TH1::AddDirectory(kFALSE);

  // Range for data fit
  double minX = settings->GetValue("minXForFit",-1);
  double maxX = settings->GetValue("maxXForFit",-1);

  // Set up numbers.
  double nSigmas = settings->GetValue("nSigmas",3.0);

  // Do we do bkg error?
  bool doFitError = settings->GetValue("doFitError",false);
  int nFitsInBkgError = settings->GetValue("nFitsInBkgError",100);

  // New: control for choosing nominal & alternate functions.
  int functionNumber = settings->GetValue("functionCode",9);
  int nPars = settings->GetValue("nParameters",3);
  int alternateFuncNumber = 0, altNPars = 0;

  // Parameters for fit
  std::cout << "Setting the "<< nPars << " parameters to "; // Lydia
  vector<double> paramDefaults;
  vector<bool> areParamsFixed;
  for (int par = 1; par<nPars+1; par++) {
    string title = Form("parameter%i",par);
    double param = settings->GetValue(title.c_str(),1.0);
    paramDefaults.push_back(param);
    title = Form("fixParameter%i",par);
    bool isFixed = settings->GetValue(title.c_str(),false);
    areParamsFixed.push_back(isFixed);
    std::cout << "   (" << par-1 << ") :" << param;
  }
  std::cout << std::endl;


  // Parameters for alternate fit, if requested
  // Note it may not have been run in search phase, so
  // do not count on picking up defaults from the input file.
  bool doFitFunctionChoiceError = settings->GetValue("doFitFunctionChoiceError",false);

  vector<double> altParDefaults;
  vector<bool> altAreParsFixed;
  if (doFitFunctionChoiceError) {
    alternateFuncNumber = settings->GetValue("alternateFunctionCode",4);
    altNPars = settings->GetValue("alternateNParameters",4);
    for (int par = 1; par < altNPars+1; par++) {
      string title = Form("altparameter%i",par);
      double param = settings->GetValue(title.c_str(),1.0);
      altParDefaults.push_back(param);
      std::cout<<"altparam "<<param<<std::endl; // Lydia
      title = Form("fixAltParameter%i",par);
      bool isFixed = settings->GetValue(title.c_str(),false);
      altAreParsFixed.push_back(isFixed);
      std::cout << "Setting alternative function param "<< par << " to "<< param << std::endl;
    }
  }

  // Do we do lumi?
  bool doLumiError = settings->GetValue("doLumiError", false);
  double luminosityErr = settings->GetValue("luminosityErr",0.90);
  if (doLumiError) {std::cout << "Lumi uncertainty: " << luminosityErr << std::endl;}

  // Do we do JER?
  bool doJERError = settings->GetValue("doJERError", false);
  double JERErr = settings->GetValue("JERErr",0.);
  if (doJERError) {std::cout << "JER uncertainty: " << JERErr << std::endl;}

  // Do we do JES?
  bool doJES = settings->GetValue("doJES",true);
  double sigmaJESShift = settings->GetValue("sigmaJESShift",0.10);
  int nJES = settings->GetValue("nJES",25);

  // Get ranges for density of gaussian points
  double startPoints = settings->GetValue("startPoints",500);
  double stopDensePoints = settings->GetValue("stopDensePoints",2000);
  double stopMediumPoints = settings->GetValue("stopMediumPoints",3000);
  double stopPoints = settings->GetValue("stopPoints",5000);

  // Create output name with ratio if necessary
  if (useSubRange) { 
     TString addon = Form("_low%d_high%d",(int)(rangeLow),(int)(rangeHigh));
     outputFileName.append(addon);
  }
  if (useResolutionWidth) {
    outputFileName.append("_resolutionwidth.root");
  } else if (thisRatio >= 0) {
    outputFileName.append(Form("_%d.root",(int)(1000*thisRatio)));
    std::cout << "Ratio specified. Now using output name " << outputFileName << std::endl;
  } else {
    outputFileName.append(".root");
    std::cout << "No ratio specified. Now using output name " << outputFileName << std::endl;
  }

  // Start code proper

  double interval = (nSigmas*2)/((double)(nJES-1));
  vector<double> jesSigmas;
  jesSigmas.push_back(0.);
  for (int i=0; i<nJES; i++) {
    double value = -1*nSigmas + i*interval;
    if (!(fabs(value - 0) < 1e-3)) jesSigmas.push_back(value);
  }

  // Get and store data
  TH1D * basicInputHisto = (TH1D*) infile->Get(dataMjjHistoName);
  MjjHistogram theHistogram((TH1D*)basicInputHisto);

  std::cout << "Contents of the data histogram: " << std::endl;
  basicInputHisto->Print("all");

  // Set up values for calculating gaussians
  // Fill with big range of values, but only look at those that fall within reasonable
  // bounds of data spectrum.
  vector<double> masses;
  for (double m=startPoints; m<stopDensePoints; m += 50.) masses.push_back(m);
  for (double m=stopDensePoints; m<stopMediumPoints; m += 100.) masses.push_back(m);
  for (double m=stopMediumPoints; m<=stopPoints; m += 200.) masses.push_back(m); 

  vector<double> widthToMass;
  if (thisRatio>=0)  widthToMass.push_back(thisRatio);
  else if (!useResolutionWidth){
    widthToMass.push_back(0.07);
    widthToMass.push_back(0.10);
    widthToMass.push_back(0.15);
  } else {
    std::cout << "Adding one value" << std::endl;
    widthToMass.push_back(0);
  }

  // Get resolution tgraph if making Gaussians of resolution width
  cout<<"check1"<<endl;
  TGraphAsymmErrors * resolutiongraph = 0;
  cout<<"check2"<<endl;
  if (useFile) {
    TH1::AddDirectory(kFALSE);
    TFile * mresf = TFile::Open(resfilename.c_str());
    TCanvas * c3 = (TCanvas*) mresf->Get("C1");
    cout<<"check3"<<endl;
//    resolutiongraph = (TGraphAsymmErrors*) ((c3->GetListOfPrimitives())->At(0));
    resolutiongraph = (TGraphAsymmErrors*) (c3->GetPrimitive("Graph"));
    mresf->Close();
    cout<<"check4"<<endl;
    delete mresf;
  } else if (useFunc) {
    cout<<"check5"<<endl;
    TF1 myfunc("resolutionFunc","[0] + [1]*x + [2]*x*x + [3]*x*x*x + [4]*x*x*x*x + [5]*x*x*x*x*x + [6]*x*x*x*x*x*x",770,8000);
    cout<<"check6"<<endl;
    for (int par = 0; par < 7; par++) {
      myfunc.SetParameter(par,respars.at(par));
    }
    cout<<"check7"<<endl;
    resolutiongraph = new TGraphAsymmErrors();
    cout<<"check 8"<<endl;
    for (int x = 771; x < 8000; x++) {
      resolutiongraph->SetPoint(x-771,double(x),myfunc.Eval(x));
    }
    cout<<"check9"<<endl;
  }

  std::cout << "Made function." << std::endl;

  ////////////////////////////////////////////////////////////
  // Set up fit function.

  // Lydia changed this part so picks start and end bins that are fully spanned by range minX-maxX
  // e.g. user picks minX maxX of 2000-3000 only bins fully within this range are fitted
  // rather than fitting e.g. 1950-3500
  // Now matches SearchPhase.cxx

  int firstBin, lastBin;
  if (minX < theHistogram.GetHistogram().GetBinLowEdge(theHistogram.GetFirstBinWithData()) || minX < 0) firstBin = theHistogram.GetFirstBinWithData();
  else firstBin = theHistogram.GetHistogram().FindBin(minX)+1;

  if (maxX > theHistogram.GetHistogram().GetBinLowEdge(theHistogram.GetLastBinWithData()+1) || maxX < 0) lastBin = theHistogram.GetLastBinWithData();
  else lastBin = theHistogram.GetHistogram().FindBin(maxX)-1;
  double minXForFit = theHistogram.GetHistogram().GetBinLowEdge(firstBin);
  double maxXForFit = theHistogram.GetHistogram().GetBinLowEdge(lastBin+1);

  std::cout << "Fitting " << minXForFit << " to " << maxXForFit << " GeV, or bins " << firstBin << " to " << lastBin << std::endl;

  /*int firstBin, lastBin;
  if (theHistogram.GetHistogram().FindBin(minX) < theHistogram.GetFirstBinWithData() || minX < 0) firstBin = theHistogram.GetFirstBinWithData();
  else firstBin = theHistogram.GetHistogram().FindBin(minX)+1;
  if (theHistogram.GetHistogram().FindBin(maxX) > theHistogram.GetLastBinWithData() || maxX < 0) lastBin = theHistogram.GetLastBinWithData();
  else lastBin = theHistogram.GetHistogram().FindBin(maxX)-1;
  double minXForFit = theHistogram.GetHistogram().GetBinLowEdge(firstBin);
  double maxXForFit = theHistogram.GetHistogram().GetBinLowEdge(lastBin+1);*/

  // Create fit function(s)
  MjjFitFunction * theMjjFitFunction;
  MjjFitFunction * theAlternateFunction;
  vector<std::pair<int,MjjFitFunction**> > functionsAndCodes;
  functionsAndCodes.push_back(std::make_pair(functionNumber,&theMjjFitFunction));
  functionsAndCodes.push_back(std::make_pair(alternateFuncNumber,&theAlternateFunction));

  for (unsigned int index = 0; index < functionsAndCodes.size(); index++) {

    int thisFuncCode = functionsAndCodes.at(index).first;
    std::cout << functionsAndCodes.at(index).second << std::endl;
    switch (thisFuncCode) {
      case 1 :
        std::cout << "Creating UA2 fit function." << std::endl;
        *functionsAndCodes.at(index).second = new UA2FitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 2 :
        std::cout << "Creating CDF (1995) fit function." << std::endl;
        *functionsAndCodes.at(index).second = new CDFFitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 3 :
        std::cout << "Creating CDF (1997) fit function." << std::endl;
        *functionsAndCodes.at(index).second = new CDF1997FitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 4 :
        std::cout << "Creating standard dijet function." << std::endl;
        *functionsAndCodes.at(index).second = new FourParamFitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 5 :
        std::cout << "Creating TeV Gravity function." << std::endl;
        *functionsAndCodes.at(index).second = new ThreeParamFitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 6 :
        std::cout << "Creating 5-parameter function, floating sqrt(s)." << std::endl;
        *functionsAndCodes.at(index).second = new FiveParamSqrtsFitFunction(minXForFit,maxXForFit);
        break;
      case 7 :
        std::cout << "Creating 5-parameter function, log(x)^2 term." << std::endl;
        *functionsAndCodes.at(index).second = new FiveParamLog2FitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 8 :
        std::cout << "Creating 6-parameter function." << std::endl;
        *functionsAndCodes.at(index).second = new SixParamFitFunction(minXForFit,maxXForFit,Ecm);
        break;
      case 9 :
        std::cout << "Creating 3-parameter function for Run II search." << std::endl;
        *functionsAndCodes.at(index).second = new ThreeParam2015FitFunction(minXForFit,maxXForFit,Ecm);
        break;
            case 10 :
                std::cout << "Creating second Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction2(minXForFit,maxXForFit,Ecm);
                break;
            case 11 :
                std::cout << "Creating third Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction3(minXForFit,maxXForFit,Ecm);
                break;
            case 12 :
                std::cout << "Creating fourth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction4(minXForFit,maxXForFit,Ecm);
                break;
            case 13 :
                std::cout << "Creating fifth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction5(minXForFit,maxXForFit,Ecm);
                break;
            case 14 :
                std::cout << "Creating sixth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction6(minXForFit,maxXForFit,Ecm);
                break;
            case 15 :
                std::cout << "Creating seventh Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction7(minXForFit,maxXForFit,Ecm);
                break;
            case 16 :
                std::cout << "Creating eigth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction8(minXForFit,maxXForFit,Ecm);
                break;
            case 17 :
                std::cout << "Creating ninth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction9(minXForFit,maxXForFit,Ecm);
                break;
            case 18 :
                std::cout << "Creating tenth Multijet function." << std::endl;
 				*functionsAndCodes.at(index).second = new MultijetFitFunction10(minXForFit,maxXForFit,Ecm);
                break;
            case 19 :
                std::cout << "Creating gamma gamma with no exponent, 2 par." << std::endl;
                *functionsAndCodes.at(index).second = new TwoParGammaGamma(minXForFit,maxXForFit,Ecm);
                break;
            case 20 :
                std::cout << "Creating gamma gamma with no exponent, 4 par." << std::endl;
                *functionsAndCodes.at(index).second = new FourParGammaGamma(minXForFit,maxXForFit,Ecm);
                break;
            case 21 :
                std::cout << "Creating gamma gamma with 1/3 exponent, 2 par." << std::endl;
                *functionsAndCodes.at(index).second = new TwoParGammaGammaWithThird(minXForFit,maxXForFit,Ecm);
                break;
            case 22 :
                std::cout << "Creating gamma gamma with 1/3 exponent, 3 par." << std::endl;
                *functionsAndCodes.at(index).second = new ThreeParGammaGammaWithThird(minXForFit,maxXForFit,Ecm);
                break;
            case 23 :
                std::cout << "Creating gamma gamma with 1/3 exponent, 4 par." << std::endl;
                *functionsAndCodes.at(index).second = new FourParGammaGammaWithThird(minXForFit,maxXForFit,Ecm);
                break;


     }
    std::cout << functionsAndCodes.at(index).second << std::endl;
  }

  theMjjFitFunction->SetParameterDefaults(paramDefaults);
  theMjjFitFunction->RestoreParameterDefaults();
  for (int par = 0; par<nPars; par++) {
    std::cout << "Fixing parameter " << par << " to " << areParamsFixed.at(par) << std::endl;
    theMjjFitFunction->GetParameter(par)->SetFixParameter(areParamsFixed.at(par));
  }

  // Create alternate function
  // This one really needs you to tell it what the defaults should be.
  if (doFitFunctionChoiceError) {
    theAlternateFunction->SetParameterDefaults(altParDefaults);
    theAlternateFunction->RestoreParameterDefaults();
  }

  std::cout << "Starting initial fit." << std::endl;

  // Create fitter
  MjjFitter theSilentFitter;

  ////////////////////////////////////////////////////////////
  // Loop over all mass points in all ranges.

  vector<TH1D> bestEstimates;
  vector<double> massesUsed;
  vector<vector<double> >  modelCLVectors; 
  for (unsigned int model=0; model<widthToMass.size(); model++) {

    std::cout << "In width " << model << std::endl;

    vector<double> CLsForModel;

    for (unsigned int thisMass=0; thisMass<masses.size(); thisMass++) {

      double thisMeanMass = masses.at(thisMass);
      std::cout << "Mass " << thisMeanMass << std::endl;

      if (useSubRange) {
        if (thisMeanMass < rangeLow || rangeHigh <=thisMeanMass) {
//          CLsForModel.push_back(-100);
          continue;
        }
      }

      ////////////////////////////////////////////////////////////
      // Create signal histogram and JES variations
      
      // Histogram base for setting binning
      TH1D binbase(*(TH1D*) infile->Get(dataMjjHistoName));
      vector<TH1D> SignalTemplates;

      double thisWidthToMass;
      if (useResolutionWidth) thisWidthToMass = resolutiongraph->Eval(thisMeanMass);
      else thisWidthToMass = widthToMass.at(model);

      std::cout << "this width is " << thisMeanMass << " * " << thisWidthToMass << " = " << thisMeanMass*thisWidthToMass <<std::endl;

      // Only compute point if it is more than 2 sigma from an edge
      if ((thisMeanMass - 2*thisMeanMass*thisWidthToMass < minXForFit)
         or (thisMeanMass + 2*thisMeanMass*thisWidthToMass > maxXForFit)) {
//        CLsForModel.push_back(-100);
        std::cout<<"Mass point too close to edge (i.e. less than 2 sigma away)"<<std::endl;
        continue;
      }

      if((!readFromFile)||(inFileFormat==NULL)){

	// Create JES shifted samples
    double JESShift;
    if (useJESFile) {
      JESShift = interpretJESFile(&JESVariationHist,thisMeanMass);
    } else JESShift = sigmaJESShift;
    std::cout<<"JESShift: "<<JESShift<<std::endl;
    JESShiftsUsed.push_back(JESShift);
        
	for (unsigned int i=0; i<jesSigmas.size(); i++) {

	  double shiftMass = thisMeanMass + jesSigmas.at(i)*JESShift*thisMeanMass;
	  double onesigma = shiftMass*thisWidthToMass;
	  double shift3SigDown = shiftMass - 3*onesigma;
	  double shift3SigUp = shiftMass + 3*onesigma;
	  
	  
	  TF1 GenericGaussian("signal",Form("TMath::Gaus(x,%f,%f)",shiftMass,onesigma), 
			      shift3SigDown, shift3SigUp);  
	  
	  TH1D JESShifted(binbase);
	  JESShifted.SetName(Form("JES_%f",jesSigmas.at(i)));
	  
	  for (int ibin=0; ibin<JESShifted.GetNbinsX()+2; ibin++) {
	    if (JESShifted.GetBinLowEdge(ibin) >= shift3SigUp ||
		JESShifted.GetBinLowEdge(ibin+1) <= shift3SigDown) {
	      JESShifted.SetBinContent(ibin,0.);
	      JESShifted.SetBinError(ibin,0.);
	    } else { 
	      double a = JESShifted.GetBinLowEdge(ibin);
	      double b = JESShifted.GetBinLowEdge(ibin)+JESShifted.GetBinWidth(ibin);
	      double content = GenericGaussian.Integral(a,b);
	      JESShifted.SetBinContent(ibin,content);
	      JESShifted.SetBinError(ibin,0.);
	    }
	  }
	  
	  SignalTemplates.push_back(JESShifted);
	}
      }else{

        //exit if no PDF specified
        if (PDF == "") return 0;

        // Open file with this mass and width
        std::cout << "thisMeanMass,ratioForNames are " << thisMeanMass << " " << ratioForNames << std::endl;
        TString infilename = Form(inFileFormat,(int) thisMeanMass,ratioForNames);
	TFile mf(infilename);

        double integral = 0;
        for (unsigned int i=0; i<jesSigmas.size(); i++) {

          TH1D JESShifted(binbase);
          JESShifted.SetName(Form("JES_%f",jesSigmas.at(i)));

          // Get hist from file
          std::cout << "About to get " << Form("finalsignal_PDF%s_width%d_JES%d",PDF.c_str(),internalRatio,i) << std::endl;
          TString histname = Form("finalsignal_PDF%s_width%d_JES%d",PDF.c_str(),internalRatio,i);
          TH1D fullhist(*(TH1D*)mf.Get(histname));

          // Rebin into correct histogram
          for (int bin = 1; bin < JESShifted.GetNbinsX()+1; bin++) {
            double binstart = JESShifted.GetBinLowEdge(bin) + 0.1;
            double binend = JESShifted.GetBinLowEdge(bin) + JESShifted.GetBinWidth(bin) - 0.1;
            JESShifted.SetBinContent(bin,fullhist.Integral(fullhist.FindBin(binstart),fullhist.FindBin(binend)));
            JESShifted.SetBinError(bin,0.0);
          }

          // Normalise to 1
          if (i==0) integral = JESShifted.Integral();
          JESShifted.Scale(1/integral);

          SignalTemplates.push_back(JESShifted);

        }
      }

      int nomIndex=-1, highestJESIndex=-1;
      for (unsigned int i=0; i<jesSigmas.size(); i++) {
        if (jesSigmas.at(i)==0.) nomIndex = i;
        if (jesSigmas.at(i)==nSigmas) highestJESIndex = i;
      }
      TH1D nominal(SignalTemplates.at(nomIndex));
      nominal.SetName("nominal");

      std::cout << "Highest JES index is " << highestJESIndex << std::endl;

      TH1D * nominalFitTemplate = (TH1D*) nominal.Clone();
      nominalFitTemplate->SetName("nominalFitTemplate");
      MjjHistogram thisSigHisto(nominalFitTemplate);

      ///////////////////////////////////////////////////////////////////////////
      // Recalculate range for process using new signal
      int extendedLastBin = lastBin;
      if (doExtendedRange) {
        for (int i=0; i<theHistogram.GetHistogram().GetNbinsX()+2; i++) {
          if (basicInputHisto->GetBinContent(i) > 0 ||
            nominalFitTemplate->GetBinContent(i) > 0 ||
            SignalTemplates.at(highestJESIndex).GetBinContent(i) > 0)
           extendedLastBin = i;
        }
      }
      std::cout << "New extended range ends at " << basicInputHisto->GetBinLowEdge(extendedLastBin+1);

      ////////////////////////////////////////////////////////////
      // Create background template

      theSilentFitter.SetSignalTemplate(nominalFitTemplate);

      MjjHistogram theBackgroundFromSimultaneousFit = theSilentFitter.FitAndGetBkgWithDataErr(*theMjjFitFunction,theHistogram,nFitsInBkgError);
      TH1D bkgTemplate = (TH1D) theBackgroundFromSimultaneousFit.GetHistogram();

      std::cout << "Finished initial fit." << std::endl;

      // What were fitted params?
      vector<double> fittedParameters = theMjjFitFunction->GetCurrentParameterValues();

      std::cout << "After fit, parameters are  ";
      for (unsigned int i=0; i<fittedParameters.size(); i++) {
        std::cout << "   (" << i << "):" << fittedParameters.at(i);
      }
      std::cout << std::endl;

      // Set up variation template for background
      TH1D bkgVariation(bkgTemplate);
      bkgVariation.SetName("BkgVariation");
      for (int i=0; i<bkgTemplate.GetNbinsX()+1; i++) {
        bkgVariation.SetBinContent(i,bkgTemplate.GetBinError(i));
        bkgVariation.SetBinError(i,0.);
      }

      // Set up fit function choice templates for background
      // Old method: Use difference between nominal and alternate in this data.
/*
      MjjHistogram bkgFromFiveParam = theSilentFitter.FitAndGetBkgWithMCErr(*theAlternateFunction,theHistogram);
      TH1D variedfit = bkgFromFiveParam.GetHistogram();
      variedfit.SetName("fitplusonesigmachoice");
      vector<std::pair<double,TH1D*> > fitvariedtemplates;
      fitvariedtemplates.push_back(std::make_pair(0,&bkgTemplate));
      fitvariedtemplates.push_back(std::make_pair(1,&variedfit));
*/
      // New method: Use average difference between the two functions across a range of pseudoexperiments
      // where the pseudoexperiments are thrown from data.
      MjjHistogram bkgFromAltFunc;
      MjjHistogram bkgWithFuncChoiceErr;
      TH1D fitChoicePlus1Sig(bkgTemplate);
      if (doFitFunctionChoiceError) {

        bkgFromAltFunc = theSilentFitter.FitAndGetBkgWithNoErr(*theAlternateFunction,theHistogram);
        vector<double> altfittedParameters = theAlternateFunction->GetCurrentParameterValues();

        // Use results of fit to data to set start parameters for alternate function in fit to PEs
        theAlternateFunction->SetParameterDefaults(altfittedParameters);

        // What were fitted params?
        std::cout << "After alternate fit, parameters are  ";
        for (unsigned int i=0; i<altfittedParameters.size(); i++) {
          std::cout << "   (" << i << "):" << altfittedParameters.at(i);
        }
        std::cout << std::endl;

        // Get histogram with errors equal to RMS of distance between functions
        // across PEs in each bin. This is the uncertainty that will be used for calculating
        // the search phase p-value using systematics.
        bkgWithFuncChoiceErr = theSilentFitter.FitAndGetBkgWithFitDiffErr(*theMjjFitFunction,*theAlternateFunction,theHistogram,100,true);

        // Create histogram of format which will be used as alternate function
        // to define function choice uncertainty when directionality matters:
        // that is, in the limit setting stage.
        fitChoicePlus1Sig.SetName("alternateFitChoiceSyst_setByRMSTimesDirectionality");
        for (int bin = 1; bin < fitChoicePlus1Sig.GetNbinsX()+1; bin++) {
  	  double nomquantity = theBackgroundFromSimultaneousFit.GetHistogram().GetBinContent(bin);
	  double varquantity = bkgFromAltFunc.GetHistogram().GetBinContent(bin);
	  if (varquantity < nomquantity) fitChoicePlus1Sig.SetBinContent(bin,nomquantity - bkgWithFuncChoiceErr.GetHistogram().GetBinError(bin));
	  else fitChoicePlus1Sig.SetBinContent(bin,nomquantity + bkgWithFuncChoiceErr.GetHistogram().GetBinError(bin));
        }
      }
      vector<std::pair<double,TH1D*> > fitvariedtemplates;
      fitvariedtemplates.push_back(std::make_pair(0,&bkgTemplate));
      fitvariedtemplates.push_back(std::make_pair(1,&fitChoicePlus1Sig));

      ///////////////////////////////////////////////////////////////////////////
      // Estimate appropriate signal range
      double maxNSignal = 0;
      double stepSize;
      if (thisMass < 1000) stepSize = 200;
      else if (thisMass < 1500) stepSize = 50;
      else stepSize = 10;  // increase nSignalEvents nStepSize events at a time
      double maxLsoFar = 0;
      double thisL = 1;
      MjjLogLikelihoodTest theLogLTest;
      TH1D sumHist(bkgTemplate);
      sumHist.SetName("HistSigEstimate");
      double integral = nominalFitTemplate->Integral();
      nominalFitTemplate->Scale(1./integral);
      while (maxLsoFar / thisL < 1e5) {

        for (int bin=0; bin<sumHist.GetNbinsX(); bin++) {
          sumHist.SetBinContent(bin,bkgTemplate.GetBinContent(bin) + nominalFitTemplate->GetBinContent(bin)*maxNSignal);
          sumHist.SetBinError(bin,0.);
        }
        MjjHistogram theSignalTemplate(&sumHist);
        TH1D weighthist = theHistogram.GetWeightsHistogram();
        theSignalTemplate.SetEffectiveFromBasicAndWeights(&weighthist);

        double logL = theLogLTest.DoTest(theHistogram,theSignalTemplate,firstBin,extendedLastBin);
        thisL = exp(-logL);

        if (std::isnan(thisL)) break;
        if (thisL > maxLsoFar) maxLsoFar = thisL;

        maxNSignal+=stepSize;
      }

      std::cout << "Estimated maximum signal range = " << maxNSignal << std::endl;

      ////////////////////////////////////////////////////////////
      // Create signal template

      TH1D nominalSignal(nominal);
      nominalSignal.SetName("nominalSignal");
      TH1D variationSignal(nominal);
      variationSignal.SetName("variationSignal");
      double totalBinContent = 0;
      for (int i=0; i<nominalSignal.GetNbinsX()+1; i++) {
        totalBinContent+=nominalSignal.GetBinContent(i);
        nominalSignal.SetBinContent(i,0.);
        nominalSignal.SetBinError(i,0.);
      }
      for (int i=0; i<variationSignal.GetNbinsX()+1; i++) {
        if (variationSignal.GetBinContent(i)==0) continue;
        double cont = variationSignal.GetBinContent(i);
        variationSignal.SetBinContent(i,cont/totalBinContent);
        variationSignal.SetBinError(i,0.);
      }

      ////////////////////////////////////////////////////////////
      // Create histograms for systematics

      // JES histos
      vector<std::pair<double,TH1D*> > signalJESVariations; signalJESVariations.clear();
      for (unsigned int i=0; i<jesSigmas.size(); i++) signalJESVariations.push_back(std::make_pair(jesSigmas.at(i),&SignalTemplates.at(i)));

      ////////////////////////////////////////////////////////////
      // Create limit-setting tools.

      // set nicer style for drawing than the ROOT default
      BCAux::SetStyle();

      // open log file
      TString logfile("log.txt");
      BCLog::OpenLog(logfile);
      BCLog::SetLogLevel(BCLog::detail);

      // create new MjjBATModel object
      MjjBATModel * m = new MjjBATModel();

      // create a new summary tool object
      BCSummaryTool * summary = new BCSummaryTool(m);

      // My stuff: adding signal, processes, systematics ...
      // Background and signal normalization are assumed (for now) to be gaussian around given values
      m->SetData(theHistogram,firstBin,extendedLastBin);

      if(doFitError) m->AddProcess("BKG",true,false,-nSigmas,nSigmas);
      else m->AddProcess("BKG",1,0.0,0.0);
      m->AddProcess("SIGNAL",true,true,0.0,maxNSignal);

      ////////////////////////////////////////////////////////////
      // Set BAT tools to all the new values.

      m->SetTemplate("BKG",bkgTemplate,bkgVariation);
      vector<string> newparams = m->GetProcess(m->GetProcessIndex("BKG"))->GetParamNames();
      for (unsigned int i=0; i<newparams.size(); i++) {
        m->SetPriorGauss(newparams.at(i).c_str(),0.,1.);
      }

      m->SetTemplate("SIGNAL",nominalSignal,variationSignal);
      vector<string> sigparams = m->GetProcess(m->GetProcessIndex("SIGNAL"))->GetParamNames();
      for (unsigned int i=0; i<sigparams.size(); i++) {
        m->SetPriorConstant(sigparams.at(i).c_str());
      }

      // Create JES uncertainty.
      if (doJES) {
        m->AddSystematic("JES",-nSigmas,nSigmas);
        m->SetPriorGauss("JES",0.,1.);
        MjjBATTemplateSyst * JESOnSignal = new MjjBATTemplateSyst(false);
        JESOnSignal->SetSpectra(signalJESVariations);
        m->SetSystematicVariation("SIGNAL","JES",JESOnSignal);
      }

      if (doFitFunctionChoiceError) {

        m->AddSystematic("FUNCCHOICE",0,1);
        m->SetPriorGauss("FUNCCHOICE",0.,1.);
        MjjBATTemplateSyst * FuncChoiceOnBkg = new MjjBATTemplateSyst(true);
        FuncChoiceOnBkg->SetSpectra(fitvariedtemplates);
        m->SetSystematicVariation("BKG","FUNCCHOICE",FuncChoiceOnBkg);

      }

      // Create luminosity uncertainty. Add variations in processes.
      if (doLumiError) {
        m->AddSystematic("LUMI",-nSigmas,nSigmas);
        m->SetPriorGauss("LUMI",0.,1.);
        MjjBATScaleChangingSyst * LumiOnSignal = new MjjBATScaleChangingSyst(luminosityErr);
        LumiOnSignal->SetScaleFromBinContent();
        m->SetSystematicVariation("SIGNAL","LUMI",LumiOnSignal);
      }

      if (doJERError) {
	// Create JER uncertainty. Add variations in processes.
	m->AddSystematic("JER",-nSigmas,nSigmas);
	m->SetPriorGauss("JER",0.,1.);
	MjjBATScaleChangingSyst * JEROnSignal = new MjjBATScaleChangingSyst(JERErr);
	JEROnSignal->SetScaleFromBinContent();
	m->SetSystematicVariation("SIGNAL","JER",JEROnSignal);
      }

      if (doISRAccError) {
        // Create ISR uncertainty. Add variations in processes.
        m->AddSystematic("ISRAcc",-nSigmas,nSigmas);
        m->SetPriorGauss("ISRAcc",0.,1.);
        MjjBATScaleChangingSyst * ISRAccOnSignal = new MjjBATScaleChangingSyst(ISRAccErr);
        ISRAccOnSignal->SetScaleFromBinContent();
        m->SetSystematicVariation("SIGNAL","ISRAcc",ISRAccOnSignal);

      }

      ////////////////////////////////////////////////////////////
      // Marginalise and get observed limits.

      // Print out all Parameters, so know including all systematics!

      for (unsigned int i=0; i<m->GetNParameters(); i++) {
        std::cout << "Parameter " << i << " is " << m->GetParameter(i)->GetName() << std::endl;
      }
      // run MCMC and marginalize posterior wrt. all parameters
      // and all combinations of two parameters
      m->MarginalizeAll();

      BCParameter * normPar = m->GetParameter(m->GetProcess(1)->GetNormalisationParamIndex());
      BCH1D * marginalizedSig = m->GetMarginalized(normPar);
      double trueCL = marginalizedSig->GetLimit(0.95);
      std::cout << "CL for mass " << thisMeanMass << " is " << trueCL << std::endl;

      delete m;
      delete summary;
  
      // close log file
      BCLog::CloseLog();

      CLsForModel.push_back(trueCL);
      massesUsed.push_back(thisMeanMass);

    }
    modelCLVectors.push_back(CLsForModel);
  }

  ////////////////////////////////////////////////////////////
  // Save everything.

  // Print plots of input variations into file for checking
  std::cout << "Writing output files " << outputFileName << std::endl;

  TFile * outfile = TFile::Open(outputFileName.c_str(), "RECREATE");
  outfile->cd();

  std::cout << "In output file " << std::endl;

  for (unsigned int i=0; i<widthToMass.size(); i++) {
    vector<double> theseCLs = modelCLVectors.at(i);
    TVectorD CLsForModelMasses(theseCLs.size());
    for (unsigned int j=0; j<theseCLs.size(); j++) {
      CLsForModelMasses[j] = theseCLs.at(j);
    }
    CLsForModelMasses.Write(Form("CLsPerMass_widthToMass%d",ratioForNames));
  }

  TVectorD writeMassesUsed(massesUsed.size());
  for (unsigned int i=0; i<massesUsed.size(); i++) {
    writeMassesUsed[i] = massesUsed.at(i);
  }
  writeMassesUsed.Write("massesUsed");

  TVectorD writeJESShiftsUsed(JESShiftsUsed.size());
  for (unsigned int i=0; i<JESShiftsUsed.size(); i++) {
    writeJESShiftsUsed[i] = JESShiftsUsed.at(i);
  }
  writeJESShiftsUsed.Write("JESShifts");

  if (useFile || useFunc)
    resolutiongraph->Write("resolution");

  outfile->Close();
  std::cout << "Closed outfile" << std::endl;
  infile->Close();
  std::cout << "Closed infile" << std::endl;
 
  totaltime.Stop();
  std::cout << "Ran in " << totaltime.CpuTime() << " seconds. " << std::endl;

  delete outfile;
  delete infile;

  return 0;

}

