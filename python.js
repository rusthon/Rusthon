var create_object = function() {
object = Object();
object.__class__ = klass;
object.__dict__ = Object();
init = get_attribute(object, "__init__");
if(init) {
init.apply(undefined, arguments);
}
return object;
}
var create_class = function(class_name, parents, attrs) {
klass = Object();
klass.bases = parents;
klass.__name__ = class_name;
klass.__dict__ = attrs;
var __call__ = function() {
args = Array.prototype.splice.apply(arguments, [0, 0, klass]);
return create_object.apply(undefined, args);
}
klass.__call__ = create_object;
return klass;
}
var get_attribute = function(object, attribute) {
if(attribute == "__call__") {
name = Object().toString.call(object);
if(name == "[object Function]") {
return object;}
}
attr = object[attribute];
if(attr) {
return attr;}
__dict__ = object.__dict__;
if(__dict__) {
attr = get_attribute(__dict__, attribute);
if(attr) {
return attr;}
}
__class__ = object.__class__;
if(__class__) {
__dict__ = __class__.__dict__;
attr = __dict__[attribute];
if(attr) {
name = Object().toString.call(attr);
if(name == "[object Function]") {
var method = function() {
o = Array.prototype.splice.apply(arguments, [0, 0, object]);
r = attr.apply(undefined, arguments);
return r;
}
return method;}
return attr;}
bases = __class__.bases;
for (i=0; i<bases.length; i++) {
base = bases[i];
attr = get_attribute(base, attribute);
if(attr) {
return attr;}
}
}
return undefined;
}
var set_attribute = function(object, attr, value) {
__dict__ = object.__dict__;
__dict__[attr] = value;

}

