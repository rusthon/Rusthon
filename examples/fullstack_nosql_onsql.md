FullStack Single File Example
-----------------------------

Fullstack is just a buzz word for a single programmer who fully implements the frontend and backend,
including webserver and database.  
On the frontend they handle all the javascript, html, css and frameworks like:
Angular.js.  In other words, it is a heavy job, with many things to manage.
Andy Shora has some interesting thoughts on it, check out
http://andyshora.com/full-stack-developers.html 

Reducing a fullstack into a single file makes things much simpler,
also using Python both on the backend and frontend greatly simplfies everything.



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
the tornado webserver saves objects into the database,
it gets from the client over the websocket.


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


class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print( 'websocket open' )
		print( self.request.connection )

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
			table.insert( ob )
			self.write_message( json.dumps('updated database:'+str(len(table))) )


	def on_close(self):
		print('websocket closed')
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
	else:
		pre.appendChild( document.createTextNode(msg+'\n') )

	print msg


def connect_ws():
	global ws
	print location.host
	addr = 'ws://' + location.host + '/websocket'
	print 'websocket test connecting to:', addr
	ws = new( WebSocket(addr) )
	ws.binaryType = 'arraybuffer'
	ws.onmessage = on_message_ws
	ws.onopen = on_open_ws
	ws.onclose = on_close_ws
	print ws


class Proxy:
	ids = 0
	def __init__(self):
		self.__id__ = Proxy.ids
		Proxy.ids += 1
		self._x = 0
		self._y = 0

		## request restore from server/database
		#msg = {RESTORE:self.__id__}
		#ws.send( JSON.stringify(msg) )

		## build widgets ##
		self._xe = document.createElement('input')
		self._xe.setAttribute('type', 'text')
		self._ye = document.createElement('input')
		self._ye.setAttribute('type', 'text')

		#@bind(self._xe.onkeypress, self)  ## TODO extra param `self`
		def update_xe(e):
			print 'update xe:' + self._xe.value
			self.x = self._xe.value
		self._xe.onkeypress = update_xe.bind(self)

		#@bind(self._ye.onkeypress, self)
		def update_ye(e):
			print 'update ye:' + self._ye.value
			self.y = self._ye.value
		self._ye.onkeypress = update_ye.bind(self)


	def restore(self, restore):
		for key in restore.keys():
			self[ '_' + key ] = restore[key]
			self[ '_' + key + 'e' ].value = restore[key]

	def getwidget(self):
		div = document.createElement('div')
		div.appendChild(document.createTextNode('x:'))
		div.appendChild( self._xe )
		div.appendChild(document.createElement('br'))
		div.appendChild(document.createTextNode('y:'))
		div.appendChild( self._ye )
		div.appendChild(document.createElement('br'))
		return div

	@getter
	def x(self):
		## note: can not do async request to server here,
		## this value is cached, and any updates server side
		## from other clients must be pushed to this instance
		## from the server through the websocket.
		return self._x

	@setter
	def x(self, v):
		print 'setter x:' + v
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
		print 'setter y:' + v
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
	global p
	## connect websocket
	#connect_ws()
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
<@myapp>
</head>
<body onload="main()">
<div id="FORM"></div>
<pre id="RESULTS">
</pre>
</body>
</html>
```