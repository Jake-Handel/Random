#include <stdio.h>
#include <stdlib.h>

//This never gets called
void win(){
    printf("YOU WIN\ncgs{Fak3_f1ag}\n");
    exit(0); //Avoid crashing
}


void edit_arr(){
    int index;
    long arr[5];
    //Get index from user
    printf("Please enter the array index you would like to edit: ");
    scanf("%d",&index);
    //Change that index to whatever user wants
    printf("What would you like to change it to?\n");
    scanf("%d", &arr[index]);
    return;
}

int main(){
    //Print banner and call edit_arr
    printf("Welcome to the array editor!!\n");
    printf("Take this before you go %d\n", win);
    edit_arr();
    printf("You are now back in the main function\n");
    return 0;
}