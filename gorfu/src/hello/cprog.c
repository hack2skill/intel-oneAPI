

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cprog.h"

myts * do_stuff(myts *s2, int k, double *py, double *ps, long count) {


      printf("xmg = %s", s2->xmg);
      printf("num = %d", s2->num);
  //    printf("d = %s", s2->d);
      
       printf("k = %d", k);
      
      for(int k=0;k<count;k++)
          printf("%f", py[k]);

      for(int k=0;k<count;k++)
          printf("%f", ps[k]);



     s2->xmg = "This is banner text";

  //   memcpy(pk.xmg, text, 32*sizeof(char));

     printf("s2 xmg in cprog = %s", s2->xmg);

     s2->num = 19;

     s2->d = 98.0;

}

void ACFunction() {
	printf("ACFunction()\n");
	AGoFunction();
} 


func_return CallMyFunction(int foo) {
	printf("call my function()\n");
	AGoFunction();
        int d = 20;

        /*
        struct mystruct  myst;


        myst.xmg = "some c text here";
        myst.d = 2.4;
        myst.num =42;
       */

        func_return rv;
        rv.msg = "hello from cprog";
        rv.id = 29;

        go_callback_int(foo, d, rv); 

        return rv;


} 


void wrap_cblas_dgemm(const enum CBLAS_ORDER Order, const enum CBLAS_TRANSPOSE TransA,
                 const enum CBLAS_TRANSPOSE TransB, const int M, const int N,
                 const int K, const double alpha, const double *A,
                 const int lda, const double *B, const int ldb,
                 const double beta, double *C, const int ldc) {

               printf(" calling cblas dgemm\n ");

              cblas_dgemm(Order, TransA,
                 TransB, M, N,
                 K, alpha, A,
                 lda, B, ldb,
                 beta, C, ldc);


}

