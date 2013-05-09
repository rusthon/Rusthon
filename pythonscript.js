var jsrange = function(num) {
var i;
var r;
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
else {

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
else {

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
else {

}

}
else {

}

var attr;
attr = object[attribute];
if(attr) {
return attr;
}
else {

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
else {

}

}
else {

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
else {

}

}
else {

}

i = backup;
}

}
else {

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
else {

}

}
else {

}

return attr;
}
else {

}

}
else {

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
else {

}

}
else {

}

i = backup;
}

}
else {

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
else {

}

return attr;
}
else {

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
else {

}

return attr;
}
else {

}

i = backup;
}

}
else {

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
else {

}

}
else {

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
else {

}

}
else {

}

i = backup;
}

}
else {

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
else {

}

if(signature.varkwarg) {
out[signature.varkwarg] = kwargs;
}
else {

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

var range = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("num")};
var arguments = get_arguments(signature, args, kwargs);
var num = arguments["num"];
var i;
var r;
i = 0;
r = get_attribute(list, "__call__")(create_array(), {});
while(i < num) {
get_attribute(get_attribute(r, "append"), "__call__")(create_array(i), {});
i = i + 1;
}
return r;
}

StopIteration = {};
parents = create_array();
StopIteration = create_class("StopIteration", parents, StopIteration);
var len = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("obj")};
var arguments = get_arguments(signature, args, kwargs);
var obj = arguments["obj"];
return get_attribute(get_attribute(obj, "__len__"), "__call__")(create_array(), {});
}

var next = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("obj")};
var arguments = get_arguments(signature, args, kwargs);
var obj = arguments["obj"];
return get_attribute(get_attribute(obj, "next"), "__call__")(create_array(), {});
}

var map = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("func", "objs")};
var arguments = get_arguments(signature, args, kwargs);
var func = arguments["func"];
var objs = arguments["objs"];
out = get_attribute(list, "__call__")(create_array(), {});
set_attribute(out, "js_object", get_attribute(map, "__call__")(create_array(func, get_attribute(objs, "js_object")), {}));
return out;
}

Iterator = {};
parents = create_array();
var Iterator____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj", "index")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var obj = arguments["obj"];
var index = arguments["index"];
set_attribute(self, "obj", obj);
set_attribute(self, "index", index);
}

Iterator.__init__ = Iterator____init__;
var Iterator__next = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
index = get_attribute(self, "index");
length = get_attribute(len, "__call__")(create_array(get_attribute(self, "obj")), {});
if(index == length) {
throw StopIteration;
}
else {

}

item = get_attribute(get_attribute(get_attribute(self, "obj"), "get"), "__call__")(create_array(get_attribute(self, "index")), {});
set_attribute(self, "index", get_attribute(self, "index") + 1);
return item;
}

Iterator.next = Iterator__next;
Iterator = create_class("Iterator", parents, Iterator);
list = {};
parents = create_array();
var list____init__ = function(args, kwargs) {
var signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var js_object = arguments["js_object"];
if(js_object) {
set_attribute(self, "js_object", js_object);
}
else {
set_attribute(self, "js_object", create_array());
}

}

list.__init__ = list____init__;
var list__append = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var obj = arguments["obj"];
var __array;
__array = get_attribute(self, "js_object");
__array.push(obj);
}

list.append = list__append;
var list__extend = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "other")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var other = arguments["other"];
var __iterator__ = get_attribute(other, "__iter__")(create_array(), {});
try {
var obj = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
get_attribute(get_attribute(self, "append"), "__call__")(create_array(obj), {});
var obj = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

}

list.extend = list__extend;
var list__insert = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index", "obj")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var index = arguments["index"];
var obj = arguments["obj"];
var __array;
__array = get_attribute(self, "js_object");
__array.splice(index, 0, obj);
}

list.insert = list__insert;
var list__remove = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var obj = arguments["obj"];
var __array;
index = get_attribute(get_attribute(self, "index"), "__call__")(create_array(obj), {});
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}

list.remove = list__remove;
var list__pop = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __array;
__array = get_attribute(self, "js_object");
return __array.pop();
}

list.pop = list__pop;
var list__index = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var obj = arguments["obj"];
var __array;
__array = get_attribute(self, "js_object");
return __array.indexOf(obj);
}

list.index = list__index;
var list__count = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "obj")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var obj = arguments["obj"];
i = 0;
var __iterator__ = get_attribute(self, "__iter__")(create_array(), {});
try {
var other = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
if(other == obj) {
i = i + 1;
}
else {

}

var other = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

return i;
}

list.count = list__count;
var list__reverse = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __array;
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}

list.reverse = list__reverse;
var list__shift = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __array;
__array = get_attribute(self, "js_object");
return __array.shift();
}

list.shift = list__shift;
var list__slice = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var start = arguments["start"];
var end = arguments["end"];
var __array;
__array = get_attribute(self, "js_object");
return __array.slice(start, end);
}

list.slice = list__slice;
var list____iter__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
return get_attribute(Iterator, "__call__")(create_array(self, 0), {});
}

list.__iter__ = list____iter__;
var list__get = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var index = arguments["index"];
var __array;
__array = get_attribute(self, "js_object");
return __array[index];
}

list.get = list__get;
var list__set = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index", "value")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var index = arguments["index"];
var value = arguments["value"];
var __array;
__array = get_attribute(self, "js_object");
__array[index] = value;
}

list.set = list__set;
var list____len__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __array;
__array = get_attribute(self, "js_object");
return __array.length;
}

list.__len__ = list____len__;
list = create_class("list", parents, list);
dict = {};
parents = create_array();
var dict____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
set_attribute(self, "js_object", {});
}

dict.__init__ = dict____init__;
var dict__get = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "key", "d")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var key = arguments["key"];
var d = arguments["d"];
var __dict;
__dict = get_attribute(self, "js_object");
if(__dict[key]) {
return __dict[key];
}
else {

}

return d;
}

dict.get = dict__get;
var dict__set = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var key = arguments["key"];
var value = arguments["value"];
var __dict;
__dict = get_attribute(self, "js_object");
__dict[key] = value;
}

dict.set = dict__set;
var dict____len__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __dict;
__dict = get_attribute(self, "js_object");
return Object.keys(__dict).length;
}

dict.__len__ = dict____len__;
var dict__keys = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var __dict;
__dict = get_attribute(self, "js_object");
__keys = Object.keys(__dict);
var out;
out = get_attribute(list, "__call__")(create_array(), {});
set_attribute(out, "js_object", __keys);
return out;
}

dict.keys = dict__keys;
dict = create_class("dict", parents, dict);
str = {};
parents = create_array();
parents.push(list);
var str____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "jsstring")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var jsstring = arguments["jsstring"];
get_attribute(get_attribute(list, "__init__"), "__call__")(create_array(self), {});
var char;
var __iterator__ = get_attribute(get_attribute(range, "__call__")(create_array(jsstring.length), {}), "__iter__")(create_array(), {});
try {
var i = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
char = jsstring.charAt(i);
get_attribute(get_attribute(self, "append"), "__call__")(create_array(char), {});
var i = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

}

str.__init__ = str____init__;
str = create_class("str", parents, str);
