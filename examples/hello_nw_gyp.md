NW.js C++ Extension
-------------
* https://github.com/nwjs/nw-gyp
* https://github.com/nodejs/node/blob/master/test/addons/hello-world/binding.cc


Gyp File
----------
```gyp
{
  'targets': [
    {
      'target_name': 'binding',
      'sources': [ 'binding.cc' ]
    }
  ]
}
```

Main Script
-------------

@binding.cc
```rusthon
#backend:c++
import node.h
import v8.h

namespace('v8')

def MyMethod(args : const FunctionCallbackInfo<Value>&):
	isolate = Isolate::GetCurrent()
	let scope(isolate) : HandleScope
	args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world".c_str() ))

def init(target: Local<Object>):
	NODE_SET_METHOD(target, "hello".c_str(), MyMethod)

NODE_MODULE(binding, init)

```

Nw.js
------
tests the c++ module from javascript

@myscript.js
```rusthon
#backend:javascript
mymodule = require('./build/Release/binding')
def test():
	alert( mymodule.hello() )

```

HTML
-----

@index.html
```html
<html>
<head>
<@myscript.js>
</head>
<body>
<button onclick="javascript:test()">clickme</button>
</body>
</html>
```