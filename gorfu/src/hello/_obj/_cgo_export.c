/* Created by cgo - DO NOT EDIT. */
#include <stdlib.h>
#include "_cgo_export.h"

extern void crosscall2(void (*fn)(void *, int, __SIZE_TYPE__), void *, int, __SIZE_TYPE__);
extern __SIZE_TYPE__ _cgo_wait_runtime_init_done();
extern void _cgo_release_context(__SIZE_TYPE__);

extern char* _cgo_topofstack(void);
#define CGO_NO_SANITIZE_THREAD
#define _cgo_tsan_acquire()
#define _cgo_tsan_release()

extern void _cgoexp_fe5c58cd6cc7_AGoFunction(void *, int, __SIZE_TYPE__);

CGO_NO_SANITIZE_THREAD
void AGoFunction()
{
	__SIZE_TYPE__ _cgo_ctxt = _cgo_wait_runtime_init_done();
	struct {
		char unused;
	} __attribute__((__packed__, __gcc_struct__)) a;
	_cgo_tsan_release();
	crosscall2(_cgoexp_fe5c58cd6cc7_AGoFunction, &a, 0, _cgo_ctxt);
	_cgo_tsan_acquire();
	_cgo_release_context(_cgo_ctxt);
}
extern void _cgoexp_fe5c58cd6cc7_go_callback_int(void *, int, __SIZE_TYPE__);

CGO_NO_SANITIZE_THREAD
void go_callback_int(int p0, int p1, func_return p2)
{
	__SIZE_TYPE__ _cgo_ctxt = _cgo_wait_runtime_init_done();
	struct {
		int p0;
		int p1;
		func_return p2;
	} __attribute__((__packed__, __gcc_struct__)) a;
	a.p0 = p0;
	a.p1 = p1;
	a.p2 = p2;
	_cgo_tsan_release();
	crosscall2(_cgoexp_fe5c58cd6cc7_go_callback_int, &a, 24, _cgo_ctxt);
	_cgo_tsan_acquire();
	_cgo_release_context(_cgo_ctxt);
}
