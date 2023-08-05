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
 *  @file Headers/Modelling_TwoPointCorrelation2D_cartesian.h
 *
 *  @brief The class Modelling_TwoPointCorrelation2D_cartesian
 *
 *  This file defines the interface of the class
 *  Modelling_TwoPointCorrelation2D_cartesian, used for modelling the 2D
 *  two-point correlation function in Cartesian coordinates,
 *  &xi;(r<SUB>p</SUB>,&pi;)
 *
 *  @author Federico Marulli, Alfonso Veropalumbo
 *
 *  @author federico.marulli3@unbo.it, alfonso.veropalumbo@unibo.it
 */

#ifndef __MODELLINGTWOPOINT2DCART__
#define __MODELLINGTWOPOINT2DCART__


#include "Modelling_TwoPointCorrelation2D.h"
#include "ModelFunction_TwoPointCorrelation2D_cartesian.h"


// ===================================================================================================


namespace cbl {
  
  namespace modelling {

    namespace twopt {
      
      /**
       *  @class Modelling_TwoPointCorrelation2D_cartesian
       *  Modelling_TwoPointCorrelation2D_cartesian.h
       *  "Headers/Modelling_TwoPointCorrelation2D_cartesian.h"
       *
       *  @brief The class Modelling_TwoPointCorrelation2D_cartesian
       *
       *  This file defines the interface of the base class
       *  Modelling_TwoPointCorrelation2D_cartesian, used for modelling
       *  the 2D two-point correlation function in cartesian coordinates
       *
       */
      class Modelling_TwoPointCorrelation2D_cartesian : public Modelling_TwoPointCorrelation2D {

      public:

	/**
	 *  @name Constructors/destructors
	 */
	///@{

	/**
	 *  @brief default constuctor
	 *  @return object of class
	 *  Modelling_TwoPointCorrelation2D_cartesian
	 */
	Modelling_TwoPointCorrelation2D_cartesian () = default;

	/**
	 *  @brief constructor
	 *  
	 *  @param twop the two-point correlation function to model
	 *
	 *  @return object of type
	 *  Modelling_TwoPointCorrelation2D_cartesian
	 */
	Modelling_TwoPointCorrelation2D_cartesian (const std::shared_ptr<cbl::measure::twopt::TwoPointCorrelation> twop)
	  : Modelling_TwoPointCorrelation2D(twop) {}

	/**
	 *  @brief constructor
	 *  
	 *  @param twop_dataset the dataset containing the two-point
	 *  correlation function to model
	 *
	 *  @return object of type
	 *  Modelling_TwoPointCorrelation_monopole
	 */
	Modelling_TwoPointCorrelation2D_cartesian (const std::shared_ptr<data::Data> twop_dataset)
	  : Modelling_TwoPointCorrelation2D() { set_data(twop_dataset); }
      
	/**
	 *  @brief default destructor
	 *  @return none
	 */
	virtual ~Modelling_TwoPointCorrelation2D_cartesian () = default;
	
	///@}


	/**
	 *  @name Member functions used to set the model parameters
	 */
	///@{
	
	/**
	 *  @brief set the fiducial model for dark matter 
	 *  two point correlation function
	 *
	 *  @return none
	 */
	void set_fiducial_xiDM ();

	/**
	 *  @brief set the model to fit the 2D two-point correlation
	 *  function, in Cartesian coordinates
	 *
	 *  @param alpha_perp_prior prior for the parameter
	 *  \f$\alpha_\perp=\frac{D_{\rm A,1}(z)}{D_{\rm A,2}(z)}\f$
	 *
	 *  @param alpha_par_prior prior for the parameter
	 *  \f$\alpha_\parallel=\frac{H_2(z)}{H_1(z)}\f$
	 *
	 *  @param fsigma8_prior prior for the parameter
	 *  \f$f(z)\sigma_8(z)\f$
	 *
	 *  @param bsigma8_prior prior for the parameter
	 *  \f$b(z)\sigma_8(z)\f$
	 *
	 *  @param sigma12_prior prior for the parameter
	 *  \f$\sigma_{12}(z)\f$
	 *
	 *  @return none
	 */
	void set_model_dispersionModel_AP (const statistics::PriorDistribution alpha_perp_prior={}, const statistics::PriorDistribution alpha_par_prior={}, const statistics::PriorDistribution fsigma8_prior={}, const statistics::PriorDistribution bsigma8_prior={}, const statistics::PriorDistribution sigma12_prior={});

	/**
	 *  @brief set the model to fit the 2D two-point correlation
	 *  function, in Cartesian coordinates
	 *
	 *  @param fsigma8_prior prior for the parameter
	 *  \f$f(z)\sigma_8(z)\f$
	 *
	 *  @param bsigma8_prior prior for the parameter
	 *  \f$b(z)\sigma_8(z)\f$
	 *
	 *  @param sigma12_prior prior for the parameter
	 *  \f$\sigma_{12}(z)\f$
	 *
	 *  @return none
	 */
	void set_model_dispersionModel (const statistics::PriorDistribution fsigma8_prior={}, const statistics::PriorDistribution bsigma8_prior={}, const statistics::PriorDistribution sigma12_prior={});
	
	///@}
      
      };
    }
  }
}

#endif
