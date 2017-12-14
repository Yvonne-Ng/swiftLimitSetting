#ifndef MJJFITTER_H
#define MJJFITTER_H

/*!
 * \class MjjFitter
 * \brief A class for fitting spectra using MjjHistogram, MjjFitFunction
 * \author Katherine Pachal
 * \date 2013
 * 
 * This class uses Minuit2Minimizer to fit a given 
 * MjjFitFunction to a given MjjHistogram and retrieve an
 * estimate of the error. Four error estimates are available:
 * - No error. The output histogram will have bins of error 0.
 * - MC error. This is the simple (toy) model of errors, 
 *   where the uncertainty on each bin is simply sqrt(bin content).
 * - Data error. The error bars are calculated using 
 *   pseudoexperiments. See method description for details.
 * - Confidence band. The error bars are calculated from
 *   the covariance matrix of the fit.
 */

// ---------------------------------------------------------

#include "Bayesian/MjjHistogram.h"
#include "Bayesian/MjjFitFunction.h"
#include "Bayesian/MathFunctions.h"
#include "Bayesian/MjjLogLikelihoodTest.h"

#include <cmath>
#include <climits>
#include <math.h>

#include <TMath.h>
#include <TRandom3.h>
#include <TFile.h>
#include <TH1D.h>
#include <TF1.h>
#include <TMinuit.h>

#include "Minuit2/Minuit2Minimizer.h"
#include "Math/Functor.h"

using namespace std;

// ---------------------------------------------------------
class MjjFitter
{

   public:
 
      /** \name Constructors and destructors */
      /** @{ */

      /**
       * The default constructor. */
      MjjFitter();

      /**
       * The default destructor. */
      ~MjjFitter();

      /** @} */
      /** \name Member functions (get) */
      /** @{ */
  
      /**
       * Check status of fit just performed.
       * If using data errors, this is the important
       * fit (real data). 
       * @return true if fit succeeded. */
      bool GetLatestFitStatus() 
          { return fLatestFitStatus; };

      /**
       * Get covariance matrix of fit just performed.
       * If using data errors, this is the important
       * fit (real data). Vector of values correspond
       * to top row right to left, second row right to
       * left, etc. 
       * @return Vector of covariance matrix elements. */
      vector<double> GetLatestFitCovarianceMatrix() 
          { return fLatestCovarianceMatrix; };

      /**
       * Get Hessian matrix of fit just performed.
       * If using data errors, this is the important
       * fit (real data). Vector of values correspond
       * to top row right to left, second row right to
       * left, etc. 
       * @return Vector of Hessian matrix elements. */
      vector<double> GetLatestFitHessianMatrix() 
          { return fLatestHessianMatrix; };


      /**
       * When using data errors, check the fraction of 
       * all fits (to data and to pseudoexperiments) which
       * succeeded. When using other errors, this should
       * be 1 for a successful fit and 0 for a failed fit.
       * @return Fraction of all fits in previously
       * performed method which succeeded. */
      double GetLatestFitSuccessRate() 
          { return fFitSuccessRate; };

      /**
       * Retrieve the vectors corresponding to the bin
       * content from the fit to each pseudoexperiment.
       * Useful development tool but not of obvious 
       * interest to users.
       * @return Vector of vectors; one vector<double>
       * for each bin. The values are the content
       * of that bin after fitting each pseudoexperiment. */
      vector<vector<double> > getBinContentVectors() 
          { return fStoreBinContentVectors; };

      const double * GetCurrentMinuitValues()
          { return fMinuitMinimizer->X(); }
 

      /** @} */
      /** \name Member functions (set) */
      /** @{ */

      /**
       * Set print level for Minuit minimizer. Range is from
       * -1 (no output) through 0 (minimal output) to
       * 3 (debug level output). Default is -1.
       * @param printLevel Level of output detail. */
      void SetPrintLevel(int printLevel)
          { fPrintLevel = printLevel; 
            fMinuitMinimizer->SetPrintLevel(fPrintLevel); };

