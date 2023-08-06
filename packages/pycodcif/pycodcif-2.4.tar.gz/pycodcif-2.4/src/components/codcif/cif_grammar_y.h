/*---------------------------------------------------------------------------*\
**$Author: andrius $
**$Date: 2017-04-12 06:39:05 -0400 (Wed, 12 Apr 2017) $ 
**$Revision: 5195 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/components/codcif/cif_grammar_y.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF_GRAMMAR_Y_H
#define __CIF_GRAMMAR_Y_H

#include <cif.h>
#include <cif_options.h>
#include <cexceptions.h>

CIF *new_cif_from_cif1_file( FILE *in, char *filename, cif_option_t co,
                             cexception_t *ex );

void cif_yy_debug_on( void );
void cif_yy_debug_off( void );

#endif
