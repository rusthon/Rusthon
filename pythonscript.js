// PythonScript Runtime - regenerated on: Tue Oct 15 19:07:52 2013
var jsrange = function(num) {
"Emulates Python's range function";
var i, r;
i = 0;
r = [];
while(i < num) {
r.push(i);
i = i + 1;
}
return r;
}
window["jsrange"] = jsrange 

var create_array = function() {
"Used to fix a bug/feature of Javascript where new Array(number)\n    created a array with number of undefined elements which is not\n    what we want";
var array;
array = [];
var iter = jsrange(arguments.length);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
array.push(arguments[i]);
i = backup;
}

return array;
}
window["create_array"] = create_array 

var adapt_arguments = function(handler) {
"Useful to transform Javascript arguments to Python arguments";
var func = function() {
handler(Array.prototype.slice.call(arguments));
}

return func;
}
window["adapt_arguments"] = adapt_arguments 

var create_class = function(class_name, parents, attrs) {
"Create a PythonScript class";
if(attrs.__metaclass__) {
var metaclass;
metaclass = attrs.__metaclass__;
attrs.__metaclass__ = undefined;
return metaclass([class_name, parents, attrs]);
}

var klass;
klass = Object();
klass.bases = parents;
klass.__name__ = class_name;
klass.__dict__ = attrs;
var __call__ = function() {
"Create a PythonScript object";
var object;
object = Object();
object.__class__ = klass;
object.__dict__ = Object();
var init;
init = get_attribute(object, "__init__");
if(init) {
init.apply(undefined, arguments);
}

return object;
}

__call__.pythonscript_function = true;
klass.__call__ = __call__;
return klass;
}
window["create_class"] = create_class 

var get_attribute = function(object, attribute) {
"Retrieve an attribute, method, property, or wrapper function.\n\n    method are actually functions which are converted to methods by\n    prepending their arguments with the current object. Properties are\n    not functions!\n\n    DOM support:\n        http://stackoverflow.com/questions/14202699/document-createelement-not-working\n        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof\n\n    Direct JavaScript Calls:\n        if an external javascript function is found, and it was not a wrapper that was generated here,\n        check the function for a 'cached_wrapper' attribute, if none is found then generate a new\n        wrapper, cache it on the function, and return the wrapper.\n    ";
if(attribute == "__call__") {
if({}.toString.call(object) === '[object Function]') {
if(object.pythonscript_function === true) {
return object;
}
else {
if(object.is_wrapper !== undefined) {
return object;
}
else {
var cached = object.cached_wrapper;
if(cached) {
return cached;
}
else {
var wrapper = function(args, kwargs) {
return object.apply(undefined, args);
}

wrapper.is_wrapper = true;
object.cached_wrapper = wrapper;
return wrapper;
}

}

}

}

}

var attr;
attr = object[attribute];
if(object instanceof HTMLDocument) {
if(typeof(attr) === 'function') {
var wrapper = function(args, kwargs) {
return attr.apply(object, args);
}

wrapper.is_wrapper = true;
return wrapper;
}
else {
return attr;
}

}
else {
if(object instanceof HTMLElement) {
if(typeof(attr) === 'function') {
var wrapper = function(args, kwargs) {
return attr.apply(object, args);
}

wrapper.is_wrapper = true;
return wrapper;
}
else {
return attr;
}

}

}

if(attr !== undefined) {
if(typeof(attr) === 'function' && attr.pythonscript_function === undefined && attr.is_wrapper === undefined) {
var wrapper = function(args, kwargs) {
return attr.apply(object, args);
}

wrapper.is_wrapper = true;
return wrapper;
}
else {
return attr;
}

}

var __class__, __dict__, __get__, bases;
__class__ = object.__class__;
if(__class__) {
__dict__ = __class__.__dict__;
attr = __dict__[attribute];
if(attr) {
__get__ = get_attribute(attr, "__get__");
if(__get__) {
return __get__([object, __class__]);
}

}

bases = __class__.bases;
var iter = jsrange(bases.length);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
var base, attr;
base = bases[i];
attr = get_attribute(base, attribute);
if(attr) {
__get__ = get_attribute(attr, "__get__");
if(__get__) {
return __get__([object, __class__]);
}

}

i = backup;
}

}

__dict__ = object.__dict__;
bases = object.__bases__;
if(__dict__) {
attr = __dict__[attribute];
if(attr != undefined) {
if(bases) {
__get__ = get_attribute(attr, "__get__");
if(__get__) {
return __get__([undefined, __class__]);
}

}

return attr;
}

}

if(bases) {
var iter = jsrange(bases.length);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
var base, attr;
base = bases[i];
attr = get_attribute(base, attribute);
if(attr) {
__get__ = get_attribute(attr, "__get__");
if(__get__) {
return __get__([object, __class__]);
}

}

i = backup;
}

}

if(__class__) {
var __dict__;
__dict__ = __class__.__dict__;
attr = __dict__[attribute];
if(attr) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
var args;
args = arguments;
if(args.length > 0) {
args[0].splice(0, 0, object);
}
else {
args = [object];
}

return attr.apply(undefined, args);
}

method.is_wrapper = true;
return method;
}
else {
return attr;
}

}

bases = __class__.bases;
var iter = jsrange(bases.length);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
var base, attr;
base = bases[i];
attr = get_attribute(base, attribute);
if(attr) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
var args;
args = arguments;
if(args.length > 0) {
args[0].splice(0, 0, object);
}
else {
args = [object];
}

