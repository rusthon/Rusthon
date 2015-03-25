Nim ThreadPool and Parallel
---------------------------


```nim

import threadpool

type
	IntSeq = seq[int]

proc calc_something(x:int, y:int): IntSeq =
	result = @[x,y,x+y]

proc start_nim_threadpool( a:cint, b:cint ): cint {.cdecl, exportc.} =
	var r: FlowVar[ IntSeq ]
	echo("a:", a)
	echo("b:", b)
	parallel:
		r = spawn calc_something( int(a), int(b) )
	return cast[cint]((^r)[2])

```

Run ThreadPool
--------------

```rusthon
#backend:c++
import nim

def main():
	nim.main()
	print 'starting nim threadpool'
	msg = start_nim_threadpool( 10, 20 )
	print msg
	print 'ok'

```

