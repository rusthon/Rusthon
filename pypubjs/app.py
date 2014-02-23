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
	def func():
		print('opening', url)
		open_editor_window( url, open(os.path.join('pypubjs',url), 'r').read() )

	edit.addEventListener('click', func)

	li.appendChild( edit )

	rem = document.createElement('button')
	rem.setAttribute('class', 'btn btn-mini btn-danger')
	rem.appendChild( document.createTextNode('remove') )
	def func():
		print('removing:', url)
		li.style.display = 'none'
		manager.remove(url)

	rem.addEventListener('click', func)
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

JsImports = []
def add_js_import( url ):
	ul = document.getElementById('IMPORTS_JS')
	_make_list_item( url, ul, JsImports )
for url in ['../pythonjs.js', '../external/jquery/jquery-latest.js', '../external/bootstrap/bootstrap.min.js']:
	add_js_import( url )

#################### app compiler #####################
win = None
def compile_app():
	global win

	def on_loaded():
		dev = win.showDevTools()
		dev.resizeTo( win.width, 130)
		dev.moveTo( win.x, win.y + win.height + 20 )

		out = ['<html><head>']

		for url in CssImports:
			out.append('<link rel="stylesheet" href="%s"/>' %url)

		out.append('<style type="text/css">')
		out.append( css_editor.getValue() )
		out.append('</style>')

		for url in JsImports:
			out.append( '<script type="text/javascript" src="%s"></script>'%url )
		
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

viswin = None
def vis_python():
	print('vis_python..............')
	global viswin

	def loaded():
		def callback(code):
			viswin.window.document.body.innerHTML = ""
			out = [
				'<html><head>',
				'<script src="../external/vis.js/vis.min.js"></script>',
				'<body>'
			]
			out.append( code )
			out.append('</body></html>')
			data = '\n'.join(out)
			print(data)
			viswin.window.document.write( data )

		translate( {'data':py_body_editor.getValue(),'callback': callback, 'vis':True} )

	if viswin is None:
		viswin = nw_gui.Window.open(
			'_blank',
			title='code graph',
			width=500,
			height=600,
			toolbar=False,
			frame=True
		)
		viswin.on('loaded', loaded)
	else:
		loaded()


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

		if file.path.endswith('.css'):
			add_css_import( file.path )
		elif file.path.endswith('.js'):
			add_js_import( file.path )
		elif file.path.endswith('.jpg') or file.path.endswith('.png'):
			ul = document.getElementById('IMAGES')
			li = ul.getElementsByTagName('li')[-1]
			#li = document.createElement('div')
			#ul.appendChild(li)
			print(len(li.childNodes))
			img = document.createElement('img')
			img.setAttribute('src', file.path)
			img.setAttribute('class', 'well img-rounded')
			img.setAttribute('width', '25%')
			li.appendChild( img )

			txt = html_editor.getValue()
			html_editor.setValue(txt+'\n<img src="%s"/>'%file.path)

		elif file.path.endswith('.mp4'):
			ul = document.getElementById('VIDEOS')
			li = ul.getElementsByTagName('li')[-1]
			video = document.createElement('video')
			video.setAttribute('width', '320')
			video.setAttribute('height', '240')
			video.setAttribute('controls', 'true')
			source = document.createElement('source')
			source.setAttribute('src', file.path)
			source.setAttribute('type', 'video/mp4')
			video.appendChild( source )
			li.appendChild( video )

		elif file.path.endswith('.mp3'):
			ul = document.getElementById('AUDIO')
			li = ul.getElementsByTagName('li')[-1]
			audio = document.createElement('audio')
			audio.setAttribute('autoplay', 'autoplay')
			audio.setAttribute('src', file.path)
			audio.setAttribute('controls', 'controls')
			source = document.createElement('source')
			source.setAttribute('src', file.path)
			source.setAttribute('type', 'audio/mpeg')
			audio.appendChild( source )
			li.appendChild( audio )

		elif file.path.endswith('.py'):
			def on_load(event):
				contents = event.target.result
				py_body_editor.setValue( contents )

			Reader.onload = on_load
			Reader.readAsText( file )

