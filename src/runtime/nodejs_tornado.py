__http = require('http')
__urlparser = require('url')


class tornado:
	@classmethod
	def HTTPError(self, code):
		return code

	class websocket:
		class WebSocketHandler:
			def __init__(self, client):
				self.request = {'connection': client }
				self.ws_connection = client

			def write_message(self, data, binary=False, mask=False):
				#if isinstance( data, dict):
				#	data = json.dumps( data )
				#	self.ws_connection.send( data, {'binary':False, 'mask':False} )
				#else:
				self.ws_connection.send( data, {'binary':binary, 'mask':mask} )

			## subclass overloads these
			def open(self):
				print 'on websocket open'

			def on_message(self, msg):
				print 'on websocket message'

			def on_close(self):
				print 'closed websocket connection'

	class web:
		class RequestHandler:
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
				self._response.writeHead(200, self._headers)
				self._response.write( data )
				self._response.end()

			def finish(self):
				self._response.end()


		class Application:
			def __init__(self, handlers):
				self._handlers = {}
				self._handler_keys = []
				#self._ws_handlers = {}  ## TODO support multiple websocket paths
				self._ws_handler = None
				for a in handlers:
					hclass = a[1]
					if issubclass( hclass, tornado.websocket.WebSocketHandler):
						#self._ws_handlers[ a[0] ] = hclass
						self._ws_handler = hclass
						self._ws_path = a[0]
					else:
						self._handlers[ a[0] ] = hclass
						self._handler_keys.append( a[0] )


				self._http_server = __http.createServer( self.on_request.bind(self) )

			def on_request(self, request, response):
				print 'got request'
				url = __urlparser.parse( request.url )
				print url.pathname
				handler = None
				prefix = None
				print self._handler_keys
				#for key in self._handlers:
				for key in self._handler_keys:
					print 'checking handler->', key
					if url.pathname.startswith(key):
						## note: new must be used here,
						## because the transpiler is unaware that the handler is a class.
						handler = new self._handlers[key]( response )
						handler.__init__(response)  ## TODO fix get_js_base_class_init
						prefix = key
						print 'GOT HANDLER', key
						break

				if handler:
					handler.set_header('Transfer-Encoding', 'chunked')
					s = url.pathname[len(prefix):]  ## strip prefix
					handler.get( path=s )  ## subclass of tornado.web.RequestHandler defines `get`
				else:
					print 'ERROR: no handler'
					print handler
					response.writeHead(404)
					response.end()

			def listen(self, port, address=""):
				print 'listening on:', port

				server = self._http_server

				if self._ws_handler:
					__ws = require('ws')  ## npm install ws
					wss = new( __ws.Server(server=server, path=self._ws_path) )
					print 'wss', wss
					self.wss = wss
					self.wss.on(
						'connection', 
						self.on_ws_connection.bind(self)
					)

				server.listen( port , address)

			def on_ws_connection(self, ws):  ## ws is a websocket client
				print 'new ws connection'
				handler = new(
					self._ws_handler( ws )
				)
				## TODO fix base class init for subclasses that are unaware of their parent class init
				handler.__init__(ws)
				handler.open()
				## handler.on_message will be called with: data, flags
				## flags.binary = true/false
				## flags.masked = true/false
				ws.on('message', handler.on_message.bind(self))


tornado.ioloop = {
			"IOLoop": {
				"instance" : lambda : {'start':lambda:None}
			} 
		}