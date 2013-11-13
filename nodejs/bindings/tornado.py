class _fake_RequestHandler:
	def __init__(self):
		pass

	def set_header(self, key, value):
		pass

	def write(self, data):
		pass

class _fake_web:
	def __init__(self):
		self.RequestHandler = _fake_RequestHandler

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