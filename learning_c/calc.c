    #include <stdio.h>

    void calc(int num1, int num2, char operator) {
        int ans = 0;
        switch(operator) {
            case '+':
                ans = num1 + num2;
                break;
            case '-':
                ans = num1 - num2;
                break;
            case '*':
                ans = num1 * num2;
                break;
            case '/':
                ans = (int)num1 / num2;
                break;
            default:
                printf("Invalid operator");
                break;
        }
        printf("%d %c %d = %d \n", num1, operator, num2, ans);
    }

    int main() {
        int num1 = 0;
        int num2 = 0;
        char operator = '\0';

        printf("Enter the first num: ");
        scanf("%d", &num1);

        printf("Enter the operator: ");
        scanf(" %c", &operator);

        printf("Enter the second num: ");
        scanf("%d", &num2);

        calc(num1, num2, operator);
    }