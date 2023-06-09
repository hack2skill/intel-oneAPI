
/*
typedef struct {

   const char *xmg;
   int num;
   double d;

} mystruct;


mystruct mys1;
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cprog.h"

mystruct * do_stuff(mystruct s2, int k, double *py, double *ps, long count) {


      printf("xmg = %s", s2.xmg);
      
       printf("k = %d", k);
      
      for(int k=0;k<count;k++)
          printf("%a", py[k]);

      for(int k=0;k<count;k++)
          printf("%a", ps[k]);


     mystruct pk;


     pk.xmg = malloc(32*sizeof(char));

     const char *text = "This is banner text";

     memcpy(pk.xmg, text, 21*sizeof(char));

}
