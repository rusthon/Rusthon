testing
-------

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

```
