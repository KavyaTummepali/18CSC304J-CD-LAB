%option noyywrap
%{
	#include<stdio.h>
	#include<string.h>
	 int num_lines = 0,num_char=0,words=0,x=0;
%}

%%


[a-zA-Z]+  { words++;  num_char += strlen(yytext);}
\n    ++num_lines;
.     ++num_char;
[0-9]+ ++x;
%%
int main(int argc, char *argv[])
{
  
    yyin = fopen(argv[1], "r");    
    yylex();         
    fclose(yyin);

    printf(" \nNo of lines %d\n",num_lines);
    printf(" \nNo of chars %d\n",num_char);
    printf(" \nNo of words %d\n",words);
     printf(" \nNo of digits %d\n",x);
   
	return 0;
}
