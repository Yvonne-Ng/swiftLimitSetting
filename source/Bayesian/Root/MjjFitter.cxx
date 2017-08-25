// ---------------------------------------------------------

#include "Bayesian/MjjFitter.h"

// ---------------------------------------------------------
MjjFitter::MjjFitter() 
{

  // create minimizer and function based on LikeMin
  // Minimizer uses specified minimization type
  // kCombined is combined Migrad + Simplex minimization
  // From mnusersguide.pdf: Migrad is generally supposed to be best. Thus combined should be okay.
  fMinuitMinimizer = new ROOT::Minuit2::Minuit2Minimizer(ROOT::Minuit2::kCombined); 

  // Use non-chatty default print level.
  fPrintLevel = -1;
  fMinuitMinimizer->SetPrintLevel(fPrintLevel);

  // Set various options for minimizer

  // Accuracy options
  ROOT::Math::MinimizerOptions::SetDefaultMaxFunctionCalls(50000);
  fMinuitMinimizer->SetMaxFunctionCalls(500000);
  fMinuitMinimizer->SetMaxIterations(100000);
  fMinuitMinimizer->SetTolerance(0.0001);

  // Indicates fitter can take longer to ensure best fit
  fMinuitMinimizer->SetStrategy(2);

  // See user manual. Value depends on type of minimization used. 
  // Chi^2, negative log likelihood have diff values. 
  // This is for -log(Likelihood). Sets FCN::up in Minuit. 
  fMinuitMinimizer->SetErrorDef(0.5); 

  // Parameter step size
  fStepSize = 0.0001;

  // Adjust printout levels for errors
  // to suppress massages like Info in <Minuit2>:[...]
  gErrorIgnoreLevel=kWarning; //1001; 

  // By default, do not use signal.
  fFitWithSignal = false;
  fSignalParameterIndex = -1;
  
  // Initialize retry value
  fRetry = 0;

}

// ---------------------------------------------------------
MjjFitter::~MjjFitter() 
{
  
}

// ---------------------------------------------------------
double MjjFitter::LikeMin(const double *params)
{

  for (int i=0; i<fFitFunction->GetNpar(); i++) {
    
    fFitFunction->SetParameter(i,params[i]);
  }

  double nSignal = 0;
  if (fFitWithSignal) nSignal = params[fSignalParameterIndex];

  double logL = 0;
  double data, weight, fitEquivalentOfNEvents; 
//  std::cout << "Using bins " << "[" << fStartBin << ", " << fStopBin << "]"<< std::endl;
  for (int bin = fStartBin; bin < fStopBin+1; bin++) {
    
    data = fEffectiveHistogramToFit.GetBinContent(bin);
    weight = fWeightsHistogram.GetBinContent(bin);
    fitEquivalentOfNEvents = fFitFunction->Integral(fBasicHistogramToFit.GetBinLowEdge(bin),fBasicHistogramToFit.GetBinLowEdge(bin+1));

    if (fMjjFitFunction.GetDoWindowExclusion()) {
      std::pair <double,double> boundaries = fMjjFitFunction.GetWindowBoundaries();

      // Exclude all bins that overlap with the bump
      // if top edge of bin touches any region of exclusion: continue
      if ((fBasicHistogramToFit.GetBinLowEdge(bin+1) >= boundaries.first &&
          fBasicHistogramToFit.GetBinLowEdge(bin+1) <= boundaries.second) ||
         (fBasicHistogramToFit.GetBinLowEdge(bin) >= boundaries.first &&
          fBasicHistogramToFit.GetBinLowEdge(bin) <= boundaries.second) ) continue;
    }
    
    double sigEquivalentOfNEvents = 0;
    if (fFitWithSignal) sigEquivalentOfNEvents = fSignalTemplate->GetBinContent(bin)*nSignal;

    if (fitEquivalentOfNEvents<0) fitEquivalentOfNEvents = 0;

    logL += -SimpleLogPoisson( data , (fitEquivalentOfNEvents + sigEquivalentOfNEvents)/weight);

//    std::cout << "In bin " << bin << " adding L(" << data << ", " << (fitEquivalentOfNEvents +  sigEquivalentOfNEvents/weight) << ") = " << -SimpleLogPoisson(data , (fitEquivalentOfNEvents + sigEquivalentOfNEvents)/weight)<< std::endl;   
 
  }

//  std::cout << "With sig parameter " << params[4] << " log l is " << logL << std::endl;

  return logL;

}

