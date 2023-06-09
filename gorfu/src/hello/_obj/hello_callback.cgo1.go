// Created by cgo - DO NOT EDIT

//line /mnt/golang/gorfu/src/hello/hello_callback.go:1
package main

//line /mnt/golang/gorfu/src/hello/hello_callback.go:4
import "fmt"
import "sync"

//line /mnt/golang/gorfu/src/hello/hello_callback.go:18
type Data_Struct struct {
//line /mnt/golang/gorfu/src/hello/hello_callback.go:20
	xdata	string
	count	int64
	p	int
	x	float64
	avl	bool
//line /mnt/golang/gorfu/src/hello/hello_callback.go:26
}

//line /mnt/golang/gorfu/src/hello/hello_callback.go:30
func AGoFunction() {
	fmt.Println("AGoFunction()")
}

//line /mnt/golang/gorfu/src/hello/hello_callback.go:35
func go_callback_int(foo _Ctype_int, p1 _Ctype_int, s1 _Ctype_struct_funcret) {

//line /mnt/golang/gorfu/src/hello/hello_callback.go:39
	fmt.Println("callback with struct s1 ", s1)
	fmt.Println("callback with struct s1 xmg %s", _Cfunc_GoString(s1.msg))
	fmt.Println("callback with struct s1 num %d", _Ctype_int(s1.id))
	fmt.Println(string(*s1.msg))
	fmt.Println(s1.id)

//line /mnt/golang/gorfu/src/hello/hello_callback.go:49
}

func MyCallback(x _Ctype_int) {
	fmt.Println("callback with", x)

}

func Example() {
								i := register(MyCallback)
								var fval _Ctype_struct_funcret
								fval = _Cfunc_CallMyFunction(_Ctype_int(i))

								fmt.Println("cfunc ret xmg %s", _Cfunc_GoString(fval.msg))
								fmt.Println("cfunc ret num %d", _Ctype_int(fval.id))

//line /mnt/golang/gorfu/src/hello/hello_callback.go:65
	unregister(i)
}

var mu sync.Mutex
var index int
var fns = make(map[int]func(_Ctype_int))

func register(fn func(_Ctype_int)) int {
	mu.Lock()
	defer mu.Unlock()
	index++
	for fns[index] != nil {
		index++
	}
	fns[index] = fn
	return index
}

func lookup(i int) func(_Ctype_int) {
	mu.Lock()
	defer mu.Unlock()
	return fns[i]
}

func unregister(i int) {
	mu.Lock()
	defer mu.Unlock()
	delete(fns, i)
}
