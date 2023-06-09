
#include "cblas.h"

typedef struct mystruct {

   const char *xmg;
   int num;
   double d;

} myts;

extern struct go_callback_int_return;

myts * do_stuff(myts *s2, int k, double *py, double *ps, long count);

void wrap_cblas_dgemm(const enum CBLAS_ORDER Order, const enum CBLAS_TRANSPOSE TransA,
                 const enum CBLAS_TRANSPOSE TransB, const int M, const int N,
                 const int K, const double alpha, const double *A,
                 const int lda, const double *B, const int ldb,
                 const double beta, double *C, const int ldc);void cblas_dgemm(const enum CBLAS_ORDER Order, const enum CBLAS_TRANSPOSE TransA,
                 const enum CBLAS_TRANSPOSE TransB, const int M, const int N,
                 const int K, const double alpha, const double *A,
                 const int lda, const double *B, const int ldb,
                 const double beta, double *C, const int ldc);


typedef struct funcret {

   const char *msg;
   int id;

} func_return;



func_return CallMyFunction(int i);
