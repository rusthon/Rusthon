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
var array = new Array();
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
klass = {};
klass.bases = parents;
klass.__name__ = class_name;
klass.__dict__ = attrs;
var __call__ = function() {
var object;
object = {};
object.__class__ = klass;
object.__dict__ = {};
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
var __dict__ = __class__.__dict__;
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
args = create_array(object);
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
var base = bases[i];
var attr = get_attribute(base, attribute);
if(attr) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
var args = arguments;
if(args.length > 0) {
args[0].splice(0, 0, object);
}
else {
args = create_array(object);
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
out = {};
if(signature.args.length) {
argslength = signature.args.length;
}
else {
argslength = 0;
}

kwargslength = Object.keys(signature.kwargs).length;
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
if(issubclass([base, B], {})) {
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

var range = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("num")};
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
var i;
var r;
i = 0;
var __args_0, __kwargs_0;
__args_0 = create_array();
__kwargs_0 = {};
r = get_attribute(list, "__call__")(__args_0, __kwargs_0);
var __args_1, __kwargs_1;
__args_1 = create_array(i);
__kwargs_1 = {};
get_attribute(get_attribute(r, append), "__call__")(__args_1, __kwargs_1);
i = i + 1;
return r;
}

var StopIteration, __StopIteration_attrs, __StopIteration_parents;
__StopIteration_attrs = {};
__StopIteration_parents = create_array();
StopIteration = create_class("StopIteration", __StopIteration_parents, __StopIteration__attrs);
var len = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
var __args_2, __kwargs_2;
__args_2 = create_array();
__kwargs_2 = {};
return get_attribute(get_attribute(obj, __len__), "__call__")(__args_2, __kwargs_2);
}

var next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("obj")};
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
var __args_3, __kwargs_3;
__args_3 = create_array();
__kwargs_3 = {};
return get_attribute(get_attribute(obj, next), "__call__")(__args_3, __kwargs_3);
}

var map = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("func", "objs")};
arguments = get_arguments(signature, args, kwargs);
var func = arguments['func'];
var objs = arguments['objs'];
var __args_4, __kwargs_4;
__args_4 = create_array();
__kwargs_4 = {};
out = get_attribute(list, "__call__")(__args_4, __kwargs_4);
var __args_5, __kwargs_5;
__args_5 = create_array(func, get_attribute(objs, js_object));
__kwargs_5 = {};
set_attribute(out, js_object, get_attribute(map, "__call__")(__args_5, __kwargs_5));
return out;
}

var Iterator, __Iterator_attrs, __Iterator_parents;
__Iterator_attrs = {};
__Iterator_parents = create_array();
var __Iterator____init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "obj", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var index = arguments['index'];
set_attribute(self, obj, obj);
set_attribute(self, index, index);
}

Iterator.__init__ = __Iterator____init__;
var __Iterator__next = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = get_attribute(self, index);
var __args_6, __kwargs_6;
__args_6 = create_array(get_attribute(self, obj));
__kwargs_6 = {};
length = get_attribute(len, "__call__")(__args_6, __kwargs_6);
var __args_7, __kwargs_7;
__args_7 = create_array(get_attribute(self, index));
__kwargs_7 = {};
item = get_attribute(get_attribute(get_attribute(self, obj), get), "__call__")(__args_7, __kwargs_7);
set_attribute(self, index, get_attribute(self, index) + 1);
return item;
}

Iterator.next = __Iterator__next;
Iterator = create_class("Iterator", __Iterator_parents, __Iterator__attrs);
var list, __list_attrs, __list_parents;
__list_attrs = {};
__list_parents = create_array();
var __list____init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
set_attribute(self, js_object, js_object);
set_attribute(self, js_object, create_array());
}

list.__init__ = __list____init__;
var __list__append = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, js_object);
__array.push(obj);
}

list.append = __list__append;
var __list__extend = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "other")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var other = arguments['other'];
var __iterator__, obj;
__iterator__ = get_attribute(other, "__iter__");
try {
obj = get_attribute(__iterator__, "next")();
while(true) {
var __args_8, __kwargs_8;
__args_8 = create_array(obj);
__kwargs_8 = {};
get_attribute(get_attribute(self, append), "__call__")(__args_8, __kwargs_8);
undefined;
obj = get_attribute(__iterator__, "next")();
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance(__exception__, StopIteration)) {

}

}

}

