/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-04-05 05:26:36 -0400 (Sun, 05 Apr 2015) $ 
**$Revision: 3216 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/externals/cexceptions/stringx.c $
\*---------------------------------------------------------------------------*/

/* exports: */
#include <stringx.h>

/* uses: */
#include <string.h>
#include <allocx.h>

#define merror( EX ) cexception_raise_in( EX, allocx_subsystem, \
					  ALLOCX_NO_MEMORY,     \
					  "Not enough memory" )

char *strdupx( const char *str, cexception_t *ex )
{
    void *s = strdup( str );
    if( !s ) merror( ex );
    return s;
}
