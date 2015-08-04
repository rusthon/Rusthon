Debugging JavaScript
--------------------

An issue with debugging javascript is having to press a hot key to bring up the devtools window each time chrome is opened.
stackoverflow [is-there-a-command-line-argument-in-chrome-to-start-the-developer-tools-on-start](http://stackoverflow.com/questions/5425443/is-there-a-command-line-argument-in-chrome-to-start-the-developer-tools-on-start)

NW.js allows for the devtools window to be opened from js.
So, when using the transpiler it will check if you have installed NW.js to your home directory in:
`~/nwjs-v0.12.2-linux-x64/` and use that to run open your webpage after translation.

And, if you apply `@debugger` decorator to the entry point function of your application, 
it will display the chrome devtools window first, and then run your application.
This allowed injected break points to work and halt execution of your script,
where you can debug things, and then press unpause to resume your script.

@myapp
```rusthon
#backend:javascript
from runtime import *


def show_error(err,f,c):
	debugger.log(err,f,c)
	errtype, errmsg = err.stack.splitlines()[0].split(':')
	errmsg = errmsg.strip()
	errvar = errmsg.split()[0]
	if errtype == 'ReferenceError':
		errvar += '.'
	show(errvar)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )

	src1 = debugger.getsource(f)
	editor.setValue(src1)

	if c is not undefined:
		src2 = debugger.getsource(c)
		editor2.setValue(src2)

		for i,ln in enumerate(src2.splitlines()):
			if errvar in ln:
				editor2.selection.moveTo(i,ln.index(errvar))
				editor2.selection.selectWord()
				break


		for i,ln in enumerate(src1.splitlines()):
			if c.name in ln:
				editor.selection.moveTo(i,ln.index(c.name))
				editor.selection.selectWord()
				break

	return False  ## True sets breakpoint

debugger.onerror = show_error


def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

def throws_error():
	a.x.y = 'oopps'

## this decorator opens chrome devtools, 
## and then calls the function after a timeout,
## to give devtools window time to open and connect.
@debugger
def main():
	global editor, editor2

	editor = ace.edit('EDITOR1')
	editor.setTheme("ace/theme/monokai")
	editor.getSession().setMode("ace/mode/javascript")
	editor.container.style.height = '50%'

	editor2 = ace.edit('EDITOR2')
	editor2.setTheme("ace/theme/monokai")
	editor2.getSession().setMode("ace/mode/javascript")
	editor2.container.style.height = '20%'


	## expression
	throws_error()

	## assignment
	#x = throws_error()

	show('everything OK')


```
Get Ace Editor
--------------
git clone into your home directory: `https://github.com/ajaxorg/ace-builds.git`

@index.html
```html
<html>
<head>
<script src="~/ace-builds/src-min/ace.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/theme-monokai.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>

<@myapp>
</head>
<body onload="main()" style="background-color:black; color:white">
<div id="EDITOR1"></div>
<pre id="CONTAINER"></pre>
<div id="EDITOR2"></div>
</body>
</html>
```