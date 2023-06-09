// Created by cgo - DO NOT EDIT

//line /mnt/golang/gorfu/src/hello/hello.go:1
package main

import "fmt"
import "util"

//line /mnt/golang/gorfu/src/hello/hello.go:9
func main() {
						fmt.Printf("hello, world\n")

//line /mnt/golang/gorfu/src/hello/hello.go:17
	fmt.Printf("%d", Ulist.Len())
						fmt.Printf("1, ")

						l1 := util.NewListItem("Alpha")
						Ulist.Append(l1)
						l2 := util.NewListItem("Phi")
						Ulist.Append(l2)

//line /mnt/golang/gorfu/src/hello/hello.go:26
	fmt.Printf("%d", Ulist.Len())
	fmt.Printf("2, ")

	var i int
	for i = 0; i < 10; i++ {
		ix := NewIntegerItem(i)
		Ulist.Append(ix)
		fmt.Printf("%d", Ulist.Len())
		fmt.Printf("3, ")
	}

//line /mnt/golang/gorfu/src/hello/hello.go:38
	Ulist.Print()

//line /mnt/golang/gorfu/src/hello/hello.go:41
	fmt.Printf("Begin C CALL ")

						var gomys2 _C_mystruct

						gomys2.xmg = _Cfunc_CString("GO TEXT FROM GO TO C")
						gomys2.num = 47
						gomys2.d = 37.4

						var ptr1 *_C_double
						var ptr2 *_C_double

						var count _C_int

//line /mnt/golang/gorfu/src/hello/hello.go:55
	count = 1176472897

						var k _C_int = 12

						fmt.Printf("GO calling c prog  ")

//line /mnt/golang/gorfu/src/hello/hello.go:64
	var ret1 *_C_mystruct

	ret1 = _C_do_stuff(gomys2, k, ptr1, ptr2, count)

	fmt.Printf("GO printing c return values ")

	fmt.Printf("%s", ret1.xmg)
	fmt.Printf("%d", ret1.num)
	fmt.Printf("%d", ret1.d)

}
