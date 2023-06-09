#include<stdio.h>
int main()
{
  int a[][2][2] = { 
                     {
                       {1, 2}, {3, 4}   }, 
                     {{5, 6}, {7, 8}}
                   }; // Works
  int b[][3] = { 
                     { 2, 4, 8 }, 
                     { 4, 8, 16 },
                     { 8, 16, 32 },
                     { 16, 32, 64 },
                     { 32, 64, 128 },
                     { 64, 128, 256 },
                     { 128, 256, 512 }
                   }; // Works


 for (int i=0;i<7;i++) {

        printf(" kers sizes for %d are %d, %d\n", b[i][0], b[i][1], b[i][2]);


 }


//  printf("%d\n", x); // prints 8*sizeof(int)
  return 0;
}
