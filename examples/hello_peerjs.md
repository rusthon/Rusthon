Peer.js Helloworld
--------

Simple chat example, for more info see:
http://peerjs.com/docs/

Get your own free peerjs key from below and replace APIKEY with it:
http://peerjs.com/peerserver


@app.js
```rusthon
#backend:javascript
from runtime import *

APIKEY = 'lwjd5qra8257b9'

PEERS = []
UID = None
peer = None

def send2peer():
	msg = document.getElementById('chat').value
	print 'sending', msg

	document.getElementById('container').appendChild(
		document.createTextNode('me>'+msg+'\n')
	)

	for con in PEERS:
		print con
		con.send(msg)

def connect2peer():
	uid = document.getElementById('peer').value
	con = peer.connect(uid)
	print 'connecting:', con
	PEERS.append(con)

	## show message from other peers ##
	def ondata(data):
		print 'ondata'
		document.getElementById('container').appendChild(
			document.createTextNode(con.peer+'>'+data+'\n')
		)

	con.on('data', ondata)

	def onclose():
		print 'peer closed!'


def onwindowload():
	global peer
	config = {
		key   : APIKEY,
		debug : 3,
		#config : {
		#	'iceServers': [
		#		{ url: 'stun:stun.l.google.com:19302' }
		#	]
		#}
	}
	peer = new(Peer(config))

	def onopen(uid):
		global UID
		print 'myuid', uid
		UID = uid
		document.getElementById('myid').value = uid

	peer.on('open', onopen)

	def onconnect(con):
		print 'connected to peer'
		PEERS.append(con)

	peer.on('connection', onconnect)


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
	<script src="http://cdn.peerjs.com/0.3/peer.min.js"></script>

</head>
<body>
<input type="text" id="myid" value=""/>

<p>
<input type="text" id="peer" value="peer-id"/>
<input type="button" onclick="javascript:connect2peer()" value="connect"/>
</p>
<p>
<input type="text" id="chat" value="..."/>
<input type="button" onclick="javascript:send2peer()" value="send"/>
</p>

<pre id="container"></pre>
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