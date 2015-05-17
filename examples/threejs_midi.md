MIDI.js
-------

view at http://localhost:8000
install and run commands
```
cd
git clone https://github.com/mudcube/MIDI.js.git
cd Rusthon
./rusthon.py ./examples/threejs_midi.md --run=myserver.py
```


@index.html
```html
<html xmlns = "http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<!-- polyfill -->
	<script src="~/MIDI.js/inc/shim/Base64.js" type="text/javascript"></script>
	<script src="~/MIDI.js/inc/shim/Base64binary.js" type="text/javascript"></script>
	<script src="~/MIDI.js/inc/shim/WebAudioAPI.js" type="text/javascript"></script>
	<!-- midi.js package -->
	<script src="~/MIDI.js/js/midi/audioDetect.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/gm.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/loader.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.audiotag.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.webaudio.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/midi/plugin.webmidi.js" type="text/javascript"></script>
	<!-- utils -->
	<script src="~/MIDI.js/js/util/dom_request_xhr.js" type="text/javascript"></script>
	<script src="~/MIDI.js/js/util/dom_request_script.js" type="text/javascript"></script>
</head>
<body>
<script type="text/javascript">

window.onload = function () {
	console.log("hi...");
	MIDI.loadPlugin({
		soundfontUrl: "./soundfont/",
		instrument: "acoustic_grand_piano",
		onprogress: function(state, progress) {
			console.log(state, progress);
		},
		onsuccess: function() {
			var delay = 0; // play one note every quarter second
			var note = 50; // the MIDI note
			var velocity = 127; // how hard the note hits
			// play the note
			MIDI.setVolume(0, 127);
			MIDI.noteOn(0, note, velocity, delay);
			MIDI.noteOff(0, note, delay + 0.75);
		}
	});
};

</script>
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