list.extend = __list__extend;
var __list__insert = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, js_object);
__array.splice(index, 0, obj);
}

list.insert = __list__insert;
var __list__remove = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
var __args_9, __kwargs_9;
__args_9 = create_array(obj);
__kwargs_9 = {};
index = get_attribute(get_attribute(self, index), "__call__")(__args_9, __kwargs_9);
__array = get_attribute(self, js_object);
__array.splice(index, 1);
}

list.remove = __list__remove;
var __list__pop = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, js_object);
return __array.pop();
}

list.pop = __list__pop;
var __list__index = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, js_object);
return __array.indexOf(obj);
}

list.index = __list__index;
var __list__count = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "obj")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
i = 0;
var __iterator__, other;
__iterator__ = get_attribute(self, "__iter__");
try {
other = get_attribute(__iterator__, "next")();
while(true) {
i = i + 1;
undefined;
other = get_attribute(__iterator__, "next")();
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance(__exception__, StopIteration)) {

}

}

return i;
}

list.count = __list__count;
var __list__reverse = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, js_object);
set_attribute(self, js_object, __array.reverse());
}

list.reverse = __list__reverse;
var __list__shift = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, js_object);
return __array.shift();
}

list.shift = __list__shift;
var __list__slice = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
var __array;
__array = get_attribute(self, js_object);
return __array.slice(start, end);
}

list.slice = __list__slice;
var __list____iter__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __args_10, __kwargs_10;
__args_10 = create_array(self, 0);
__kwargs_10 = {};
return get_attribute(Iterator, "__call__")(__args_10, __kwargs_10);
}

list.__iter__ = __list____iter__;
var __list__get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var __array;
__array = get_attribute(self, js_object);
return __array[index];
}

list.get = __list__get;
var __list__set = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
var __array;
__array = get_attribute(self, js_object);
__array[index] = value;
}

list.set = __list__set;
var __list____len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, js_object);
return __array.length;
}

list.__len__ = __list____len__;
list = create_class("list", __list_parents, __list__attrs);
var dict, __dict_attrs, __dict_parents;
__dict_attrs = {};
__dict_parents = create_array();
var __dict____init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
set_attribute(self, js_object, js_object);
set_attribute(self, js_object, {});
}

dict.__init__ = __dict____init__;
var __dict__get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "d")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var d = arguments['d'];
var __dict;
__dict = get_attribute(self, js_object);
return __dict[key];
return d;
}

dict.get = __dict__get;
var __dict__set = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
var __dict;
__dict = get_attribute(self, js_object);
__dict[key] = value;
}

dict.set = __dict__set;
var __dict____len__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict;
__dict = get_attribute(self, js_object);
return Object.keys(__dict).length;
}

dict.__len__ = __dict____len__;
var __dict__keys = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __dict;
__dict = get_attribute(self, js_object);
__keys = Object.keys(__dict);
var out;
var __args_11, __kwargs_11;
__args_11 = create_array();
__kwargs_11 = {};
out = get_attribute(list, "__call__")(__args_11, __kwargs_11);
set_attribute(out, js_object, __keys);
return out;
}

dict.keys = __dict__keys;
dict = create_class("dict", __dict_parents, __dict__attrs);
var str, __str_attrs, __str_parents;
__str_attrs = {};
__str_parents = create_array();
__str_parents.push(list);
var __str____init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "jsstring")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var jsstring = arguments['jsstring'];
var __args_12, __kwargs_12;
__args_12 = create_array(self);
__kwargs_12 = {};
get_attribute(get_attribute(list, __init__), "__call__")(__args_12, __kwargs_12);
var char;
var __iterator__, i;
var __args_13, __kwargs_13;
__args_13 = create_array(jsstring.length);
__kwargs_13 = {};
__iterator__ = get_attribute(get_attribute(range, "__call__")(__args_13, __kwargs_13), "__iter__");
try {
i = get_attribute(__iterator__, "next")();
while(true) {
char = jsstring.charAt(i);
var __args_14, __kwargs_14;
__args_14 = create_array(char);
__kwargs_14 = {};
get_attribute(get_attribute(self, append), "__call__")(__args_14, __kwargs_14);
undefined;
undefined;
i = get_attribute(__iterator__, "next")();
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance(__exception__, StopIteration)) {

}

}

}

str.__init__ = __str____init__;
str = create_class("str", __str_parents, __str__attrs);