return attr.apply(undefined, args);
}

method.is_wrapper = true;
return method;
}
else {
return attr;
}

}

i = backup;
}

}

if(object instanceof Array) {
if(attribute == "__getitem__") {
var wrapper = function(args, kwargs) {
return object[args[0]];
}

wrapper.is_wrapper = true;
return wrapper;
}
else {
if(attribute == "__setitem__") {
var wrapper = function(args, kwargs) {
object[args[0]] = args[1];
}

wrapper.is_wrapper = true;
return wrapper;
}

}

}
else {
if(attribute == "__getitem__") {
var wrapper = function(args, kwargs) {
return object[args[0]];
}

wrapper.is_wrapper = true;
return wrapper;
}
else {
if(attribute == "__setitem__") {
var wrapper = function(args, kwargs) {
object[args[0]] = args[1];
}

wrapper.is_wrapper = true;
return wrapper;
}

}

}

return undefined;
}
window["get_attribute"] = get_attribute 

var set_attribute = function(object, attribute, value) {
"Set an attribute on an object by updating its __dict__ property";
var __dict__, __class__;
__class__ = object.__class__;
if(__class__) {
var attr, bases;
__dict__ = __class__.__dict__;
attr = __dict__[attribute];
if(attr != undefined) {
__set__ = get_attribute(attr, "__set__");
if(__set__) {
__set__([object, value]);
return undefined;
}

}

bases = __class__.bases;
var iter = jsrange(bases.length);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
var base;
base = bases[i];
attr = get_attribute(base, attribute);
if(attr) {
__set__ = get_attribute(attr, "__set__");
if(__set__) {
__set__([object, value]);
return undefined;
}

}

i = backup;
}

}

__dict__ = object.__dict__;
if(__dict__) {
__dict__[attribute] = value;
}
else {
object[attribute] = value;
}

}
window["set_attribute"] = set_attribute 

set_attribute.pythonscript_function = true;
var get_arguments = function(signature, args, kwargs) {
"Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve\n    the actual parameters.\n\n    This will set default keyword arguments and retrieve positional arguments\n    in kwargs if their called as such";
if(args === undefined) {
args = [];
}

if(kwargs === undefined) {
kwargs = Object();
}

out = Object();
if(signature.args.length) {
argslength = signature.args.length;
}
else {
argslength = 0;
}

if(args.length > signature.args.length) {
console.log("ERROR args:", args, "kwargs:", kwargs, "sig:", signature);
throw TypeError("function called with wrong number of arguments");
}

j = 0;
while(j < argslength) {
arg = signature.args[j];
if(kwargs) {
kwarg = kwargs[arg];
if(arg  in  kwargs) {
out[arg] = kwarg;
}
else {
if(j < args.length) {
out[arg] = args[j];
}
else {
if(arg  in  signature.kwargs) {
out[arg] = signature.kwargs[arg];
}
else {
console.log("ERROR args:", args, "kwargs:", kwargs, "sig:", signature, j);
throw TypeError("function called with wrong number of arguments");
}

}

}

}
else {
if(j < args.length) {
out[arg] = args[j];
}
else {
if(arg  in  signature.kwargs) {
out[arg] = signature.kwargs[arg];
}
else {
console.log("ERROR args:", args, "kwargs:", kwargs, "sig:", signature, j);
throw TypeError("function called with wrong number of arguments");
}

}

}

j += 1
}
args = args.slice(j);
if(signature.vararg) {
out[signature.vararg] = args;
}

if(signature.varkwarg) {
out[signature.varkwarg] = kwargs;
}

return out;
}
window["get_arguments"] = get_arguments 

get_arguments.pythonscript_function = true;
var type = function(args, kwargs) {
var class_name, parents, attrs;
class_name = args[0];
parents = args[1];
attrs = args[2];
return create_class(class_name, parents, attrs);
}
window["type"] = type 

type.pythonscript_function = true;
var getattr = function(args, kwargs) {
var object, attribute;
object = args[0];
attribute = args[1];
return get_attribute(object, attribute);
}
window["getattr"] = getattr 

var setattr = function(args, kwargs) {
var object, attribute, value;
object = args[0];
attribute = args[1];
value = args[2];
return set_attribute(object, attribute, value);
}
window["setattr"] = setattr 

var issubclass = function(args, kwargs) {
var C, B, base;
C = args[0];
B = args[1];
if(C === B) {
return true;
}

var iter = jsrange(C.bases.length);
for (var index=0; index < iter.length; index++) {
var backup = index;
index = iter[index];
base = C.bases[index];
if(issubclass([base, B], Object())) {
return true;
}

index = backup;
}

return false;
}
window["issubclass"] = issubclass 

var isinstance = function(args, kwargs) {
var object_class, object, klass;
object = args[0];
klass = args[1];
object_class = object.__class__;
if(object_class === undefined) {
return false;
}

return issubclass(create_array(object_class, klass));
}
window["isinstance"] = isinstance 

