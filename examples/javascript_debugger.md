Debugging JavaScript
--------------------

https://github.com/rusthon/Rusthon/wiki/JavaScript-Debugger

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


def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)


## this decorator opens chrome devtools, 
## and then calls the function after a timeout,
## to give devtools window time to open and connect.
@debugger
def main():
	show('enter main')
	show('calling foo')
	foo()
	show('everything OK')

def foo():
	show('calling bar may fail...')
	## expression
	bar()

	## assignment
	#x = bar()

	show('foo OK')

def bar():
	a.x.y = 'oopps'
	show( some_missing_object[ 'x' ] )
	mytypo()

	show('bar OK')


```
Get Ace Editor
--------------
git clone into your home directory: `https://github.com/ajaxorg/ace-builds.git`



@index.html
```html
<html>
<head>
<script src="~/ace-builds/src-min/ace.js" git="https://github.com/ajaxorg/ace-builds.git"></script>
<script src="~/ace-builds/src-min/theme-monokai.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>

<@myapp>
</head>
<body onload="main()" style="font-family:arial">
<pre id="CONTAINER"></pre>
</body>
</html>
```