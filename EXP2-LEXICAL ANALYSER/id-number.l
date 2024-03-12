%option noyywrap
%{
	#include<stdio.h>
	#include <math.h>
	#include<string.h>
	
%}

DIGIT    [0-9]
ID       [a-z][a-z0-9]*
 


%%
{DIGIT}+    {
            printf( "An integer: %s (%d)\n", yytext,
                    atoi( yytext ) );
            }

{DIGIT}+"."{DIGIT}*        {
            printf( "A float: %s (%g)\n", yytext,
                    atof( yytext ) );
            }
{ID}        printf( "An identifier: %s\n", yytext );
"+"|"-"|"*"|"/"   printf( "An operator: %s\n", yytext );
"++"       printf("unary op %s\n", yytext );
%%
int main()
{

yylex();
	return 0;
}