var json_to_pythonscript = function(json) {
var jstype, item, output;
jstype = typeof json;
if(jstype == "number") {
return json;
}

if(jstype == "string") {
return json;
}

if(Object.prototype.toString.call(json) === '[object Array]') {
output = list.__call__([]);
var append;
var iter = json;
for (var item=0; item < iter.length; item++) {
var backup = item;
item = iter[item];
append = get_attribute(output, "append");
append([json_to_pythonscript(item)]);
item = backup;
}

return output;
}

output = dict.__call__([]);
var iter = Object.keys(json);
for (var key=0; key < iter.length; key++) {
var backup = key;
key = iter[key];
set = get_attribute(output, "set");
set([key, json_to_pythonscript(json[key])]);
key = backup;
}

return output;
}
window["json_to_pythonscript"] = json_to_pythonscript
var _create_empty_object = function(arr) {
var o;
o = Object.create( null );
var iter = arr;
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
o[ i ] = true;
i = backup;
}

return o;
}
window["_create_empty_object"] = _create_empty_object 

_create_empty_object.pythonscript_function=true;
var int = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("a")};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
if(a instanceof String) {
return window.parseInt( a );
}
else {
return Math.round( a );
}

}
window["int"] = int 

int.pythonscript_function = true;
var float = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("a")};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
if(a instanceof String) {
return window.parseFloat( a );
}
else {
return a;
}

}
window["float"] = float 

float.pythonscript_function = true;
var str = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("s")};
arguments = get_arguments(signature, args, kwargs);
var s = arguments['s'];
return "" + s;
}
window["str"] = str 

str.pythonscript_function = true;
var _setup_str_prototype = function(args, kwargs) {
"\n    Extend JavaScript String.prototype with methods that implement the Python str API.\n    The decorator @String.prototype.[name] assigns the function to the prototype,\n    and ensures that the special 'this' variable will work.\n    ";
var func = function(a) {
if(this.substring(0, a.length) == a) {
return true;
}
else {
return false;
}

}

String.prototype.startswith=func;
var func = function(a) {
if(this.substring(this.length - a.length, this.length) == a) {
return true;
}
else {
return false;
}

}

String.prototype.endswith=func;
var func = function(a) {
var i, out;
out = "";
if(a instanceof Array) {
arr = a;
}
else {
arr = a.__dict__.js_object;
}

i = 0;
var iter = arr;
for (var value=0; value < iter.length; value++) {
var backup = value;
value = iter[value];
out += value;
i += 1;
if(i < arr.length) {
out += this;
}

value = backup;
}

return out;
}

String.prototype.join=func;
var func = function() {
return this.toUpperCase(  );
}

String.prototype.upper=func;
var func = function() {
return this.toLowerCase(  );
}

String.prototype.lower=func;
var func = function(a) {
return this.indexOf( a );
}

String.prototype.index=func;
var func = function() {
var digits;
digits = _create_empty_object( ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] );
var iter = this;
for (var char=0; char < iter.length; char++) {
var backup = char;
char = iter[char];
if(char  in  digits) {
/*pass*/
}
else {
return false;
}

char = backup;
}

return true;
}

String.prototype.isdigit=func;
}
window["_setup_str_prototype"] = _setup_str_prototype 

_setup_str_prototype.pythonscript_function = true;
_setup_str_prototype(create_array(), Object());
var range = function(args, kwargs) {
var i, r;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
"Emulates Python's range function";
var i, r;
i = 0;
r = get_attribute(list, "__call__")(create_array(), Object());
while(i < num) {
var __args_0, __kwargs_0;
__args_0 = create_array(i);
__kwargs_0 = Object();
get_attribute(get_attribute(r, "append"), "__call__")(__args_0, __kwargs_0);
i += 1
}
return r;
}
window["range"] = range 

range.pythonscript_function = true;
var StopIteration, __StopIteration_attrs, __StopIteration_parents;
window["__StopIteration_attrs"] = Object();
window["__StopIteration_parents"] = create_array();
StopIteration = create_class("StopIteration", window["__StopIteration_parents"], window["__StopIteration_attrs"]);
var len = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(obj, "__len__")(create_array(), Object());
}
window["len"] = len 

len.pythonscript_function = true;
var next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(obj, "next")(create_array(), Object());
}
window["next"] = next 

next.pythonscript_function = true;
var map = function(args, kwargs) {
var out;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("func", "objs")};
arguments = get_arguments(signature, args, kwargs);
var func = arguments['func'];
var objs = arguments['objs'];
out = get_attribute(list, "__call__")(create_array(), Object());
var __args_1, __kwargs_1;
__args_1 = create_array(func, get_attribute(objs, "js_object"));
__kwargs_1 = Object();
set_attribute(out, "js_object", get_attribute(map, "__call__")(__args_1, __kwargs_1));
return out;
}
window["map"] = map 

map.pythonscript_function = true;
var min = function(args, kwargs) {
var a;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("lst")};
arguments = get_arguments(signature, args, kwargs);
var lst = arguments['lst'];
a = undefined;
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
try {
value = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
if(a === undefined) {
a = value;
}
else {
if(value < a) {
a = value;
}

}

value = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

return a;
}
window["min"] = min 

min.pythonscript_function = true;
var max = function(args, kwargs) {
var a;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("lst")};
arguments = get_arguments(signature, args, kwargs);
var lst = arguments['lst'];
a = undefined;
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
try {
value = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
if(a === undefined) {
a = value;
}
else {
if(value > a) {
a = value;
}

}

value = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

return a;
}
window["max"] = max 

max.pythonscript_function = true;
var abs = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
return Math.abs(num);
}
window["abs"] = abs 

