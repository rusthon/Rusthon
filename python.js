var create_array = function() {
array = new Array();
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
i = 1
r = [0]
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
if(parameters.args.length) {
argslength = parameters.args.length}
else {
argslength = 0}

kwargslength = Object.keys(parameters.kwargs).length
j = 0
var iter = range(argslength);
for (i=0; i < iter.length; i++) {
var backup = i
i = iter[i];
arg = parameters.args[j]
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
if(parameters.vararg) {
out[parameters.vararg] = args;}

if(parameters.varkwarg) {
out[parameters.varkwarg] = kwargs;}

return out;
}

