// PythonScript Runtime - regenerated on: Thu Nov  7 21:54:00 2013
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
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
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

bases = __class__.__bases__;
var iter = jsrange(bases.length);
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
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
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
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
if(attribute  in  __class__.__properties__) {
return __class__.__properties__[attribute]["get"]([object], Object());
}

__dict__ = __class__.__dict__;
attr = __dict__[attribute];
if(attribute  in  __dict__) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
var args;
args = Array.prototype.slice.call(arguments);
if(args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && args.length == 2) {
/*pass*/
}
else {
args = [args, Object()];
}

args[0].splice(0, 0, object);
return attr.apply(undefined, args);
}

method.is_wrapper = true;
object[attribute] = method;
return method;
}
else {
return attr;
}

}

bases = __class__.__bases__;
var iter = bases;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var base=0; base < iter.length; base++) {
var backup = base;
base = iter[base];
attr = _get_upstream_attribute(base, attribute);
if(attr) {
if({}.toString.call(attr) === '[object Function]') {
var method = function() {
var args;
args = Array.prototype.slice.call(arguments);
if(args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && args.length == 2) {
/*pass*/
}
else {
args = [args, Object()];
}

args[0].splice(0, 0, object);
return attr.apply(undefined, args);
}

method.is_wrapper = true;
object[attribute] = method;
return method;
}
else {
return attr;
}

}

base = backup;
}

var iter = bases;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var base=0; base < iter.length; base++) {
var backup = base;
base = iter[base];
var prop;
prop = _get_upstream_property(base, attribute);
if(prop) {
return prop["get"]([object], Object());
}

base = backup;
}

if("__getattr__"  in  __dict__) {
return __dict__["__getattr__"]([object, attribute], Object());
}

var iter = bases;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var base=0; base < iter.length; base++) {
var backup = base;
base = iter[base];
var f;
f = _get_upstream_attribute(base, "__getattr__");
if(f) {
return f([object, attribute], Object());
}

base = backup;
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

var _get_upstream_attribute = function(base, attr) {
if(attr  in  base.__dict__) {
return base.__dict__[attr];
}

var iter = base.__bases__;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var parent=0; parent < iter.length; parent++) {
var backup = parent;
parent = iter[parent];
return _get_upstream_attribute(parent, attr);
parent = backup;
}

}
window["_get_upstream_attribute"] = _get_upstream_attribute 

var _get_upstream_property = function(base, attr) {
if(attr  in  base.__properties__) {
return base.__properties__[attr];
}

var iter = base.__bases__;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var parent=0; parent < iter.length; parent++) {
var backup = parent;
parent = iter[parent];
return _get_upstream_property(parent, attr);
parent = backup;
}

}
window["_get_upstream_property"] = _get_upstream_property 

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

bases = __class__.__bases__;
var iter = jsrange(bases.length);
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
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
if(args.length > signature.args.length) {
if(signature.vararg) {
/*pass*/
}
else {
console.log("ERROR args:", args, "kwargs:", kwargs, "sig:", signature);
throw TypeError("Supplemental positional arguments provided but signature doesn't accept them");
}

}

j = 0;
while(j < signature.args.length) {
name = signature.args[j];
if(name  in  kwargs) {
out[name] = kwargs[name];
}
else {
if(j < args.length) {
out[name] = args[j];
}
else {
if(name  in  signature.kwargs) {
out[name] = signature.kwargs[name];
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
_PythonJS_UID = 0;
var create_class = function(class_name, parents, attrs, props) {
var metaclass, klass;
"Create a PythonScript class";
if(attrs.__metaclass__) {
metaclass = attrs.__metaclass__;
attrs.__metaclass__=undefined;
return metaclass( [class_name, parents, attrs] );
}

klass = {  };
klass.__bases__=parents;
klass.__name__=class_name;
klass.__dict__=attrs;
klass.__properties__=props;
var __call__ = function() {
var init, object;
"Create a PythonJS object";
var object;
object = {  };
object.__class__=klass;
object.__dict__={  };
var iter = klass.__dict__;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var name=0; name < iter.length; name++) {
var backup = name;
name = iter[name];
if(typeof(klass.__dict__[name]) == "function") {
get_attribute( object,name );
}

name = backup;
}

init = get_attribute( object,"__init__" );
if(init) {
init.apply( undefined,arguments );
}

return object;
}

__call__.NAME = "__call__";
__call__.args_signature = [];
__call__.kwargs_signature = {};
__call__.types_signature = {};
__call__.pythonscript_function=true;
klass.__call__=__call__;
return klass;
}
window["create_class"] = create_class 

create_class.NAME = "create_class";
create_class.args_signature = ["class_name","parents","attrs","props"];
create_class.kwargs_signature = {};
create_class.types_signature = {};
var type = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"bases": undefined, "class_dict": undefined}, "args": create_array("ob_or_class_name", "bases", "class_dict")};
signature["function_name"] = "type";
arguments = get_arguments(signature, args, kwargs);
var ob_or_class_name = arguments['ob_or_class_name'];
var bases = arguments['bases'];
var class_dict = arguments['class_dict'];
"\n    type(object) -> the object's type\n    type(name, bases, dict) -> a new type  ## broken? - TODO test\n    ";
if(bases === undefined && class_dict === undefined) {
return ob_or_class_name.__class__;
}
else {
return create_class( ob_or_class_name,bases,class_dict );
}

}
window["type"] = type 

type.NAME = "type";
type.args_signature = ["ob_or_class_name", "bases", "class_dict"];
type.kwargs_signature = { bases:undefined,class_dict:undefined };
type.types_signature = { bases:"None",class_dict:"None" };
type.pythonscript_function = true;
var getattr = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"property": false}, "args": create_array("ob", "attr", "property")};
signature["function_name"] = "getattr";
arguments = get_arguments(signature, args, kwargs);
var ob = arguments['ob'];
var attr = arguments['attr'];
var property = arguments['property'];
if(property) {
prop = _get_upstream_property( ob.__class__,attr );
if(prop && prop["get"]) {
return prop[ "get" ]( [ob],{  } );
}
else {
console.log("ERROR: getattr property error", prop);
}

}
else {
return get_attribute( ob,attr );
}

}
window["getattr"] = getattr 

getattr.NAME = "getattr";
getattr.args_signature = ["ob", "attr", "property"];
getattr.kwargs_signature = { property:false };
getattr.types_signature = { property:"False" };
getattr.pythonscript_function = true;
var setattr = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"property": false}, "args": create_array("ob", "attr", "value", "property")};
signature["function_name"] = "setattr";
arguments = get_arguments(signature, args, kwargs);
var ob = arguments['ob'];
var attr = arguments['attr'];
var value = arguments['value'];
var property = arguments['property'];
if(property) {
prop = _get_upstream_property( ob.__class__,attr );
if(prop && prop["set"]) {
prop[ "set" ]( [ob, value],{  } );
}
else {
console.log("ERROR: setattr property error", prop);
}

}
else {
set_attribute( ob,attr,value );
}

}
window["setattr"] = setattr 

setattr.NAME = "setattr";
setattr.args_signature = ["ob", "attr", "value", "property"];
setattr.kwargs_signature = { property:false };
setattr.types_signature = { property:"False" };
setattr.pythonscript_function = true;
var issubclass = function(args, kwargs) {
var i, bases;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("C", "B")};
signature["function_name"] = "issubclass";
arguments = get_arguments(signature, args, kwargs);
var C = arguments['C'];
var B = arguments['B'];
if(C === B) {
return true;
}

