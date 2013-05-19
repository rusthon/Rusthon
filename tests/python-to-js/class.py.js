['B']
['C']
['signature', 'args', 'kwargs']
['"A"', '__A_parents', '__A_attrs']
['A', '"__call__"']
['__args_0', '__kwargs_0']
['a', '"METHOD"']
['get_attribute(a, "METHOD")', '"__call__"']
['__args_1', '__kwargs_1']
['a', '"METHOD"']
['get_attribute(a, "METHOD")', '"__call__"']
['__args_2', '__kwargs_2']
var A, __A_attrs, __A_parents;
__A_attrs = {};
__A_parents = create_array();
__A_parents.push(B);
__A_parents.push(C);
var __A_METHOD = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {"d": 4, "e": 5}, "args": create_array("self", "a", "b", "c", "d", "e")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var a = arguments['a'];
var b = arguments['b'];
var c = arguments['c'];
var d = arguments['d'];
var e = arguments['e'];
return a + b + c + d + e;
}

__A_attrs.METHOD = __A_METHOD;
A = create_class("A", __A_parents, __A_attrs);
var __args_0, __kwargs_0;
__args_0 = create_array();
__kwargs_0 = {};
a = get_attribute(A, "__call__")(__args_0, __kwargs_0);
var __args_1, __kwargs_1;
__args_1 = create_array(1, 2, 3);
__kwargs_1 = {};
console.log(get_attribute(get_attribute(a, "METHOD"), "__call__")(__args_1, __kwargs_1));
var __args_2, __kwargs_2;
__args_2 = create_array(1, 2, 3, 6, 7);
__kwargs_2 = {};
console.log(get_attribute(get_attribute(a, "METHOD"), "__call__")(__args_2, __kwargs_2));
