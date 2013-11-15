from nodejs.tornado import *

PAGE = """
<html>
<head>
<script type="text/javascript">
var ws = null;
function test() {
	console.log("trying to open new ws connection");
	ws = new WebSocket("ws://localhost:8080/websocket");
	ws.onopen = function() {
		ws.send("hello server")
	}
	ws.onmessage = function(e) {
		console.log(e.data)
	}
	ws.onclose = function() {
		console.log("ws closed")
	}
}

</script>

</head>
<body onload="test()">
<h1>websocket test</h1>
</body>
</html>
"""

class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		self.set_header("Content-Type", "text/html")
		self.write( PAGE )
		print 'send page'


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print 'websocket open'

	def on_message(self, msg, flags=None):
		print 'got message from client:', msg
		self.write_message( 'hi client' )


handlers = [
	('/websocket', WebSocketHandler),
	('/', MainHandler),
]

app = tornado.web.Application( handlers )
app.listen( 8080 )