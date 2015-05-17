Three.js and MIDI.js Example
-------

view at http://localhost:8000
install and run commands
```
cd
git clone https://github.com/mudcube/MIDI.js.git
git clone https://github.com/reality3d/3d-piano-player.git
cd Rusthon
./rusthon.py ./examples/threejs_midi.md --run=myserver.py
```

MIDI App
--------

@app.js
```rusthon
#backend:javascript

def onwindowload():
	def onloadplug():

		## play test note
		delay = 0.8
		note = 50
		velocity = 127
		MIDI.setVolume(0, 127)
		MIDI.noteOn(0, note, velocity, delay)
		MIDI.noteOff(0, note, delay)

		def onmidievent(data):
			print 'midi event'
			print data
			pianoKey = data.note - MIDI.pianoKeyOffset - 3
			if data.message == 144:
				print 'note on', pianoKey
			else:
				print 'note off', pianoKey
		MIDI.Player.addListener(onmidievent)
		MIDI.Player.timeWarp = 1.0 # speed the song is played back

		def onmidiload():
			print 'midi file loaded'
			MIDI.Player.start()

		MIDI.Player.loadFile("~/3d-piano-player/midi/bach_846.mid", onmidiload)


	MIDI.loadPlugin({
		'onsuccess' : onloadplug,
		'soundfontUrl': "./soundfont/",
		'instrument': "acoustic_grand_piano",
		'onprogress': lambda state, progress: console.log(state, progress),
	})


window.onload = onwindowload

```



HTML
----

@index.html
```html
<html xmlns = "http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<!-- shim -->
	<script src="~/MIDI.js/inc/shim/Base64.js" type="text/javascript"></script>
	<script src="~/MIDI.js/inc/shim/Base64binary.js" type="text/javascript"></script>
	<script src="~/MIDI.js/inc/shim/WebAudioAPI.js" type="text/javascript"></script>
	<script src="~/MIDI.js/inc/shim/WebMIDIAPI.js" type="text/javascript"></script>
	<!-- jasmid package -->
	<script src="~/MIDI.js/inc/jasmid/stream.js"></script>
	<script src="~/MIDI.js/inc/jasmid/midifile.js"></script>
	<script src="~/MIDI.js/inc/jasmid/replayer.js"></script>

	<!-- midi.js package -->
	<script src="~/MIDI.js/js/midi/audioDetect.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/gm.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/loader.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.audiotag.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.webaudio.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.webmidi.js" type="text/javascript"></script>

	<script src="~/MIDI.js/js/midi/player.js" type="text/javascript"></script>

	<!-- utils -->
	<script src="~/MIDI.js/js/util/dom_request_xhr.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/util/dom_request_script.js" type="text/javascript"></script>
</head>
<body>
<@app.js>
</body>
</html>

```

@myserver.py
```python
#!/usr/bin/python

PORT = int(os.environ.get("PORT", 8000))

## inlines rusthon into script ##
from rusthon import *
import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import os, sys, subprocess, datetime, json, time, mimetypes


class MainHandler( tornado.web.RequestHandler ):

	def get(self, path=None):
		print('path', path)
		guess = path
		if not path or path == '/': guess = 'index.html'
		mime_type, encoding = mimetypes.guess_type(guess)
		if mime_type: self.set_header("Content-Type", mime_type)

		if path == 'favicon.ico' or path.endswith('.map'):
			self.write('')

		elif path.startswith('~/3d-piano-player/midi'):
			path = os.path.expanduser(path)
			self.write( open(path, 'rb').read() )

		elif path and '.' in path:
			path = os.path.join(
				os.path.expanduser('~/MIDI.js/examples'),
				path
			)
			self.write( open(path).read() )
		else:
			self.write( open('index.html').read() )


## Tornado Handlers ##
Handlers = [
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]

## main ##
def main():
	print('<starting tornado server>')
	app = tornado.web.Application(
		Handlers,
		#cookie_secret = 'some random text',
		#login_url = '/login',
		#xsrf_cookies = False,
	)
	app.listen( PORT )
	tornado.ioloop.IOLoop.instance().start()

## start main ##
main()

```