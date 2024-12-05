#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    int index;
    char flag[] = "\ncgs{P1ace_H0ld3r_Fl@g}"; //Create flag here
    char edit_me[63];

    //Set all letters in string to 'A'
    for (int i=0;i<63;i++){
        edit_me[i] = 'A';
    }

    //Get user to tell us what letter we are changing
    printf("What index would you like to make 'B'?\n");
    scanf("%d",&index);

    //Change that letter
    edit_me[index] = 'B';

    //Print our string
    printf("Now the string looks like this!\n%s\n", edit_me);
}