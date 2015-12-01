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
	with pointers:
		args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world".c_str() ))

def init(target: Local<Object>):
	NODE_SET_METHOD(target, "hello".c_str(), MyMethod)

NODE_MODULE(binding, init)

```


var assert = require('assert');
var binding = require('./build/Release/binding');
assert.equal('world', binding.hello());
console.log('binding.hello() =', binding.hello());