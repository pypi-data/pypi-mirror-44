/*---------------------------------------------------------------------------*\
**$Author: andrius $
**$Date: 2017-11-07 04:53:10 -0500 (Tue, 07 Nov 2017) $ 
**$Revision: 5724 $
**$URL: svn://www.crystallography.net/cod-tools/tags/v2.4/src/components/codcif/cif_lexer.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF_LEXER_H
#define __CIF_LEXER_H

#include <stdio.h>
#include <unistd.h> /* for ssize_t */
#include <cexceptions.h>
#include <cif_compiler.h>

int ciflex( void );
void cifrestart( void );

void cif_lexer_set_compiler( CIF_COMPILER *ccc );

void cif_flex_reset_counters( void );

int cif_flex_current_line_number( void );
void cif_flex_set_current_line_number( ssize_t line );
int cif_flex_current_position( void );
void cif_flex_set_current_position( ssize_t pos );
const char *cif_flex_current_line( void );

int cif_flex_previous_line_number( void );
int cif_flex_previous_position( void );
const char *cif_flex_previous_line( void );

int cif_lexer_set_report_long_items( int flag );
int cif_lexer_report_long_items( void );
int cif_lexer_set_line_length_limit( int max_length );
int cif_lexer_set_tag_length_limit( int max_length );

extern int ciferror( const char *message );

#endif
