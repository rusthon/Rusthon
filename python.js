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
if(_.isFunction(object)) {
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
if(_.isFunction(attr)) {
var method = function() {
arguments[0].splice(0, 0, object);
return attr.apply(undefined, arguments);
}

return method;}

return attr;}

bases = __class__.bases
for (i=0; i<bases.length; i++) {
base = bases[i]
attr = get_attribute(base, attribute)
if(attr) {
return attr;}

}
}

return undefined;
}

var set_attribute = function(object, attr, value) {
__dict__ = object.__dict__
__dict__.___set(attr, value);
}

var get_arguments = function(parameters, args, kwargs) {
out = {}
if(parameters.args.length) {
argslength = parameters.args.length}
else {
argslength = 0}

kwargslength = Object.keys(parameters.kwargs).length
j = 0
for (i=0; i<argslength; i++) {
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

}

args = args.slice(j)
if(parameters.vararg) {
out[parameters.vararg] = args;}

if(parameters.varkwarg) {
out[parameters.varkwarg] = kwargs;}

return out;
}

