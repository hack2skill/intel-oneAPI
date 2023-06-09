package main


import "fmt"
import "sync"
//import "unsafe"

/*
#include "cprog.h"
#include <stdio.h>
extern void ACFunction();
//extern C.func_return CallMyFunction(int i);
//extern struct myts;
*/
import "C"


type Data_Struct struct {

    xdata string
    count int64
    p int
    x float64
    avl bool

}


//export AGoFunction
func AGoFunction() {
	fmt.Println("AGoFunction()")
}

//export go_callback_int
func go_callback_int(foo C.int, p1 C.int, s1 C.func_return) {
//	fn := lookup(int(foo))
//	fn(p1)

	fmt.Println("callback with struct s1 ", s1)
	fmt.Println("callback with struct s1 xmg %s", C.GoString(s1.msg))
	fmt.Println("callback with struct s1 num %d", C.int(s1.id))
	fmt.Println(string( *s1.msg))
	fmt.Println(s1.id)

        

//        return 10, "hi there"

}

func MyCallback(x C.int) {
	fmt.Println("callback with", x)

}

func Example() {
	i := register(MyCallback)
	var fval C.func_return
        fval = C.CallMyFunction(C.int(i))

	fmt.Println("cfunc ret xmg %s", C.GoString(fval.msg))
	fmt.Println("cfunc ret num %d", C.int(fval.id))


	unregister(i)
}

var mu sync.Mutex
var index int
var fns = make(map[int]func(C.int))

func register(fn func(C.int)) int {
	mu.Lock()
	defer mu.Unlock()
	index++
	for fns[index] != nil {
		index++
	}
	fns[index] = fn
	return index
}

func lookup(i int) func(C.int) {
	mu.Lock()
	defer mu.Unlock()
	return fns[i]
}

func unregister(i int) {
	mu.Lock()
	defer mu.Unlock()
	delete(fns, i)
}