      /**
       * Set signal template to be used in fit.
       * Automatically sets flag to activate
       * signal template. Any fit will now compare
       * the data to the function specified 
       * plus this template normalised to the 
       * value of an additional signal parameter
       * added the the Minuit2Minimizer.
       * @param sigTemplate The shape of signal to be
       * added to the function by the fitter. */
      void SetSignalTemplate(TH1D * sigTemplate); 

      void SetMinuitVariable(int variable, double value)
          { fMinuitMinimizer->SetVariableValue(variable,value); };

      /**
       * Activate or deactivate the use of the signal
       * template in the fit. Should be called with
       * true to use the template and false otherwise.
       * @param useSig Use or do not use signal in fit. */
      void ActivateSignalTemplate(bool useSig) 
          { fFitWithSignal = useSig; };

      /** @} */
      /** \name Member functions (fitting methods) */
      /** @{ */

      /**
       * Fit the given histogram with the given MjjFitFunction.
       * The fit can then be retrieved via the MjjFitFunction.
       * @param mjjHistogram The histogram to fit.
       * @param mjjFitFunction The function to use in the fit.
       * @return true if fit succeeded, false if it failed. */
      bool Fit(MjjHistogram & mjjHistogram, MjjFitFunction & mjjFitFunction);

      /**
       * Fit the given histogram with the given MjjFitFunction
       * and return an MjjHistogram corresponding to the fit result.
       * Error bars in this histogram are zero. Fast method.
       * @param fitFunction The function to use in the fit.
       * @param histToFit The MjjHistogram to fit.
       * @return An MjjHistogram with bin contents matching the fitted function. */
      MjjHistogram FitAndGetBkgWithNoErr(MjjFitFunction & fitFunction,MjjHistogram & histToFit);

      /**
       * Fit the given histogram with the given MjjFitFunction
       * and return an MjjHistogram corresponding to the fit result.
       * Error bars in this histogram are the square root of the bin
       * content. Fast method.
       * @param fitFunction The function to use in the fit.
       * @param histToFit The MjjHistogram to fit.
       * @return An MjjHistogram with bin contents matching the fitted function. */
      MjjHistogram FitAndGetBkgWithMCErr(MjjFitFunction & fitFunction,MjjHistogram & histToFit);

      /**
       * Fit the given histogram with the given MjjFitFunction
       * and return an MjjHistogram corresponding to the fit result.
       * Error bars in this histogram are derived from pseudoexperiments.
       * nFluctuations pseudoexperiments are performed, each is fit 
       * independently, and a histogram is derived from the function.
       * The standard deviation of these fit values in each bin is 
       * then used to set an error band on that bin in the final 
       * histogram. Slower method.
       * @param fitFunction The function to use in the fit.
       * @param histToFit The MjjHistogram to fit.
       * @param nFluctuations Number of pseudoexperiments to use.
       * @return An MjjHistogram with bin contents matching the fitted function. */
      MjjHistogram FitAndGetBkgWithDataErr(MjjFitFunction & fitFunction,MjjHistogram & histToFit, int nFluctuations=1000);

      MjjHistogram FitAndGetBkgWithFitDiffErr(MjjFitFunction & nominal, MjjFitFunction & alternate, MjjHistogram & histToFit, int nFluctuations=1000, bool throwFromData=false);

      /**
       * Fit the given histogram with the given MjjFitFunction
       * and return an MjjHistogram corresponding to the fit result.
       * Error bars in this histogram are calculated as a confidence
       * interval on the function using the same formula found in 
       * ROOT's TVirtualFitter::GetConfidenceIntervals. Only 
       * reliable if the covariance matrix is correctly calculated.
       * If you can rely on the output of Minuit and Hesse, then
       * this is a fast method.
       * @param fitFunction The function to use in the fit.
       * @param histToFit The MjjHistogram to fit.
       * @return An MjjHistogram with bin contents matching the fitted function. */
      MjjHistogram FitAndGetBkgWithConfidenceBand(MjjFitFunction & fitFunction,MjjHistogram & histToFit);

