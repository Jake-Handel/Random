    #include <stdio.h>

    void guessNumber(int guess) {
        int myNum;
        while (myNum != guess) {
            printf("Enter an integer: ");
            scanf("%d", &myNum);
            if (myNum < guess) {
            printf("The number is higher than %d\n", myNum);
            }   else {
            printf("The number is lower than %d\n", myNum);
            }
        }
        printf("You guessed it! %d\n", guess);
    }

    int main() {
        guessNumber(555);
    }