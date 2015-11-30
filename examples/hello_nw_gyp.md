NW.js C++ Extension
-------------
* https://github.com/nwjs/nw-gyp
* for more info see https://github.com/civetweb/civetweb/blob/master/docs/Embedding.md

Gyp File
----------
@binding.gyp
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
	#Isolate* isolate = Isolate::GetCurrent();
	#HandleScope scope(isolate);
	#args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world"));

	isolate = Isolate::GetCurrent()
	scope = HandleScope(isolate)
	args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world"));

def init(target: Handle<Object>):
	NODE_SET_METHOD(target, "hello", MyMethod)

NODE_MODULE(binding, init)

```


var assert = require('assert');
var binding = require('./build/Release/binding');
assert.equal('world', binding.hello());
console.log('binding.hello() =', binding.hello());