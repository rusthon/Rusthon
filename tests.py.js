var test_equal = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("a", "b", "message")};
var arguments = get_arguments(signature, args, kwargs);
var a = arguments["a"];
var b = arguments["b"];
var message = arguments["message"];
if(a == b) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

var test_true = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("a", "message")};
var arguments = get_arguments(signature, args, kwargs);
var a = arguments["a"];
var message = arguments["message"];
if(a) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

var test_false = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("a", "message")};
var arguments = get_arguments(signature, args, kwargs);
var a = arguments["a"];
var message = arguments["message"];
if(!a) {
console.log(message);
}
else {
console.log(message, "failed");
}

}

tests = get_attribute(list, "__call__")(create_array(), {});
var test_issubclass = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array()};
var arguments = get_arguments(signature, args, kwargs);
A = {};
parents = create_array();
A = create_class("A", parents, A);
B = {};
parents = create_array();
parents.push(A);
B = create_class("B", parents, B);
C = {};
parents = create_array();
parents.push(B);
C = create_class("C", parents, C);
D = {};
parents = create_array();
D = create_class("D", parents, D);
E = {};
parents = create_array();
parents.push(C, D);
E = create_class("E", parents, E);
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(C, C), {}), "C is a subclass of C"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(C, B), {}), "C is a subclass of B"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(C, A), {}), "C is a subclass of A"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(B, B), {}), "B is a subclass of B"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(B, A), {}), "B is a subclass of A"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(A, A), {}), "A is a subclass of A"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(A, B), {}), "A is not a subclass of B"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(B, C), {}), "B is not a subclass of C"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(D, A), {}), "D is not a subclass of A"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(D, C), {}), "D is not a subclass of C"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(E, E), {}), "E is subclass of E"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(E, D), {}), "E is subclass of D"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(E, C), {}), "E is subclass of C"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(E, B), {}), "E is subclass of B"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(issubclass, "__call__")(create_array(E, A), {}), "E is subclass of A"), {});
}

get_attribute(get_attribute(tests, "append"), "__call__")(create_array(test_issubclass), {});
var test_isinstance = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array()};
var arguments = get_arguments(signature, args, kwargs);
A = {};
parents = create_array();
A = create_class("A", parents, A);
B = {};
parents = create_array();
parents.push(A);
B = create_class("B", parents, B);
X = {};
parents = create_array();
X = create_class("X", parents, X);
Y = {};
parents = create_array();
parents.push(X);
Y = create_class("Y", parents, Y);
get_attribute(test_true, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(get_attribute(A, "__call__")(create_array(), {}), A), {}), "A() is an instance of A"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(get_attribute(B, "__call__")(create_array(), {}), A), {}), "B() is an instance of A"), {});
get_attribute(test_true, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(get_attribute(B, "__call__")(create_array(), {}), A), {}), "B() is an instance of B"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(B, B), {}), "B is not an instance of B"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(B, A), {}), "B is not an instance of A"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(get_attribute(B, "__call__")(create_array(), {}), X), {}), "B() is not an instance of X"), {});
get_attribute(test_false, "__call__")(create_array(get_attribute(isinstance, "__call__")(create_array(get_attribute(B, "__call__")(create_array(), {}), Y), {}), "B() is not an instance of Y"), {});
}

get_attribute(get_attribute(tests, "append"), "__call__")(create_array(test_isinstance), {});
var __iterator__ = get_attribute(tests, "__iter__")(create_array(), {});
try {
var test = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
get_attribute(test, "__call__")(create_array(), {});
var test = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

