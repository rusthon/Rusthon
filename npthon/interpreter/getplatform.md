getplatform.c
-----------


@getplatform.c
```c
#include "Python.h"
#ifndef PLATFORM
#define PLATFORM "unknown"
#endif
const char *
Py_GetPlatform(void)
{
	return PLATFORM;
}
```
___