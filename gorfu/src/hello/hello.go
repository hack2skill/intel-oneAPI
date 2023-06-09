package main

import "fmt"
import "util"
import "unsafe"
import "nnet"

/*
#cgo LDFLAGS: -lblas
#include "cprog.h"
#include "cblas.h"
*/
import "C"

func main() {
    fmt.Printf("hello, world\n")


 //     var  list *util.List

 //     list = util.NewList()

    fmt.Printf("%d",Ulist.Len())
    fmt.Printf("1, ")

      l1 := util.NewListItem("Alpha");
      Ulist.Append(l1);
      l2 := util.NewListItem("Phi");
      Ulist.Append(l2);


    fmt.Printf("%d",Ulist.Len())
    fmt.Printf("2, ")

      var i int
      for i=0; i<10;i++ {
         ix := NewIntegerItem(i)         
         Ulist.Append(ix)
         fmt.Printf("%d",Ulist.Len())
         fmt.Printf("3, ")
      }


      Ulist.Print()

    
         fmt.Printf("Begin C CALL ")

           var gomys2 C.myts

      //     var d5 Data_Struct

           gomys2.xmg = C.CString("GO TEXT FROM GO TO C")
           gomys2.num = 47
           gomys2.d = 37

           dptr1 :=  []C.double{1.2, 3.1, 5.6, 29.3, 14.7, 6.0 }
           dptr2 := []C.double{ 5.2, 33.1, 54.6, 21.3, 11.7, 3.0 }

           ptr1 := (*C.double)(unsafe.Pointer(&dptr1[0]))
           ptr2 := (*C.double)(unsafe.Pointer(&dptr2[0]))

           var count C.long


           count =40 

           var k C.int = 12

         fmt.Printf("GO calling c prog  ")

       //   ret1 =  
            C.do_stuff(&gomys2, k, ptr1, ptr2, count)
   
          fmt.Printf("GO printing c return values ")

            

 	Example();

           // lets try some matmul
           // void cblas_dgemm(const enum CBLAS_ORDER Order, const enum CBLAS_TRANSPOSE TransA,
          //       const enum CBLAS_TRANSPOSE TransB, const int M, const int N,
          //       const int K, const double alpha, const double  *A,
          //       const int lda, const double  *B, const int ldb,
          //       const double beta, double  *C, const int ldc);

          var mcols, krows, ncols, nrows C.int
          var alpha, beta C.double
           mcols =  3
           krows = 4  

          nrows = 3
          ncols = 3

          alpha = 1.0
          beta = 0.0

          // lets populate A and B matrices
          
              ax := make([]C.double, mcols*krows);
              bx := make([]C.double, krows*nrows);
              cx := make([]C.double, mcols*ncols);

         fmt.Printf (" Intializing matrix data \n\n");
         var p C.int
         for p = 0; p < (mcols*krows); p++ {
            ax[p] = (C.double)(p+1)
         }

         for p = 0; p < (krows*nrows); p++ {
             bx[p] = (C.double) (-p-1)
         }

         for p = 0; p < (mcols*ncols); p++ {
             cx[p] = 0.0
         }

          var axptr, bxptr, cxptr *C.double
          axptr = &ax[0]
          bxptr = &bx[0]
          cxptr = &cx[0]

          var colmajor C.enum_CBLAS_ORDER = C.CblasColMajor 
          
          var htTrans C.enum_CBLAS_TRANSPOSE = C.CblasNoTrans

          C.wrap_cblas_dgemm(colmajor, htTrans, htTrans, mcols, nrows, krows, alpha, axptr, mcols, bxptr, krows, beta, cxptr, nrows)     

          
          str := gomys2.xmg

          fmt.Printf(" hret %s = ", C.GoString(str))
          fmt.Printf("hret %d", gomys2.num);
          fmt.Printf("hret %d", gomys2.d);


          fmt.Printf(" A MATRIX $$$$$$$");

           var m,j C.int
           for m=0;m<mcols*krows;m++ {
               j++
               fmt.Printf("%f", ax[m]);

               fmt.Printf(", ");

              if j >= krows {
                 j = 0
                 fmt.Printf("  \n ,");
              }

           }

          fmt.Printf(" B MATRIX $$$$$$$$$$$$$$$$$$$");

           for m=0;m<krows*nrows;m++ {
               j++
               fmt.Printf("%f", bx[m]);

               fmt.Printf(", ");

              if j >= nrows {
                 j = 0
                 fmt.Printf(" \n ,");
              }

           }

          fmt.Printf(" RESULTS FOR DEGEMM $$$$$$$$$$$$$$$$$$$");

           for m=0;m<mcols*nrows;m++ {
               j++
               fmt.Printf("%f", cx[m]);

               fmt.Printf(", ");

              if j >= nrows {
                 j = 0
                 fmt.Printf(" \n ,");
              }

           }


	fmt.Printf("Network program begin\n ");


        var NN nnet.Network

       
        
        

        NN.BuildSteps();

}



