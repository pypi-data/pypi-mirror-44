/********************************************************************
 *  Copyright (C) 2016 by Federico Marulli and Alfonso Veropalumbo  *
 *  federico.marulli3@unibo.it                                      *
 *                                                                  *
 *  This program is free software; you can redistribute it and/or   * 
 *  modify it under the terms of the GNU General Public License as  *
 *  published by the Free Software Foundation; either version 2 of  *
 *  the License, or (at your option) any later version.             *
 *                                                                  *
 *  This program is distributed in the hope that it will be useful, *
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of  *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   *
 *  GNU General Public License for more details.                    *
 *                                                                  *
 *  You should have received a copy of the GNU General Public       *
 *  License along with this program; if not, write to the Free      *
 *  Software Foundation, Inc.,                                      *
 *  59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.       *
 ********************************************************************/

/**
 *  @file
 *  Modelling/TwoPointCorrelation/Modelling_TwoPointCorrelation_multipoles.cpp
 *
 *  @brief Methods of the class
 *  Modelling_TwoPointCorrelation_multipoles
 *
 *  This file contains the implementation of the methods of the class
 *  Modelling_TwoPointCorrelation_multipoles, used to model the
 *  multipoles of the two-point correlation function
 *
 *  @authors Federico Marulli, Alfonso Veropalumbo
 *
 *  @authors federico.marulli3@unbo.it, alfonso.veropalumbo@unibo.it
 */


#include "Data1D.h"
#include "Modelling_TwoPointCorrelation_multipoles.h"

using namespace std;

using namespace cbl;


// ============================================================================================


cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::Modelling_TwoPointCorrelation_multipoles (const std::shared_ptr<cbl::measure::twopt::TwoPointCorrelation> twop)
  : Modelling_TwoPointCorrelation1D_monopole(twop), m_nmultipoles(3), m_nmultipoles_fit(3)
{
  m_ModelIsSet = false;

  m_multipoles_order.erase(m_multipoles_order.begin(), m_multipoles_order.end());

  int size = m_data->ndata()/m_nmultipoles;

  for (int j=0; j<m_nmultipoles; j++)
    for (int i=0; i<size; i++)
      m_multipoles_order.push_back(j);

  m_use_pole.resize(3, true);
}


// ============================================================================================


cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::Modelling_TwoPointCorrelation_multipoles (const std::shared_ptr<data::Data> twop_dataset, const int nmultipoles)
  : Modelling_TwoPointCorrelation1D_monopole(twop_dataset), m_nmultipoles(nmultipoles), m_nmultipoles_fit(nmultipoles)
{
  m_ModelIsSet = false;

  m_multipoles_order.erase(m_multipoles_order.begin(), m_multipoles_order.end());
  m_use_pole.resize(3, false);

  int size = m_data->ndata()/m_nmultipoles;

  for (int j=0; j<m_nmultipoles; j++) {
    m_use_pole[j]=true;
    for (int i=0; i<size; i++)
      m_multipoles_order.push_back(j);
  }

}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fit_range (const double xmin, const double xmax, const int nmultipoles)
{
  vector<vector<double>> fr(m_nmultipoles, vector<double>(2, -1.));

  int mp = (0<nmultipoles && nmultipoles<m_nmultipoles) ? nmultipoles : m_nmultipoles;

  for (int i=0; i<mp; i++) {
    fr[i][0] = xmin;
    fr[i][1] = xmax;
  }

  set_fit_range(fr);
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fit_range (const std::vector<std::vector<double>> fit_range)
{
  if ((int)fit_range.size()!=m_nmultipoles)
    ErrorCBL("Error in cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fit_range() of Modelling_TwoPointCorrelation_multipoles.cpp: the dimension input matrix must be equal to the number of multipoles to be fitted, i.e."+conv(m_nmultipoles, par::fINT)+"!");

  m_use_pole = {false, false, false};

  m_multipoles_order.erase(m_multipoles_order.begin(), m_multipoles_order.end());

  int size = m_data->ndata()/m_nmultipoles;
  vector<bool> mask(m_data->ndata(), false);
  vector<double> xx;

  for (int j=0; j<m_nmultipoles; j++) {
    for (int i=0; i<size; i++) {
      if (fit_range[j][0]<m_data->xx(i+j*size) && m_data->xx(i+j*size)<fit_range[j][1]) {
	m_multipoles_order.push_back(j);
	xx.push_back(m_data->xx(i+j*size));
	m_use_pole[j] = true;
	mask[i+j*size] = true;
      }
    }
  }

  vector<double> data, error;
  vector<vector<double>> covariance;
  m_data->cut(mask, data, error, covariance);

  m_data_fit = make_shared<cbl::data::Data1D>(cbl::data::Data1D(xx, data, covariance));
  m_fit_range = true; 
  
  m_nmultipoles_fit = 0;
  for (size_t i =0; i<m_use_pole.size(); i++)
    m_nmultipoles_fit += m_use_pole[i];

  if (m_ModelIsSet) 
    m_data_model->dataset_order = m_multipoles_order;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fiducial_PkDM ()
{
  m_data_model->nmultipoles = m_nmultipoles;

  m_data_model->kk = logarithmic_bin_vector(m_data_model->step, max(m_data_model->k_min, 1.e-4), min(m_data_model->k_max, 500.));
  vector<double> Pk(m_data_model->step, 0);

  for (size_t i=0; i<(size_t)m_data_model->step; i++) 
    Pk[i] =  m_data_model->cosmology->Pk(m_data_model->kk[i], m_data_model->method_Pk, false, m_data_model->redshift, m_data_model->output_root, m_data_model->norm, m_data_model->k_min, m_data_model->k_max, m_data_model->prec, m_data_model->file_par);

  m_data_model->func_Pk = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(m_data_model->kk, Pk, "Spline"));
  
  if (m_data_model->Pk_mu_model=="dispersion_dewiggled") {    
    vector<double> PkNW(m_data_model->step,0);
    for (size_t i=0; i<(size_t)m_data_model->step; i++) 
      PkNW[i] =  m_data_model->cosmology->Pk(m_data_model->kk[i], "EisensteinHu", false, m_data_model->redshift, m_data_model->output_root, m_data_model->norm, m_data_model->k_min, m_data_model->k_max, m_data_model->prec, m_data_model->file_par);
    
    m_data_model->func_Pk_NW = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(m_data_model->kk, PkNW, "Spline"));
  }
  
  else if (m_data_model->Pk_mu_model=="dispersion_modecoupling") {
    vector<double> kk_1loop, Pk_1loop;
    for (size_t i=0; i<(size_t)m_data_model->step; i++) {
      if(m_data_model->kk[i] < par::pi) {
	kk_1loop.push_back(m_data_model->kk[i]);
	Pk_1loop.push_back(m_data_model->cosmology->Pk_1loop(m_data_model->kk[i], m_data_model->func_Pk, 0,  m_data_model->k_min, 5., m_data_model->prec)); 
      }
    }
    m_data_model->func_Pk1loop = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(kk_1loop, Pk_1loop, "Spline"));
  }

  else ErrorCBL("Error in cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fiducial_PkDM() of Modelling_TwoPointCorrelation_multipoles.cpp: the chosen model ("+m_data_model->Pk_mu_model+") is not currently implemented!");
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_fiducial_xiDM ()
{
  cout << endl; coutCBL << "Setting up the fiducial two-point correlation function model" << endl;

  m_data_model->nmultipoles = 3;

  const vector<double> rad = linear_bin_vector(m_data_model->step, m_data_model->r_min, m_data_model->r_max);

  if (m_data_model->sigmaNL==0) {    

    vector<double> Pk(m_data_model->step,0);
    m_data_model->kk = logarithmic_bin_vector(m_data_model->step, max(m_data_model->k_min, 1.e-4), min(m_data_model->k_max, 500.));

    for (size_t i=0; i<(size_t)m_data_model->step; i++) 
      Pk[i] =  m_data_model->cosmology->Pk(m_data_model->kk[i], m_data_model->method_Pk, m_data_model->NL, m_data_model->redshift, m_data_model->output_root, m_data_model->norm, m_data_model->k_min, m_data_model->k_max, m_data_model->prec, m_data_model->file_par);

    m_data_model->func_Pk = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(m_data_model->kk, Pk, "Spline"));

  }

  else {

    vector<double> Pk(m_data_model->step, 0), PkNW(m_data_model->step, 0);
    m_data_model->kk = logarithmic_bin_vector(m_data_model->step, max(m_data_model->k_min, 1.e-4), min(m_data_model->k_max, 500.));

    for (size_t i=0; i<(size_t)m_data_model->step; i++) {
      Pk[i] =  m_data_model->cosmology->Pk(m_data_model->kk[i], m_data_model->method_Pk, false, m_data_model->redshift, m_data_model->output_root, m_data_model->norm, m_data_model->k_min, m_data_model->k_max, m_data_model->prec, m_data_model->file_par);
      PkNW[i] =  m_data_model->cosmology->Pk(m_data_model->kk[i], "EisensteinHu", false, m_data_model->redshift, m_data_model->output_root, m_data_model->norm, m_data_model->k_min, m_data_model->k_max, m_data_model->prec, m_data_model->file_par);
    }

    m_data_model->func_Pk = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(m_data_model->kk, Pk, "Spline"));
    m_data_model->func_Pk_NW = make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(m_data_model->kk, PkNW, "Spline"));
  }

  vector<double> parameters = {1., 1., m_data_model->sigmaNL_perp, m_data_model->sigmaNL_par, m_data_model->bias, m_data_model->linear_growth_rate_z, 0., 0.};

  vector<vector<double>> xil = Xi_l(rad, m_data_model->nmultipoles, 0, parameters, {m_data_model->func_Pk, m_data_model->func_Pk_NW}, m_data_model->prec);

  m_data_model->func_multipoles.erase(m_data_model->func_multipoles.begin(), m_data_model->func_multipoles.end());
  for (int i=0; i< m_data_model->nmultipoles; i++)
    m_data_model->func_multipoles.push_back(make_shared<cbl::glob::FuncGrid>(cbl::glob::FuncGrid(rad, xil[i], "Spline")));

}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_model_fullShape_DeWiggled (const statistics::PriorDistribution alpha_perpendicular_prior, const statistics::PriorDistribution alpha_parallel_prior, const statistics::PriorDistribution SigmaNL_perpendicular_prior, const statistics::PriorDistribution SigmaNL_parallel_prior, statistics::PriorDistribution fsigma8_prior, statistics::PriorDistribution bsigma8_prior, const statistics::PriorDistribution SigmaS_prior, const bool compute_PkDM)
{
  m_data_model->Pk_mu_model = "dispersion_dewiggled";

  // compute the fiducial dark matter two-point correlation function
  if (compute_PkDM) set_fiducial_PkDM();

  m_data_model->nmultipoles = m_nmultipoles_fit;
  m_data_model->dataset_order = m_multipoles_order;
  m_data_model->use_pole = m_use_pole;

  // set the model parameters
  const int nparameters = 7;

  vector<statistics::ParameterType> parameterType(nparameters, statistics::ParameterType::_Base_);

  vector<string> parameterName(nparameters);
  parameterName[0] = "alpha_perpendicular";
  parameterName[1] = "alpha_parallel";
  parameterName[2] = "SigmaNL_perpendicular";
  parameterName[3] = "SigmaNL_parallel";
  parameterName[4] = "f*sigma8";
  parameterName[5] = "b*sigma8";
  parameterName[6] = "Sigma_S";

  vector<statistics::PriorDistribution> priors = {alpha_perpendicular_prior, alpha_parallel_prior, SigmaNL_perpendicular_prior, SigmaNL_parallel_prior, fsigma8_prior, bsigma8_prior, SigmaS_prior};

  //set the priors
  m_set_prior(priors);
  
  // construct the model
  m_model = make_shared<statistics::Model1D>(statistics::Model1D(&xiMultipoles, nparameters, parameterType, parameterName, m_data_model));
  m_ModelIsSet = true;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_model_fullShape_ModeCoupling (const statistics::PriorDistribution alpha_perpendicular_prior, const statistics::PriorDistribution alpha_parallel_prior, statistics::PriorDistribution fsigma8_prior, statistics::PriorDistribution bsigma8_prior, const statistics::PriorDistribution SigmaV_prior, const statistics::PriorDistribution AMC_prior, const bool compute_PkDM)
{
  m_data_model->Pk_mu_model = "dispersion_modecoupling";

  // compute the fiducial dark matter two-point correlation function
  if (compute_PkDM) set_fiducial_PkDM();

  m_data_model->nmultipoles = m_nmultipoles_fit;
  m_data_model->dataset_order = m_multipoles_order;
  m_data_model->use_pole = m_use_pole;

  // set the model parameters
  const int nparameters = 6;

  vector<statistics::ParameterType> parameterType(nparameters, statistics::ParameterType::_Base_);

  vector<string> parameterName(nparameters);
  parameterName[0] = "alpha_perpendicular";
  parameterName[1] = "alpha_parallel";
  parameterName[2] = "f*sigma8";
  parameterName[3] = "b*sigma8";
  parameterName[4] = "sigma_v";
  parameterName[5] = "AMC";

  vector<statistics::PriorDistribution> priors = {alpha_perpendicular_prior, alpha_parallel_prior, fsigma8_prior, bsigma8_prior, SigmaV_prior, AMC_prior};

  //set the priors
  m_set_prior(priors);

  // construct the model
  m_model = make_shared<statistics::Model1D>(statistics::Model1D(&xiMultipoles, nparameters, parameterType, parameterName, m_data_model));
  m_ModelIsSet = true;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_model_fullShape_sigma8_bias (const statistics::PriorDistribution sigma8_prior, const statistics::PriorDistribution bias_prior)
{
  // compute the fiducial dark matter two-point correlation function
  set_fiducial_PkDM();

  m_data_model->nmultipoles = m_nmultipoles_fit;
  m_data_model->dataset_order = m_multipoles_order;
  m_data_model->use_pole = m_use_pole;

  // set the model parameters
  const int nparameters = 2;

  vector<statistics::ParameterType> parameterType(nparameters, statistics::ParameterType::_Base_);

  vector<string> parameterName(nparameters);
  parameterName[0] = "sigma8";
  parameterName[1] = "bias";

  vector<statistics::PriorDistribution> priors = {sigma8_prior, bias_prior};

  //set the priors
  m_set_prior(priors);

  // construct the model
  m_model = make_shared<statistics::Model1D>(statistics::Model1D(&xiMultipoles_sigma8_bias, nparameters, parameterType, parameterName, m_data_model));
  m_ModelIsSet = true;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::set_model_BAO (const statistics::PriorDistribution alpha_perpendicular_prior, const statistics::PriorDistribution alpha_parallel_prior, const statistics::PriorDistribution B0_prior, const statistics::PriorDistribution B2_prior, const statistics::PriorDistribution A00_prior, const statistics::PriorDistribution A20_prior, const statistics::PriorDistribution A01_prior, const statistics::PriorDistribution A21_prior, const statistics::PriorDistribution A02_prior, const statistics::PriorDistribution A22_prior, const bool compute_XiDM)
{
  // compute the fiducial dark matter two-point correlation function
  if (compute_XiDM) set_fiducial_xiDM();

  m_data_model->nmultipoles = m_nmultipoles_fit;
  m_data_model->dataset_order = m_multipoles_order;
  m_data_model->use_pole = m_use_pole;

  // set the model parameters
  const int nparameters = 10;

  vector<statistics::ParameterType> parameterType(nparameters, statistics::ParameterType::_Base_);

  vector<string> parameterName(nparameters);
  parameterName[0] = "alpha_perpendicular";
  parameterName[1] = "alpha_parallel";
  parameterName[2] = "B0";
  parameterName[3] = "B2";
  parameterName[4] = "A00";
  parameterName[5] = "A20";
  parameterName[6] = "A01";
  parameterName[7] = "A21";
  parameterName[8] = "A02";
  parameterName[9] = "A22";

  vector<statistics::PriorDistribution> priors = {alpha_perpendicular_prior, alpha_parallel_prior, B0_prior, B2_prior, A00_prior, A20_prior, A01_prior, A21_prior, A02_prior, A22_prior};

  //set the priors
  m_set_prior(priors);

  // construct the model
  m_model = make_shared<statistics::Model1D>(statistics::Model1D(&xiMultipoles_BAO, nparameters, parameterType, parameterName, m_data_model));
  m_ModelIsSet = true;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::write_model (const std::string output_dir, const std::string output_file, const int nmultipoles, const std::vector<double> xx, const std::vector<double> parameters)
{
  if (m_likelihood==NULL) ErrorCBL("Error in cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::write_model() of Modelling_TwoPointCorrelation_multipoles.cpp: this function requires the likelihood to be defined (with the function set_likelihood)!");
  
  int nmultipoles_original = m_data_model->nmultipoles;
  vector<int> dataset_order_original = m_data_model->dataset_order;

  m_data_model->nmultipoles = nmultipoles;

  vector<bool> new_use_pole(3, false);
  vector<int> new_dataset_order;
  vector<double> new_xx;
  
  if (xx.size()==0)
    new_xx = m_data_fit->xx();
  else
    for (int n=0; n<m_data_model->nmultipoles; n++) {
      new_use_pole[n] = true;
      for (size_t i=0; i<xx.size(); i++) {
	new_xx.push_back(xx[i]);
	new_dataset_order.push_back(n);
      }
    }

  m_data_model->dataset_order = new_dataset_order;
  m_data_model->use_pole = new_use_pole;

  m_likelihood->write_model(output_dir, output_file, parameters, new_xx);

  m_data_model->dataset_order = dataset_order_original;
  m_data_model->nmultipoles = nmultipoles_original;
  m_data_model->use_pole = m_use_pole;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::write_model_at_bestfit (const std::string output_dir, const std::string output_file, const int nmultipoles, const std::vector<double> xx)
{
  if(m_posterior==NULL)
    ErrorCBL("Error in write_model_at_bestfit of Modelling_TwoPointCorrelation_multipoles.cpp. No posterior found! Run maximize_posterior() first");

  int nmultipoles_original = m_data_model->nmultipoles;
  vector<int> dataset_order_original = m_data_model->dataset_order;

  m_data_model->nmultipoles=nmultipoles;

  vector<bool> new_use_pole(3, false);
  vector<int> new_dataset_order;
  vector<double> new_xx;

  if (xx.size()==0)
    new_xx = m_data_fit->xx();
  else
    for (int n=0; n<m_data_model->nmultipoles; n++) {
      new_use_pole[n] = true;
      for (size_t i=0; i<xx.size(); i++) {
	new_xx.push_back(xx[i]);
	new_dataset_order.push_back(n);
      }
    }

  m_data_model->dataset_order = new_dataset_order;
  m_data_model->use_pole = new_use_pole;
  m_posterior->write_model_at_bestfit(output_dir, output_file, new_xx);

  m_data_model->dataset_order = dataset_order_original;
  m_data_model->nmultipoles = nmultipoles_original;
  m_data_model->use_pole = m_use_pole;
}


// ============================================================================================


void cbl::modelling::twopt::Modelling_TwoPointCorrelation_multipoles::write_model_from_chains (const std::string output_dir, const std::string output_file, const int nmultipoles, const std::vector<double> xx, const int start, const int thin)
{
  if(m_posterior==NULL)
    ErrorCBL("Error in write_model_from_chains of Modelling_TwoPointCorrelation_multipoles.cpp. No posterior found! Run sample_posterior() first");

  int nmultipoles_original = m_data_model->nmultipoles;
  vector<int> dataset_order_original = m_data_model->dataset_order;

  m_data_model->nmultipoles=nmultipoles;

  vector<bool> new_use_pole(3, false);
  vector<int> new_dataset_order;
  vector<double> new_xx;

  if (xx.size()==0)
    new_xx = m_data_fit->xx();
  else
    for (int n=0; n<m_data_model->nmultipoles; n++) {
      new_use_pole[n] = true;
      for (size_t i=0; i<xx.size(); i++) {
	new_xx.push_back(xx[i]);
	new_dataset_order.push_back(n);
      }
    }

  m_data_model->dataset_order = new_dataset_order;
  m_data_model->use_pole = new_use_pole;
  m_posterior->write_model_from_chain(output_dir, output_file, new_xx, {}, start, thin);

  m_data_model->dataset_order = dataset_order_original;
  m_data_model->nmultipoles = nmultipoles_original;
  m_data_model->use_pole = m_use_pole;
}