bases = C.__bases__;
i = 0;
while(i < get_attribute(bases, "length")) {
if(get_attribute(issubclass, "__call__")([get_attribute(bases, "__getitem__")([i], Object()), B], Object())) {
return true;
}

i += 1
}
return false;
}
window["issubclass"] = issubclass 

issubclass.NAME = "issubclass";
issubclass.args_signature = ["C", "B"];
issubclass.kwargs_signature = {  };
issubclass.types_signature = {  };
issubclass.pythonscript_function = true;
var isinstance = function(args, kwargs) {
var ob_class;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("ob", "klass")};
signature["function_name"] = "isinstance";
arguments = get_arguments(signature, args, kwargs);
var ob = arguments['ob'];
var klass = arguments['klass'];
ob_class = ob.__class__;
if(ob_class === undefined) {
return false;
}
else {
return get_attribute(issubclass, "__call__")([ob_class, klass], Object());
}

}
window["isinstance"] = isinstance 

isinstance.NAME = "isinstance";
isinstance.args_signature = ["ob", "klass"];
isinstance.kwargs_signature = {  };
isinstance.types_signature = {  };
isinstance.pythonscript_function = true;
var int = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("a")};
signature["function_name"] = "int";
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

int.NAME = "int";
int.args_signature = ["a"];
int.kwargs_signature = {  };
int.types_signature = {  };
int.pythonscript_function = true;
var float = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("a")};
signature["function_name"] = "float";
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

float.NAME = "float";
float.args_signature = ["a"];
float.kwargs_signature = {  };
float.types_signature = {  };
float.pythonscript_function = true;
var round = function(args, kwargs) {
var b;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("a", "places")};
signature["function_name"] = "round";
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
var places = arguments['places'];
b = "" + a;
if(b.indexOf(".") == -1) {
return a;
}
else {
c = b.split( "." );
x = c[ 0 ];
y = c[ 1 ].substring( 0,places );
return parseFloat( x + "." + y );
}

}
window["round"] = round 

round.NAME = "round";
round.args_signature = ["a", "places"];
round.kwargs_signature = {  };
round.types_signature = {  };
round.pythonscript_function = true;
var str = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("s")};
signature["function_name"] = "str";
arguments = get_arguments(signature, args, kwargs);
var s = arguments['s'];
return "" + s;
}
window["str"] = str 

str.NAME = "str";
str.args_signature = ["s"];
str.kwargs_signature = {  };
str.types_signature = {  };
str.pythonscript_function = true;
var _setup_str_prototype = function(args, kwargs) {
"\n    Extend JavaScript String.prototype with methods that implement the Python str API.\n    The decorator @String.prototype.[name] assigns the function to the prototype,\n    and ensures that the special 'this' variable will work.\n    ";
var func = function(a) {
if(this.indexOf(a) == -1) {
return false;
}
else {
return true;
}

}

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.__contains__=func;
var func = function(index) {
return this[ index ];
}

func.NAME = "func";
func.args_signature = ["index"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.get=func;
var func = function(self) {
return get_attribute(Iterator, "__call__")([this, 0], Object());
}

func.NAME = "func";
func.args_signature = ["self"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.__iter__=func;
var func = function(idx) {
return this[ idx ];
}

func.NAME = "func";
func.args_signature = ["idx"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.__getitem__=func;
var func = function() {
return this.length;
}

func.NAME = "func";
func.args_signature = [];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.__len__=func;
var func = function(a) {
if(this.substring(0, a.length) == a) {
return true;
}
else {
return false;
}

}

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.startswith=func;
var func = function(a) {
if(this.substring(this.length - a.length, this.length) == a) {
return true;
}
else {
return false;
}

}

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.endswith=func;
var func = function(a) {
var i, arr, out;
out = "";
if(a instanceof Array) {
arr = a;
}
else {
arr = a.__dict__.js_object;
}

i = 0;
var iter = arr;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
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

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.join=func;
var func = function() {
return this.toUpperCase(  );
}

func.NAME = "func";
func.args_signature = [];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.upper=func;
var func = function() {
return this.toLowerCase(  );
}

func.NAME = "func";
func.args_signature = [];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.lower=func;
var func = function(a) {
return this.indexOf( a );
}

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.index=func;
var func = function() {
var digits;
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
var iter = this;
if (! (iter instanceof Array) ) { iter = Object.keys(iter) }
for (var char=0; char < iter.length; char++) {
var backup = char;
char = iter[char];
if(char  in  digits || Object.hasOwnProperty.call(digits, "__contains__") && digits["__contains__"](char)) {
/*pass*/
}
else {
return false;
}

char = backup;
}

return true;
}

func.NAME = "func";
func.args_signature = [];
func.kwargs_signature = {};
func.types_signature = {};
String.prototype.isdigit=func;
}
window["_setup_str_prototype"] = _setup_str_prototype 

_setup_str_prototype.NAME = "_setup_str_prototype";
_setup_str_prototype.args_signature = [];
_setup_str_prototype.kwargs_signature = {  };
_setup_str_prototype.types_signature = {  };
_setup_str_prototype.pythonscript_function = true;
get_attribute(_setup_str_prototype, "__call__")(create_array(), Object());
var _setup_array_prototype = function(args, kwargs) {
var func = function(a) {
if(this.indexOf(a) == -1) {
return false;
}
else {
return true;
}

}

func.NAME = "func";
func.args_signature = ["a"];
func.kwargs_signature = {};
func.types_signature = {};
Array.prototype.__contains__=func;
var func = function() {
return this.length;
}

func.NAME = "func";
func.args_signature = [];
func.kwargs_signature = {};
func.types_signature = {};
Array.prototype.__len__=func;
var func = function(index) {
return this[ index ];
}

func.NAME = "func";
func.args_signature = ["index"];
func.kwargs_signature = {};
func.types_signature = {};
Array.prototype.get=func;
var func = function(self) {
return get_attribute(Iterator, "__call__")([this, 0], Object());
}

func.NAME = "func";
func.args_signature = ["self"];
func.kwargs_signature = {};
func.types_signature = {};
Array.prototype.__iter__=func;
}
window["_setup_array_prototype"] = _setup_array_prototype 

_setup_array_prototype.NAME = "_setup_array_prototype";
_setup_array_prototype.args_signature = [];
_setup_array_prototype.kwargs_signature = {  };
_setup_array_prototype.types_signature = {  };
_setup_array_prototype.pythonscript_function = true;
get_attribute(_setup_array_prototype, "__call__")(create_array(), Object());
var range = function(args, kwargs) {
var i, r;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
signature["function_name"] = "range";
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
"Emulates Python's range function";
var i, r;
i = 0;
r = get_attribute(list, "__call__")(create_array(), Object());
while(i < num) {
get_attribute(get_attribute(r, "append"), "__call__")([i], Object());
i += 1
}
return r;
}
window["range"] = range 

range.NAME = "range";
range.args_signature = ["num"];
range.kwargs_signature = {  };
range.types_signature = {  };
range.pythonscript_function = true;
var StopIteration, __StopIteration_attrs, __StopIteration_parents;
window["__StopIteration_attrs"] = Object();
window["__StopIteration_parents"] = create_array();
window["__StopIteration_properties"] = Object();
StopIteration = create_class("StopIteration", window["__StopIteration_parents"], window["__StopIteration_attrs"], window["__StopIteration_properties"]);
var len = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
signature["function_name"] = "len";
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(get_attribute(obj, "__len__"), "__call__")(create_array(), Object());
}
window["len"] = len 

len.NAME = "len";
len.args_signature = ["obj"];
len.kwargs_signature = {  };
len.types_signature = {  };
len.pythonscript_function = true;
var next = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("obj")};
signature["function_name"] = "next";
arguments = get_arguments(signature, args, kwargs);
var obj = arguments['obj'];
return get_attribute(get_attribute(obj, "next"), "__call__")(create_array(), Object());
}
window["next"] = next 

next.NAME = "next";
next.args_signature = ["obj"];
next.kwargs_signature = {  };
next.types_signature = {  };
next.pythonscript_function = true;
var map = function(args, kwargs) {
var out;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("func", "objs")};
signature["function_name"] = "map";
arguments = get_arguments(signature, args, kwargs);
var func = arguments['func'];
var objs = arguments['objs'];
out = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(out, "js_object", get_attribute(map, "__call__")([func, get_attribute(objs, "js_object")], Object()));
return out;
}
window["map"] = map 

