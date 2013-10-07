// PythonScript Runtime - regenerated on: Mon Oct  7 06:29:29 2013
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
window["func"] = func 

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
window["__call__"] = __call__ 

klass.__call__ = __call__;
return klass;
}
window["create_class"] = create_class 

var get_attribute = function(object, attribute) {
"Retrieve an attribute, method or property\n\n    method are actually functions which are converted to methods by\n    prepending their arguments with the current object. Properties are\n    not functions!";
if(attribute == "__call__") {
if({}.toString.call(object) === '[object Function]') {
return object;
}

}

var attr;
attr = object[attribute];
if(attr) {
return attr;
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
window["method"] = method 

return method;
}

return attr;
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
window["method"] = method 

return method;
}

return attr;
}

i = backup;
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

j = 0;
while(j < argslength) {
arg = signature.args[j];
if(kwargs) {
kwarg = kwargs[arg];
if(kwarg) {
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
throw TypeError;
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
throw TypeError;
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

var type = function(args, kwargs) {
var class_name, parents, attrs;
class_name = args[0];
parents = args[1];
attrs = args[2];
return create_class(class_name, parents, attrs);
}
window["type"] = type 

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
var range = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
"Emulates Python's range function";
var i, r;
i = 0;
r = list(create_array(), Object());
while(i < num) {
var __args_0, __kwargs_0;
__args_0 = create_array(i);
__kwargs_0 = Object();
get_attribute(get_attribute(r, "append"), "__call__")(__args_0, __kwargs_0);
i = i + 1;
}
return r;
}
window["range"] = range 

var StopIteration, __StopIteration_attrs, __StopIteration_parents;
__StopIteration_attrs = Object();
__StopIteration_parents = create_array();
StopIteration = create_class("StopIteration", __StopIteration_parents, __StopIteration_attrs);
var len = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(obj, "__len__")(create_array(), Object());
}
window["len"] = len 

var next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(obj, "next")(create_array(), Object());
}
window["next"] = next 

var map = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("func", "objs")};
arguments = get_arguments(signature, args, kwargs);
var func = arguments['func'];
var objs = arguments['objs'];
out = list(create_array(), Object());
var __args_1, __kwargs_1;
__args_1 = create_array(func, get_attribute(objs, "js_object"));
__kwargs_1 = Object();
set_attribute(out, "js_object", get_attribute(map, "__call__")(__args_1, __kwargs_1));
return out;
}
window["map"] = map 

var Iterator, __Iterator_attrs, __Iterator_parents;
__Iterator_attrs = Object();
__Iterator_parents = create_array();
var __Iterator___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var index = arguments['index'];
set_attribute(self, "obj", obj);
set_attribute(self, "index", index);
}
window["__Iterator___init__"] = __Iterator___init__ 

__Iterator_attrs["__init__"] = __Iterator___init__;
var __Iterator_next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = get_attribute(self, "index");
var __args_2, __kwargs_2;
__args_2 = create_array(get_attribute(self, "obj"));
__kwargs_2 = Object();
length = get_attribute(len, "__call__")(__args_2, __kwargs_2);
if(index == length) {
throw StopIteration;
}

var __args_3, __kwargs_3;
__args_3 = create_array(get_attribute(self, "index"));
__kwargs_3 = Object();
item = get_attribute(get_attribute(get_attribute(self, "obj"), "get"), "__call__")(__args_3, __kwargs_3);
set_attribute(self, "index", get_attribute(self, "index") + 1);
return item;
}
window["__Iterator_next"] = __Iterator_next 

__Iterator_attrs["next"] = __Iterator_next;
Iterator = create_class("Iterator", __Iterator_parents, __Iterator_attrs);
var list, __list_attrs, __list_parents;
__list_attrs = Object();
__list_parents = create_array();
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

__list_attrs["__init__"] = __list___init__;
var __list_append = function(args, kwargs) {
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

__list_attrs["append"] = __list_append;
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
var __args_4, __kwargs_4;
__args_4 = create_array(obj);
__kwargs_4 = Object();
get_attribute(get_attribute(self, "append"), "__call__")(__args_4, __kwargs_4);
obj = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {

}

}

}
window["__list_extend"] = __list_extend 

