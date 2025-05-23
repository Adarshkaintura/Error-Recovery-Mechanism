%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"  
void yyerror(const char *s);
%}

%%
"int"           { return INT; }
"float"         { return FLOAT; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }
[a-zA-Z][a-zA-Z0-9]* { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+          { yylval.num = atoi(yytext); return NUMBER; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULT; }
"/"             { return DIV; }
"="             { return ASSIGN; }
";"             { return SEMICOLON; }
"("             { return LPAREN; }
")"             { return RPAREN; }
"{"             { return LBRACE; }
"}"             { return RBRACE; }
[ \t\n]         ; /* Skip whitespace */
.               { yyerror("Unknown character"); }
%%

int yywrap() {
    return 1;
}