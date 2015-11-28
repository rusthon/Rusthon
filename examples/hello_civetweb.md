C++11 Webserver Example
-------------
* requires https://github.com/civetweb/civetweb
* ported from: https://github.com/civetweb/civetweb/blob/master/examples/embedded_cpp/embedded_cpp.cpp

Auto Build CivetWeb
----------
@https://github.com/civetweb/civetweb.git
```bash
make clean
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
	pass

def main():
	print 'init civet test...'
	let options : const char* = {'document_root', '.', 'listening_ports', '8080', 0}
	server = new CivetServer( options )
	print 'exit'
```