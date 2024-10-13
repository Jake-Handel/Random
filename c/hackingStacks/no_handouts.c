#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

//This never gets called
void win(){
    int fd;
    char flag[64];

    memset(flag,0,64);

    fd = open("flag.txt",O_RDONLY);
    read(fd,flag,63);
    printf("YOU WIN\n%s\n", flag);
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
    printf("I am not giving you the address this time!!");
    edit_arr();
    printf("You are now back in the main function\n");
    return 0;
}
