package main

import "fmt"
import "util"

// #include <cprog.h>
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

           var gomys2 _C_mystruct

           gomys2.xmg = C.CString("GO TEXT FROM GO TO C")
           gomys2.num = 47
           gomys2.d = 37.4

           var ptr1 *_C_double
           var ptr2 *_C_double

           var count _C_int


           count = 1176472897

           var k _C_int = 12

         fmt.Printf("GO calling c prog  ")

         //var  retptr *_Ctype_struct_myts
         //retptr = C.do_stuff(gomys2.xmg, k, ptr1, ptr2, count)

          var ret1 *_C_mystruct
        
          ret1 =  _C_do_stuff(gomys2, k, ptr1, ptr2, count)
   
         fmt.Printf("GO printing c return values ")

            fmt.Printf("%s", ret1.xmg);
            fmt.Printf("%d", ret1.num);
            fmt.Printf("%d", ret1.d);

}
