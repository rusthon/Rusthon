NodeJS fake Tornado module
-------

see [nodejs_tornado.py](../src/runtime/nodejs_tornado.py)


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
hello world from nodejs tornado web server
</body>
</html>

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
		guess = path
		if not path or path == '/': guess = 'index.html'
		#mime_type, encoding = mimetypes.guess_type(guess)
		#if mime_type: self.set_header("Content-Type", mime_type)

		if path == 'favicon.ico' or path.endswith('.map'):
			self.write('')
		else:
			self.write( open('index.html').read() )




## Tornado Handlers ##
Handlers = [
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
