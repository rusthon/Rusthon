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


def show_error(err,f):
	debugger.log(err,f)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )

	src = debugger.getsource(f)
	editor.setValue(src)

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
	global editor
	show('main..')
	editor = ace.edit('EDITOR')
	editor.setTheme("ace/theme/monokai")
	editor.getSession().setMode("ace/mode/javascript")
	editor.container.style.height = '70%'

	## expression
	throws_error()

	## assignment
	#x = throws_error()


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
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>

<@myapp>
</head>
<body onload="main()">
<pre id="CONTAINER"></pre>
<div id="EDITOR"></div>
</body>
</html>
```