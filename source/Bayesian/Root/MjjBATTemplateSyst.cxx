// ---------------------------------------------------------

#include "Bayesian/MjjBATTemplateSyst.h"

// ---------------------------------------------------------
MjjBATTemplateSyst::MjjBATTemplateSyst(bool isScale)
{

  fIsScale = isScale;

}

// ---------------------------------------------------------
MjjBATTemplateSyst::~MjjBATTemplateSyst() 
{

}

// ---------------------------------------------------------
vector<double> MjjBATTemplateSyst::GetAdjustment(double param) 
{

  vector<double> bins;

  double lowBinVal,highBinVal,newVal = 0;

  for (unsigned int i=0; i<(fCorrespondingSigmas.size()-1); i++) {
    if (param > fCorrespondingSigmas.at(i+1)) continue;

    for (int bin=0; bin<fNBinsInSpectra; bin++) {
      lowBinVal = fDiscreteSpectra.at(i).GetBinContent(bin);
      highBinVal = fDiscreteSpectra.at(i+1).GetBinContent(bin);
      newVal = (highBinVal-lowBinVal)/(fCorrespondingSigmas.at(i+1)-fCorrespondingSigmas.at(i)) 
               * (param-fCorrespondingSigmas.at(i)) + lowBinVal;
      bins.push_back(newVal);
    }

    break;
  }

  return bins;


}

// ---------------------------------------------------------
double MjjBATTemplateSyst::GetBinAdjustment(int bin, double param) 
{

  double lowBinVal,highBinVal,newVal = 0;

  for (unsigned int i=0; i<(fCorrespondingSigmas.size()-1); i++) {
    if (param > fCorrespondingSigmas.at(i+1)) continue;
    lowBinVal = fDiscreteSpectra.at(i).GetBinContent(bin);
    highBinVal = fDiscreteSpectra.at(i+1).GetBinContent(bin);

    newVal = (highBinVal-lowBinVal)/(fCorrespondingSigmas.at(i+1)-fCorrespondingSigmas.at(i)) 
             * (param-fCorrespondingSigmas.at(i)) + lowBinVal;

    break;
  }

  return newVal;

}

// ------------------------------------------
void MjjBATTemplateSyst::SetSpectra(vector<std::pair<double,TH1D*> > sigmasAndSpectra) 
{

  if (fDiscreteSpectra.size() > 0 || fCorrespondingSigmas.size() > 0 ) 
          std::cout << "Caution: overwriting old spectra" << std::endl;
  fDiscreteSpectra.clear();
  fCorrespondingSigmas.clear();

  std::sort(sigmasAndSpectra.begin(), sigmasAndSpectra.end(), sort_pairs_TH1D());

  for (unsigned int i=0; i<sigmasAndSpectra.size(); i++) {
    if (sigmasAndSpectra.at(i).first==0) {
      fNBinsInSpectra = sigmasAndSpectra.at(i).second->GetNbinsX()+2;
      fOriginalIndex = i;
      fBinStructure = *sigmasAndSpectra.at(i).second->GetXaxis()->GetXbins();
    }
  }

  double integralToMatch = sigmasAndSpectra.at(fOriginalIndex).second->Integral();
  TH1D * holdNormalizedOriginal = (TH1D*) sigmasAndSpectra.at(fOriginalIndex).second->Clone();
  holdNormalizedOriginal->SetName("normorig_holder");
  for (int j=0; j<holdNormalizedOriginal->GetNbinsX()+2; j++) {
    double bincontent = holdNormalizedOriginal->GetBinContent(j);
    holdNormalizedOriginal->SetBinContent(j,bincontent/integralToMatch);
  }

  for (unsigned int i=0; i<sigmasAndSpectra.size(); i++) {
    TH1D thisHistogram(*sigmasAndSpectra.at(i).second);
    std::string name(thisHistogram.GetName());
    thisHistogram.SetName(Form((name+"_%d").c_str(),i));
    for (int j=0; j<thisHistogram.GetNbinsX()+1; j++) {
      double bincontent = thisHistogram.GetBinContent(j);
      thisHistogram.SetBinContent(j,bincontent/integralToMatch - holdNormalizedOriginal->GetBinContent(j));
      thisHistogram.SetBinError(j,0.);
    }
    fCorrespondingSigmas.push_back(sigmasAndSpectra.at(i).first);
    fDiscreteSpectra.push_back(thisHistogram);
  }

  delete holdNormalizedOriginal;

  return;

}

// ------------------------------------------