abs.pythonscript_function = true;
var ord = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("char")};
arguments = get_arguments(signature, args, kwargs);
var char = arguments['char'];
return char.charCodeAt(0);
}
window["ord"] = ord 

ord.pythonscript_function = true;
var chr = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
return String.fromCharCode(num);
}
window["chr"] = chr 

chr.pythonscript_function = true;
var Iterator, __Iterator_attrs, __Iterator_parents;
window["__Iterator_attrs"] = Object();
window["__Iterator_parents"] = create_array();
var __Iterator___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var index = arguments['index'];
self["__dict__"]["obj"] = obj;
self["__dict__"]["index"] = index;
}
window["__Iterator___init__"] = __Iterator___init__ 

__Iterator___init__.pythonscript_function = true;
window["__Iterator_attrs"]["__init__"] = __Iterator___init__;
var __Iterator_next = function(args, kwargs) {
var index, length, item;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = self["__dict__"]["index"];
var __args_2, __kwargs_2;
__args_2 = create_array(self["__dict__"]["obj"]);
__kwargs_2 = Object();
length = get_attribute(len, "__call__")(__args_2, __kwargs_2);
if(index == length) {
throw StopIteration;
}

var __args_3, __kwargs_3;
__args_3 = create_array(self["__dict__"]["index"]);
__kwargs_3 = Object();
item = get_attribute(get_attribute(self["__dict__"]["obj"], "get"), "__call__")(__args_3, __kwargs_3);
self["__dict__"]["index"] = self["__dict__"]["index"] + 1;
return item;
}
window["__Iterator_next"] = __Iterator_next 

__Iterator_next.pythonscript_function = true;
window["__Iterator_attrs"]["next"] = __Iterator_next;
Iterator = create_class("Iterator", window["__Iterator_parents"], window["__Iterator_attrs"]);
var tuple, __tuple_attrs, __tuple_parents;
window["__tuple_attrs"] = Object();
window["__tuple_parents"] = create_array();
var __tuple___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
self["__dict__"]["js_object"] = create_array();
if(js_object instanceof Array) {
arr = self["__dict__"]["js_object"];
i = 0;
length = js_object.length;
while(i < length) {
arr.push( js_object[i] );
i += 1
}
}
else {
if(js_object) {
throw TypeError;
}

}

}
window["__tuple___init__"] = __tuple___init__ 

__tuple___init__.pythonscript_function = true;
window["__tuple_attrs"]["__init__"] = __tuple___init__;
var __tuple___getitem__ = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = self["__dict__"]["js_object"];
return __array[index];
}
window["__tuple___getitem__"] = __tuple___getitem__ 

__tuple___getitem__.pythonscript_function = true;
window["__tuple_attrs"]["__getitem__"] = __tuple___getitem__;
var __tuple___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_4, __kwargs_4;
__args_4 = create_array(self, 0);
__kwargs_4 = Object();
return get_attribute(Iterator, "__call__")(__args_4, __kwargs_4);
}
window["__tuple___iter__"] = __tuple___iter__ 

__tuple___iter__.pythonscript_function = true;
window["__tuple_attrs"]["__iter__"] = __tuple___iter__;
var __tuple___len__ = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = self["__dict__"]["js_object"];
return __array.length;
}
window["__tuple___len__"] = __tuple___len__ 

__tuple___len__.pythonscript_function = true;
window["__tuple_attrs"]["__len__"] = __tuple___len__;
var __tuple_index = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
__array = self["__dict__"]["js_object"];
return __array.indexOf(obj);
}
window["__tuple_index"] = __tuple_index 

__tuple_index.pythonscript_function = true;
window["__tuple_attrs"]["index"] = __tuple_index;
var __tuple_count = function(args, kwargs) {
var i;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
i = 0;
var __iterator__, other;
__iterator__ = get_attribute(get_attribute(self, "__iter__"), "__call__")(create_array(), Object());
try {
other = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
if(other == obj) {
i = i + 1;
}

other = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

return i;
}
window["__tuple_count"] = __tuple_count 

__tuple_count.pythonscript_function = true;
window["__tuple_attrs"]["count"] = __tuple_count;
var __tuple_get = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = self["__dict__"]["js_object"];
return __array[index];
}
window["__tuple_get"] = __tuple_get 

__tuple_get.pythonscript_function = true;
window["__tuple_attrs"]["get"] = __tuple_get;
tuple = create_class("tuple", window["__tuple_parents"], window["__tuple_attrs"]);
var list, __list_attrs, __list_parents;
window["__list_attrs"] = Object();
window["__list_parents"] = create_array();
var __list___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
if(js_object) {
set_attribute(self, "js_object", js_object);
}
else {
set_attribute(self, "js_object", create_array());
}

}
window["__list___init__"] = __list___init__ 

__list___init__.pythonscript_function = true;
window["__list_attrs"]["__init__"] = __list___init__;
var __list___getitem__ = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = get_attribute(self, "js_object");
return __array[index];
}
window["__list___getitem__"] = __list___getitem__ 

__list___getitem__.pythonscript_function = true;
window["__list_attrs"]["__getitem__"] = __list___getitem__;
var __list___setitem__ = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
__array = get_attribute(self, "js_object");
__array[index] = value;
}
window["__list___setitem__"] = __list___setitem__ 

__list___setitem__.pythonscript_function = true;
window["__list_attrs"]["__setitem__"] = __list___setitem__;
var __list_append = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
__array.push(obj);
}
window["__list_append"] = __list_append 

