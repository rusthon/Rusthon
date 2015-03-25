pyfpe.c
-----------


@pyfpe.c
```c
#include "pyconfig.h"
#include "pyfpe.h"
```

 The signal handler for SIGFPE is actually declared in an external
 module fpectl, or as preferred by the user.  These variable
 definitions are required in order to compile Python without
 getting missing externals, but to actually handle SIGFPE requires
 defining a handler and enabling generation of SIGFPE.

```c
#ifdef WANT_SIGFPE_HANDLER
jmp_buf PyFPE_jbuf;
int PyFPE_counter = 0;
#endif
```

>warning when compiling an empty file.

```c
double
PyFPE_dummy(void *dummy)
{
	return 1.0;
}
```
___