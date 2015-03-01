Lua Backend
-------
The Lua backend is experimental.

command line:
```bash
./rusthon.py ./examples/hello_lua.md --run=mytest.lua
```

@mytest.lua
```rusthon
#backend:lua

def main():
	print 'hello world from lua'

main()

```