__list_append.pythonscript_function = true;
window["__list_attrs"]["append"] = __list_append;
var __list_extend = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "other")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var other = arguments['other'];
var __iterator__, obj;
__iterator__ = get_attribute(get_attribute(other, "__iter__"), "__call__")(create_array(), Object());
try {
obj = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
var __args_5, __kwargs_5;
__args_5 = create_array(obj);
__kwargs_5 = Object();
get_attribute(get_attribute(self, "append"), "__call__")(__args_5, __kwargs_5);
obj = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

}
window["__list_extend"] = __list_extend 

__list_extend.pythonscript_function = true;
window["__list_attrs"]["extend"] = __list_extend;
var __list_insert = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
__array.splice(index, 0, obj);
}
window["__list_insert"] = __list_insert 

__list_insert.pythonscript_function = true;
window["__list_attrs"]["insert"] = __list_insert;
var __list_remove = function(args, kwargs) {
var index, __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
var __args_6, __kwargs_6;
__args_6 = create_array(obj);
__kwargs_6 = Object();
index = get_attribute(get_attribute(self, "index"), "__call__")(__args_6, __kwargs_6);
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}
window["__list_remove"] = __list_remove 

__list_remove.pythonscript_function = true;
window["__list_attrs"]["remove"] = __list_remove;
var __list_pop = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.pop();
}
window["__list_pop"] = __list_pop 

__list_pop.pythonscript_function = true;
window["__list_attrs"]["pop"] = __list_pop;
var __list_index = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
return __array.indexOf(obj);
}
window["__list_index"] = __list_index 

__list_index.pythonscript_function = true;
window["__list_attrs"]["index"] = __list_index;
var __list_count = function(args, kwargs) {
var i;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
i = 0;
var __iterator__, other;
__iterator__ = get_attribute(get_attribute(self, "__iter__"), "__call__")(create_array(), Object());
try {
other = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
if(other == obj) {
i = i + 1;
}

other = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

return i;
}
window["__list_count"] = __list_count 

__list_count.pythonscript_function = true;
window["__list_attrs"]["count"] = __list_count;
var __list_reverse = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}
window["__list_reverse"] = __list_reverse 

__list_reverse.pythonscript_function = true;
window["__list_attrs"]["reverse"] = __list_reverse;
var __list_shift = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.shift();
}
window["__list_shift"] = __list_shift 

__list_shift.pythonscript_function = true;
window["__list_attrs"]["shift"] = __list_shift;
var __list_slice = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "start", "end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
var __array;
__array = get_attribute(self, "js_object");
return __array.slice(start, end);
}
window["__list_slice"] = __list_slice 

__list_slice.pythonscript_function = true;
window["__list_attrs"]["slice"] = __list_slice;
var __list___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_7, __kwargs_7;
__args_7 = create_array(self, 0);
__kwargs_7 = Object();
return get_attribute(Iterator, "__call__")(__args_7, __kwargs_7);
}
window["__list___iter__"] = __list___iter__ 

__list___iter__.pythonscript_function = true;
window["__list_attrs"]["__iter__"] = __list___iter__;
var __list_get = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var __array;
__array = get_attribute(self, "js_object");
return __array[index];
}
window["__list_get"] = __list_get 

__list_get.pythonscript_function = true;
window["__list_attrs"]["get"] = __list_get;
var __list_set = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
var __array;
__array = get_attribute(self, "js_object");
__array[index] = value;
}
window["__list_set"] = __list_set 

__list_set.pythonscript_function = true;
window["__list_attrs"]["set"] = __list_set;
var __list___len__ = function(args, kwargs) {
var __array;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.length;
}
window["__list___len__"] = __list___len__ 

__list___len__.pythonscript_function = true;
window["__list_attrs"]["__len__"] = __list___len__;
list = create_class("list", window["__list_parents"], window["__list_attrs"]);
var dict, __dict_attrs, __dict_parents;
window["__dict_attrs"] = Object();
window["__dict_parents"] = create_array();
__dict_UID = 0;
window["__dict_attrs"]["UID"] = __dict_UID;
var __dict___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
if(js_object) {
if(js_object instanceof Array) {
self["__dict__"]["js_object"] = Object.create(null);
i = 0;
while(i < get_attribute(js_object, "length")) {
var key = js_object[i]["key"];
var value = js_object[i]["value"];
var __args_8, __kwargs_8;
__args_8 = create_array(key, value);
__kwargs_8 = Object();
get_attribute(get_attribute(self, "set"), "__call__")(__args_8, __kwargs_8);
i += 1
}
}
else {
self["__dict__"]["js_object"] = js_object;
}

}
else {
self["__dict__"]["js_object"] = Object();
}

}
window["__dict___init__"] = __dict___init__ 

