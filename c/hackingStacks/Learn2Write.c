#include <stdio.h>
#include <stdlib.h>

int main(){
    int target[5] = {0,1,2,3,4};
    int flag = 0; //Set flag to value
    int index;

    //Print banner and get index user would like to edit
    printf("What index in the array would you like to edit?\n");
    scanf("%d",&index);

    //Get what the user would like to change that index to
    printf("What would you like to change it to?\n");
    scanf("%d",&target[index]);

    //If the flag is 420 give flag
    if (flag == 420){
        printf("Congrats, here is a flag!!\ncgs{This_is_a_fake_flag}\n");
    } else { //If not, show them the array
        printf("Here is your array\n");
        for (int i = 0; i < 5; i++){
            printf("%d ", target[i]);
        }
        printf("\n");
    }

    return 0;
}