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

#debugger.onerror = lambda e,f: show_error(e,f)

def show_error(err,f):
	#show(err)
	#show(err.stack)
	#show(err.line)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )
	show('---------------------------')
	show(f)
	print err
	print f

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
	show('main..')
	## expression
	throws_error()
	## assignment
	#x = throws_error()


```

@index.html
```html
<html>
<head>
<@myapp>
</head>
<body onload="main()">
<pre id="CONTAINER">
</pre>
</body>
</html>
```