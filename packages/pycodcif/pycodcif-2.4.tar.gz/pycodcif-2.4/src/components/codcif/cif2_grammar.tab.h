/* A Bison parser, made by GNU Bison 3.3.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2019 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_CIF2_CIF2_GRAMMAR_TAB_H_INCLUDED
# define YY_CIF2_CIF2_GRAMMAR_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int cif2debug;
#endif
/* "%code requires" blocks.  */
#line 36 "cif2_grammar.y" /* yacc.c:1921  */

    #include <cif_compiler.h>

#line 52 "cif2_grammar.tab.h" /* yacc.c:1921  */

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    _DATA_ = 258,
    _SAVE_HEAD = 259,
    _SAVE_FOOT = 260,
    _TAG = 261,
    _LOOP_ = 262,
    _DQSTRING = 263,
    _SQSTRING = 264,
    _UQSTRING = 265,
    _DQ3STRING = 266,
    _SQ3STRING = 267,
    _TEXT_FIELD = 268,
    _INTEGER_CONST = 269,
    _REAL_CONST = 270,
    _TABLE_ENTRY_SEP = 271
  };
#endif
/* Tokens.  */
#define _DATA_ 258
#define _SAVE_HEAD 259
#define _SAVE_FOOT 260
#define _TAG 261
#define _LOOP_ 262
#define _DQSTRING 263
#define _SQSTRING 264
#define _UQSTRING 265
#define _DQ3STRING 266
#define _SQ3STRING 267
#define _TEXT_FIELD 268
#define _INTEGER_CONST 269
#define _REAL_CONST 270
#define _TABLE_ENTRY_SEP 271

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 40 "cif2_grammar.y" /* yacc.c:1921  */

    char *s;
    typed_value *typed_value;

#line 101 "cif2_grammar.tab.h" /* yacc.c:1921  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE cif2lval;

int cif2parse (void);

#endif /* !YY_CIF2_CIF2_GRAMMAR_TAB_H_INCLUDED  */
