/*---------------------------------------------------------------------------*\
** $Author: saulius $
** $Date: 2015-07-21 10:39:27 -0400 (Tue, 21 Jul 2015) $
** $Revision: 3587 $
** $URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/externals/cexceptions/stdiox.c $
\*---------------------------------------------------------------------------*/

/* exports: */
#include <stdiox.h>

/* uses: */
#include <cexceptions.h>
#include <cxprintf.h>
#include <errno.h>
#include <string.h>

void *stdiox_subsystem = &stdiox_subsystem;

FILE *fopenx( const char *filename, const char *mode, cexception_t *ex )
{
    FILE *f = fopen( filename, mode );

    if( f == NULL ) {
        cexception_raise_syserror
            ( ex, stdiox_subsystem, STDIOX_FILE_OPEN_ERROR,
              "could not open file", strerror( errno ));
    }

    return f;
}

void fclosex( FILE *file, cexception_t *ex )
{
    if( fclose( file ) != 0 ) {
        cexception_raise_syserror
            ( ex, stdiox_subsystem, STDIOX_FILE_CLOSE_ERROR,
              "could not close file", strerror( errno ));
    }
}
