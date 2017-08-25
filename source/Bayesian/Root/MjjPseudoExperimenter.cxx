// ---------------------------------------------------------

#include "Bayesian/MjjPseudoExperimenter.h"

// ---------------------------------------------------------
MjjPseudoExperimenter::MjjPseudoExperimenter() 
{
  fFitSuccessRate = 0;
}

// ---------------------------------------------------------
MjjPseudoExperimenter::~MjjPseudoExperimenter() 
{

}

// ---------------------------------------------------------
MjjStatisticsBundle MjjPseudoExperimenter::GetPseudoExperimentStatsOnHistogram(MjjHistogram & templateHist, MjjHistogram & observedHist, MjjStatisticalTest * theStatTest, int firstBinToUse, int lastBinToUse, int nExperiments)
{

  vector<MjjStatisticalTest*> theStatisticalTests;
  theStatisticalTests.clear();
  theStatisticalTests.push_back(theStatTest);

  vector<MjjStatisticsBundle> theVectorOfStatsBundles = GetPseudoExperimentStatsOnHistogram
        (templateHist, observedHist, theStatisticalTests, firstBinToUse, lastBinToUse, nExperiments);

  MjjStatisticsBundle theStatsBundle = theVectorOfStatsBundles.at(0);

  return theStatsBundle;

}

