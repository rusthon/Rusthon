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

def get_debugger_overlay():
	global editor, editor2

	overlay = document.getElementById('DEBUG_OVERLAY')
	if overlay is None:
		print 'creating new debug overlay'
		overlay = document.createElement('div')
		document.body.appendChild(overlay)
		overlay.style.position='absolute'
		overlay.style.zIndex = 100
		overlay.style.top = 0
		overlay.style.left = 0
		overlay.style.width = '100%'
		overlay.style.height = '100%'
		overlay.style.backgroundColor = 'black'
		overlay.style.color = 'grey'
		overlay.style.opacity = 0.9

		header = document.createElement('h2')
		header.appendChild(document.createTextNode('header...'))
		overlay.appendChild(header)

		def _set_header(txt):
			header.firstChild.nodeValue=txt

		overlay._set_header = _set_header

		ediv1 = document.createElement('div')
		ediv1.setAttribute('id', 'EDITOR1')
		overlay.appendChild(ediv1)

		header2 = document.createElement('h2')
		header2.appendChild(document.createTextNode('header...'))
		overlay.appendChild(header2)

		def _set_header2(txt):
			header2.firstChild.nodeValue=txt

		overlay._set_header2 = _set_header2


		ediv2 = document.createElement('div')
		ediv2.setAttribute('id', 'EDITOR2')
		overlay.appendChild(ediv2)
		ediv2.style.fontSize='18px'

		editor = ace.edit('EDITOR1')
		editor.setTheme("ace/theme/monokai")
		editor.getSession().setMode("ace/mode/javascript")
		#editor.container.style.height = '50%'
		editor.renderer.setOption('showLineNumbers', false)

		editor.setOption("maxLines", 100)
		editor.setOption("minLines", 2)

		editor2 = ace.edit('EDITOR2')
		editor2.setTheme("ace/theme/monokai")
		editor2.getSession().setMode("ace/mode/javascript")
		#editor2.container.style.height = '20%'
		editor2.renderer.setOption('showLineNumbers', false)
		editor2.setAutoScrollEditorIntoView(true)
		editor2.resize()

		editor2.setOption("maxLines", 100)
		editor2.setOption("minLines", 2)

	return overlay

def show_error(err,f,c):
	debugger.log(err,f,c)
	overlay = get_debugger_overlay()

	errtype, errmsg = err.stack.splitlines()[0].split(':')
	errmsg = errmsg.strip()
	errvar = errmsg.split()[0]

	search = []
	if errtype == 'ReferenceError':
		errvar += '.'
		search.append( errvar + '.' )

		a = ['the variable']
		for i,word in enumerate(errmsg.split()):
			if i==0:
				a.append('`' + word + '`')
			else:
				a.append(word)
		errmsg = ' '.join(a)

	search.append(errvar)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )

	src1 = debugger.getsource(f)
	editor.setValue(src1)

	if c is not undefined:
		overlay._set_header( errtype + ' caused by function: `' + c.name + '`')
		overlay._set_header2( errmsg )

		src2 = debugger.getsource(c)
		editor2.setValue(src2)

		for i,ln in enumerate(src2.splitlines()):
			if errvar in ln:
				editor2.selection.moveTo(i,ln.index(errvar))
				editor2.selection.selectWord()
				break


		for i,ln in enumerate(src1.splitlines()):
			if c.name+'(' in ln:
				editor.selection.moveTo(i,ln.index(c.name))
				editor.selection.selectWord()
				break

	return False  ## True sets breakpoint

debugger.onerror = show_error


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
	show('calling bar')
	a.x.y = 'oopps'
	show('bar OK')


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
<body onload="main()" style="font-family:arial">
<pre id="CONTAINER"></pre>
</body>
</html>
```