__dict___init__.pythonscript_function = true;
window["__dict_attrs"]["__init__"] = __dict___init__;
var __dict_get = function(args, kwargs) {
var __dict;
var signature, arguments;
signature = {"kwargs": {"_default": undefined}, "args": create_array("self", "key", "_default")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var _default = arguments['_default'];
__dict = self["__dict__"]["js_object"];
if(typeof(key) === 'object') {
var uid = "@"+key.uid;
if(uid in __dict) {
return __dict[uid];
}

}
else {
if(typeof(key) === 'function') {
var uid = "@"+key.uid;
if(uid in __dict) {
return __dict[uid];
}

}
else {
if(key in __dict) {
return __dict[key];
}

}

}

return _default;
}
window["__dict_get"] = __dict_get 

__dict_get.pythonscript_function = true;
window["__dict_attrs"]["get"] = __dict_get;
var __dict_set = function(args, kwargs) {
var __dict;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
__dict = self["__dict__"]["js_object"];
if(typeof(key) === 'object') {
if(key.uid === undefined) {
uid = self["__class__"]["__dict__"]["UID"];
key.uid = uid;
self["__class__"]["__dict__"]["UID"] += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
if(typeof(key) === 'function') {
if(key.uid === undefined) {
uid = self["__class__"]["__dict__"]["UID"];
key.uid = uid;
self["__class__"]["__dict__"]["UID"] += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
__dict[key] = value;
}

}

}
window["__dict_set"] = __dict_set 

__dict_set.pythonscript_function = true;
window["__dict_attrs"]["set"] = __dict_set;
var __dict___len__ = function(args, kwargs) {
var __dict;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
__dict = self["__dict__"]["js_object"];
return Object.keys(__dict).length;
}
window["__dict___len__"] = __dict___len__ 

__dict___len__.pythonscript_function = true;
window["__dict_attrs"]["__len__"] = __dict___len__;
var __dict___getitem__ = function(args, kwargs) {
var __dict;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
__dict = self["__dict__"]["js_object"];
if(typeof(key) === 'object') {
var uid = key.uid;
return __dict["@"+uid];
}
else {
if(typeof(key) === 'function') {
var uid = key.uid;
return __dict["@"+uid];
}
else {
return __dict[key];
}

}

}
window["__dict___getitem__"] = __dict___getitem__ 

__dict___getitem__.pythonscript_function = true;
window["__dict_attrs"]["__getitem__"] = __dict___getitem__;
var __dict___setitem__ = function(args, kwargs) {
var __dict;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
__dict = self["__dict__"]["js_object"];
if(typeof(key) === 'object') {
if(key.uid === undefined) {
uid = self["__class__"]["__dict__"]["UID"];
key.uid = uid;
self["__class__"]["__dict__"]["UID"] += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
if(typeof(key) === 'function') {
if(key.uid === undefined) {
uid = self["__class__"]["__dict__"]["UID"];
key.uid = uid;
self["__class__"]["__dict__"]["UID"] += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
__dict[key] = value;
}

}

}
window["__dict___setitem__"] = __dict___setitem__ 

__dict___setitem__.pythonscript_function = true;
window["__dict_attrs"]["__setitem__"] = __dict___setitem__;
var __dict_keys = function(args, kwargs) {
var __dict, __keys, out;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
__dict = self["__dict__"]["js_object"];
__keys = Object.keys(__dict);
out = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(out, "js_object", __keys);
return out;
}
window["__dict_keys"] = __dict_keys 

__dict_keys.pythonscript_function = true;
window["__dict_attrs"]["keys"] = __dict_keys;
var __dict_values = function(args, kwargs) {
var __dict, __keys, i, out;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
__dict = self["__dict__"]["js_object"];
__keys = Object.keys(__dict);
out = get_attribute(list, "__call__")(create_array(), Object());
i = 0;
while(i < get_attribute(__keys, "length")) {
var __args_9, __kwargs_9;
__args_9 = create_array(__dict[ __keys[i] ]);
__kwargs_9 = Object();
get_attribute(get_attribute(out, "append"), "__call__")(__args_9, __kwargs_9);
i += 1
}
return out;
}
window["__dict_values"] = __dict_values 

__dict_values.pythonscript_function = true;
window["__dict_attrs"]["values"] = __dict_values;
dict = create_class("dict", window["__dict_parents"], window["__dict_attrs"]);
var array, __array_attrs, __array_parents;
window["__array_attrs"] = Object();
window["__array_parents"] = create_array();
__array_typecodes = get_attribute(dict, "__call__")([], {"js_object": [{"key": "c", "value": 1}, {"key": "b", "value": 1}, {"key": "B", "value": 1}, {"key": "u", "value": 2}, {"key": "h", "value": 2}, {"key": "H", "value": 2}, {"key": "i", "value": 4}, {"key": "I", "value": 4}, {"key": "l", "value": 4}, {"key": "L", "value": 4}, {"key": "f", "value": 4}, {"key": "d", "value": 8}, {"key": "float32", "value": 4}, {"key": "float16", "value": 2}, {"key": "float8", "value": 1}]});
window["__array_attrs"]["typecodes"] = __array_typecodes;
__array_typecode_names = get_attribute(dict, "__call__")([], {"js_object": [{"key": "c", "value": "Int8"}, {"key": "b", "value": "Int8"}, {"key": "B", "value": "Uint8"}, {"key": "u", "value": "Uint16"}, {"key": "h", "value": "Int16"}, {"key": "H", "value": "Uint16"}, {"key": "i", "value": "Int32"}, {"key": "I", "value": "Uint32"}, {"key": "f", "value": "Float32"}, {"key": "d", "value": "Float64"}, {"key": "float32", "value": "Float32"}, {"key": "float16", "value": "Int16"}, {"key": "float8", "value": "Int8"}]});
window["__array_attrs"]["typecode_names"] = __array_typecode_names;
var __array___init__ = function(args, kwargs) {
var size, buff;
var signature, arguments;
signature = {"kwargs": {"initializer": undefined, "little_endian": false}, "args": create_array("self", "typecode", "initializer", "little_endian")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var typecode = arguments['typecode'];
var initializer = arguments['initializer'];
var little_endian = arguments['little_endian'];
self["__dict__"]["typecode"] = typecode;
self["__dict__"]["itemsize"] = get_attribute(self["__class__"]["__dict__"]["typecodes"], "__getitem__")([typecode], Object());
self["__dict__"]["little_endian"] = little_endian;
if(initializer) {
var __args_10, __kwargs_10;
__args_10 = create_array(initializer);
__kwargs_10 = Object();
self["__dict__"]["length"] = get_attribute(len, "__call__")(__args_10, __kwargs_10);
self["__dict__"]["bytes"] = self["__dict__"]["length"] * self["__dict__"]["itemsize"];
if(self["__dict__"]["typecode"] == "float8") {
var __args_11, __kwargs_11;
__args_11 = create_array(initializer);
__kwargs_11 = Object();
var __args_12, __kwargs_12;
__args_12 = create_array(get_attribute(min, "__call__")(__args_11, __kwargs_11));
__kwargs_12 = Object();
var __args_13, __kwargs_13;
__args_13 = create_array(initializer);
__kwargs_13 = Object();
var __args_14, __kwargs_14;
__args_14 = create_array(get_attribute(list, "__call__")([], {"js_object": [get_attribute(abs, "__call__")(__args_12, __kwargs_12), get_attribute(max, "__call__")(__args_13, __kwargs_13)]}));
__kwargs_14 = Object();
self["__dict__"]["_scale"] = get_attribute(max, "__call__")(__args_14, __kwargs_14);
self["__dict__"]["_norm_get"] = self["__dict__"]["_scale"] / 127;
self["__dict__"]["_norm_set"] = 1.0 / self["__dict__"]["_norm_get"];
}
else {
if(self["__dict__"]["typecode"] == "float16") {
var __args_15, __kwargs_15;
__args_15 = create_array(initializer);
__kwargs_15 = Object();
var __args_16, __kwargs_16;
__args_16 = create_array(get_attribute(min, "__call__")(__args_15, __kwargs_15));
__kwargs_16 = Object();
var __args_17, __kwargs_17;
__args_17 = create_array(initializer);
__kwargs_17 = Object();
var __args_18, __kwargs_18;
__args_18 = create_array(get_attribute(list, "__call__")([], {"js_object": [get_attribute(abs, "__call__")(__args_16, __kwargs_16), get_attribute(max, "__call__")(__args_17, __kwargs_17)]}));
__kwargs_18 = Object();
self["__dict__"]["_scale"] = get_attribute(max, "__call__")(__args_18, __kwargs_18);
self["__dict__"]["_norm_get"] = self["__dict__"]["_scale"] / 32767;
self["__dict__"]["_norm_set"] = 1.0 / self["__dict__"]["_norm_get"];
}

}

}
else {
self["__dict__"]["length"] = 0;
self["__dict__"]["bytes"] = 0;
}

size = self["__dict__"]["bytes"];
buff = new ArrayBuffer(size);
self["__dict__"]["dataview"] = new DataView(buff);
self["__dict__"]["buffer"] = buff;
var __args_19, __kwargs_19;
__args_19 = create_array(initializer);
__kwargs_19 = Object();
get_attribute(get_attribute(self, "fromlist"), "__call__")(__args_19, __kwargs_19);
}
window["__array___init__"] = __array___init__ 

__array___init__.pythonscript_function = true;
window["__array_attrs"]["__init__"] = __array___init__;
var __array___len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return self["__dict__"]["length"];
}
window["__array___len__"] = __array___len__ 

__array___len__.pythonscript_function = true;
window["__array_attrs"]["__len__"] = __array___len__;
var __array___getitem__ = function(args, kwargs) {
var func_name, step, dataview, func, offset;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
step = self["__dict__"]["itemsize"];
offset = step * index;
dataview = self["__dict__"]["dataview"];
func_name = "get" + get_attribute(self["__class__"]["__dict__"]["typecode_names"], "__getitem__")([self["__dict__"]["typecode"]], Object());
func = dataview[func_name].bind(dataview);
if(offset < self["__dict__"]["bytes"]) {
value = func(offset);
if(self["__dict__"]["typecode"] == "float8") {
value = value * self["__dict__"]["_norm_get"];
}
else {
if(self["__dict__"]["typecode"] == "float16") {
value = value * self["__dict__"]["_norm_get"];
}

}

return value;
}
else {
throw IndexError;
}

}
window["__array___getitem__"] = __array___getitem__ 

__array___getitem__.pythonscript_function = true;
window["__array_attrs"]["__getitem__"] = __array___getitem__;
var __array___setitem__ = function(args, kwargs) {
var func_name, step, dataview, func, offset;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
step = self["__dict__"]["itemsize"];
if(index < 0) {
index = self["__dict__"]["length"] + index - 1;
}

offset = step * index;
dataview = self["__dict__"]["dataview"];
func_name = "set" + get_attribute(self["__class__"]["__dict__"]["typecode_names"], "__getitem__")([self["__dict__"]["typecode"]], Object());
func = dataview[func_name].bind(dataview);
if(offset < self["__dict__"]["bytes"]) {
if(self["__dict__"]["typecode"] == "float8") {
value = value * self["__dict__"]["_norm_set"];
}
else {
if(self["__dict__"]["typecode"] == "float16") {
value = value * self["__dict__"]["_norm_set"];
}

}

func(offset, value);
}
else {
throw IndexError;
}

}
window["__array___setitem__"] = __array___setitem__ 

__array___setitem__.pythonscript_function = true;
window["__array_attrs"]["__setitem__"] = __array___setitem__;
var __array___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_20, __kwargs_20;
__args_20 = create_array(self, 0);
__kwargs_20 = Object();
return get_attribute(Iterator, "__call__")(__args_20, __kwargs_20);
}
window["__array___iter__"] = __array___iter__ 

__array___iter__.pythonscript_function = true;
window["__array_attrs"]["__iter__"] = __array___iter__;
var __array_get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
return __array___getitem__([self, index]);
}
window["__array_get"] = __array_get 

__array_get.pythonscript_function = true;
window["__array_attrs"]["get"] = __array_get;
var __array_fromlist = function(args, kwargs) {
var typecode, func_name, dataview, length, step, func, size;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "lst")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var lst = arguments['lst'];
var __args_21, __kwargs_21;
__args_21 = create_array(lst);
__kwargs_21 = Object();
length = get_attribute(len, "__call__")(__args_21, __kwargs_21);
step = self["__dict__"]["itemsize"];
typecode = self["__dict__"]["typecode"];
size = length * step;
dataview = self["__dict__"]["dataview"];
func_name = "set" + get_attribute(self["__class__"]["__dict__"]["typecode_names"], "__getitem__")([typecode], Object());
func = dataview[func_name].bind(dataview);
if(size <= self["__dict__"]["bytes"]) {
i = 0;
offset = 0;
while(i < length) {
item = get_attribute(lst, "__getitem__")([i], Object());
if(typecode == "float8") {
item *= self["__dict__"]["_norm_set"]
}
else {
if(typecode == "float16") {
item *= self["__dict__"]["_norm_set"]
}

}

func(offset,item);
offset += step
i += 1
}
}
else {
throw TypeError;
}

}
window["__array_fromlist"] = __array_fromlist 

__array_fromlist.pythonscript_function = true;
window["__array_attrs"]["fromlist"] = __array_fromlist;
var __array_resize = function(args, kwargs) {
var source, new_buff, target, new_size, buff;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "length")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var length = arguments['length'];
buff = self["__dict__"]["buffer"];
source = new Uint8Array(buff);
new_size = length * self["__dict__"]["itemsize"];
new_buff = new ArrayBuffer(new_size);
target = new Uint8Array(new_buff);
target.set(source);
self["__dict__"]["length"] = length;
self["__dict__"]["bytes"] = new_size;
self["__dict__"]["buffer"] = new_buff;
self["__dict__"]["dataview"] = new DataView(new_buff);
}
window["__array_resize"] = __array_resize 

__array_resize.pythonscript_function = true;
window["__array_attrs"]["resize"] = __array_resize;
var __array_append = function(args, kwargs) {
var length;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
length = self["__dict__"]["length"];
var __args_22, __kwargs_22;
__args_22 = create_array(self["__dict__"]["length"] + 1);
__kwargs_22 = Object();
get_attribute(get_attribute(self, "resize"), "__call__")(__args_22, __kwargs_22);
get_attribute(get_attribute(self, "__setitem__"), "__call__")([length, value], Object());
}
window["__array_append"] = __array_append 

__array_append.pythonscript_function = true;
window["__array_attrs"]["append"] = __array_append;
var __array_extend = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "lst")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var lst = arguments['lst'];
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
try {
value = get_attribute(__iterator__, "next")(create_array(), Object());
while(true) {
var __args_23, __kwargs_23;
__args_23 = create_array(value);
__kwargs_23 = Object();
get_attribute(get_attribute(self, "append"), "__call__")(__args_23, __kwargs_23);
value = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {
/*pass*/
}

}

}
window["__array_extend"] = __array_extend 

