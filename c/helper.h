#include <stdio.h>
#include <stdlib.h>
 
// #include "editor.h"
 
int get_int()
{
    char number[50];
    fgets(number, sizeof(number), stdin);
    return atoi(number);
}
 
char get_char()
{
    char c[2];
    fgets(c, sizeof(c), stdin);
    return c[0];
}

