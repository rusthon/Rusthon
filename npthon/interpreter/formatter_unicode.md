formatter_unicode.c
-----------


@formatter_unicode.c
```c
```

>built-in formatter for unicode.  That is, unicode.__format__().

```c
#include "Python.h"
#ifdef Py_USING_UNICODE
#include "../Objects/stringlib/unicodedefs.h"
#define FORMAT_STRING _PyUnicode_FormatAdvanced
```

we can live with only the string versions of those.  The builtin
>format() will convert them to unicode.

```c
#include "../Objects/stringlib/formatter.h"
#endif
```
___