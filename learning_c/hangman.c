/* Credit to https://www.geeksforgeeks.org/c/hangman-game-in-c/ for the inspiration and the template */

/* Imports */
#include <stdio.h>   // Allows input/output operations (printf, scanf, getchar, etc.)
#include <string.h>  // Allows string manipulation functions (strlen, strcpy, strcmp, etc.)
#include <stdlib.h>  // Allows memory allocation and random number generation (malloc, rand, srand, etc.)
#include <time.h>    // Allows time-related functions for seeding random numbers (time, etc.)
#include <ctype.h>   // Allows character type testing and conversion (isalpha, tolower, toupper, etc.)
#include <stdbool.h> // Allows boolean type (bool, true, false)

/* Secret Word  Generation */
#define MAXWORDLEN 30
#define MAXGUESSES 6

struct wordHint {
    char word[MAXWORDLEN];
    char hint[MAXWORDLEN];
};

/* Display Word Call */
void displayWord(const char word[], const bool guessed[]);

/* Draw Hangman Call */
void drawHangman(int guesses);

/* Main Code Logic */
int main() {

    srand(time(NULL)); // Seed the random number generator

    struct wordHint words[] = {
        {"apple", "A common fruit"},
        {"banana", "A yellow fruit"},
        {"cherry", "A red fruit"},
        {"date", "A brown fruit"},
        {"elderberry", "A dark fruit"},
        {"fig", "A sweet fruit"},
        {"grape", "A small fruit"},
        {"honeydew", "A green fruit"},
        {"kiwi", "A brown fruit with green flesh"},
        {"lemon", "A sour yellow fruit"}
    };

    int wordIndex = rand() % 10;

    const char* secretWord = words[wordIndex].word;
    const char* hint = words[wordIndex].hint;

    int wordLength = strlen(secretWord);
    char guessedWord[MAXWORDLEN] = { 0 };
    bool guessedLetters[26] = { false };
    
    printf("Welcome to Hangman!\n");
    printf("The hint is: %s\n", hint);

    int tries = 0;

    while (tries < MAXGUESSES) {
        printf("\n");
        displayWord(secretWord, guessedLetters);
        drawHangman(tries);

        char guess;
        printf("Enter a letter: ");
        scanf(" %c", &guess);
        guess = tolower(guess);

        if (guessedLetters[guess - 'a']) {
            printf("You already guessed that letter!\n");
            continue;
        }
        
        guessedLetters[guess - 'a'] = true;

        bool found = false;

        for (int i = 0; i < wordLength; i++) {
            if (secretWord[i] == guess) {
                found = true;
                guessedWord[i] = guess;
                break;
            }
        }

        if (found) {
            printf("Good guess!\n");
        } else {
            printf("The letter '%c' is not in the word. \n", guess);
            tries++;
        }

        // Check if all letters have been guessed
        bool wordComplete = true;
        for (int i = 0; i < wordLength; i++) {
            if (!guessedLetters[secretWord[i] - 'a']) {
                wordComplete = false;
                break;
            }
        }

        if (wordComplete) {
            printf("Congratulations! You guessed the word: %s\n", secretWord);
            break;
        }
    }

    if (tries >= MAXGUESSES) {
        printf("Sorry, you ran out of guesses. The word was: %s\n", secretWord);
    }

    return 0;
}

/* Display Word Function */
void displayWord(const char word[], const bool guessed[]) {
    int length = strlen(word);
    for (int i = 0; i < length; i++) {
        if (guessed[word[i] - 'a']) {
            printf("%c ", word[i]);
        } else {
            printf("_ ");
        }
    }
    printf("\n");
}

/* Draw Hangman Function */
void drawHangman(int guesses) {
    printf("  +---+\n");
    printf("  |   |\n");
    
    if (guesses > 0) {
        printf("  O   |\n");
    } else {
        printf("      |\n");
    }
    
    if (guesses > 2) {
        printf(" /|\\  |\n");
    } else if (guesses > 1) {
        printf("  |   |\n");
    } else {
        printf("      |\n");
    }
    
    if (guesses > 4) {
        printf(" / \\  |\n");
    } else if (guesses > 3) {
        printf(" /    |\n");
    } else {
        printf("      |\n");
    }
    
    printf("      |\n");
    printf("=========\n");
}