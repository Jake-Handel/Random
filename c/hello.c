#include <stdio.h>

int main() {
 
   int i, j;
   int rows = 4;
   for (i = 1; i <= rows; i++) {
      for (j = 4; j >= i; j--) {
         printf("*");
      }
      printf("\n");
   }
   return 0;
}