__list_attrs["extend"] = __list_extend;
var __list_insert = function(args, kwargs) {
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

__list_attrs["insert"] = __list_insert;
var __list_remove = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
var __args_5, __kwargs_5;
__args_5 = create_array(obj);
__kwargs_5 = Object();
index = get_attribute(get_attribute(self, "index"), "__call__")(__args_5, __kwargs_5);
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}
window["__list_remove"] = __list_remove 

__list_attrs["remove"] = __list_remove;
var __list_pop = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.pop();
}
window["__list_pop"] = __list_pop 

__list_attrs["pop"] = __list_pop;
var __list_index = function(args, kwargs) {
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

__list_attrs["index"] = __list_index;
var __list_count = function(args, kwargs) {
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

}

}

return i;
}
window["__list_count"] = __list_count 

__list_attrs["count"] = __list_count;
var __list_reverse = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}
window["__list_reverse"] = __list_reverse 

__list_attrs["reverse"] = __list_reverse;
var __list_shift = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.shift();
}
window["__list_shift"] = __list_shift 

__list_attrs["shift"] = __list_shift;
var __list_slice = function(args, kwargs) {
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

__list_attrs["slice"] = __list_slice;
var __list___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_6, __kwargs_6;
__args_6 = create_array(self, 0);
__kwargs_6 = Object();
return get_attribute(Iterator, "__call__")(__args_6, __kwargs_6);
}
window["__list___iter__"] = __list___iter__ 

__list_attrs["__iter__"] = __list___iter__;
var __list_get = function(args, kwargs) {
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

__list_attrs["get"] = __list_get;
var __list_set = function(args, kwargs) {
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

__list_attrs["set"] = __list_set;
var __list___len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.length;
}
window["__list___len__"] = __list___len__ 

__list_attrs["__len__"] = __list___len__;
list = create_class("list", __list_parents, __list_attrs);
var dict, __dict_attrs, __dict_parents;
__dict_attrs = Object();
__dict_parents = create_array();
var __dict___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
if(js_object) {
set_attribute(self, "js_object", js_object);
}
else {
set_attribute(self, "js_object", Object());
}

}
window["__dict___init__"] = __dict___init__ 

__dict_attrs["__init__"] = __dict___init__;
var __dict_get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "d")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var d = arguments['d'];
var __dict;
__dict = get_attribute(self, "js_object");
if(__dict[key]) {
return __dict[key];
}

return d;
}
window["__dict_get"] = __dict_get 

__dict_attrs["get"] = __dict_get;
var __dict_set = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
var __dict;
__dict = get_attribute(self, "js_object");
__dict[key] = value;
}
window["__dict_set"] = __dict_set 

__dict_attrs["set"] = __dict_set;
var __dict___len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict;
__dict = get_attribute(self, "js_object");
return Object.keys(__dict).length;
}
window["__dict___len__"] = __dict___len__ 

__dict_attrs["__len__"] = __dict___len__;
var __dict_keys = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict, out;
__dict = get_attribute(self, "js_object");
__keys = Object.keys(__dict);
out = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(out, "js_object", __keys);
return out;
}
window["__dict_keys"] = __dict_keys 

__dict_attrs["keys"] = __dict_keys;
dict = create_class("dict", __dict_parents, __dict_attrs);
var str, __str_attrs, __str_parents;
__str_attrs = Object();
__str_parents = create_array();
var __str___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "jsstring")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var jsstring = arguments['jsstring'];
set_attribute(self, "jsstring", jsstring);
}
window["__str___init__"] = __str___init__ 

__str_attrs["__init__"] = __str___init__;
var __str___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_7, __kwargs_7;
__args_7 = create_array(get_attribute(self, "jsstring"), 0);
__kwargs_7 = Object();
return get_attribute(Iterator, "__call__")(__args_7, __kwargs_7);
}
window["__str___iter__"] = __str___iter__ 

__str_attrs["__iter__"] = __str___iter__;
str = create_class("str", __str_parents, __str_attrs);