// ---------------------------------------------------------
double MjjFitter::SimpleLogPoisson(double x, double par) 
{

  // Replacement for call to log(TMath::PoissonI(x,par))

  int ix = Int_t(x);

  if (ix<0)
    // Poisson does return 0;
    return -1*std::numeric_limits<double>::max();
  else if (ix == 0.0)
    // Poisson does return 1./Exp(par);
    return -1*par;
  else {
    Double_t lnpoisson = ix*log(par)-par-TMath::LnGamma(ix+1.);
    // Poisson does return Exp(lnpoisson);
    return lnpoisson;
  }

}

// ---------------------------------------------------------
void MjjFitter::SetSignalTemplate(TH1D * sigTemplate) 
{

  // Create new TH1D with unique name
  fSignalTemplate = (TH1D*) sigTemplate->Clone();
  std::string newName = "sigtemp_";
  newName.append(sigTemplate->GetName());
  fSignalTemplate->SetName(newName.c_str());

  // Normalize it so that amount by which it is scaled
  // will equal number of events
  double integral = fSignalTemplate->Integral();
  for (int i=0; i<fSignalTemplate->GetNbinsX()+2; i++) {
    double oldContent = fSignalTemplate->GetBinContent(i);
    fSignalTemplate->SetBinContent(i, oldContent/integral);
  }

  // Switch fitting default to use signal.
  fFitWithSignal = true;

  return;

}

// ---------------------------------------------------------
bool MjjFitter::MinuitMLFit ()
{

  // Erase parameters from previous fit, if any
  fMinuitMinimizer->Clear();

  // Number of params
  int numberOfParameters = (int) fFitFunction->GetNpar();

  // initializes all function parameters and sets limits if applicable
  vector <double> initialParamVals;
  for (int iLoop=0;iLoop<numberOfParameters;iLoop++){

    initialParamVals.push_back(fMjjFitFunction.GetParameter(iLoop)->GetParamDefault());

    bool isParamFixed = fMjjFitFunction.GetParameter(iLoop)->GetIsFixed();
    std::pair<bool,bool> hasLimits = fMjjFitFunction.GetParameter(iLoop)->GetHasParamLimits();
    double minLimit = fMjjFitFunction.GetParameter(iLoop)->GetParamLimitLow();
    double maxLimit = fMjjFitFunction.GetParameter(iLoop)->GetParamLimitHigh();

    // Is this a retry? If so, deviate slightly from initial start value.
    double adjustment = (fRetry%2)*(-0.1*fRetry)*initialParamVals[iLoop];

    if (isParamFixed) {
      fMinuitMinimizer->SetFixedVariable(iLoop,Form("a%d",iLoop),initialParamVals[iLoop]);
    } else if (hasLimits.first==true && hasLimits.second==true) {
      fMinuitMinimizer->SetLimitedVariable(iLoop,Form("a%d",iLoop), 
              initialParamVals[iLoop]+adjustment, fStepSize, minLimit, maxLimit);
    } else if (hasLimits.first==true && hasLimits.second==false) {
      fMinuitMinimizer->SetLowerLimitedVariable(iLoop,Form("a%d",iLoop), 
              initialParamVals[iLoop]+adjustment, fStepSize, minLimit);
    } else if (hasLimits.first==false && hasLimits.second==true) {
      fMinuitMinimizer->SetUpperLimitedVariable(iLoop,Form("a%d",iLoop), 
              initialParamVals[iLoop]+adjustment, fStepSize, maxLimit);
    } else {
      fMinuitMinimizer->SetVariable(iLoop,Form("a%d",iLoop), 
              initialParamVals[iLoop]+adjustment, fStepSize);
    }
  }

  if (fFitWithSignal) {
    int sigParam = numberOfParameters;
    fMinuitMinimizer->SetLowerLimitedVariable(sigParam,Form("a%d",sigParam),0., 1,0.);
    initialParamVals.push_back(0);
    fSignalParameterIndex = sigParam;
    numberOfParameters++;
  }

  // This is just a wrapper for the function we defined in LikeMin, letting it be used by Minuit
  ROOT::Math::Functor functor = ROOT::Math::Functor(this, &MjjFitter::LikeMin, numberOfParameters); 
  fMinuitMinimizer->SetFunction(functor);

  // Perform minimization.
  fMinuitMinimizer->Minimize();
  fFitFunction->SetParErrors(fMinuitMinimizer->Errors());

  // Did it work?
  bool didWork = false;
  if (fMinuitMinimizer->Status() < 2) didWork = true;

//   ///DEBUG: 
//  fPrintLevel=1;
  if (fPrintLevel != -1) {
    cout << "Printing Minuit results: " << endl;
    fMinuitMinimizer->PrintResults();
    const double  *par_result = fMinuitMinimizer->X();
    std::cout << "Parameter results were: " << par_result[0] << " " << par_result[1] << " " << par_result[2] << " " << par_result[3] << " " << par_result[4] << std::endl;
    if (fPrintLevel != -1) cout <<  "-logL: " << LikeMin(par_result) << endl;
  }

  return didWork;

}

