NodeJS fake Tornado module
-------

see [nodejs_tornado.py](../src/runtime/nodejs_tornado.py)

note: you need to install the nodejs module `ws`, run `sudo npm install -g ws`.

To run this example run these commands in your shell, nodejs will be used to run it:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/nodejs_tornado.md --run=myapp.js
```

Then open a web browser and go to http://localhost:8000

html
-----

@index.html
```html
<html>
<head>
</head>
<body>
<@myscript>
</body>
</html>
```

@myscript
```rusthon
#backend:javascript
from runtime import *

ws = None

def on_open_ws():
	print 'websocket open'
	ws.send('hello server')

def on_close_ws():
	print 'websocket close'

def on_message_ws(event):
	print 'on message', event
	print event.data

def connect_ws():
	global ws
	document.body.appendChild( document.createTextNode('testing websocket') )
	addr = 'ws://' + location.host + '/websocket'
	print 'websocket test connecting to:', addr
	ws = new( WebSocket(addr) )
	ws.binaryType = 'arraybuffer'
	ws.onmessage = on_message_ws
	ws.onopen = on_open_ws
	ws.onclose = on_close_ws
	print ws

connect_ws()

```


@myapp.js
```rusthon
#backend:javascript
from runtime import *
from nodejs import *
from nodejs.tornado import *

PORT = 8000

class MainHandler( tornado.web.RequestHandler ):

	def get(self, path=None):
		print('path', path)
		if path == 'favicon.ico' or path.endswith('.map'):
			self.write('')
		else:
			self.write( open('index.html').read() )


class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print( 'websocket open' )
		print( self.request.connection )
		self.write_message('hello client')

	def on_message(self, msg):
		print 'websocket - got %s bytes' %len(msg)
		print msg

	def on_close(self):
		print('websocket closed')
		if self.ws_connection:
			self.close()

## Tornado Handlers ##
Handlers = [
	('/websocket', WebSocketHandler),
	('/', MainHandler),  ## order is important, this comes last.
]

## main ##
def main():
	print('<starting tornado server>')
	app = new tornado.web.Application( Handlers )
	app.listen( PORT )
	tornado.ioloop.IOLoop.instance().start()

## start main ##
main()


```
