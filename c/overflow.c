#include <stdio.h>

int main() {
    int a = 15;
    int b = 30;
    int c = 45;

    int *whatsthis = &a;
    printf("whatsthis is: %d\n",*whatsthis);
    printf("whatsthis address is: %p\n",whatsthis);
    printf("b address is: %p\n",&b);
    whatsthis = whatsthis - 2;
    printf("whatsthis address is: %p\n",whatsthis);
    printf("whatsthis is: %d\n",*whatsthis);

    return 0;
}