
result = (^r)[2]

```nim

import threadpool

type
	IntSeq = seq[int]

proc calc_something(): IntSeq =
	result = @[100,200,300]

proc start_nim_threadpool( a:cint, b:cint, s:cstring ): cint {.cdecl, exportc.} =
	var r: FlowVar[ IntSeq ]
	echo(s)
	echo("a:", a)
	echo("b:", b)
	parallel:
		r = spawn calc_something()
	return a+b
```

```rusthon
#backend:c++
import nim

def main():
	nim.main()
	print 'calling nim function'
	s = 'mymessage to nim'
	msg = start_nim_threadpool( 10, 20, cstr(s) )
	print msg
	print 'ok'

```

