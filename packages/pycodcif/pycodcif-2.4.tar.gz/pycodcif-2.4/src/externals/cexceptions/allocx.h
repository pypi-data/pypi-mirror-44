/*---------------------------------------------------------------------------*\
** $Author: saulius $
** $Date: 2015-04-05 04:51:47 -0400 (Sun, 05 Apr 2015) $
** $Revision: 3207 $
** $URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/externals/cexceptions/allocx.h $
\*---------------------------------------------------------------------------*/

#ifndef __ALLOCX_H
#define __ALLOCX_H

/* memory allocation functions that use cexception handling */

#include <stdlib.h>
#include <cexceptions.h>

typedef enum {
    ALLOCX_OK = 0,
    ALLOCX_NO_MEMORY = 99,
    ALLOCX_last
} ALLOCX_ERROR;

extern void *allocx_subsystem;

void *mallocx( size_t size, cexception_t *ex );
void *callocx( size_t size, size_t nr, cexception_t *ex );
void *reallocx( void *buffer, size_t new_size, cexception_t *ex );
void *creallocx( void *buffer,
		 size_t old_element_nr,
		 size_t new_element_nr,
		 size_t element_size,
		 cexception_t *ex );
void freex( void* );

#endif