// ---------------------------------------------------------
bool MjjFitter::Fit(MjjHistogram & mjjHistogram, MjjFitFunction & mjjFitFunction) 
{

  fMjjFitFunction = mjjFitFunction;

  //get fit function
  fFitFunction = mjjFitFunction.GetFitFunction();

  // Get histogram for preliminary fit
  TH1D normalizedHistogramToFit = (TH1D) mjjHistogram.GetNormalizedHistogram();

  // get histograms for main fit
  fBasicHistogramToFit = (TH1D) mjjHistogram.GetHistogram();
  fEffectiveHistogramToFit = (TH1D) mjjHistogram.GetEffectiveHistogram();
  fWeightsHistogram = (TH1D) mjjHistogram.GetWeightsHistogram();

  // Fit within range specified by function
  double minXForFit = mjjFitFunction.GetMinXVal();
  double maxXForFit = mjjFitFunction.GetMaxXVal();

  std::cout << "Actual fit range is " << minXForFit << " - " << maxXForFit << std::endl;

  // Get start and stop bin values
  fStartBin = fBasicHistogramToFit.FindBin(minXForFit+1);
  if (fBasicHistogramToFit.FindBin(maxXForFit-1) > fBasicHistogramToFit.GetXaxis()->GetNbins()) 
       fStopBin = fBasicHistogramToFit.GetXaxis()->GetNbins();
  else fStopBin = fBasicHistogramToFit.FindBin(maxXForFit-1);

  mjjFitFunction.RestoreParameterDefaults();

  // Preliminary ROOT fit to get parameters near expected values
  for (int i=0; i<5; i++)  normalizedHistogramToFit.Fit(fFitFunction,"R0q");
  double * ROOTFitParams = fFitFunction->GetParameters();

  // ML fit using Minuit minimizer
  fLatestFitStatus = MinuitMLFit();

  // If it didn't work, keep trying up to
  // 5 times until it does.
  fRetry = 0;
  while (!fLatestFitStatus && fRetry<5) {
    fRetry++;
    std::cout << "Retry number " << fRetry << std::endl;
    fFitFunction->SetParameters(ROOTFitParams);
    fLatestFitStatus = MinuitMLFit();
  }

  if (fLatestFitStatus == false) std::cout << "Fit failed to converge after five retries." << std::endl;

  return fLatestFitStatus;

}