// ---------------------------------------------------------
vector<MjjStatisticsBundle> MjjPseudoExperimenter::GetPseudoExperimentStatsOnHistogram(MjjHistogram & templateHist, MjjHistogram & observedHist, vector<MjjStatisticalTest*> theStatTests, int firstBinToUse, int lastBinToUse, int nExperiments)
{

  int nPseudoExperiments = nExperiments;

  // Clear info from last iteration
  vector<double> originalStats;
  originalStats.clear();
  vector<vector<double> > originalFurtherInformation;
  originalFurtherInformation.clear();

  vector<vector<double> > StatisticTestResults;
  StatisticTestResults.clear();
  vector<vector<vector<double> > > StatisticFurtherInformation;
  StatisticFurtherInformation.clear();

  for (unsigned int i=0; i<theStatTests.size(); i++) {  

    // Get basic statistic between templateHist, observedHist
    double thisOriginalStat = theStatTests.at(i)->DoTest(observedHist, templateHist, firstBinToUse, lastBinToUse);
    originalStats.push_back(thisOriginalStat);
    vector<double> thisOriginalFurtherInformation = theStatTests.at(i)->GetFurtherInformation();
    originalFurtherInformation.push_back(thisOriginalFurtherInformation);

    // Make empty vectors to hold statistical information from pseudoexperiments
    vector<double> theseStatResultsFromPseudoexperiments;
    theseStatResultsFromPseudoexperiments.clear();
    StatisticTestResults.push_back(theseStatResultsFromPseudoexperiments);
    vector<vector<double> > theseFurtherInfosFromPseudoexperiments;
    theseFurtherInfosFromPseudoexperiments.clear();
    StatisticFurtherInformation.push_back(theseFurtherInfosFromPseudoexperiments);
  }

  // Create histograms for pseudoexperiments
  TH1D h_bkg((TH1D) templateHist.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",h_bkg.GetName()));
  h_bkg.SetName(bkgname);
  TH1D h_pseudo((TH1D) templateHist.GetHistogram());
  TString pseudoname(Form("%s_internal_pseudo",h_pseudo.GetName()));
  h_pseudo.SetName(pseudoname);

  h_pseudo.Clear();

  if (lastBinToUse > h_bkg.GetNbinsX()+1) lastBinToUse = h_bkg.GetNbinsX()+1;

  for (int pseudoexperiment = 1; pseudoexperiment < nPseudoExperiments+1; pseudoexperiment++) {

    std::cout << "on PE " << pseudoexperiment << std::endl;

    // Independently fluctuate each bin and store new value in h_pseudo
    templateHist.PoissonFluctuateBinByBin(&h_pseudo);
    MjjHistogram pseudoHist(&h_pseudo);

    vector<double> localVectorOfStatistics;
    localVectorOfStatistics.clear();
    vector<vector<double> > localVectorOfFurtherInformation;
    localVectorOfFurtherInformation.clear();

    bool skip=false;
    for (unsigned int i=0; i<theStatTests.size(); i++) {
      double statisticOfFluctuatedToControlHist = theStatTests.at(i)->DoTest(pseudoHist,templateHist,firstBinToUse,lastBinToUse);
      vector<double> furtherInfoOfFluctuatedToControlHist = theStatTests.at(i)->GetFurtherInformation();

      // Protect against unphysical values: if any test returs nan or inf, skip pseudoexperiment
      if (std::isnan(statisticOfFluctuatedToControlHist) || std::isinf(statisticOfFluctuatedToControlHist)) {skip=true; std::cout << "failed in test " << i << std::endl; }

      localVectorOfStatistics.push_back(statisticOfFluctuatedToControlHist);
      localVectorOfFurtherInformation.push_back(furtherInfoOfFluctuatedToControlHist);

    }

    if (skip) {
      pseudoexperiment--;
      continue;
    }

    // Do this in a separate loop because first needed to check that 
    // no returned statistic is invalid
    for (unsigned int i=0; i<theStatTests.size(); i++) {
      StatisticTestResults.at(i).push_back(localVectorOfStatistics.at(i));
      StatisticFurtherInformation.at(i).push_back(localVectorOfFurtherInformation.at(i));
    }
  }

  // There is no fit here: make sure fit param histograms don't exist
  // just in case user tries to get them
  fParameterHistsFromLatestPseudoexperiments.clear();

  // Need an MjjStatisticsBundle for each test.
  vector<MjjStatisticsBundle> resultVector;
  resultVector.clear();

  // For each test,
  // store all results in an MjjStatisticsBundle
  for (unsigned int i=0; i<theStatTests.size(); i++) {
    TH1D statisticsHist(MakeHistoFromStats(StatisticTestResults.at(i)));
    TString thisname(Form("%s_%d", statisticsHist.GetName(),i));
    statisticsHist.SetName(thisname);
    MjjStatisticsBundle result;
    result.originalStatistic = originalStats.at(i);
    result.originalFurtherInformation = originalFurtherInformation.at(i);
    result.statisticsFromPseudoexperiments = StatisticTestResults.at(i);
    result.statisticsFromPseudoexperimentsHist = statisticsHist;
    result.furtherInformationFromPseudoexperiments = StatisticFurtherInformation.at(i);
    resultVector.push_back(result);
  }

  return resultVector;

}

// ---------------------------------------------------------
MjjStatisticsBundle MjjPseudoExperimenter::GetPseudoExperimentStatsOnFunction(MjjFitFunction & functionToFit, MjjHistogram & observedHist, MjjStatisticalTest * theStatTest, int firstBinToUse, int lastBinToUse, int nExperiments)
{

  vector<MjjStatisticalTest*> theStatisticalTests;
  theStatisticalTests.clear();
  theStatisticalTests.push_back(theStatTest);

  vector<MjjStatisticsBundle> theVectorOfStatsBundles = GetPseudoExperimentStatsOnFunction
        (functionToFit, observedHist, theStatisticalTests, firstBinToUse, lastBinToUse, nExperiments);

  MjjStatisticsBundle theStatsBundle = theVectorOfStatsBundles.at(0);

  return theStatsBundle;
  
}

// ---------------------------------------------------------
vector<MjjStatisticsBundle> MjjPseudoExperimenter::GetPseudoExperimentStatsOnFunction(MjjFitFunction & functionToFit, MjjHistogram & observedHist, vector<MjjStatisticalTest*> theStatTests, int firstBinToUse, int lastBinToUse, int nExperiments)
{

  // Get parameters
  int nPseudoExperiments = nExperiments;

  int successes = nExperiments+1;
  int total = nExperiments+1;

  // Clear info from last iteration
  vector<double> originalStats;
  originalStats.clear();
  vector<vector<double> > originalFurtherInformation;
  originalFurtherInformation.clear();

  vector<vector<double> > StatisticTestResults;
  StatisticTestResults.clear();
  vector<vector<vector<double> > > StatisticFurtherInformation;
  StatisticFurtherInformation.clear();

  // Make vectors to store fit parameters for each
  vector<vector<double> > parameterVectors;
  parameterVectors.clear();
  for (int i=0; i<functionToFit.GetNParams(); i++) {
    vector<double> veccontent;
    veccontent.clear();
    parameterVectors.push_back(veccontent);
  }

  // Want a quiet fitter because there are so many pseudoexperiments
  MjjFitter thePseudoExpFitter;

  TH1D h_observed((TH1D) observedHist.GetHistogram());
  TString obsname(Form("%s_internal_obs",h_observed.GetName()));
  h_observed.SetName(obsname);
  TH1D weights((TH1D) observedHist.GetWeightsHistogram());

  // Fit function to data and derive a background histogram
  MjjHistogram templateBkg = thePseudoExpFitter.FitAndGetBkgWithMCErr(functionToFit,observedHist);
  templateBkg.SetEffectiveFromBasicAndWeights(&weights);

  // Fix last bin to within size of histo
  if (lastBinToUse > h_observed.GetNbinsX()+1) lastBinToUse = h_observed.GetNbinsX()+1;

  for (unsigned int i=0; i<theStatTests.size(); i++) {

    // Get basic statistic between templateHist, observedHist
    double thisOriginalStat = theStatTests.at(i)->DoTest(templateBkg, observedHist, firstBinToUse, lastBinToUse);
    originalStats.push_back(thisOriginalStat);
    vector<double> thisOriginalFurtherInformation = theStatTests.at(i)->GetFurtherInformation();
    originalFurtherInformation.push_back(thisOriginalFurtherInformation);

    // Make empty vectors to hold statistical information from pseudoexperiments
    vector<double> theseStatResultsFromPseudoexperiments;
    theseStatResultsFromPseudoexperiments.clear();
    StatisticTestResults.push_back(theseStatResultsFromPseudoexperiments);
    vector<vector<double> > theseFurtherInfosFromPseudoexperiments;
    theseFurtherInfosFromPseudoexperiments.clear();
    StatisticFurtherInformation.push_back(theseFurtherInfosFromPseudoexperiments);

  }

  // Create histograms for pseudoexperiments
  TH1D h_bkg((TH1D) templateBkg.GetHistogram());
  TString bkgname(Form("%s_internal_bkg",h_bkg.GetName()));
  h_bkg.SetName(bkgname);
  TH1D h_pseudo((TH1D) templateBkg.GetHistogram());
  TString pseudoname(Form("%s_internal_pseudo",h_pseudo.GetName()));
  h_pseudo.SetName(pseudoname);

  h_pseudo.Clear();

  // Now do the pseudoexperiments!
  for (int pseudoexperiment = 1; pseudoexperiment <= nPseudoExperiments; pseudoexperiment++) {

    // Independently fluctuate each bin and store new value in h_pseudo
    templateBkg.PoissonFluctuateBinByBin(&h_pseudo);
    MjjHistogram pseudoHist(&h_pseudo);

    // Fit to hist and retrieve histogram form of fitted function
    MjjHistogram templateHist = thePseudoExpFitter.FitAndGetBkgWithMCErr(functionToFit,pseudoHist);
    templateHist.SetEffectiveFromBasicAndWeights(&weights);
    bool didFitWork = thePseudoExpFitter.GetLatestFitStatus();

    // Protect against failed fits
    if(!didFitWork) {
      pseudoexperiment--;
      total++;
      continue;
    }

    vector<double> localVectorOfStatistics;
    localVectorOfStatistics.clear();
    vector<vector<double> > localVectorOfFurtherInformation;
    localVectorOfFurtherInformation.clear();

    bool skip=false;
    for (unsigned int i=0; i<theStatTests.size(); i++) {
      double statisticOfFluctuatedToControlHist = theStatTests.at(i)->DoTest(templateHist,pseudoHist,firstBinToUse,lastBinToUse);
      vector<double> furtherInfoOfFluctuatedToControlHist = theStatTests.at(i)->GetFurtherInformation();

      // Record if there are unphysical values
      if (std::isnan(statisticOfFluctuatedToControlHist) || std::isinf(statisticOfFluctuatedToControlHist)) skip=true;

      localVectorOfStatistics.push_back(statisticOfFluctuatedToControlHist);
      localVectorOfFurtherInformation.push_back(furtherInfoOfFluctuatedToControlHist);
    }
    // Protect against unphysical values
    if (skip) {
      pseudoexperiment--;
      total++;
      successes++;
      continue;
    }

    // Successful fit and pseudoexperiment! Store parameter values:
    vector<double> fittedParameters = functionToFit.GetCurrentParameterValues();
    for (int i=0; i<functionToFit.GetNParams(); i++) {
      parameterVectors.at(i).push_back(fittedParameters.at(i));
    }

    // Do this in a separate loop because first needed to check that 
    // no returned statistic is invalid
    for (unsigned int i=0; i<theStatTests.size(); i++) {
      StatisticTestResults.at(i).push_back(localVectorOfStatistics.at(i)); 
      StatisticFurtherInformation.at(i).push_back(localVectorOfFurtherInformation.at(i)); 
    }

  }

  // Make histograms of parameters from fit
  fParameterHistsFromLatestPseudoexperiments.clear();
  for (int i=0; i<functionToFit.GetNParams(); i++) {
    TH1D paramHist(MakeHistoFromStats(parameterVectors.at(i)));
    TString thisname(Form("param_%s_%d", paramHist.GetName(),i));
    paramHist.SetName(thisname);
    fParameterHistsFromLatestPseudoexperiments.push_back(paramHist);
  }

  // Need an MjjStatisticsBundle for each test.
  vector<MjjStatisticsBundle> resultVector;
  resultVector.clear();

  // For each test,
  // store all results in an MjjStatisticsBundle
  for (unsigned int i=0; i<theStatTests.size(); i++) {
    TH1D statisticsHist(MakeHistoFromStats(StatisticTestResults.at(i)));
    TString thisname(Form("%s_%d", statisticsHist.GetName(),i));
    statisticsHist.SetName(thisname);
    MjjStatisticsBundle result;
    result.originalStatistic = originalStats.at(i);
    result.originalFurtherInformation = originalFurtherInformation.at(i);
    result.statisticsFromPseudoexperiments = StatisticTestResults.at(i);
    result.statisticsFromPseudoexperimentsHist = statisticsHist;
    result.furtherInformationFromPseudoexperiments = StatisticFurtherInformation.at(i);
    resultVector.push_back(result);
  }
  
  fFitSuccessRate = (double) successes/(double) total;
  

  return resultVector;

}

// ---------------------------------------------------------

