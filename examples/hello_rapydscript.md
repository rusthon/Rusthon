testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/hello_rapydscript.md
```

html
----


@index.html
```html
<html>
<head>

<@my_rapydscript.js>
<@my_rusthon_script.js>

</head>
<body>
<button onclick="javascript:hi_from_rapyd()">clickme</button>

</body>
</html>
```

rapydscript
-----------
You need to install RapydScript for this to work.
http://www.rapydscript.com/

Test calling Rusthon translated JS from RapydScript.

@my_rapydscript.js
```rapydscript

𝑭𝑶𝑶𝒃𝒂𝒓 = 'UNICODE_OK'

def hi_from_rapyd():
	window.alert('hey rapydscript!')
	a = [1,2,3]
	hi_from_rusthon(a)

```


rusthon javascript backend
--------------------------

@my_rusthon_script.js
```rusthon
#backend:javascript
from runtime import *

def hi_from_rusthon(v):
	assert inline('𝑭𝑶𝑶𝒃𝒂𝒓') == 'UNICODE_OK'
	assert len(v) == 3
	assert v[0] == 1
	for x in v:
		print(x)

```