map.NAME = "map";
map.args_signature = ["func", "objs"];
map.kwargs_signature = {  };
map.types_signature = {  };
map.pythonscript_function = true;
var min = function(args, kwargs) {
var a;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("lst")};
signature["function_name"] = "min";
arguments = get_arguments(signature, args, kwargs);
var lst = arguments['lst'];
a = undefined;
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
value = __next__();
if(a === undefined) {
a = value;
}
else {
if(value < a) {
a = value;
}

}

}
return a;
}
window["min"] = min 

min.NAME = "min";
min.args_signature = ["lst"];
min.kwargs_signature = {  };
min.types_signature = {  };
min.pythonscript_function = true;
var max = function(args, kwargs) {
var a;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("lst")};
signature["function_name"] = "max";
arguments = get_arguments(signature, args, kwargs);
var lst = arguments['lst'];
a = undefined;
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
value = __next__();
if(a === undefined) {
a = value;
}
else {
if(value > a) {
a = value;
}

}

}
return a;
}
window["max"] = max 

max.NAME = "max";
max.args_signature = ["lst"];
max.kwargs_signature = {  };
max.types_signature = {  };
max.pythonscript_function = true;
var abs = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
signature["function_name"] = "abs";
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
return Math.abs(num);
}
window["abs"] = abs 

abs.NAME = "abs";
abs.args_signature = ["num"];
abs.kwargs_signature = {  };
abs.types_signature = {  };
abs.pythonscript_function = true;
var ord = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("char")};
signature["function_name"] = "ord";
arguments = get_arguments(signature, args, kwargs);
var char = arguments['char'];
return char.charCodeAt(0);
}
window["ord"] = ord 

ord.NAME = "ord";
ord.args_signature = ["char"];
ord.kwargs_signature = {  };
ord.types_signature = {  };
ord.pythonscript_function = true;
var chr = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("num")};
signature["function_name"] = "chr";
arguments = get_arguments(signature, args, kwargs);
var num = arguments['num'];
return String.fromCharCode(num);
}
window["chr"] = chr 

chr.NAME = "chr";
chr.args_signature = ["num"];
chr.kwargs_signature = {  };
chr.types_signature = {  };
chr.pythonscript_function = true;
var Iterator, __Iterator_attrs, __Iterator_parents;
window["__Iterator_attrs"] = Object();
window["__Iterator_parents"] = create_array();
window["__Iterator_properties"] = Object();
var __Iterator___init__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj", "index")};
signature["function_name"] = "__Iterator___init__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var index = arguments['index'];
self["__dict__"]["obj"] = obj;
self["__dict__"]["index"] = index;
self["__dict__"]["length"] = get_attribute(len, "__call__")([obj], Object());
self["__dict__"]["obj_get"] = get_attribute(obj, "get");
}
window["__Iterator___init__"] = __Iterator___init__ 

__Iterator___init__.NAME = "__Iterator___init__";
__Iterator___init__.args_signature = ["self", "obj", "index"];
__Iterator___init__.kwargs_signature = {  };
__Iterator___init__.types_signature = {  };
__Iterator___init__.pythonscript_function = true;
window["__Iterator_attrs"]["__init__"] = __Iterator___init__;
var __Iterator_next = function(args, kwargs) {
var index, length, item;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__Iterator_next";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = self["__dict__"]["index"];
length = get_attribute(len, "__call__")([self["__dict__"]["obj"]], Object());
if(index == length) {
throw StopIteration;
}

item = get_attribute(get_attribute(self["__dict__"]["obj"], "get"), "__call__")([self["__dict__"]["index"]], Object());
self["__dict__"]["index"] = self["__dict__"]["index"] + 1;
return item;
}
window["__Iterator_next"] = __Iterator_next 

__Iterator_next.NAME = "__Iterator_next";
__Iterator_next.args_signature = ["self"];
__Iterator_next.kwargs_signature = {  };
__Iterator_next.types_signature = {  };
__Iterator_next.pythonscript_function = true;
window["__Iterator_attrs"]["next"] = __Iterator_next;
var __Iterator_next_fast = function(args, kwargs) {
var index;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__Iterator_next_fast";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
index = self.__dict__.index;
self.__dict__.index += 1;
return self.__dict__.obj_get( [index],{  } );
}
window["__Iterator_next_fast"] = __Iterator_next_fast 

__Iterator_next_fast.NAME = "__Iterator_next_fast";
__Iterator_next_fast.args_signature = ["self"];
__Iterator_next_fast.kwargs_signature = {  };
__Iterator_next_fast.types_signature = {  };
__Iterator_next_fast.pythonscript_function = true;
window["__Iterator_attrs"]["next_fast"] = __Iterator_next_fast;
Iterator = create_class("Iterator", window["__Iterator_parents"], window["__Iterator_attrs"], window["__Iterator_properties"]);
var tuple, __tuple_attrs, __tuple_parents;
window["__tuple_attrs"] = Object();
window["__tuple_parents"] = create_array();
window["__tuple_properties"] = Object();
var __tuple___init__ = function(args, kwargs) {
var i, arr, length;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
signature["function_name"] = "__tuple___init__";
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
if(get_attribute(isinstance, "__call__")([js_object, list], Object())) {
self["__dict__"]["js_object"] = get_attribute(get_attribute(get_attribute(js_object, "js_object"), "slice"), "__call__")([0], Object());
}
else {
if(get_attribute(isinstance, "__call__")([js_object, tuple], Object())) {
self["__dict__"]["js_object"] = get_attribute(get_attribute(get_attribute(js_object, "js_object"), "slice"), "__call__")([0], Object());
}
else {
if(get_attribute(isinstance, "__call__")([js_object, array], Object())) {
arr = create_array();
var __iterator__, v;
__iterator__ = get_attribute(get_attribute(js_object, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
v = __next__();
arr.push( v );
}
self["__dict__"]["js_object"] = arr;
}
else {
throw TypeError;
}

}

}

}
else {
if(js_object) {
throw TypeError;
}

}

}

self["wrapped"] = self["__dict__"]["js_object"];
}
window["__tuple___init__"] = __tuple___init__ 

__tuple___init__.NAME = "__tuple___init__";
__tuple___init__.args_signature = ["self", "js_object"];
__tuple___init__.kwargs_signature = { js_object:undefined };
__tuple___init__.types_signature = { js_object:"None" };
__tuple___init__.pythonscript_function = true;
window["__tuple_attrs"]["__init__"] = __tuple___init__;
var __tuple___getitem__ = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__tuple___getitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = self["__dict__"]["js_object"];
return __array[index];
}
window["__tuple___getitem__"] = __tuple___getitem__ 

