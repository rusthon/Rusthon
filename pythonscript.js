




var jsrange = function(num) {
var i, r;
i = 0;
r = [];
while(i < num) {
r.push(i);
i = i + 1;
}
return r;
}

var create_array = function() {
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

var adapt_arguments = function(handler) {
var func = function() {
handler(Array.prototype.slice.call(arguments));
}

return func;
}

var create_class = function(class_name, parents, attrs) {
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

klass.__call__ = __call__;
return klass;
}

var get_attribute = function(object, attribute) {
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

return method;
}

return attr;
}

i = backup;
}

}

return undefined;
}

var set_attribute = function(object, attribute, value) {
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

var get_arguments = function(signature, args, kwargs) {
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
var iter = jsrange(argslength);
for (var i=0; i < iter.length; i++) {
var backup = i;
i = iter[i];
arg = signature.args[j];
if(kwargs) {
kwarg = kwargs[arg];
if(kwarg) {
out[arg] = kwarg;
}
else {
out[arg] = args[j];
j = j + 1;
}

}
else {
out[arg] = args[j];
j = j + 1;
}

i = backup;
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

var type = function(args, kwargs) {
var class_name, parents, attrs;
class_name = args[0];
parents = args[1];
attrs = args[2];
return create_class(class_name, parents, attrs);
}

var getattr = function(args, kwargs) {
var object, attribute;
object = args[0];
attribute = args[1];
return get_attribute(object, attribute);
}

var setattr = function(args, kwargs) {
var object, attribute, value;
object = args[0];
attribute = args[1];
value = args[2];
return set_attribute(object, attribute, value);
}

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

var range = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
var i, r;
i = 0;
var __args_0, __kwargs_0;
__args_0 = create_array();
__kwargs_0 = Object();
r = get_attribute(list, "__call__")(__args_0, __kwargs_0);
while(i < num) {
var __args_1, __kwargs_1;
__args_1 = create_array(i);
__kwargs_1 = Object();
get_attribute(get_attribute(r, "append"), "__call__")(__args_1, __kwargs_1);
i = i + 1;
}
return r;
}

var StopIteration, __StopIteration_attrs, __StopIteration_parents;
__StopIteration_attrs = Object();
__StopIteration_parents = create_array();
StopIteration = create_class("StopIteration", __StopIteration_parents, __StopIteration_attrs);
var len = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
var __args_2, __kwargs_2;
__args_2 = create_array();
__kwargs_2 = Object();
return get_attribute(get_attribute(obj, "__len__"), "__call__")(__args_2, __kwargs_2);
}

var next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
var __args_3, __kwargs_3;
__args_3 = create_array();
__kwargs_3 = Object();
return get_attribute(get_attribute(obj, "next"), "__call__")(__args_3, __kwargs_3);
}

var map = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("func", "objs")};
arguments = get_arguments(signature, args, kwargs);
var func = arguments['func'];
var objs = arguments['objs'];
var __args_4, __kwargs_4;
__args_4 = create_array();
__kwargs_4 = Object();
out = get_attribute(list, "__call__")(__args_4, __kwargs_4);
var __args_5, __kwargs_5;
__args_5 = create_array(func, get_attribute(objs, "js_object"));
__kwargs_5 = Object();
set_attribute(out, "js_object", get_attribute(map, "__call__")(__args_5, __kwargs_5));
return out;
}

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

__Iterator_attrs.__init__ = __Iterator___init__;
var __Iterator_next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = get_attribute(self, "index");
var __args_6, __kwargs_6;
__args_6 = create_array(get_attribute(self, "obj"));
__kwargs_6 = Object();
length = get_attribute(len, "__call__")(__args_6, __kwargs_6);
if(index == length) {
throw StopIteration;
}

var __args_7, __kwargs_7;
__args_7 = create_array(get_attribute(self, "index"));
__kwargs_7 = Object();
item = get_attribute(get_attribute(get_attribute(self, "obj"), "get"), "__call__")(__args_7, __kwargs_7);
set_attribute(self, "index", get_attribute(self, "index") + 1);
return item;
}

__Iterator_attrs.next = __Iterator_next;
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

__list_attrs.__init__ = __list___init__;
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

__list_attrs.append = __list_append;
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
var __args_8, __kwargs_8;
__args_8 = create_array(obj);
__kwargs_8 = Object();
get_attribute(get_attribute(self, "append"), "__call__")(__args_8, __kwargs_8);
obj = get_attribute(__iterator__, "next")(create_array(), Object());
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {

}

}

}

__list_attrs.extend = __list_extend;
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

__list_attrs.insert = __list_insert;
var __list_remove = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
var __args_9, __kwargs_9;
__args_9 = create_array(obj);
__kwargs_9 = Object();
index = get_attribute(get_attribute(self, "index"), "__call__")(__args_9, __kwargs_9);
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}

__list_attrs.remove = __list_remove;
var __list_pop = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.pop();
}

__list_attrs.pop = __list_pop;
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

__list_attrs.index = __list_index;
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

__list_attrs.count = __list_count;
var __list_reverse = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}

__list_attrs.reverse = __list_reverse;
var __list_shift = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.shift();
}

__list_attrs.shift = __list_shift;
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

__list_attrs.slice = __list_slice;
var __list___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_10, __kwargs_10;
__args_10 = create_array(self, 0);
__kwargs_10 = Object();
return get_attribute(Iterator, "__call__")(__args_10, __kwargs_10);
}

__list_attrs.__iter__ = __list___iter__;
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

__list_attrs.get = __list_get;
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

__list_attrs.set = __list_set;
var __list___len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.length;
}

__list_attrs.__len__ = __list___len__;
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

__dict_attrs.__init__ = __dict___init__;
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

__dict_attrs.get = __dict_get;
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

__dict_attrs.set = __dict_set;
var __dict___len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict;
__dict = get_attribute(self, "js_object");
return Object.keys(__dict).length;
}

__dict_attrs.__len__ = __dict___len__;
var __dict_keys = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict, out;
__dict = get_attribute(self, "js_object");
__keys = Object.keys(__dict);
var __args_11, __kwargs_11;
__args_11 = create_array();
__kwargs_11 = Object();
out = get_attribute(list, "__call__")(__args_11, __kwargs_11);
set_attribute(out, "js_object", __keys);
return out;
}

__dict_attrs.keys = __dict_keys;
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

__str_attrs.__init__ = __str___init__;
var __str___iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_12, __kwargs_12;
__args_12 = create_array(get_attribute(self, "jsstring"), 0);
__kwargs_12 = Object();
return get_attribute(Iterator, "__call__")(__args_12, __kwargs_12);
}

__str_attrs.__iter__ = __str___iter__;
str = create_class("str", __str_parents, __str_attrs);
