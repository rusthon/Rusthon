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
		overlay.setAttribute('id', 'DEBUG_OVERLAY')
		document.body.appendChild(overlay)
		overlay.style.position='absolute'
		overlay.style.zIndex = 100
		overlay.style.bottom = 0
		overlay.style.right = 0
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

		closebut = document.createElement('button')
		closebut.appendChild(document.createTextNode('close'))
		overlay.appendChild( closebut )
		closebut.style.position='absolute'
		closebut.style.bottom = 4
		closebut.style.right = 4
		def closecb(): overlay.style.visibility='hidden'
		closebut.onclick = closecb

		mbut = document.createElement('button')
		mbut.appendChild(document.createTextNode('-'))
		overlay.appendChild( mbut )
		mbut.style.position='absolute'
		mbut.style.bottom = 4
		mbut.style.right = 55
		def mbutcb():
			overlay.style.height='80%'
			overlay.style.width='70%'
		mbut.onclick = mbutcb


		subheader = document.createElement('h4')
		subheader.appendChild(document.createTextNode('subheader'))
		overlay.appendChild(subheader)

		def _set_subheader(txt):
			subheader.firstChild.nodeValue=txt

		overlay._set_subheader = _set_subheader

		cbut = document.createElement('button')
		cbut.appendChild( document.createTextNode('call') )
		cbut.style.position = 'absolute'
		cbut.style.right = 100
		header.appendChild( cbut )

		input = document.createElement('input')
		input.setAttribute('type', 'text')
		input.size = 10
		input.style.position = 'absolute'
		input.style.right = 10
		header.appendChild( input )

		overlay._header1_controls = {'call':cbut, 'args':input}


		#####################################
		ediv1 = document.createElement('div')
		ediv1.setAttribute('id', 'EDITOR1')
		overlay.appendChild(ediv1)

		header2 = document.createElement('h2')
		header2.appendChild(document.createTextNode('header2'))
		overlay.appendChild(header2)

		cbut = document.createElement('button')
		cbut.appendChild( document.createTextNode('call') )
		cbut.style.position = 'absolute'
		cbut.style.right = 100
		header2.appendChild( cbut )

		input = document.createElement('input')
		input.setAttribute('type', 'text')
		input.size = 10
		input.style.position = 'absolute'
		input.style.right = 10
		header2.appendChild( input )

		overlay._header2_controls = {'call':cbut, 'args':input}

		def _set_header2(txt):
			header2.firstChild.nodeValue=txt

		overlay._set_header2 = _set_header2


		ediv2 = document.createElement('div')
		ediv2.setAttribute('id', 'EDITOR2')
		overlay.appendChild(ediv2)
		ediv2.style.fontSize='18px'

		def __redef_on_edit(e,t):
			if t.__editfunc is not None:
				t.__editfunc.redefine( t.getValue() )

		editor = ace.edit('EDITOR1')
		editor.__function = None
		editor.on('input', __redef_on_edit)

		editor.setTheme("ace/theme/monokai")
		editor.getSession().setMode("ace/mode/javascript")
		#editor.container.style.height = '50%'
		editor.renderer.setOption('showLineNumbers', false)

		editor.setOption("maxLines", 100)
		editor.setOption("minLines", 2)

		editor2 = ace.edit('EDITOR2')
		editor2.__function = None
		editor2.on('input', __redef_on_edit)

		editor2.setTheme("ace/theme/monokai")
		editor2.getSession().setMode("ace/mode/javascript")
		#editor2.container.style.height = '20%'
		editor2.renderer.setOption('showLineNumbers', false)
		editor2.setAutoScrollEditorIntoView(true)
		#editor2.resize()

		editor2.setOption("maxLines", 100)
		editor2.setOption("minLines", 2)

		#editor2.on('input', lambda e,t: console.log(t.getValue()) )
		#editor2.on('input', lambda e,t: console.log(e) )


	return overlay

def show_error(err,f,c):
	debugger.log(err,f,c)
	overlay = get_debugger_overlay()

	errtype, errmsg = err.stack.splitlines()[0].split(':')
	errmsg = errmsg.strip()
	errvar = errmsg.split()[0]

	search = []
	if errtype == 'ReferenceError':
		search.append( errvar + '.' )  ## checks for attributes
		search.append( errvar + '(' )  ## checks for func calls
		search.append( errvar + '[' )  ## checks for func calls

		errmsg_custom = []
		for i,word in enumerate(errmsg.split()):
			if i==0:
				errmsg_custom.append('`' + word + '`')
			else:
				errmsg_custom.append(word)

	search.append(errvar)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )

	src1 = debugger.getsource(f)
	editor.__editfunc = None
	editor.setValue(src1)
	editor.__editfunc = f

	def callfunc1():
		args = overlay._header1_controls['args'].value.split(',')
		try: f.apply(None, args)
		except:
			print 'ERROR in edited function: '+f.name
			debugger.onerror(__exception__, f,c)
	overlay._header1_controls['call'].onclick = callfunc1


	if c is not undefined:
		overlay._set_header( errtype + ' caused in call to: `' + c.name + '`')


		def callfunc2():
			args = overlay._header2_controls['args'].value.split(',')
			try: c.apply(None, args)
			except:
				print 'ERROR in edited function: '+c.name
				debugger.onerror(__exception__, f,c)

		overlay._header2_controls['call'].onclick = callfunc2

		src2 = debugger.getsource(c)
		editor2.__editfunc = None
		editor2.setValue(src2)
		editor2.__editfunc = c

		foundit = False
		for i,ln in enumerate(src2.splitlines()):
			for term in search:
				if term in ln:
					editor2.selection.moveTo(i,ln.index(term))
					editor2.selection.selectWord()
					if term.endswith('('):
						errmsg_custom.insert(0, 'the function')
					else:
						errmsg_custom.insert(0, 'the variable')
					errmsg = ' '.join(errmsg_custom)
					foundit = True
					break
			if foundit:
				break

		if foundit:
			overlay._set_header2( errmsg )
		else:
			overlay._set_header2( 'function: '+c.name )
			editor2.selection.clearSelection()


		for i,ln in enumerate(src1.splitlines()):
			if not foundit:
				for term in search:
					if term in ln:
						editor.selection.moveTo(i,ln.index(term))
						editor.selection.selectWord()
						if term.endswith('('):
							errmsg_custom.insert(0, 'the function')
						else:
							errmsg_custom.insert(0, 'the variable')
						errmsg = ' '.join(errmsg_custom)
						foundit = True
						break
				if foundit:
					break
			else:
				if c.name+'(' in ln:
					editor.selection.moveTo(i,ln.index(c.name))
					editor.selection.selectWord()
					break

		if foundit:
			editor.container.style.fontSize='18px'
			editor2.container.style.fontSize='12px'
			overlay._set_header( errmsg )
			overlay._set_subheader( errtype + ' caused in call to: `' + c.name + '`')

		if src1.splitlines().length > 15:
			editor.container.style.fontSize='14px'

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
	#mytypo()
	show( some_missing_object[ 'x' ] )
	a.x.y = 'oopps'
	show('bar OK')
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1
	b = 1+1


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