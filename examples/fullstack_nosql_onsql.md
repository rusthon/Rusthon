FullStack Single File Example
-----------------------------

Fullstack development includes: webserver, database, object relational mapping, javascript and html with css.
This example includes all of these in a single file, in less than 300 lines of code.

Dataset
--------
Dataset is a database abstraction layer that makes using SQL dead simple.

https://dataset.readthedocs.org/en/latest/

```
git clone git://github.com/pudo/dataset.git
cd dataset/
sudo python setup.py install
```

Tornado Server
-------------
the tornado webserver saves objects into the SQL database using Dataset.

```
./rusthon.py ./examples/hello_fullstack.md --run=myserver.py
```

@myserver.py
```python
#!/usr/bin/python
import dataset
import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import os, sys, subprocess, datetime, json, time, mimetypes

PORT = int(os.environ.get("PORT", 8000))

## connect to database ##
##db = dataset.connect('sqlite:///mydatabase.db')
db = dataset.connect('sqlite:///:memory:')

# dataset will get or create `mytable`
table = db['mytable']


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
			self.write( open(path).read() )
		else:
			self.write( open('index.html').read() )


Clients = []

class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print( 'websocket open' )
		print( self.request.connection )
		Clients.append( self )

	def on_message(self, msg):
		ob = json.loads( msg )
		## if a simple test string ##
		if isinstance(ob, str):
			print ob
		elif isinstance(ob, list):
			print 'doing database search'
			results = []
			for search in ob:
				assert isinstance(search, dict)
				## `**search` unpacks to something like `name="foo"`
				r = table.find_one( **search )
				if r: results.append(r)
			if results:
				print results
				self.write_message(json.dumps(results))
			else:
				self.write_message(json.dumps("nothing found in databases"))

		elif isinstance(ob, dict):
			print 'saving object into database'
			print ob
			if len( list(table.find(id=ob['id'])) ):
				table.update( ob, ['id'] )
			else:
				table.insert( ob )
			self.write_message( json.dumps('updated database:'+str(ob)) )

			for other in Clients:
				if other is self: continue
				print 'updating other client with new data'
				other.write_message( msg )

	def on_close(self):
		print('websocket closed')
		if self in Clients:
			Clients.remove( self )
		if self.ws_connection:
			self.close()



## Tornado Handlers ##
Handlers = [
	(r'/websocket', WebSocketHandler),
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]

print('<starting tornado server>')
app = tornado.web.Application(
	Handlers,
	#cookie_secret = 'some random text',
	#login_url = '/login',
	#xsrf_cookies = False,
)
app.listen( PORT )
tornado.ioloop.IOLoop.instance().start()

```

Client Side
-----------


@myapp
```rusthon
#backend:javascript
from runtime import *

ws = None

def on_open_ws():
	print 'websocket open'
	ws.send(JSON.stringify('hello server'))

def on_close_ws():
	print 'websocket close'

def on_message_ws(event):
	print 'on message', event
	msg = None
	if instanceof(event.data, ArrayBuffer):
		print 'got binary bytes', event.data.byteLength
		arr = new(Uint8Array(event.data))
		txt = String.fromCharCode.apply(None, arr)
		msg = JSON.parse(txt)
	else:
		msg = JSON.parse(event.data)

	pre = document.getElementById('RESULTS')
	if isinstance(msg, list):
		for res in msg:
			s = JSON.stringify(res)
			pre.appendChild( document.createTextNode(s+'\n') )
	elif isinstance(msg, string):
		pre.appendChild( document.createTextNode(msg+'\n') )
	else:
		proxy = man.instances[ msg.id ]
		#a = { msg['key'] : msg['value'] }  ## TODO support this syntax
		a = {}
		a[ msg['key'] ] = msg['value']
		proxy.restore( a )


def connect_ws():
	global ws
	addr = 'ws://' + location.host + '/websocket'
	print 'websocket test connecting to:', addr
	ws = new( WebSocket(addr) )
	ws.binaryType = 'arraybuffer'
	ws.onmessage = on_message_ws
	ws.onopen = on_open_ws
	ws.onclose = on_close_ws


class Proxy:
	ids = 0
	def __init__(self):
		self.__id__ = Proxy.ids
		Proxy.ids += 1
		with 𝕚𝕟𝕡𝕦𝕥 as "%s=_=document.createElement('input');_.setAttribute('type','text');%s=0;":
			𝕚𝕟𝕡𝕦𝕥( self._xe, self._x )
			𝕚𝕟𝕡𝕦𝕥( self._ye, self._y )

		@bind(self._xe.onkeyup, self)
		def update_xe(e):
			print 'update xe:' + self._xe.value
			self.x = self._xe.value

		@bind(self._ye.onkeyup, self)
		def update_ye(e):
			print 'update ye:' + self._ye.value
			self.y = self._ye.value


	def restore(self, restore):
		for key in restore.keys():
			self[ '_' + key ] = restore[key]
			self[ '_' + key + 'e' ].value = restore[key]

	def getwidget(self):
		div = document.createElement('div')
		with 𝓕 as "div.appendChild(document.createTextNode(%s));div.appendChild(%s);div.appendChild(document.createElement('br'))":
			𝓕('some field X:', self._xe )
			𝓕('some field Y:', self._ye )
		return div

	@getter
	def x(self):
		return self._x
	@setter
	def x(self, v):
		if v != self._x:
			msg = {id:self.__id__, key:'x', value:v}
			ws.send( JSON.stringify(msg) )
			self._x = v
			self._xe.value = v  ## updates widget

	@getter
	def y(self):
		return self._y
	@setter
	def y(self, v):
		if v != self._y:
			msg = {id:self.__id__, key:'y', value:v}
			ws.send( JSON.stringify(msg) )
			self._y = v
			self._ye.value = v  ## updates widget

class Manager:
	def __init__(self):
		self.instances = {}
	def makeproxy(self):
		p = new Proxy()
		self.instances[p.__id__] = p
		return p

@debugger
def main():
	global man, p
	## connect websocket
	connect_ws()
	man = Manager()
	con = document.getElementById('FORM')
	h = document.createElement('h3')
	h.appendChild(document.createTextNode('update database:'))
	con.appendChild(h)
	p = man.makeproxy()
	con.appendChild(p.getwidget())

```

HTML
-----

@index.html
```html
<html>
<head>
<link href='~/bootstrap-3.3.5-dist/css/bootstrap.css' rel='stylesheet' zip="https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip"/>
<script src="~/rusthon_cache/jquery-2.1.4.min.js" source="http://code.jquery.com/jquery-2.1.4.min.js"></script>
<script src="~/bootstrap-3.3.5-dist/js/bootstrap.min.js"></script>
<@myapp>
</head>
<body onload="main()">
<div id="FORM" class="well"></div>
<pre id="RESULTS" class="well">
</pre>
</body>
</html>
```