## TODO clean up below using @bind

def __debugger_overlay():
	overlay = document.getElementById('DEBUG_OVERLAY')
	if overlay is None:
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

		if ace is not undefined:
			overlay.style.opacity = 0.9

			editor = ace.edit('EDITOR1')
			editor.__function = None
			editor.on('input', __redef_on_edit)
			editor.setTheme("ace/theme/monokai")
			editor.getSession().setMode("ace/mode/javascript")
			editor.renderer.setOption('showLineNumbers', false)
			editor.setOption("maxLines", 100)
			editor.setOption("minLines", 2)

			editor2 = ace.edit('EDITOR2')
			editor2.__function = None
			editor2.on('input', __redef_on_edit)

			editor2.setTheme("ace/theme/monokai")
			editor2.getSession().setMode("ace/mode/javascript")
			editor2.renderer.setOption('showLineNumbers', false)
			editor2.setAutoScrollEditorIntoView(true)
			editor2.setOption("maxLines", 100)
			editor2.setOption("minLines", 2)

		else:
			editor = document.createElement('textarea')
			editor2 = document.createElement('textarea')
			ediv1.appendChild(editor)
			ediv2.appendChild(editor2)

			editor.rows = 12
			editor.cols = 70

			editor2.rows = 12
			editor2.cols = 70

			editor.container = ediv1
			editor2.container = ediv2

			editor.appendChild(document.createTextNode(''))
			editor2.appendChild(document.createTextNode(''))

			def __getValue():
				return this.firstChild.nodeValue
			def __setValue(txt):
				this.firstChild.nodeValue = txt

			editor.getValue = __getValue
			editor.setValue = __setValue
			editor2.getValue = __getValue
			editor2.setValue = __setValue

			def __pass(): pass
			__selection = {
				'moveTo' : __pass,
				'selectWord' : __pass,
				'clearSelection' : __pass
			}
			editor.selection = __selection
			editor2.selection = __selection

	overlay.editor1 = editor
	overlay.editor2 = editor2
	return overlay


def __debugger_onerror_overlay(err,f,c):
	if err.stack is undefined:
		## why is the stack empty from TypeError thrown from the runtime type checking?
		inline('throw err')

	if err._skip is not undefined:
		return False
	err._skip = True
	debugger.log(err,f,c)

	if document is undefined:  ## inside nodejs
		return

	overlay = __debugger_overlay()
	editor = overlay.editor1
	editor2 = overlay.editor2

	errtype, errmsg = err.stack.splitlines()[0].split(':')
	errmsg = errmsg.strip()
	errvar = errmsg.split()[0]

	search = []
	#if errtype == 'ReferenceError':
	search.append( errvar + '.' )  ## checks for attributes
	search.append( errvar + '(' )  ## checks for func calls
	search.append( errvar + '[' )  ## checks for func calls
	#search.append(errvar)  ## the logic below needs to be smarter to fallback on this

	errmsg_custom = []
	for i,word in enumerate(errmsg.split()):
		if i==0:
			errmsg_custom.append('`' + word + '`')
		else:
			errmsg_custom.append(word)


	src1 = debugger.getsource(f)
	editor.__editfunc = None
	editor.setValue(src1)
	editor.__editfunc = f

	def callfunc1():
		f.redefine(editor.getValue())
		args = overlay._header1_controls['args'].value.split(',')
		try: f.apply(None, args)
		except:
			print 'ERROR in edited function: '+f.name
			#debugger.onerror(__exception__, f,c)

	overlay._header1_controls['call'].onclick = callfunc1

	if c is not undefined:
		overlay._set_header( errtype + ' caused in call to: `' + c.name + '`')

		def callfunc2():
			c.redefine(editor2.getValue())
			args = overlay._header2_controls['args'].value.split(',')
			try: c.apply(None, args)
			except:
				print 'ERROR in edited function: '+c.name
				#debugger.onerror(__exception__, f,c)
				#raise __exception__

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

			for i,ln in enumerate(src1.splitlines()):
				if c.name+'(' in ln:
					editor.selection.moveTo(i,ln.index(c.name))
					editor.selection.selectWord()
					break
		else:
			overlay._set_header2( 'function: '+c.name )
			editor2.selection.clearSelection()

			for i,ln in enumerate(src1.splitlines()):
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

			if foundit:
				editor.container.style.fontSize='18px'
				editor2.container.style.fontSize='12px'
				overlay._set_header( errmsg )
				overlay._set_subheader( errtype + ' caused in call to: `' + c.name + '`')

		if src1.splitlines().length > 15:
			editor.container.style.fontSize='14px'

	## returns True uses injected breakpoints
	if debugger.breakpoints:
		return True
	else:
		return False


def __debugger_clean_source(f):
	source = []
	for line in f.toString().splitlines():
		if line.strip().startswith('/***/'):  ## skip injected try/catch for debugger
			continue
		else:
			source.append(line)
	return '\n'.join(source)

def __debugger_log(e,f, called):
	console.error(e.stack)
	console.error('ABORT function->' + f.name)
	#console.warn(f.toString())
	print debugger.getsource( f )

	badline = None
	for line in e.stack.splitlines():
		if line.strip().startswith('at '):
			fname = line.split('(')[0][6:].strip()
			console.warn('  error in function->' + fname)
			if badline is None:
				badline = fname
			if fname == f.name:
				break
		else:
			console.error(line)

	if called is not undefined:
		console.error('exception in function->'+called.name)
		print debugger.getsource(called)

	return True  ## if returns True then halt (breakpoint)


debugger = {
	'log'     : __debugger_log,
	'onerror' : __debugger_onerror_overlay,  ## by default do not use breakpoints
	'getsource' : __debugger_clean_source,
	'showdevtools' : lambda : require('nw.gui').Window.get().showDevTools(),
	'breakpoints'  : False,
}
