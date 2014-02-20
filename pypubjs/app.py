# PythonJS Integrated Development Environment "pypubjs"
# by Brett Hartshorn - copyright 2014
# License: "New BSD"

nw_gui = require('nw.gui')
Reader = new( FileReader() )
Editors = {}

css_editor = ace.edit( 'EDITOR_CSS' )
css_editor.setTheme("ace/theme/monokai")
css_editor.getSession().setMode("ace/mode/css")
css_editor.setValue( 'body {\n  background-color:lightgray;\n}\n' )

js_body_editor = ace.edit( 'EDITOR_BODY_JS' )
js_body_editor.setTheme("ace/theme/monokai")
js_body_editor.getSession().setMode("ace/mode/javascript")
js_body_editor.setValue( 'console.log("hello world")' )

js_head_editor = ace.edit( 'EDITOR_HEAD_JS' )
js_head_editor.setTheme("ace/theme/monokai")
js_head_editor.getSession().setMode("ace/mode/javascript")
js_head_editor.setValue( '' )

py_body_editor = ace.edit( 'EDITOR_BODY_PY' )
py_body_editor.setTheme("ace/theme/monokai")
py_body_editor.getSession().setMode("ace/mode/python")
py_body_editor.setValue( 'def test():\n  window.alert("hello world")' )

py_head_editor = ace.edit( 'EDITOR_HEAD_PY' )
py_head_editor.setTheme("ace/theme/monokai")
py_head_editor.getSession().setMode("ace/mode/python")
py_head_editor.setValue( '' )


_html_ = """
<div class="well">
	<button class="btn" onclick="test()">
		clickme
	</button>
</div>
"""

html_editor = ace.edit( 'EDITOR_HTML' )
html_editor.setTheme("ace/theme/monokai")
html_editor.getSession().setMode("ace/mode/html")
html_editor.setValue( _html_ )

## setup default imports ##
def _make_list_item( url, ul, manager ):
	li = document.createElement('li')
	ul.appendChild( li )
	manager.append( url )
	li.setAttribute('class', 'well')

	edit = document.createElement('button')
	edit.setAttribute('class', 'btn btn-mini btn-success')
	edit.appendChild( document.createTextNode('edit') )
	li.appendChild( edit )

	rem = document.createElement('button')
	rem.setAttribute('class', 'btn btn-mini btn-danger')
	rem.appendChild( document.createTextNode('remove') )
	li.appendChild( rem )

	input = document.createElement('input')
	input.setAttribute('type', 'text')
	input.setAttribute('class', 'input-medium span5 pull-right')
	input.setAttribute('placeholder', url)
	li.appendChild( input )


CssImports = []
def add_css_import( url ):
	ul = document.getElementById('IMPORTS_CSS')
	_make_list_item( url, ul, CssImports )

for url in ['../external/css/bootstrap.css', '../external/css/darkstrap.css']:
	add_css_import( url )


#################### app compiler #####################
win = None
def compile_app():
	global win

	def on_loaded():
		dev = win.showDevTools()
		dev.resizeTo( win.width, 130)
		dev.moveTo( win.x, win.y + win.height + 20 )

		out = [
			'<html><head>',
			'<script src="../pythonjs.js"></script>'
		]

		for url in CssImports:
			out.append('<link rel="stylesheet" href="%s"/>' %url)

		out.append('<style type="text/css">')
		out.append( css_editor.getValue() )
		out.append('</style>')

		out.append('<script type="text/javascript">')
		out.append( js_head_editor.getValue() )
		out.append('</script>')

		def callback1(js):
			out.append('<script type="text/javascript">')
			out.append( js )
			out.append('</script>')
			out.append('</head>')

			out.append('<body>')
			out.append( html_editor.getValue() )

			## post init scripts ##
			out.append('<script type="text/javascript">')
			out.append( js_body_editor.getValue() )
			out.append('</script>')

			def callback2(js):
				out.append('<script type="text/javascript">')
				out.append( js )
				out.append('</script>')
				out.append('</body></html>')
				data = '\n'.join(out)
				print(data)
				win.window.document.write( data )

			translate( {'data':py_body_editor.getValue(),'callback': callback2} )

		translate( {'data':py_head_editor.getValue(),'callback': callback1} )

	if win is None:
		win = nw_gui.Window.open(
			'',
			width=480,
			height=350,
			toolbar=False,
			frame=True
		)
		win.on('loaded', on_loaded)

	else:
		#win.window.document.documentElement.innerHTML=""  ## broken?
		win.window.document.body.innerHTML=""
		on_loaded()


def open_editor_window( filename, data ):
	win = nw_gui.Window.open(
		'editor.html',
		title=filename,
		width=700,
		height=550,
		toolbar=False,
		frame=True
	)
	def loaded():
		win.window.editor.setValue(data)
	win.on('loaded', loaded)
	Editors[ filename ] = win


def allow_drop(e):
	e.preventDefault()

def on_drop(e):
	print 'on-drop', e
	e.preventDefault()
	#url = e.dataTransfer.getData("text/uri-list")
	#url = e.dataTransfer.getData("text/plain")
	if e.dataTransfer.files.length:
		file = e.dataTransfer.files[0]
		print file.path
		with javascript:
			def custom_on_load(event):
				contents = event.target.result
				print contents
				print 'contents loaded for file: ' + file.name
				ul = document.getElementById('python_files')
				li = document.createElement('li')
				ul.appendChild( li )

				li.appendChild( document.createTextNode(file.name+' ') )


				def on_click(e):
					open_editor_window( file.name, contents )
				bu = document.createElement('button')
				bu.setAttribute('class', 'btn btn-warning')
				bu.addEventListener('click', on_click)
				bu.appendChild( document.createTextNode('edit') )
				li.appendChild( bu )


		Reader.onload = custom_on_load
		Reader.readAsText( file )

