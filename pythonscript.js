var create_array = function() {
var array = new Array();
var iter = range(arguments.length);
for (i=0; i < iter.length; i++) {
var backup = i
i = iter[i];
array.push(arguments[i]);
i = backup
}

return array;
}

var range = function(num) {
i = 0
r = []
while(i < num) {
r.push(i);
i = i + 1
}
return r;
}

var adapt_arguments = function(handler) {
var func = function() {
handler(Array.prototype.slice.call(arguments));
}

return func;
}

var create_object = function() {
object = {}
object.__class__ = klass
object.__dict__ = {}
init = get_attribute(object, "__init__")
if(init) {
init.apply(undefined, arguments);}

return object;
}

var create_class = function(class_name, parents, attrs) {
klass = {}
klass.bases = parents
klass.__name__ = class_name
klass.__dict__ = attrs
var __call__ = function() {
args = arguments.___insert(0, klass)
return create_object.apply(undefined, args);
}

klass.__call__ = create_object
return klass;
}

var get_attribute = function(object, attribute) {
if(attribute == "__call__") {
if({}.toString.call(object) === '[object Function]') {
return object;}
}

attr = object[attribute]
if(attr) {
return attr;}

__dict__ = object.__dict__
if(__dict__) {
attr = __dict__[attribute]
if(attr) {
return attr;}
}

__class__ = object.__class__
if(__class__) {
__dict__ = __class__.__dict__
attr = __dict__[attribute]
if(attr) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
arguments[0].splice(0, 0, object);
return attr.apply(undefined, arguments);
}

return method;}

return attr;}

bases = __class__.bases
var iter = range(bases.length);
for (i=0; i < iter.length; i++) {
var backup = i
i = iter[i];
base = bases[i]
attr = get_attribute(base, attribute)
if(attr) {
return attr;}

i = backup
}
}

return undefined;
}

var set_attribute = function(object, attr, value) {
__dict__ = object.__dict__
__dict__[attr] = value;
}

var get_arguments = function(signature, args, kwargs) {
out = {}
if(signature.args.length) {
argslength = signature.args.length}
else {
argslength = 0}

kwargslength = Object.keys(signature.kwargs).length
j = 0
var iter = range(argslength);
for (i=0; i < iter.length; i++) {
var backup = i
i = iter[i];
arg = signature.args[j]
if(kwargs) {
kwarg = kwargs[arg]
if(kwarg) {
out[arg] = kwarg;
delete kwargs[arg];}
else {
out[arg] = args[j];
j = j + 1}
}
else {
out[arg] = args[j];
j = j + 1}

i = backup
}

args = args.slice(j)
if(signature.vararg) {
out[signature.vararg] = args;}

if(signature.varkwarg) {
out[signature.varkwarg] = kwargs;}

return out;
}

StopIteration = {};
parents = create_array();
StopIteration = create_class("StopIteration", parents, StopIteration);
var len = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
return get_attribute(get_attribute(obj, "__len__"), "__call__")(create_array(), {});
}

var next = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
return get_attribute(get_attribute(obj, "next"), "__call__")(create_array(), {});
}

var map = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("func", "objs")};
var arguments = get_arguments(signature, args, kwargs);
objs = arguments["objs"];
func = arguments["func"];
out = get_attribute(list, "__call__")(create_array(), {});
set_attribute(out, "js_object", map(func, objs.js_object));
return out;
}

Iterator = {};
parents = create_array();
var Iterator____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj", "index")};
var arguments = get_arguments(signature, args, kwargs);
index = arguments["index"];
obj = arguments["obj"];
self = arguments["self"];
set_attribute(self, "obj", obj);
set_attribute(self, "index", index);
}

Iterator.__init__ = Iterator____init__;
var Iterator__next = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
if(get_attribute(self, "index") >= get_attribute(len, "__call__")(create_array(get_attribute(self, "obj")), {})) {
throw StopIteration}

item = None;
set_attribute(self, "index", self.index + 1);
return item;
}

Iterator.next = Iterator__next;
Iterator = create_class("Iterator", parents, Iterator);
list = {};
parents = create_array();
var list____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
set_attribute(self, "js_object", create_array());
}

list.__init__ = list____init__;
var list__append = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
__array.push(obj);
}

list.append = list__append;
var list__extend = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "other")};
var arguments = get_arguments(signature, args, kwargs);
other = arguments["other"];
self = arguments["self"];
var __iterator__ = other.__iter__()
try {
var obj = __iterator__.next();
while(true) {
self.append(obj);
var obj = __iterator__.next()
};
}
catch(__exception__) {
;
}

}

list.extend = list__extend;
var list__insert = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index", "obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
index = arguments["index"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
__array.splice(index, 0, obj);
}

list.insert = list__insert;
var list__remove = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
self = arguments["self"];
index = get_attribute(get_attribute(self, "index"), "__call__")(create_array(obj), {});
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}

list.remove = list__remove;
var list__pop = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
__array = get_attribute(self, "js_object");
return __array.pop();
}

list.pop = list__pop;
var list__index = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
return __array.indexOf(obj);
}

list.index = list__index;
var list__count = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
obj = arguments["obj"];
self = arguments["self"];
i = 0;
var __iterator__ = self.__iter__()
try {
var other = __iterator__.next();
while(true) {
if(other == obj) {
i = i + 1}

var other = __iterator__.next()
};
}
catch(__exception__) {
;
}

return i;
}

list.count = list__count;
var list__reverse = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}

list.reverse = list__reverse;
var list__shift = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
__array = get_attribute(self, "js_object");
return __array.shift();
}

list.shift = list__shift;
var list__slice = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
var arguments = get_arguments(signature, args, kwargs);
end = arguments["end"];
start = arguments["start"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
return __array.slice(start, end);
}

list.slice = list__slice;
var list____iter__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
self = arguments["self"];
return get_attribute(Iterator, "__call__")(create_array(self, 0), {});
}

list.__iter__ = list____iter__;
var list__get = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index")};
var arguments = get_arguments(signature, args, kwargs);
index = arguments["index"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
return __array[index];
}

list.get = list__get;
var list__set = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index", "value")};
var arguments = get_arguments(signature, args, kwargs);
value = arguments["value"];
index = arguments["index"];
self = arguments["self"];
__array = get_attribute(self, "js_object");
__array[index] = value;
}

list.set = list__set;
list = create_class("list", parents, list);
