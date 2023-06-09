// Created by cgo - DO NOT EDIT

package main

import "unsafe"

import _ "runtime/cgo"

import "syscall"

var _ syscall.Errno
func _Cgo_ptr(ptr unsafe.Pointer) unsafe.Pointer { return ptr }

//go:linkname _Cgo_always_false runtime.cgoAlwaysFalse
var _Cgo_always_false bool
//go:linkname _Cgo_use runtime.cgoUse
func _Cgo_use(interface{})
type _Ctype_char int8

type _Ctype_func_return _Ctype_struct_funcret

type _Ctype_int int32

type _Ctype_struct_funcret struct {
	msg	*_Ctype_char
	id	_Ctype_int
	_	[4]byte
}

type _Ctype_void [0]byte

//go:linkname _cgo_runtime_cgocall runtime.cgocall
func _cgo_runtime_cgocall(unsafe.Pointer, uintptr) int32

//go:linkname _cgo_runtime_cgocallback runtime.cgocallback
func _cgo_runtime_cgocallback(unsafe.Pointer, unsafe.Pointer, uintptr, uintptr)

//go:linkname _cgoCheckPointer runtime.cgoCheckPointer
func _cgoCheckPointer(interface{}, ...interface{})

//go:linkname _cgoCheckResult runtime.cgoCheckResult
func _cgoCheckResult(interface{})

//go:cgo_import_static _cgo_fe5c58cd6cc7_Cfunc_CallMyFunction
//go:linkname __cgofn__cgo_fe5c58cd6cc7_Cfunc_CallMyFunction _cgo_fe5c58cd6cc7_Cfunc_CallMyFunction
var __cgofn__cgo_fe5c58cd6cc7_Cfunc_CallMyFunction byte
var _cgo_fe5c58cd6cc7_Cfunc_CallMyFunction = unsafe.Pointer(&__cgofn__cgo_fe5c58cd6cc7_Cfunc_CallMyFunction)

//go:cgo_unsafe_args
func _Cfunc_CallMyFunction(p0 _Ctype_int) (r1 _Ctype_struct_funcret) {
	_cgo_runtime_cgocall(_cgo_fe5c58cd6cc7_Cfunc_CallMyFunction, uintptr(unsafe.Pointer(&p0)))
	if _Cgo_always_false {
		_Cgo_use(p0)
	}
	return
}

//go:linkname _cgo_runtime_gostring runtime.gostring
func _cgo_runtime_gostring(*_Ctype_char) string

func _Cfunc_GoString(p *_Ctype_char) string {
	return _cgo_runtime_gostring(p)
}
//go:cgo_export_dynamic AGoFunction
//go:linkname _cgoexp_fe5c58cd6cc7_AGoFunction _cgoexp_fe5c58cd6cc7_AGoFunction
//go:cgo_export_static _cgoexp_fe5c58cd6cc7_AGoFunction
//go:nosplit
//go:norace
func _cgoexp_fe5c58cd6cc7_AGoFunction(a unsafe.Pointer, n int32, ctxt uintptr) {
	fn := _cgoexpwrap_fe5c58cd6cc7_AGoFunction
	_cgo_runtime_cgocallback(**(**unsafe.Pointer)(unsafe.Pointer(&fn)), a, uintptr(n), ctxt);
}

func _cgoexpwrap_fe5c58cd6cc7_AGoFunction() {
	AGoFunction()
}
//go:cgo_export_dynamic go_callback_int
//go:linkname _cgoexp_fe5c58cd6cc7_go_callback_int _cgoexp_fe5c58cd6cc7_go_callback_int
//go:cgo_export_static _cgoexp_fe5c58cd6cc7_go_callback_int
//go:nosplit
//go:norace
func _cgoexp_fe5c58cd6cc7_go_callback_int(a unsafe.Pointer, n int32, ctxt uintptr) {
	fn := _cgoexpwrap_fe5c58cd6cc7_go_callback_int
	_cgo_runtime_cgocallback(**(**unsafe.Pointer)(unsafe.Pointer(&fn)), a, uintptr(n), ctxt);
}

func _cgoexpwrap_fe5c58cd6cc7_go_callback_int(p0 _Ctype_int, p1 _Ctype_int, p2 _Ctype_struct_funcret) {
	go_callback_int(p0, p1, p2)
}