__array_extend.pythonscript_function = true;
window["__array_attrs"]["extend"] = __array_extend;
var __array_to_array = function(args, kwargs) {
var i, arr;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
arr = create_array();
i = 0;
while(i < self["__dict__"]["length"]) {
item = __array___getitem__([self, i]);
arr.push( item );
i += 1
}
return arr;
}
window["__array_to_array"] = __array_to_array 

__array_to_array.pythonscript_function = true;
window["__array_attrs"]["to_array"] = __array_to_array;
var __array_to_list = function(args, kwargs) {
var lst;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
lst = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(lst, "js_object", get_attribute(self, "to_array")(create_array(), Object()));
return lst;
}
window["__array_to_list"] = __array_to_list 

__array_to_list.pythonscript_function = true;
window["__array_attrs"]["to_list"] = __array_to_list;
var __array_to_ascii = function(args, kwargs) {
var i, length, arr, string;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
string = "";
arr = get_attribute(self, "to_array")(create_array(), Object());
i = 0;
length = get_attribute(arr, "length");
while(i < length) {
var num = arr[i];
var char = String.fromCharCode(num);
string += char
i += 1
}
return string;
}
window["__array_to_ascii"] = __array_to_ascii 

__array_to_ascii.pythonscript_function = true;
window["__array_attrs"]["to_ascii"] = __array_to_ascii;
array = create_class("array", window["__array_parents"], window["__array_attrs"]);