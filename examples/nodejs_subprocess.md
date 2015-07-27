NodeJS fake Python subprocess module
-------

tries to emulate python subprocess module, so far this is a minimal implementation,
because nodejs is async, this is also async and you need to pass a callback to get the result of the subprocess.

see [builtins_nodejs.py](../src/runtime/builtins_nodejs.py)

* subprocess.call
* subprocess.Popen

To run this example run these commands in your shell, nodejs will be used to run it:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/nodejs_subprocess.md --run=myapp.js
```


@myapp.js
```rusthon
#backend:javascript
from runtime import *
from nodejs import *

def cb(data):
	print data

subprocess.call(executeable='ls', args=['-lh'], callback=cb)
p = subprocess.Popen(executeable='ls', args=['-h'], callback=cb)

```