__tuple___getitem__.NAME = "__tuple___getitem__";
__tuple___getitem__.args_signature = ["self", "index"];
__tuple___getitem__.kwargs_signature = {  };
__tuple___getitem__.types_signature = {  };
__tuple___getitem__.pythonscript_function = true;
window["__tuple_attrs"]["__getitem__"] = __tuple___getitem__;
var __tuple___iter__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__tuple___iter__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return get_attribute(Iterator, "__call__")([self, 0], Object());
}
window["__tuple___iter__"] = __tuple___iter__ 

__tuple___iter__.NAME = "__tuple___iter__";
__tuple___iter__.args_signature = ["self"];
__tuple___iter__.kwargs_signature = {  };
__tuple___iter__.types_signature = {  };
__tuple___iter__.return_type = "Iterator";
__tuple___iter__.pythonscript_function = true;
window["__tuple_attrs"]["__iter__"] = __tuple___iter__;
var __tuple___len__ = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__tuple___len__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = self["__dict__"]["js_object"];
return __array.length;
}
window["__tuple___len__"] = __tuple___len__ 

__tuple___len__.NAME = "__tuple___len__";
__tuple___len__.args_signature = ["self"];
__tuple___len__.kwargs_signature = {  };
__tuple___len__.types_signature = {  };
__tuple___len__.pythonscript_function = true;
window["__tuple_attrs"]["__len__"] = __tuple___len__;
var __tuple_index = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__tuple_index";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
__array = self["__dict__"]["js_object"];
return __array.indexOf(obj);
}
window["__tuple_index"] = __tuple_index 

__tuple_index.NAME = "__tuple_index";
__tuple_index.args_signature = ["self", "obj"];
__tuple_index.kwargs_signature = {  };
__tuple_index.types_signature = {  };
__tuple_index.pythonscript_function = true;
window["__tuple_attrs"]["index"] = __tuple_index;
var __tuple_count = function(args, kwargs) {
var i;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__tuple_count";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
i = 0;
var __iterator__, other;
__iterator__ = get_attribute(get_attribute(self, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
other = __next__();
if(other == obj) {
i = i + 1;
}

}
return i;
}
window["__tuple_count"] = __tuple_count 

__tuple_count.NAME = "__tuple_count";
__tuple_count.args_signature = ["self", "obj"];
__tuple_count.kwargs_signature = {  };
__tuple_count.types_signature = {  };
__tuple_count.pythonscript_function = true;
window["__tuple_attrs"]["count"] = __tuple_count;
var __tuple_get = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__tuple_get";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = self["__dict__"]["js_object"];
return __array[index];
}
window["__tuple_get"] = __tuple_get 

__tuple_get.NAME = "__tuple_get";
__tuple_get.args_signature = ["self", "index"];
__tuple_get.kwargs_signature = {  };
__tuple_get.types_signature = {  };
__tuple_get.pythonscript_function = true;
window["__tuple_attrs"]["get"] = __tuple_get;
var __tuple___contains__ = function(args, kwargs) {
var arr;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__tuple___contains__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
arr = self["__dict__"]["js_object"];
if(arr.indexOf(value) == -1) {
return false;
}
else {
return true;
}

}
window["__tuple___contains__"] = __tuple___contains__ 

__tuple___contains__.NAME = "__tuple___contains__";
__tuple___contains__.args_signature = ["self", "value"];
__tuple___contains__.kwargs_signature = {  };
__tuple___contains__.types_signature = {  };
__tuple___contains__.pythonscript_function = true;
window["__tuple_attrs"]["__contains__"] = __tuple___contains__;
tuple = create_class("tuple", window["__tuple_parents"], window["__tuple_attrs"], window["__tuple_properties"]);
var list, __list_attrs, __list_parents;
window["__list_attrs"] = Object();
window["__list_parents"] = create_array();
window["__list_properties"] = Object();
var __list___init__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
signature["function_name"] = "__list___init__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
if(js_object) {
if(js_object instanceof Array) {
set_attribute(self, "js_object", js_object);
}
else {
if(get_attribute(isinstance, "__call__")([js_object, list], Object()) || get_attribute(isinstance, "__call__")([js_object, tuple], Object()) || get_attribute(isinstance, "__call__")([js_object, array], Object())) {
set_attribute(self, "js_object", create_array());
var __iterator__, v;
__iterator__ = get_attribute(get_attribute(js_object, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
v = __next__();
get_attribute(get_attribute(self, "append"), "__call__")([v], Object());
}
}
else {
throw TypeError;
}

}

}
else {
set_attribute(self, "js_object", create_array());
}

self["wrapped"] = get_attribute(self, "js_object");
}
window["__list___init__"] = __list___init__ 

__list___init__.NAME = "__list___init__";
__list___init__.args_signature = ["self", "js_object"];
__list___init__.kwargs_signature = { js_object:undefined };
__list___init__.types_signature = { js_object:"None" };
__list___init__.pythonscript_function = true;
window["__list_attrs"]["__init__"] = __list___init__;
var __list___getitem__ = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__list___getitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
__array = get_attribute(self, "js_object");
return __array[index];
}
window["__list___getitem__"] = __list___getitem__ 

__list___getitem__.NAME = "__list___getitem__";
__list___getitem__.args_signature = ["self", "index"];
__list___getitem__.kwargs_signature = {  };
__list___getitem__.types_signature = {  };
__list___getitem__.pythonscript_function = true;
window["__list_attrs"]["__getitem__"] = __list___getitem__;
var __list___setitem__ = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
signature["function_name"] = "__list___setitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
__array = get_attribute(self, "js_object");
__array[index] = value;
}
window["__list___setitem__"] = __list___setitem__ 

__list___setitem__.NAME = "__list___setitem__";
__list___setitem__.args_signature = ["self", "index", "value"];
__list___setitem__.kwargs_signature = {  };
__list___setitem__.types_signature = {  };
__list___setitem__.pythonscript_function = true;
window["__list_attrs"]["__setitem__"] = __list___setitem__;
var __list_append = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__list_append";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
__array.push(obj);
}
window["__list_append"] = __list_append 

__list_append.NAME = "__list_append";
__list_append.args_signature = ["self", "obj"];
__list_append.kwargs_signature = {  };
__list_append.types_signature = {  };
__list_append.pythonscript_function = true;
window["__list_attrs"]["append"] = __list_append;
var __list_extend = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "other")};
signature["function_name"] = "__list_extend";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var other = arguments['other'];
var __iterator__, obj;
__iterator__ = get_attribute(get_attribute(other, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
obj = __next__();
get_attribute(get_attribute(self, "append"), "__call__")([obj], Object());
}
}
window["__list_extend"] = __list_extend 

__list_extend.NAME = "__list_extend";
__list_extend.args_signature = ["self", "other"];
__list_extend.kwargs_signature = {  };
__list_extend.types_signature = {  };
__list_extend.pythonscript_function = true;
window["__list_attrs"]["extend"] = __list_extend;
var __list_insert = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "obj")};
signature["function_name"] = "__list_insert";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
__array.splice(index, 0, obj);
}
window["__list_insert"] = __list_insert 

__list_insert.NAME = "__list_insert";
__list_insert.args_signature = ["self", "index", "obj"];
__list_insert.kwargs_signature = {  };
__list_insert.types_signature = {  };
__list_insert.pythonscript_function = true;
window["__list_attrs"]["insert"] = __list_insert;
var __list_remove = function(args, kwargs) {
var index, __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__list_remove";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
index = get_attribute(get_attribute(self, "index"), "__call__")([obj], Object());
__array = get_attribute(self, "js_object");
__array.splice(index, 1);
}
window["__list_remove"] = __list_remove 

