/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2011-03-08 13:45:40 -0500 (Tue, 08 Mar 2011) $ 
**$Revision: 1590 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/externals/cexceptions/cxprintf.h $
\*---------------------------------------------------------------------------*/

#ifndef __CEX_REPORT_H
#define __CEX_REPORT_H

#include <stdarg.h>

const char* cxprintf( const char * format, ... );
const char* vcxprintf( const char * format, va_list args );

#endif
