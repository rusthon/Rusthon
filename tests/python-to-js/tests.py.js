['"B"', '__B_parents', '__B_attrs']
['"C"', '__C_parents', '__C_attrs']
['B']
['C']
['"A"', '__A_parents', '__A_attrs']
['egg']
['signature', 'args', 'kwargs']
['list', '"__call__"']
['args']
['create_array(args)', None]
['dict', '"__call__"']
['kwargs']
['create_array(kwargs)', None]
['args', '"__iter__"']
['__iterator__', '"next"']
['__iterator__', '"next"']
['function']
['create_array(function)']
['function']
['create_array(function)']
['__args_0', 'args']
['function', '"__call__"']
['__args_0', '__kwargs_0']
var B, __B_attrs, __B_parents;
__B_attrs = {};
__B_parents = create_array();
B = create_class("B", __B_parents, __B_attrs);
var C, __C_attrs, __C_parents;
__C_attrs = {};
__C_parents = create_array();
C = create_class("C", __C_parents, __C_attrs);
var A, __A_attrs, __A_parents;
__A_attrs = {};
__A_parents = create_array();
__A_parents.push(B);
__A_parents.push(C);
A = create_class("A", __A_parents, __A_attrs);
var a, object, args, str;
a = new Object();
object = {"spam": 7, "egg": 8};
args = create_array(5, 6);
str = toString(egg);
var function = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"c": 3, "d": 4}, "args": create_array("a", "b", "c", "d"), "vararg": "args", "varkwarg": "kwargs"};
arguments = get_arguments(signature, args, kwargs);
var a = arguments['a'];
var b = arguments['b'];
var c = arguments['c'];
var d = arguments['d'];
var args arguments['args'];
args = get_attribute(list, "__call__")(create_array(args));
var kwargs = arguments["kwargs"];
kwargs = get_attribute(dict, "__call__")(create_array(kwargs));
console.log(a, b, c, d);
sum = a + b + c + d;
console.log(sum);
var __iterator__, arg;
__iterator__ = get_attribute(args, "__iter__");
try {
arg = get_attribute(__iterator__, "next")();
while(true) {
console.log(args);
undefined;
arg = get_attribute(__iterator__, "next")();
}
}
catch(__exception__) {
if (__exception__ == StopIteration || isinstance([__exception__, StopIteration])) {

}

}

console.log(kwargs);
}

function = deco_b(create_array(function));
function = deco_a(create_array(function));
var __args_0, __kwargs_0;
__args_0 = create_array(1, 2, 3, 4);
__args_0.push.apply(__args_0, args);
__kwargs_0 = {};
for (var name in kwargs) { __kwargs_0[name] = kwargs[name]; };
get_attribute(function, "__call__")(__args_0, __kwargs_0);