// ---------------------------------------------------------
MjjHistogram MjjFitter::FitAndGetBkgWithNoErr(MjjFitFunction & fitFunction, MjjHistogram & histToFit) 
{

  fitFunction.RestoreParameterDefaults();
  Fit(histToFit,fitFunction);
  
  TH1D backgroundFromFunc((TH1D) histToFit.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",backgroundFromFunc.GetName()));
  backgroundFromFunc.SetName(bkgname);
  TH1D weights((TH1D) histToFit.GetWeightsHistogram());
  TString weightname(Form("%s_internal_weights",weights.GetName()));
  weights.SetName(weightname);

  fitFunction.MakeHistFromFunction(&backgroundFromFunc); 
  MjjHistogram backgroundNoErr(&backgroundFromFunc);
  backgroundNoErr.SetEffectiveFromBasicAndWeights(&weights);

  fFitSuccessRate = (double) fLatestFitStatus;
  return backgroundNoErr;

}

// ---------------------------------------------------------
MjjHistogram MjjFitter::FitAndGetBkgWithMCErr(MjjFitFunction & fitFunction, MjjHistogram & histToFit)
{
  fitFunction.RestoreParameterDefaults();
  Fit(histToFit,fitFunction);

  TH1D backgroundFromFunc((TH1D) histToFit.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",backgroundFromFunc.GetName()));
  backgroundFromFunc.SetName(bkgname);
  TH1D weights((TH1D) histToFit.GetWeightsHistogram());
  TString weightname(Form("%s_internal_weights",weights.GetName()));
  weights.SetName(weightname);

  fitFunction.MakeHistFromFunction(&backgroundFromFunc); 
  for (int i=1; i<=backgroundFromFunc.GetNbinsX(); i++) {
    double thisBinErr = sqrt(backgroundFromFunc.GetBinContent(i));
    backgroundFromFunc.SetBinError(i,thisBinErr);
    std::cout<<"Bin "<<i<<" MCErr: "<<thisBinErr<<std::endl;
  }
  MjjHistogram backgroundMCErr(&backgroundFromFunc);
  backgroundMCErr.SetEffectiveFromBasicAndWeights(&weights);

  fFitSuccessRate = (double) fLatestFitStatus;
  return backgroundMCErr;

}

// ---------------------------------------------------------
MjjHistogram MjjFitter::FitAndGetBkgWithDataErr(MjjFitFunction & fitFunction, MjjHistogram & histToFit, int nFluctuations) 
{
  //int successes = nFluctuations+1;
  //int total = nFluctuations+1;
  int successes = nFluctuations;
  int total = nFluctuations;

  TH1D background((TH1D) histToFit.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",background.GetName()));
  background.SetName(bkgname); 
  TH1D weights((TH1D) histToFit.GetWeightsHistogram());
  TString weightname(Form("%s_internal_weights",weights.GetName()));
  weights.SetName(weightname);

  fitFunction.RestoreParameterDefaults();
  bool didImportantFitWork = Fit(histToFit,fitFunction);
  vector<double> storeImportantCovarianceMatrix = fLatestCovarianceMatrix;
  vector<double> correctFitParameters = fitFunction.GetCurrentParameterValues();

  if (!didImportantFitWork) background.Fatal("MjjFitter::FitAndGetBkgWithDataErr","Main fit failed!");

  fitFunction.MakeHistFromFunction(&background); 

  // Use MjjHistogram to get proper fluctuations.
  MjjHistogram bkgTemplate(&background);
  bkgTemplate.SetEffectiveFromBasicAndWeights(&weights);

  // Beginning of calculation of error bars on background.
  ///////////////////////////////////////////////////////////////////////////////

  // This construction seems complicated but it's a good way to rearrange data 
  // from ordering by fluctuation to ordering by bin
  fStoreBinContentVectors.clear();
  for (int i=1; i<=background.GetNbinsX(); i++) {
    vector<double> veccontent;
    veccontent.clear();
    fStoreBinContentVectors.push_back(veccontent);
  }


  // Create histograms for pseudoexperiments
  TH1D fluctData(background);
  TString fluctdataname(Form("%s_internal_pseudodata",fluctData.GetName()));
  fluctData.SetName(fluctdataname);

  fluctData.Clear();

  for (int i = 0; i<nFluctuations; i++) {

    bkgTemplate.PoissonFluctuateBinByBin(&fluctData);
    MjjHistogram fluctDataHist(&fluctData);
    MjjHistogram fluctBkgHist = FitAndGetBkgWithNoErr(fitFunction,fluctDataHist);
    
    TH1D fluctBkg((TH1D)fluctBkgHist.GetHistogram());
    TString fluctbkgname(Form("%s_internal_pseudobkg",fluctBkg.GetName()));
    fluctBkg.SetName(fluctbkgname);
    std::cout<<"PE #: "<<i<<std::endl;
    // If fit fails don't count this.
    if (fLatestFitStatus==false) {
      nFluctuations++;
      successes--;
      continue;
    }
    else{
	    if (fluctBkgHist.GetHistogram().Integral() <= 0.){
		    nFluctuations++;
		    successes--;
		    continue;
	    }
    } 
    // Lydia
    std::cout<<"In FitAndGetBkgWithDataErr"<<std::endl;
    //
    // Store bin contents in vector<double> corresponding to this bin
    for (int j=1; j<=fluctBkg.GetNbinsX(); j++) {
      fStoreBinContentVectors.at(j-1).push_back(fluctBkg.GetBinContent(j));
    }


  }

  double RMSOfThisBin;
  for (int i=1; i<=background.GetNbinsX(); i++) {

      /* Lydia RMS test
      std::cout<<"Number: "<<i<<std::endl;
      std::cout<<"LowEdge: "<<background.GetBinLowEdge(i)<<std::endl;
      std::cout<<"A: "<<background.GetBinContent(i)<<std::endl;
      TFile f("/home/beresford/TriJet/StatisticalAnalysis/Bayesian/RMS.root","update");
      double Center = background.GetBinContent(i);
      double Ten = background.GetBinContent(i)/10.;
      TH1F h1("hgaus","histo from a gaussian",100,Center-Ten,Center+Ten);
      string str = std::to_string(i);
      string name = "Hist";
      name += str;
      const char* cstr2 = name.c_str();       // if you really want a C-style pointer
      h1.SetName(cstr2);

      int size = fStoreBinContentVectors.at(i-1).size();

      for (int j=0; j<size; ++j){ 
        //std::cout<<fStoreBinContentVectors.at(i-1).at(j)<<std::endl;
        h1.Fill(fStoreBinContentVectors.at(i-1).at(j));
      }
      f.cd();
      h1.Write();
      f.Write();*/

    if (fStoreBinContentVectors.at(i-1).size() == 0) background.SetBinError(i,sqrt(background.GetBinContent(i)));
    else {
      RMSOfThisBin = GetRMS(fStoreBinContentVectors.at(i-1));
       
      background.SetBinError(i,RMSOfThisBin);
    }
  //f.Close();
  }
  ///////////////////////////////////////////////////////////////////////////////
  // End of calculation of error bars on background.

  // Make an MjjHistogram
  MjjHistogram theResult(&background);
  theResult.SetEffectiveFromBasicAndWeights(&weights);

  // Restore values from primary fit
  fitFunction.SetCurrentParameterValues(correctFitParameters);
  fLatestFitStatus = didImportantFitWork;  // Keep result of main fit
  fLatestCovarianceMatrix = storeImportantCovarianceMatrix; // Keep result of main fit
  fFitSuccessRate = (double)successes/(double)total;

  return theResult;

}

// ---------------------------------------------------------
MjjHistogram MjjFitter::FitAndGetBkgWithFitDiffErr(MjjFitFunction & nominal, MjjFitFunction & alternate, MjjHistogram & histToFit, int nFluctuations, bool throwFromData) 
{
  int successes = nFluctuations+1;
  int total = nFluctuations+1;

  TH1D background((TH1D) histToFit.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",background.GetName()));
  background.SetName(bkgname); 
  TH1D weights((TH1D) histToFit.GetWeightsHistogram());
  TString weightname(Form("%s_internal_weights",weights.GetName()));
  weights.SetName(weightname);

  nominal.RestoreParameterDefaults(); alternate.RestoreParameterDefaults();
  bool didImportantFitWork = Fit(histToFit,nominal);
  vector<double> storeImportantCovarianceMatrix = fLatestCovarianceMatrix;
  vector<double> correctFitParameters = nominal.GetCurrentParameterValues();

  if (!didImportantFitWork) background.Fatal("MjjFitter::FitAndGetBkgWithDiffErr","Main fit failed!");

  nominal.MakeHistFromFunction(&background); 

  // Use MjjHistogram to get proper fluctuations.
  MjjHistogram bkgTemplate(&background);
  bkgTemplate.SetEffectiveFromBasicAndWeights(&weights);

  // Beginning of calculation of error bars on background.
  ///////////////////////////////////////////////////////////////////////////////

  // This construction seems complicated but it's a good way to rearrange data 
  // from ordering by fluctuation to ordering by bin
  fStoreBinContentVectors.clear();
  for (int i=1; i<=background.GetNbinsX(); i++) {
    vector<double> veccontent;
    veccontent.clear();
    fStoreBinContentVectors.push_back(veccontent);
  }


  // Create histograms for pseudoexperiments
  TH1D fluctData(background);
  TString fluctdataname(Form("%s_internal_pseudodata",fluctData.GetName()));
  fluctData.SetName(fluctdataname);

  fluctData.Clear();
  for (int i = 0; i<nFluctuations; i++) {

    std::cout << "Doing new error on PE #" << i << std::endl;
    std::cout << "Using throwFromData="<<throwFromData << std::endl;

    if (throwFromData) histToFit.PoissonFluctuateBinByBin(&fluctData);
    else bkgTemplate.PoissonFluctuateBinByBin(&fluctData);
    MjjHistogram fluctDataHist(&fluctData);
    MjjHistogram fluctBkgHistNom = FitAndGetBkgWithNoErr(nominal,fluctDataHist);
    bool fit1 = fLatestFitStatus;
    MjjHistogram fluctBkgHistVar = FitAndGetBkgWithNoErr(alternate,fluctDataHist);
    // If either fit fails don't count this.
    if (fit1==false || fLatestFitStatus==false) {
      nFluctuations++;
      successes--;
      continue;
    }
    else{
	    if (fluctBkgHistNom.GetHistogram().Integral() <= 0. || fluctBkgHistVar.GetHistogram().Integral() <= 0.){
		    nFluctuations++;
		    successes--;
		    continue;
	    }
    } 

    // Store difference between two fits in vector<double> corresponding to this bin
    for (int j=1; j<=fluctBkgHistNom.GetHistogram().GetNbinsX(); j++) 
      fStoreBinContentVectors.at(j-1).push_back(fluctBkgHistNom.GetHistogram().GetBinContent(j) - fluctBkgHistVar.GetHistogram().GetBinContent(j));


  }

  double RMSOfThisBin;
  for (int i=1; i<=background.GetNbinsX(); i++) {
    if (fStoreBinContentVectors.at(i-1).size() == 0) background.SetBinError(i,sqrt(background.GetBinContent(i)));
    else {
      RMSOfThisBin = GetRMS(fStoreBinContentVectors.at(i-1));
      background.SetBinError(i,RMSOfThisBin);
    }
  }
  ///////////////////////////////////////////////////////////////////////////////
  // End of calculation of error bars on background.

  // Make an MjjHistogram
  MjjHistogram theResult(&background);
  theResult.SetEffectiveFromBasicAndWeights(&weights);

  // Restore values from primary fit
  nominal.SetCurrentParameterValues(correctFitParameters);
  fLatestFitStatus = didImportantFitWork;  // Keep result of main fit
  fLatestCovarianceMatrix = storeImportantCovarianceMatrix; // Keep result of main fit
  fFitSuccessRate = (double)successes/(double)total;

  return theResult;

}

// ---------------------------------------------------------
MjjHistogram MjjFitter::FitAndGetBkgWithConfidenceBand(MjjFitFunction & fitFunction, MjjHistogram & histToFit) 
{

  fitFunction.RestoreParameterDefaults();
  Fit(histToFit,fitFunction);

  TF1 * fittedFunction = fitFunction.GetFitFunction();

  TH1D data((TH1D) histToFit.GetHistogram());
  TString dataname(Form("%s_internal_bkg",data.GetName()));
  data.SetName(dataname);
  TH1D weights((TH1D) histToFit.GetWeightsHistogram());
  TString weightname(Form("%s_internal_weights",weights.GetName()));
  weights.SetName(weightname);

  double * covarianceMatrix = new double [fittedFunction->GetNpar()*fittedFunction->GetNpar()];
  fMinuitMinimizer->GetCovMatrix(covarianceMatrix);

  std::cout << "Using xmin, xmax: " << fitFunction.GetMinXVal() << " " << fitFunction.GetMaxXVal() << std::endl;
  TH1D backgroundWithErrors(*GetConfidenceBand(&data, fittedFunction, covarianceMatrix, fitFunction.GetMinXVal(), fitFunction.GetMaxXVal(), 0.683));
  MjjHistogram result(&backgroundWithErrors);
  result.SetEffectiveFromBasicAndWeights(&weights);

  fFitSuccessRate = (double) fLatestFitStatus;
  return result;

}

// ---------------------------------------------------------
void MjjFitter::StoreLatestFitMatrices(int dimensionOfMatrix) 
{

  fLatestCovarianceMatrix.clear();
  fLatestHessianMatrix.clear();

  double hessElem [dimensionOfMatrix*dimensionOfMatrix];
  fMinuitMinimizer->GetHessianMatrix(hessElem);

  // Store items of covariance matrix in the order:
  // Left to right, starting on the top row, then second, etc.
  for (int i=0; i<dimensionOfMatrix; i++) {
    for (int j=0; j<dimensionOfMatrix; j++) {
      double thisElement = fMinuitMinimizer->CovMatrix(i,j);
      fLatestCovarianceMatrix.push_back(thisElement);
      fLatestHessianMatrix.push_back(hessElem[i*dimensionOfMatrix + j]);
    }
  }

  return;

}

// ---------------------------------------------------------
TH1D * MjjFitter::GetConfidenceBand(TH1D * data, TF1 * fittedFunction,  double * covarianceMatrix, double xmin, double xmax, double CL) 
{

  int npar = fittedFunction->GetNpar();
  double * grad = new double [npar];
  double x[1];
  int binfirst, binlast;
  if (xmin < 0) binfirst = data->GetXaxis()->GetFirst();
  else binfirst = data->FindBin(xmin+1);
  if (xmax < 0) binlast = data->GetXaxis()->GetLast();
  else binlast = data->FindBin(xmax-1);
  double t = TMath::StudentQuantile(0.5 + CL/2, fittedFunction->GetNDF());
  double chidf = TMath::Sqrt(fittedFunction->GetChisquare()/fittedFunction->GetNDF());

  TH1D * answer = (TH1D *) data->Clone();

  for (int bin=1; bin < answer->GetNbinsX()+1; bin++) {
    if (bin>binfirst-1 && bin<binlast+1) {
      x[0] = data->GetXaxis()->GetBinCenter(bin);
      fittedFunction->GradientPar(x,grad);
      double sum = 0;
      for (int i=0; i<npar; i++) {
        for (int j=0; j<npar; j++) {
          sum += covarianceMatrix[i*npar+j]*grad[i]*grad[j];
        }
      }
      double c = sqrt(sum);
      answer->SetBinContent(bin,fittedFunction->Eval(x[0])*answer->GetBinWidth(bin));
      answer->SetBinError(bin,c*t*chidf*answer->GetBinWidth(bin));
    } else {
      answer->SetBinContent(bin,0);
      answer->SetBinError(bin,0);
    }
  }
  delete [] grad;
  return answer;
}

// ---------------------------------------------------------

