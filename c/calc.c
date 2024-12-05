#include <stdio.h>

int main() {
    char operator;
    double firstNumber, secondNumber;

    // Displaying the available operations to the user
    printf("Enter an operator (+, -, *, /): ");
    scanf("%c", &operator);

    // Asking the user to input the numbers
    printf("Enter two numbers: ");
    scanf("%lf %lf", &firstNumber, &secondNumber);

    // Performing the calculation based on the operator
    switch (operator) {
        case '+':
            printf("%.2lf + %.2lf = %.2lf\n", firstNumber, secondNumber, firstNumber + secondNumber);
            break;
        case '-':
            printf("%.2lf - %.2lf = %.2lf\n", firstNumber, secondNumber, firstNumber - secondNumber);
            break;
        case '*':
            printf("%.2lf * %.2lf = %.2lf\n", firstNumber, secondNumber, firstNumber * secondNumber);
            break;
        case '/':
            // Checking if the second number is not zero
            if (secondNumber != 0.0)
                printf("%.2lf / %.2lf = %.2lf\n", firstNumber, secondNumber, firstNumber / secondNumber);
            else
                printf("Error! Division by zero is not allowed.\n");
            break;
        default:
            printf("Error! Operator is not correct.\n");
    }

    return 0;
}
