NodeJS Fake Python Builtin Modules
---------------------

using `from nodejs import *` imports these modules that wrap around the nodejs api.

* os
* sys
* open
* tempfile

To run this example run these commands in your shell, nodejs will be used to run it:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/nodejs_file.md --run=myapp.js
```


@myapp.js
```rusthon
#backend:javascript
from runtime import *
from nodejs import *

f = open('/tmp/test.txt')
f.write('hello world')
f.close()

a = open('/tmp/test.txt', 'r')
print a.read()

tdir = tempfile.gettempdir()
print tdir

print sys.argv
print sys.stdin

print os.environ
print os.getcwd()
print os.getpid()

print dir(os)
print dir(sys)

```
