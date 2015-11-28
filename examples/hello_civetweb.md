C++11 Webserver Example
-------------
* requires https://github.com/civetweb/civetweb
* for more info see https://github.com/civetweb/civetweb/blob/master/docs/Embedding.md

Auto Build CivetWeb
----------
@https://github.com/civetweb/civetweb.git
```bash
make lib WITH_CPP=1 WITH_WEBSOCKETS=1 WITH_IPV6=0 WITH_LUA=0 
sudo cp -v ./include/CivetServer.h /usr/local/include/.
sudo cp -v ./include/civetweb.h /usr/local/include/.
sudo cp -v libcivetweb.a /usr/local/lib/.
```

Main Script
-------------
* @link:civetweb
```rusthon
#backend:c++
import CivetServer.h
from time import sleep

class MyHandler( CivetHandler ):
	def __init__(self):
		print 'init MyHandler'

	def handleGet(self, server:CivetServer*, conn: struct mg_connection*) -> bool:
		mg_printf( conn, "hello world".c_str() )
		return True

def main():
	print 'init civet test...'
	let options : const char* = {'document_root', '.', 'listening_ports', '8080', 0}
	server = new CivetServer( options )
	handler = new MyHandler()
	server.addHandler("/helloworld", handler)
	sleep(30)
	print 'exit'
```