__list_remove.NAME = "__list_remove";
__list_remove.args_signature = ["self", "obj"];
__list_remove.kwargs_signature = {  };
__list_remove.types_signature = {  };
__list_remove.pythonscript_function = true;
window["__list_attrs"]["remove"] = __list_remove;
var __list_pop = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__list_pop";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.pop();
}
window["__list_pop"] = __list_pop 

__list_pop.NAME = "__list_pop";
__list_pop.args_signature = ["self"];
__list_pop.kwargs_signature = {  };
__list_pop.types_signature = {  };
__list_pop.pythonscript_function = true;
window["__list_attrs"]["pop"] = __list_pop;
var __list_index = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__list_index";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
var __array;
__array = get_attribute(self, "js_object");
return __array.indexOf(obj);
}
window["__list_index"] = __list_index 

__list_index.NAME = "__list_index";
__list_index.args_signature = ["self", "obj"];
__list_index.kwargs_signature = {  };
__list_index.types_signature = {  };
__list_index.pythonscript_function = true;
window["__list_attrs"]["index"] = __list_index;
var __list_count = function(args, kwargs) {
var i;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "obj")};
signature["function_name"] = "__list_count";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var obj = arguments['obj'];
i = 0;
var __iterator__, other;
__iterator__ = get_attribute(get_attribute(self, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
other = __next__();
if(other == obj) {
i = i + 1;
}

}
return i;
}
window["__list_count"] = __list_count 

__list_count.NAME = "__list_count";
__list_count.args_signature = ["self", "obj"];
__list_count.kwargs_signature = {  };
__list_count.types_signature = {  };
__list_count.pythonscript_function = true;
window["__list_attrs"]["count"] = __list_count;
var __list_reverse = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__list_reverse";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
set_attribute(self, "js_object", __array.reverse());
}
window["__list_reverse"] = __list_reverse 

__list_reverse.NAME = "__list_reverse";
__list_reverse.args_signature = ["self"];
__list_reverse.kwargs_signature = {  };
__list_reverse.types_signature = {  };
__list_reverse.pythonscript_function = true;
window["__list_attrs"]["reverse"] = __list_reverse;
var __list_shift = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__list_shift";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.shift();
}
window["__list_shift"] = __list_shift 

__list_shift.NAME = "__list_shift";
__list_shift.args_signature = ["self"];
__list_shift.kwargs_signature = {  };
__list_shift.types_signature = {  };
__list_shift.pythonscript_function = true;
window["__list_attrs"]["shift"] = __list_shift;
var __list_slice = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "start", "end")};
signature["function_name"] = "__list_slice";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
var __array;
__array = get_attribute(self, "js_object");
return __array.slice(start, end);
}
window["__list_slice"] = __list_slice 

__list_slice.NAME = "__list_slice";
__list_slice.args_signature = ["self", "start", "end"];
__list_slice.kwargs_signature = {  };
__list_slice.types_signature = {  };
__list_slice.pythonscript_function = true;
window["__list_attrs"]["slice"] = __list_slice;
var __list___iter__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__list___iter__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return get_attribute(Iterator, "__call__")([self, 0], Object());
}
window["__list___iter__"] = __list___iter__ 

__list___iter__.NAME = "__list___iter__";
__list___iter__.args_signature = ["self"];
__list___iter__.kwargs_signature = {  };
__list___iter__.types_signature = {  };
__list___iter__.return_type = "Iterator";
__list___iter__.pythonscript_function = true;
window["__list_attrs"]["__iter__"] = __list___iter__;
var __list_get = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__list_get";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var __array;
__array = get_attribute(self, "js_object");
return __array[index];
}
window["__list_get"] = __list_get 

__list_get.NAME = "__list_get";
__list_get.args_signature = ["self", "index"];
__list_get.kwargs_signature = {  };
__list_get.types_signature = {  };
__list_get.pythonscript_function = true;
window["__list_attrs"]["get"] = __list_get;
var __list_set = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
signature["function_name"] = "__list_set";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
var value = arguments['value'];
var __array;
__array = get_attribute(self, "js_object");
__array[index] = value;
}
window["__list_set"] = __list_set 

__list_set.NAME = "__list_set";
__list_set.args_signature = ["self", "index", "value"];
__list_set.kwargs_signature = {  };
__list_set.types_signature = {  };
__list_set.pythonscript_function = true;
window["__list_attrs"]["set"] = __list_set;
var __list___len__ = function(args, kwargs) {
var __array;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__list___len__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var __array;
__array = get_attribute(self, "js_object");
return __array.length;
}
window["__list___len__"] = __list___len__ 

__list___len__.NAME = "__list___len__";
__list___len__.args_signature = ["self"];
__list___len__.kwargs_signature = {  };
__list___len__.types_signature = {  };
__list___len__.pythonscript_function = true;
window["__list_attrs"]["__len__"] = __list___len__;
var __list___contains__ = function(args, kwargs) {
var arr;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__list___contains__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
arr = get_attribute(self, "js_object");
if(arr.indexOf(value) == -1) {
return false;
}
else {
return true;
}

}
window["__list___contains__"] = __list___contains__ 

__list___contains__.NAME = "__list___contains__";
__list___contains__.args_signature = ["self", "value"];
__list___contains__.kwargs_signature = {  };
__list___contains__.types_signature = {  };
__list___contains__.pythonscript_function = true;
window["__list_attrs"]["__contains__"] = __list___contains__;
list = create_class("list", window["__list_parents"], window["__list_attrs"], window["__list_properties"]);
var dict, __dict_attrs, __dict_parents;
window["__dict_attrs"] = Object();
window["__dict_parents"] = create_array();
window["__dict_properties"] = Object();
__dict_UID = 0;
window["__dict_attrs"]["UID"] = __dict_UID;
var __dict___init__ = function(args, kwargs) {
var i, jsob;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"js_object": undefined}, "args": create_array("self", "js_object")};
signature["function_name"] = "__dict___init__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var js_object = arguments['js_object'];
if(js_object) {
if(js_object instanceof Array) {
set_attribute(self, "js_object", Object());
i = 0;
while(i < get_attribute(js_object, "length")) {
var key = js_object[i]["key"];
var value = js_object[i]["value"];
get_attribute(get_attribute(self, "set"), "__call__")([key, value], Object());
i += 1
}
}
else {
set_attribute(self, "js_object", js_object);
}

}
else {
set_attribute(self, "js_object", Object());
}

jsob = get_attribute(self, "js_object");
self["wrapped"] = jsob;
}
window["__dict___init__"] = __dict___init__ 

__dict___init__.NAME = "__dict___init__";
__dict___init__.args_signature = ["self", "js_object"];
__dict___init__.kwargs_signature = { js_object:undefined };
__dict___init__.types_signature = { js_object:"None" };
__dict___init__.pythonscript_function = true;
window["__dict_attrs"]["__init__"] = __dict___init__;
var __dict_get = function(args, kwargs) {
var __dict;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"_default": undefined}, "args": create_array("self", "key", "_default")};
signature["function_name"] = "__dict_get";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var _default = arguments['_default'];
__dict = get_attribute(self, "js_object");
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

