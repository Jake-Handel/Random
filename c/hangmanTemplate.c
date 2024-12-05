#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAX_WORD_LENGTH 100
#define MAX_ATTEMPTS 6

void clearScreen() {
    // Simple way to clear the screen
    printf("\e[1;1H\e[2J");
}

// This function is for printing out the current state of the guessed word
// i.e. which letters have been guessed and where they are
// For example: p _ _ _ _ a m m _ _ _
void printWord(char *word, int *guessed) {
    int length = strlen(word);
    for (int i = 0; i < length; i++) {
        if (guessed[i]) {
            printf("%c ", word[i]);
        } else {
            printf("_ ");
        }
    }
    printf("\n");
}

// Check whether all letters in word have been guessed
int isWordGuessed(char *word, int *guessed) {
    int length = strlen(word);
    for (int i = 0; i < length; i++) {
        if (!guessed[i]) {
            return 0;  // Not all letters guessed
        }
    }
    return 1;  // All letters guessed
}

// Main game function
void hangman() {
    int attemptsLeft = MAX_ATTEMPTS;
    char guessedLetters[26] = {0}; // To store already guessed letters
    int guessed[100] = {0}; // Array to keep track of which letters are guessed

    // Use these words as a start, you can add some more later if you want :)
    char *words[] = {
    "abandon", "ability", "absence", "academy", "account", "airplane", "amazing", "anxiety", "apparel", "arrival",
    "baggage", "barrier", "bizarre", "bottle", "breathe", "brother", "building", "calendar", "carriage", "capture",
    "cattle", "ceremony", "chicken", "climate", "complete", "country", "cousin", "creation", "culture", "current",
    "daughter", "defense", "deserve", "detect", "diamond", "difficult", "disease", "elevator", "emotion", "encounter",
    "engineer", "exercise", "fashion", "freedom", "furniture", "gallery", "garden", "genuine", "holiday", "horizon",
    "imagine", "inspire", "isolate", "journey", "language", "library", "manner", "memory", "message", "nature",
    "officer", "opinion", "picture", "practice", "product", "project", "quality", "realize", "receive", "research",
    "revenue", "service", "society", "sponsor", "station", "strategy", "success", "tactic", "travel", "umbrella",
    "victory", "village", "weather", "wilderness", "wonder", "yesterday", "zealous", "zodiac", "animal", "barbecue",
    "bicycle", "college", "courage", "cucumber", "debate", "diamond", "dynamic", "engine", "essential", "festival",
    "frequent", "furniture", "gallery", "happiness", "immediate", "important", "journal", "knowledge", "leisure",
    "literature", "magazine", "maintain", "mission", "modern", "natural", "ordinary", "package", "powerful", "private",
    "puzzle", "quality", "reliability", "science", "solution", "sports", "student", "teacher", "training", "universe",
    "vacation", "vocabulary", "wonderful", "youth", "zebra", "zoo", "abandon", "accept", "access", "adventure", "advice",
    "airport", "amendment", "analysis", "approach", "artistic", "balance", "beautiful", "behavior", "biscuit", "bottle",
    "brother", "camera", "capital", "category", "chocolate", "climate", "classic", "classroom", "comfort", "complete",
    "council", "cousin", "creative", "cultural", "decision", "delight", "detailed", "director", "discovery", "element",
    "energy", "engine", "enhance", "exercise", "explore", "factory", "feedback", "forever", "fortunate", "freedom",
    "frustrate", "gather", "gesture", "harmony", "horizon", "improve", "include", "inspire", "journey", "justice",
    "library", "magnetic", "mission", "national", "obvious", "outcome", "package", "persistence", "planning", "possible",
    "problem", "process", "project", "quality", "reliable", "science", "solution", "standard", "strategy", "success",
    "system", "theory", "training", "universe", "upgrade", "utility", "victory", "volume", "wealth", "winning", "xenon",
    "yesterday", "zephyr", "zodiac", "amazing", "ancient", "apply", "baggage", "balance", "canvas", "carpet", "casual",
    "center", "ceramic", "classic", "complete", "courage", "creative", "delicate", "dynamic", "efficient", "examine",
    "fashion", "feature", "general", "happiness", "highlight", "humanity", "incredible", "integrate", "journalist",
    "landscape", "mysterious", "narrative", "objective", "opinion", "original", "perspective", "predict", "profound",
    "relevant", "respect", "revenue", "sincere", "society", "structure", "suitable", "technical", "trending", "unique",
    "valuable", "venture", "version", "visual", "welfare", "workshop", "adventure", "analysis", "approach", "benefit",
    "bizarre", "bravery", "courage", "creative", "delicate", "detective", "elegant", "engage", "equality", "flourish",
    "formula", "gallery", "genuine", "horizon", "important", "insight", "inspire", "master", "modern", "natural",
    "objective", "optimize", "practice", "priority", "process", "purpose", "refine", "reliable", "science", "strategic",
    "success", "support", "symbolic", "technology", "trending", "universal", "vibrant", "virtual", "welcome", "wonder",
    "youthful", "zealous", "abstract", "accessory", "academy", "alliance", "beyond", "benefit", "capital", "charity",
    "classic", "concept", "creative", "decade", "dynamic", "education", "enthusiastic", "fascinate", "fellowship",
    "generation", "growth", "horizon", "institute", "interact", "invest", "journey", "leadership", "motivate", "mystic",
    "navigate", "optimum", "paradigm", "pioneering", "precision", "reflect", "resolve", "sustainable", "talented",
    "transform", "triumph", "vanguard", "venture", "wellness", "worthy", "yearning", "zephyr", "abstraction", "advantage",
    "ambition", "articulate", "assess", "beneficial", "connect", "concept", "cultivate", "diversity", "embrace",
    "engage", "explore", "facilitate", "feedback", "framework", "growth", "harmony", "inspire", "intelligent",
    "innovative", "leverage", "negotiate", "optimize", "outcome", "paradigm", "participate", "revolution", "scalable",
    "strategic", "synthesize", "transform", "unveil", "visionary", "widespread", "x-factor", "yearning", "zealous",
    "abstract", "achievement", "adopt", "amplify", "atmosphere", "capture", "clarify", "consolidate", "contribute",
    "curiosity", "dedicated", "develop", "emerge", "evolve", "focus", "framework", "generate", "improve", "initiative",
    "integrate", "interact", "innovate", "leadership", "merge", "model", "nurture", "optimize", "pivot", "progress",
    "realize", "resilience", "result", "strengthen", "success", "support", "thrive", "transform", "understand",
    "value", "vision", "yield", "zenith"
};


    
    // Pick a random word from words ^
    int arrSize = sizeof(words) / sizeof(words[0]);
    srand(time(0)); // Initialize random number generator
    int randomWordIndex = rand() % arrSize;
    char *word = words[randomWordIndex]; 

    int wordLength = strlen(word);

    // Main game loop
    while (attemptsLeft > 0) {
        clearScreen();
        printf("Hangman Game\n");
        printf("Attempts left: %d\n", attemptsLeft);
        printf("Guessed letters: ");
        
        for (int i = 0; i < 26; i++) {
            if (guessedLetters[i] != 0) {
                printf("%c ", guessedLetters[i]);
            }
        }
        printf("\n");

        // Use printWord() here!
        printWord(word, guessed);

        // Query user for letter guess and store the character
        char guess;
        printf("Enter a letter: ");
        scanf(" %c", &guess);
        guess = tolower(guess); // Convert to lowercase for consistency

        // Make sure the user doesn't guess a letter they already have!
        int alreadyGuessed = 0;
        for (int i = 0; i < 26; i++) {
            if (guessedLetters[i] == guess) {
                alreadyGuessed = 1;
                break;
            }
        }
        if (alreadyGuessed) {
            printf("You already guessed that letter!\n");
            continue;
        }

        // If it's a new letter, store it as a guess
        for (int i = 0; i < 26; i++) {
            if (guessedLetters[i] == 0) {
                guessedLetters[i] = guess;
                break;
            }
        }

        // Check whether the letter is in the word or not
        int correctGuess = 0;
        for (int i = 0; i < wordLength; i++) {
            if (word[i] == guess) {
                guessed[i] = 1;
                correctGuess = 1;
            }
        }

        if (!correctGuess) {
            attemptsLeft--;
        }

        // Check whether the word is guessed and exit if so.
        if (isWordGuessed(word, guessed)) {
            clearScreen();
            printf("Congratulations! You guessed the word: %s\n", word);
            return;
        }
    }
    
    // If we get to here it means the user didn't get the word :(
    clearScreen();
    printf("Out of attempts! The word was: %s\n", word);
}

int main() {
    hangman();
    return 0;
}