      /** 
       * Defines likelihood calculation used internally 
       * by Minuit. 
       * @param params Array of parameter values for calculation.
       * @return Log Likelihood for those parameter values. */
      double LikeMin(const double *params);

      /** @} */

   private:

      /** 
       * Copy results of covariance and Hessian matrices
       * from latest fit into storage arrays.
       * @param Dimension of one edge of matrix. */
      void StoreLatestFitMatrices(int dimensionOfMatrix);

      /** 
       * Calculate confidence band for the specified
       * confidence interval and range, using the data 
       * histogram, the covariance matrix, and the (already 
       * fitted) function.  Returns histogram with errors set
       * by confidence band. 
       * @param data Histogram defining bin structure
       * @param fittedFunction Function already fitted to shape
       * @param covarianceMatrix Covariance matrix as an array
       * of doubles found during fit 
       * @param xmin Minimum x-value for calculation 
       * @param xmax Maximum x-value for calculation
       * @param CL Confidence level for band to represent
       * @return A histogram with bin values from the function
       * and bin errors from the confidence band calculation. */
      TH1D * GetConfidenceBand(TH1D * data, TF1 * fittedFunction, double * covarianceMatrix, double xmin=-1, double xmax=-1, double CL=0.683);

      /**
       * Calculates log(Poisson) in fewer steps to retain
       * sensitivity to very large numbers.
       * For use in LikeMin. */
      double SimpleLogPoisson(double x, double par);

      /** 
       * Call Minuit with likelihood, parameters, etc
       * already defined.
       * @return Success or failure. */
      bool MinuitMLFit();

      /** 
       * Status of latest important fit. */
      bool fLatestFitStatus;

      /** 
       * A container of components of covariance matrix
       * from latest important fit. */
      vector<double> fLatestCovarianceMatrix;

      /** 
       * A container of components of Hessian matrix
       * from latest important fit. */
      vector<double> fLatestHessianMatrix;

      /** 
       * Percentage of fits in latest fitting procedure
       * which succeeded. If just one fit, 0 or 1. */
      double fFitSuccessRate;

      /** 
       * A container of vectors of bin contents used
       * for calculating errors via pseudoexperiments. */
      vector<vector<double> > fStoreBinContentVectors;

      /** 
       * Specifies whether or not to use signal in fit. */
      bool fFitWithSignal;

      /** 
       * Index of fit parameter which corresponds to signal. */
      int fSignalParameterIndex;

      /** 
       * Template used for fits with signal. */
      TH1D * fSignalTemplate;

      /** 
       * The minimiser object. */
      ROOT::Minuit2::Minuit2Minimizer * fMinuitMinimizer;

      /** 
       * The level of print statements from the minimizer. */
      int fPrintLevel;

      /** 
       * First bin to be included in fit. */
      int fStartBin;

      /** 
       * Last bin to be included in fit. */
      int fStopBin;

      /** 
       * The MjjFitFunction to be used in the fit. */
      MjjFitFunction fMjjFitFunction;

      /** 
       * The TF1 object belonging to the fit function. */
      TF1 * fFitFunction;

      /** 
       * The basic histogram (in event numbers) to be fit. */
      TH1D fBasicHistogramToFit;

      /** 
       * The effective histogram (unweighted to handle
       * true statistics) to be fit */
      TH1D fEffectiveHistogramToFit;

      /** 
       * The histogram of effective weights of the data. */ 
      TH1D fWeightsHistogram;

      /** 
       * The histogram of effective weights of the data. */
      TGraph fEffBinCenters;

      /** 
       * Step size to be used by Minuit parameters. */
      double fStepSize;

      /** 
       * How many times has this fit been attempted so far? */
      int fRetry;

};

#endif
