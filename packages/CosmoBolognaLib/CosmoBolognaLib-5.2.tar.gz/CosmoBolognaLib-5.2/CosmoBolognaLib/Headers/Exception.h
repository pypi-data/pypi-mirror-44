/********************************************************************
 *  Copyright (C) 2010 by Federico Marulli                          *
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
 *  @file Headers/Exception.h
 *
 *  @brief The class Exception Class used to handle the exceptions
 *
 *  This file defines the interface of the class Exception, used to
 *  handle the exceptions
 *
 *  @author Federico Marulli 
 *
 *  @author federico.marulli3@unbo.it
 */

#ifndef __EXCEP__
#define __EXCEP__

namespace cbl {

  namespace glob {
    
    /**
     *  @enum ExitCode
     *  @brief the exit status
     */
    enum class ExitCode {
    
      /// generic error
      _error_,
    
      /// error related to the Input/Output 
      _IO_,
    
      /// error due to work in progress
      _workInProgress_
    
    };

    /**
     * @brief return a std::vector containing the
     * ExitCode names
     * @return a std::vector containing the
     * ExitCode names
     */
    inline std::vector<std::string> ExitCodeNames () {return {"error", "IO", "workInProgress"}; }

    /**
     * @brief cast an enum of type ExitCode
     * from its index
     * @param exitCodeIndex the exitCode index
     * @return object of class ExitCode
     */
    inline ExitCode ExitCodeCast (const int exitCodeIndex) {return castFromValue<ExitCode>(exitCodeIndex);}

    /**
     * @brief cast an enum of type ExitCode
     * from its name
     * @param exitCodeName the exitCode name
     * @return object of class ExitCode
     */
    inline ExitCode ExitCodeCast (const std::string exitCodeName) {return castFromName<ExitCode>(exitCodeName, ExitCodeNames());}

    /**
     * @brief cast an enum of type ExitCode
     * from indeces
     * @param exitCodeIndeces the exitCode indeces
     * @return std::vector of objects of class ExitCode
     */
    inline std::vector<ExitCode> ExitCodeCast (const std::vector<int> exitCodeIndeces) {return castFromValues<ExitCode>(exitCodeIndeces);} 

    /**
     * @brief cast an enum of type ExitCode
     * from thier names
     * @param exitCodeNames the exitCode names
     * @return std::vector of objects of class ExitCode
     */
    inline std::vector<ExitCode> ExitCodeCast (const std::vector<std::string> exitCodeNames) {return castFromNames<ExitCode>(exitCodeNames, ExitCodeNames());}

    /**
     *  @class Exception Exception.h
     *  "Headers/Exception.h"
     *
     *  @brief The class Exception
     *
     *  This is the class used to handle the exceptions
     */
    class Exception : public std::exception
    {
    
    protected:

      /// the message describing the exception
      std::string m_message;

      /// the exit status
      ExitCode m_exitCode;

  
    public:
    
      /**
       *  @name Constructors/destructors
       */
      ///@{

      /**
       *  @brief default constructor
       *  @return object of class Data
       */
      Exception ()
	: m_message(par::col_red+"\n*** CosmoBolognaLib generic error! ***\n"+par::col_default), m_exitCode(ExitCode::_error_) {}

      /**
       *  @brief constructor
       *
       *  @param message the output message
       *  @param exitCode the exit status
       *  @param header header of the error message
       *
       *  @return object of class Exception
       */
      explicit Exception (const std::string message, const ExitCode exitCode=ExitCode::_error_, const std::string header="\n")
	: m_exitCode(exitCode)
      {
	m_message = header;
	
	switch (exitCode)
	  {
	  case(ExitCode::_error_):
	    m_message += par::col_red + "*** Error! ***\n";
	    break;
	  
	  case(ExitCode::_IO_):
	    m_message += par::col_red + "*** Input/Output error ***\n";
	    break;
	  
	  case(ExitCode::_workInProgress_):
	    m_message += par::col_purple + "*** Work in progress! ***\n";
	    break;
	  }

	m_message += message + "\n\n" + par::col_default;
      }
    
      /**
       *  @brief default destructor
       *  @return none
       */
      virtual ~Exception () noexcept = default;

      ///@}

    
      /**
       *  @brief get the exit status
       *  @return the exit status
       */
      ExitCode exitCode () const noexcept
      { return m_exitCode; }

      /**
       *  @brief the error description
       *
       *  @return a pointer to the error description message
       */
      const char* what () const noexcept override
      { return m_message.c_str(); }
  
    };
  
  }
}

#endif
