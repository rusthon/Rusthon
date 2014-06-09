with javascript:
	__http = require('http')
	__urlparser = require('url')
	__ws = require('ws')  ## npm install ws

class _fake_RequestHandler:
	def __init__(self, response):
		self._response = response
		self._headers = {}

	def set_header(self, key, value):
		self._headers[ key ] = value
		if key == 'Content-Length':
			self._headers.pop( 'Transfer-Encoding' )
			print 'set Content-Length and popped Transfer-Encoding'
			print value
		elif key == 'Content-Type':
			print 'set Content-Type'
			print value

	def write(self, data):
		self._response.writeHead(200, self._headers[...])
		self._response.write( data )
		self._response.end()

	def finish(self):
		self._response.end()


class _fake_app:
	def __init__(self, handlers):
		self._handlers = {}
		self._handler_keys = []
		#self._ws_handlers = {}  ## TODO support multiple websocket paths
		self._ws_handler = None
		for a in handlers:
			hclass = a[1]
			if issubclass( hclass, _fake_WebSocketHandler):
				#self._ws_handlers[ a[0] ] = hclass
				self._ws_handler = hclass
				self._ws_path = a[0]
			else:
				self._handlers[ a[0] ] = hclass
				self._handler_keys.append( a[0] )


		self[...] = __http.createServer( self.on_request )

	def on_request(self, request, response):
		print 'got request'
		url = __urlparser.parse( request.url )
		print url.pathname
		handler = None
		prefix = None
		#for key in self._handlers:
		for key in self._handler_keys:
			print 'checking handler->', key
			if url.pathname.startswith(key):
				handler = self._handlers[key]( response )
				prefix = key
				print 'GOT HANDLER', key
				break

		if handler:
			handler.set_header('Transfer-Encoding', 'chunked')
			s = url.pathname[len(prefix):]  ## strip prefix
			handler.get( s )  ## subclass of tornado.web.RequestHandler defines `get`
		else:
			print 'ERROR: no handler'
			response.writeHead(404)
			response.end()

	def listen(self, port, address=""):
		print 'listening on:', port

		server = self[...]

		if self._ws_handler:
			options = {
				'server' : server,
				'path' : self._ws_path
			}
			with javascript:
				wss = new( __ws.Server(options[...]) )
			print 'wss', wss
			self.wss = wss
			self.wss.on('connection', self.on_ws_connection)

		server.listen( port , address)

	def on_ws_connection(self, ws):  ## ws is a websocket client
		print 'new ws connection'
		handler = self._ws_handler( ws )
		handler.open()
		## handler.on_message will be called with: data, flags
		## flags.binary = true/false
		## flags.masked = true/false
		ws.on('message', handler.on_message)



class _fake_web:
	def __init__(self):
		self.RequestHandler = _fake_RequestHandler
		self.Application = _fake_app

	def HTTPError(self, code):
		return code

class _fake_request:
	def __init__(self, client):
		self.connection = client

class _fake_WebSocketHandler:
	def __init__(self, client):
		self.request = _fake_request( client )
		self.ws_connection = client

	def write_message(self, data, binary=False, mask=False):
		if isinstance( data, dict):
			data = json.dumps( data[...] )
			self.ws_connection.send( data, {'binary':False, 'mask':False}[...] )
		else:
			self.ws_connection.send( data, {'binary':binary, 'mask':mask}[...] )

	## subclass overloads these
	def open(self):
		print 'on websocket open'

	def on_message(self, msg):
		print 'on websocket message'

	def on_close(self):
		print 'closed websocket connection'
		

class _fake_websocket:
	def __init__(self):
		self.WebSocketHandler = _fake_WebSocketHandler




class _fake_tornado:
	def __init__(self):
		self.web = _fake_web()
		self.websocket = _fake_websocket()
		with javascript:
			start = lambda : None
			self.ioloop = {
				"IOLoop": {
					"instance" : lambda : {'start':start}
				} 
			}

tornado = _fake_tornado()
