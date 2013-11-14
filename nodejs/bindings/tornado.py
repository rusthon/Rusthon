__http = require('http')
__urlparser = require('url')

class _fake_RequestHandler:
	def __init__(self, response):
		self._response = response

	def set_header(self, key, value):
		pass

	def write(self, data):
		self._response.write( data )
		self._response.end()

class _fake_app:
	def __init__(self, handlers):
		self._handlers = {}
		for a in handlers:
			self._handlers[ a[0] ] = a[1]

		self[...] = __http.createServer( self.on_request )

	def on_request(self, request, response):
		print 'got request'
		url = __urlparser.parse( request.url )
		print url.pathname
		hclass = self._handlers[ url.pathname ]
		handler = hclass( response )
		handler.get( url.pathname )

	def listen(self, port):
		print 'listening on:', port
		with javascript:
			self[...].listen( port )

class _fake_web:
	def __init__(self):
		self.RequestHandler = _fake_RequestHandler
		self.Application = _fake_app

	def HTTPError(self, code):
		return code

class _fake_WebSocketHandler:
	def __init__(self):
		self.ws_connection = None

	def open(self):
		pass

	def on_message(self, msg):
		pass

	def on_close(self):
		print 'closed connection'
		

class _fake_websocket:
	def __init__(self):
		self.WebSocketHandler = _fake_WebSocketHandler




class _fake_tornado:
	def __init__(self):
		self.web = _fake_web()
		self.websocket = _fake_websocket()

tornado = _fake_tornado()