__dict_get.NAME = "__dict_get";
__dict_get.args_signature = ["self", "key", "_default"];
__dict_get.kwargs_signature = { _default:undefined };
__dict_get.types_signature = { _default:"None" };
__dict_get.pythonscript_function = true;
window["__dict_attrs"]["get"] = __dict_get;
var __dict_set = function(args, kwargs) {
var __dict, uid;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
signature["function_name"] = "__dict_set";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
__dict = get_attribute(self, "js_object");
if(typeof(key) === 'object') {
if(key.uid === undefined) {
uid = _PythonJS_UID;
key.uid = uid;
_PythonJS_UID += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
if(typeof(key) === 'function') {
if(key.uid === undefined) {
uid = _PythonJS_UID;
key.uid = uid;
_PythonJS_UID += 1
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

__dict_set.NAME = "__dict_set";
__dict_set.args_signature = ["self", "key", "value"];
__dict_set.kwargs_signature = {  };
__dict_set.types_signature = {  };
__dict_set.pythonscript_function = true;
window["__dict_attrs"]["set"] = __dict_set;
var __dict___len__ = function(args, kwargs) {
var __dict;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__dict___len__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
__dict = get_attribute(self, "js_object");
return Object.keys(__dict).length;
}
window["__dict___len__"] = __dict___len__ 

__dict___len__.NAME = "__dict___len__";
__dict___len__.args_signature = ["self"];
__dict___len__.kwargs_signature = {  };
__dict___len__.types_signature = {  };
__dict___len__.pythonscript_function = true;
window["__dict_attrs"]["__len__"] = __dict___len__;
var __dict___getitem__ = function(args, kwargs) {
var __dict;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key")};
signature["function_name"] = "__dict___getitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
__dict = get_attribute(self, "js_object");
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

__dict___getitem__.NAME = "__dict___getitem__";
__dict___getitem__.args_signature = ["self", "key"];
__dict___getitem__.kwargs_signature = {  };
__dict___getitem__.types_signature = {  };
__dict___getitem__.pythonscript_function = true;
window["__dict_attrs"]["__getitem__"] = __dict___getitem__;
var __dict___setitem__ = function(args, kwargs) {
var __dict, uid;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
signature["function_name"] = "__dict___setitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
__dict = get_attribute(self, "js_object");
if(typeof(key) === 'object') {
if(key.uid === undefined) {
uid = _PythonJS_UID;
key.uid = uid;
_PythonJS_UID += 1
}

var uid = key.uid;
__dict["@"+uid] = value;
}
else {
if(typeof(key) === 'function') {
if(key.uid === undefined) {
uid = _PythonJS_UID;
key.uid = uid;
_PythonJS_UID += 1
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

__dict___setitem__.NAME = "__dict___setitem__";
__dict___setitem__.args_signature = ["self", "key", "value"];
__dict___setitem__.kwargs_signature = {  };
__dict___setitem__.types_signature = {  };
__dict___setitem__.pythonscript_function = true;
window["__dict_attrs"]["__setitem__"] = __dict___setitem__;
var __dict_keys = function(args, kwargs) {
var arr;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__dict_keys";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
arr = Object.keys( self["wrapped"] );
var __args_0, __kwargs_0;
__args_0 = [];
__kwargs_0 = {"js_object": arr};
return get_attribute(list, "__call__")([], __kwargs_0);
}
window["__dict_keys"] = __dict_keys 

__dict_keys.NAME = "__dict_keys";
__dict_keys.args_signature = ["self"];
__dict_keys.kwargs_signature = {  };
__dict_keys.types_signature = {  };
__dict_keys.return_type = "list";
__dict_keys.pythonscript_function = true;
window["__dict_attrs"]["keys"] = __dict_keys;
var __dict_pop = function(args, kwargs) {
var js_object, v;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"d": undefined}, "args": create_array("self", "key", "d")};
signature["function_name"] = "__dict_pop";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var d = arguments['d'];
v = get_attribute(get_attribute(self, "get"), "__call__")([key, undefined], Object());
if(v === undefined) {
return d;
}
else {
js_object = get_attribute(self, "js_object");
delete js_object[key];
return v;
}

}
window["__dict_pop"] = __dict_pop 

__dict_pop.NAME = "__dict_pop";
__dict_pop.args_signature = ["self", "key", "d"];
__dict_pop.kwargs_signature = { d:undefined };
__dict_pop.types_signature = { d:"None" };
__dict_pop.pythonscript_function = true;
window["__dict_attrs"]["pop"] = __dict_pop;
var __dict_values = function(args, kwargs) {
var __dict, __keys, i, out;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__dict_values";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
__dict = get_attribute(self, "js_object");
__keys = Object.keys(__dict);
out = get_attribute(list, "__call__")(create_array(), Object());
i = 0;
while(i < get_attribute(__keys, "length")) {
get_attribute(get_attribute(out, "append"), "__call__")([__dict[ __keys[i] ]], Object());
i += 1
}
return out;
}
window["__dict_values"] = __dict_values 

__dict_values.NAME = "__dict_values";
__dict_values.args_signature = ["self"];
__dict_values.kwargs_signature = {  };
__dict_values.types_signature = {  };
__dict_values.pythonscript_function = true;
window["__dict_attrs"]["values"] = __dict_values;
var __dict___contains__ = function(args, kwargs) {
var keys;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__dict___contains__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
keys = Object.keys( self["wrapped"] );
if(typeof(value) == "object") {
key = "@" + value.uid;
}
else {
key = "" + value;
}

if(keys.indexOf(key) == -1) {
return false;
}
else {
return true;
}

}
window["__dict___contains__"] = __dict___contains__ 

__dict___contains__.NAME = "__dict___contains__";
__dict___contains__.args_signature = ["self", "value"];
__dict___contains__.kwargs_signature = {  };
__dict___contains__.types_signature = {  };
__dict___contains__.pythonscript_function = true;
window["__dict_attrs"]["__contains__"] = __dict___contains__;
var __dict___iter__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__dict___iter__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return get_attribute(Iterator, "__call__")([get_attribute(get_attribute(self, "keys"), "__call__")(create_array(), Object()), 0], Object());
}
window["__dict___iter__"] = __dict___iter__ 

__dict___iter__.NAME = "__dict___iter__";
__dict___iter__.args_signature = ["self"];
__dict___iter__.kwargs_signature = {  };
__dict___iter__.types_signature = {  };
__dict___iter__.return_type = "Iterator";
__dict___iter__.pythonscript_function = true;
window["__dict_attrs"]["__iter__"] = __dict___iter__;
dict = create_class("dict", window["__dict_parents"], window["__dict_attrs"], window["__dict_properties"]);
var array, __array_attrs, __array_parents;
window["__array_attrs"] = Object();
window["__array_parents"] = create_array();
window["__array_properties"] = Object();
__array_typecodes = get_attribute(dict, "__call__")([], {"js_object": [{"key": "c", "value": 1}, {"key": "b", "value": 1}, {"key": "B", "value": 1}, {"key": "u", "value": 2}, {"key": "h", "value": 2}, {"key": "H", "value": 2}, {"key": "i", "value": 4}, {"key": "I", "value": 4}, {"key": "l", "value": 4}, {"key": "L", "value": 4}, {"key": "f", "value": 4}, {"key": "d", "value": 8}, {"key": "float32", "value": 4}, {"key": "float16", "value": 2}, {"key": "float8", "value": 1}, {"key": "int32", "value": 4}, {"key": "uint32", "value": 4}, {"key": "int16", "value": 2}, {"key": "uint16", "value": 2}, {"key": "int8", "value": 1}, {"key": "uint8", "value": 1}]});
window["__array_attrs"]["typecodes"] = __array_typecodes;
__array_typecode_names = get_attribute(dict, "__call__")([], {"js_object": [{"key": "c", "value": "Int8"}, {"key": "b", "value": "Int8"}, {"key": "B", "value": "Uint8"}, {"key": "u", "value": "Uint16"}, {"key": "h", "value": "Int16"}, {"key": "H", "value": "Uint16"}, {"key": "i", "value": "Int32"}, {"key": "I", "value": "Uint32"}, {"key": "f", "value": "Float32"}, {"key": "d", "value": "Float64"}, {"key": "float32", "value": "Float32"}, {"key": "float16", "value": "Int16"}, {"key": "float8", "value": "Int8"}, {"key": "int32", "value": "Int32"}, {"key": "uint32", "value": "Uint32"}, {"key": "int16", "value": "Int16"}, {"key": "uint16", "value": "Uint16"}, {"key": "int8", "value": "Int8"}, {"key": "uint8", "value": "Uint8"}]});
window["__array_attrs"]["typecode_names"] = __array_typecode_names;
var __array___init__ = function(args, kwargs) {
var size, buff;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": {"initializer": undefined, "little_endian": false}, "args": create_array("self", "typecode", "initializer", "little_endian")};
signature["function_name"] = "__array___init__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var typecode = arguments['typecode'];
var initializer = arguments['initializer'];
var little_endian = arguments['little_endian'];
self["__dict__"]["typecode"] = typecode;
self["__dict__"]["itemsize"] = get_attribute(get_attribute(self, "typecodes"), "__getitem__")([typecode], Object());
self["__dict__"]["little_endian"] = little_endian;
if(initializer) {
self["__dict__"]["length"] = get_attribute(len, "__call__")([initializer], Object());
self["__dict__"]["bytes"] = self["__dict__"]["length"] * self["__dict__"]["itemsize"];
if(self["__dict__"]["typecode"] == "float8") {
self["__dict__"]["_scale"] = get_attribute(max, "__call__")([get_attribute(list, "__call__")([], {"js_object": [get_attribute(abs, "__call__")([get_attribute(min, "__call__")([initializer], Object())], Object()), get_attribute(max, "__call__")([initializer], Object())]})], Object());
self["__dict__"]["_norm_get"] = self["__dict__"]["_scale"] / 127;
self["__dict__"]["_norm_set"] = 1.0 / self["__dict__"]["_norm_get"];
}
else {
if(self["__dict__"]["typecode"] == "float16") {
self["__dict__"]["_scale"] = get_attribute(max, "__call__")([get_attribute(list, "__call__")([], {"js_object": [get_attribute(abs, "__call__")([get_attribute(min, "__call__")([initializer], Object())], Object()), get_attribute(max, "__call__")([initializer], Object())]})], Object());
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
get_attribute(get_attribute(self, "fromlist"), "__call__")([initializer], Object());
}
window["__array___init__"] = __array___init__ 

__array___init__.NAME = "__array___init__";
__array___init__.args_signature = ["self", "typecode", "initializer", "little_endian"];
__array___init__.kwargs_signature = { initializer:undefined,little_endian:false };
__array___init__.types_signature = { initializer:"None",little_endian:"False" };
__array___init__.pythonscript_function = true;
window["__array_attrs"]["__init__"] = __array___init__;
var __array___len__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__array___len__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return self["__dict__"]["length"];
}
window["__array___len__"] = __array___len__ 

__array___len__.NAME = "__array___len__";
__array___len__.args_signature = ["self"];
__array___len__.kwargs_signature = {  };
__array___len__.types_signature = {  };
__array___len__.pythonscript_function = true;
window["__array_attrs"]["__len__"] = __array___len__;
var __array___contains__ = function(args, kwargs) {
var arr;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__array___contains__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
arr = get_attribute(get_attribute(self, "to_array"), "__call__")(create_array(), Object());
if(arr.indexOf(value) == -1) {
return false;
}
else {
return true;
}

}
window["__array___contains__"] = __array___contains__ 

__array___contains__.NAME = "__array___contains__";
__array___contains__.args_signature = ["self", "value"];
__array___contains__.kwargs_signature = {  };
__array___contains__.types_signature = {  };
__array___contains__.pythonscript_function = true;
window["__array_attrs"]["__contains__"] = __array___contains__;
var __array___getitem__ = function(args, kwargs) {
var func_name, dataview, value, step, func, offset;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__array___getitem__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
step = self["__dict__"]["itemsize"];
offset = step * index;
dataview = self["__dict__"]["dataview"];
func_name = "get" + get_attribute(get_attribute(self, "typecode_names"), "__getitem__")([self["__dict__"]["typecode"]], Object());
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

__array___getitem__.NAME = "__array___getitem__";
__array___getitem__.args_signature = ["self", "index"];
__array___getitem__.kwargs_signature = {  };
__array___getitem__.types_signature = {  };
__array___getitem__.pythonscript_function = true;
window["__array_attrs"]["__getitem__"] = __array___getitem__;
var __array___setitem__ = function(args, kwargs) {
var index, func_name, dataview, value, step, func, offset;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index", "value")};
signature["function_name"] = "__array___setitem__";
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
func_name = "set" + get_attribute(get_attribute(self, "typecode_names"), "__getitem__")([self["__dict__"]["typecode"]], Object());
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

__array___setitem__.NAME = "__array___setitem__";
__array___setitem__.args_signature = ["self", "index", "value"];
__array___setitem__.kwargs_signature = {  };
__array___setitem__.types_signature = {  };
__array___setitem__.pythonscript_function = true;
window["__array_attrs"]["__setitem__"] = __array___setitem__;
var __array___iter__ = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__array___iter__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
return get_attribute(Iterator, "__call__")([self, 0], Object());
}
window["__array___iter__"] = __array___iter__ 

__array___iter__.NAME = "__array___iter__";
__array___iter__.args_signature = ["self"];
__array___iter__.kwargs_signature = {  };
__array___iter__.types_signature = {  };
__array___iter__.return_type = "Iterator";
__array___iter__.pythonscript_function = true;
window["__array_attrs"]["__iter__"] = __array___iter__;
var __array_get = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__array_get";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
return __array___getitem__([self, index], Object());
}
window["__array_get"] = __array_get 

__array_get.NAME = "__array_get";
__array_get.args_signature = ["self", "index"];
__array_get.kwargs_signature = {  };
__array_get.types_signature = {  };
__array_get.pythonscript_function = true;
window["__array_attrs"]["get"] = __array_get;
var __array_fromlist = function(args, kwargs) {
var typecode, i, func_name, dataview, length, item, step, func, offset, size;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "lst")};
signature["function_name"] = "__array_fromlist";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var lst = arguments['lst'];
length = get_attribute(len, "__call__")([lst], Object());
step = self["__dict__"]["itemsize"];
typecode = self["__dict__"]["typecode"];
size = length * step;
dataview = self["__dict__"]["dataview"];
func_name = "set" + get_attribute(get_attribute(self, "typecode_names"), "__getitem__")([typecode], Object());
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

__array_fromlist.NAME = "__array_fromlist";
__array_fromlist.args_signature = ["self", "lst"];
__array_fromlist.kwargs_signature = {  };
__array_fromlist.types_signature = {  };
__array_fromlist.pythonscript_function = true;
window["__array_attrs"]["fromlist"] = __array_fromlist;
var __array_resize = function(args, kwargs) {
var source, new_buff, target, new_size, buff;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "length")};
signature["function_name"] = "__array_resize";
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

__array_resize.NAME = "__array_resize";
__array_resize.args_signature = ["self", "length"];
__array_resize.kwargs_signature = {  };
__array_resize.types_signature = {  };
__array_resize.pythonscript_function = true;
window["__array_attrs"]["resize"] = __array_resize;
var __array_append = function(args, kwargs) {
var length;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__array_append";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
length = self["__dict__"]["length"];
get_attribute(get_attribute(self, "resize"), "__call__")([self["__dict__"]["length"] + 1], Object());
get_attribute(get_attribute(self, "__setitem__"), "__call__")([length, value], Object());
}
window["__array_append"] = __array_append 

__array_append.NAME = "__array_append";
__array_append.args_signature = ["self", "value"];
__array_append.kwargs_signature = {  };
__array_append.types_signature = {  };
__array_append.pythonscript_function = true;
window["__array_attrs"]["append"] = __array_append;
var __array_extend = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "lst")};
signature["function_name"] = "__array_extend";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var lst = arguments['lst'];
var __iterator__, value;
__iterator__ = get_attribute(get_attribute(lst, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
value = __next__();
get_attribute(get_attribute(self, "append"), "__call__")([value], Object());
}
}
window["__array_extend"] = __array_extend 

__array_extend.NAME = "__array_extend";
__array_extend.args_signature = ["self", "lst"];
__array_extend.kwargs_signature = {  };
__array_extend.types_signature = {  };
__array_extend.pythonscript_function = true;
window["__array_attrs"]["extend"] = __array_extend;
var __array_to_array = function(args, kwargs) {
var i, item, arr;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__array_to_array";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
arr = create_array();
i = 0;
while(i < self["__dict__"]["length"]) {
item = __array___getitem__([self, i], Object());
arr.push( item );
i += 1
}
return arr;
}
window["__array_to_array"] = __array_to_array 

__array_to_array.NAME = "__array_to_array";
__array_to_array.args_signature = ["self"];
__array_to_array.kwargs_signature = {  };
__array_to_array.types_signature = {  };
__array_to_array.pythonscript_function = true;
window["__array_attrs"]["to_array"] = __array_to_array;
var __array_to_list = function(args, kwargs) {
var lst;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__array_to_list";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
lst = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(lst, "js_object", get_attribute(get_attribute(self, "to_array"), "__call__")(create_array(), Object()));
return lst;
}
window["__array_to_list"] = __array_to_list 

__array_to_list.NAME = "__array_to_list";
__array_to_list.args_signature = ["self"];
__array_to_list.kwargs_signature = {  };
__array_to_list.types_signature = {  };
__array_to_list.pythonscript_function = true;
window["__array_attrs"]["to_list"] = __array_to_list;
var __array_to_ascii = function(args, kwargs) {
var i, length, arr, string;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__array_to_ascii";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
string = "";
arr = get_attribute(get_attribute(self, "to_array"), "__call__")(create_array(), Object());
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

__array_to_ascii.NAME = "__array_to_ascii";
__array_to_ascii.args_signature = ["self"];
__array_to_ascii.kwargs_signature = {  };
__array_to_ascii.types_signature = {  };
__array_to_ascii.pythonscript_function = true;
window["__array_attrs"]["to_ascii"] = __array_to_ascii;
array = create_class("array", window["__array_parents"], window["__array_attrs"], window["__array_properties"]);
var _to_pythonjs = function(args, kwargs) {
var set, keys, raw, jstype, output, append;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("json")};
signature["function_name"] = "_to_pythonjs";
arguments = get_arguments(signature, args, kwargs);
var json = arguments['json'];
var jstype, item, output;
jstype = typeof json;
if(jstype == "number") {
return json;
}

if(jstype == "string") {
return json;
}

if(Object.prototype.toString.call(json) === '[object Array]') {
output = get_attribute(list, "__call__")(create_array(), Object());
raw = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(raw, "js_object", json);
var append;
append = get_attribute(output, "append");
var __iterator__, item;
__iterator__ = get_attribute(get_attribute(raw, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
item = __next__();
get_attribute(append, "__call__")([get_attribute(_to_pythonjs, "__call__")([item], Object())], Object());
}
return output;
}

output = get_attribute(dict, "__call__")(create_array(), Object());
var set;
set = get_attribute(output, "set");
keys = get_attribute(list, "__call__")(create_array(), Object());
set_attribute(keys, "js_object", Object.keys(json));
var __iterator__, key;
__iterator__ = get_attribute(get_attribute(keys, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
key = __next__();
get_attribute(set, "__call__")([key, get_attribute(_to_pythonjs, "__call__")([json[key]], Object())], Object());
}
return output;
}
window["_to_pythonjs"] = _to_pythonjs 

_to_pythonjs.NAME = "_to_pythonjs";
_to_pythonjs.args_signature = ["json"];
_to_pythonjs.kwargs_signature = {  };
_to_pythonjs.types_signature = {  };
_to_pythonjs.pythonscript_function = true;
var json_to_pythonjs = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("json")};
signature["function_name"] = "json_to_pythonjs";
arguments = get_arguments(signature, args, kwargs);
var json = arguments['json'];
return get_attribute(_to_pythonjs, "__call__")([get_attribute(get_attribute(JSON, "parse"), "__call__")([json], Object())], Object());
}
window["json_to_pythonjs"] = json_to_pythonjs 

json_to_pythonjs.NAME = "json_to_pythonjs";
json_to_pythonjs.args_signature = ["json"];
json_to_pythonjs.kwargs_signature = {  };
json_to_pythonjs.types_signature = {  };
json_to_pythonjs.pythonscript_function = true;
var _to_json = function(args, kwargs) {
var r, key, value;
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("pythonjs")};
signature["function_name"] = "_to_json";
arguments = get_arguments(signature, args, kwargs);
var pythonjs = arguments['pythonjs'];
if(get_attribute(isinstance, "__call__")([pythonjs, list], Object())) {
r = create_array();
var __iterator__, i;
__iterator__ = get_attribute(get_attribute(pythonjs, "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
i = __next__();
get_attribute(get_attribute(r, "push"), "__call__")([get_attribute(_to_json, "__call__")([i], Object())], Object());
}
}
else {
if(get_attribute(isinstance, "__call__")([pythonjs, dict], Object())) {
var r;
r = Object();
var __iterator__, key;
__iterator__ = get_attribute(get_attribute(get_attribute(get_attribute(pythonjs, "keys"), "__call__")(create_array(), Object()), "__iter__"), "__call__")(create_array(), Object());
var __next__;
__next__ = get_attribute(__iterator__, "next_fast");
while(__iterator__.__dict__.index < __iterator__.__dict__.length) {
key = __next__();
value = get_attribute(_to_json, "__call__")([get_attribute(get_attribute(pythonjs, "get"), "__call__")([key], Object())], Object());
key = get_attribute(_to_json, "__call__")([key], Object());
r[ key ] = value;
}
}
else {
r = pythonjs;
}

}

return r;
}
window["_to_json"] = _to_json 

_to_json.NAME = "_to_json";
_to_json.args_signature = ["pythonjs"];
_to_json.kwargs_signature = {  };
_to_json.types_signature = {  };
_to_json.pythonscript_function = true;
var pythonjs_to_json = function(args, kwargs) {
if(args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2) {
/*pass*/
}
else {
args = Array.prototype.slice.call(arguments);
kwargs = Object();
}

var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("pythonjs")};
signature["function_name"] = "pythonjs_to_json";
arguments = get_arguments(signature, args, kwargs);
var pythonjs = arguments['pythonjs'];
return get_attribute(get_attribute(JSON, "stringify"), "__call__")([get_attribute(_to_json, "__call__")([pythonjs], Object())], Object());
}
window["pythonjs_to_json"] = pythonjs_to_json 

pythonjs_to_json.NAME = "pythonjs_to_json";
pythonjs_to_json.args_signature = ["pythonjs"];
pythonjs_to_json.kwargs_signature = {  };
pythonjs_to_json.types_signature = {  };
pythonjs_to_json.pythonscript_function = true;