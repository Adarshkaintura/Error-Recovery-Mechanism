%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern int yylex();
void yyerror(const char *s);
extern FILE *yyin;
char *parse_tree = NULL;
void append_to_tree(const char *node);
%}

%union {
    int num;
    char *str;
}

%token INT FLOAT IF ELSE WHILE
%token <str> IDENTIFIER
%token <num> NUMBER
%token PLUS MINUS MULT DIV ASSIGN SEMICOLON LPAREN RPAREN LBRACE RBRACE

%type <str> program statement_list statement declaration assignment expression term factor

/* Define operator precedence to resolve conflicts */
%left PLUS MINUS
%left MULT DIV

%%

program:
    statement_list { parse_tree = strdup($1); }
    ;

statement_list:
    statement { $$ = strdup($1); }
    | statement_list statement {
        char *temp = malloc(strlen($1) + strlen($2) + 10);
        sprintf(temp, "%s\n%s", $1, $2);
        $$ = temp;
        append_to_tree(temp);
    }
    ;

statement:
    declaration SEMICOLON { $$ = strdup($1); }
    | assignment SEMICOLON { $$ = strdup($1); }
    | error SEMICOLON { $$ = strdup("Error recovered"); }
    | error RBRACE { $$ = strdup("Error recovered at }"); }
    ;

declaration:
    INT IDENTIFIER { 
        char *temp = malloc(100);
        sprintf(temp, "int %s", $2);
        $$ = temp;
    }
    ;

assignment:
    IDENTIFIER ASSIGN expression {
        char *temp = malloc(100);
        sprintf(temp, "%s = %s", $1, $3);
        $$ = temp;
    }
    ;

expression:
    term { $$ = $1; }
    | expression PLUS term {
        char *temp = malloc(100);
        sprintf(temp, "%s + %s", $1, $3);
        $$ = temp;
    }
    | expression MINUS term {
        char *temp = malloc(100);
        sprintf(temp, "%s - %s", $1, $3);
        $$ = temp;
    }
    ;

term:
    factor { $$ = $1; }
    | term MULT factor {
        char *temp = malloc(100);
        sprintf(temp, "%s * %s", $1, $3);
        $$ = temp;
    }
    | term DIV factor {
        char *temp = malloc(100);
        sprintf(temp, "%s / %s", $1, $3);
        $$ = temp;
    }
    ;

factor:
    NUMBER { 
        char *temp = malloc(20);
        sprintf(temp, "%d", $1);
        $$ = temp;
    }
    | IDENTIFIER { $$ = strdup($1); }
    | LPAREN expression RPAREN { $$ = $2; }
    ;

%%

void append_to_tree(const char *node) {
    if (!parse_tree) {
        parse_tree = strdup(node);
    } else {
        char *temp = malloc(strlen(parse_tree) + strlen(node) + 10);
        sprintf(temp, "%s\n%s", parse_tree, node);
        free(parse_tree);
        parse_tree = temp;
    }
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yyin = stdin;
    yyparse();
    printf("Parse Tree:\n%s\n", parse_tree);
    return 0;
}