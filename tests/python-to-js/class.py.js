A = {};
parents = create_array();
parents.push(B, C);
var A__METHOD = function(args, kwargs) {
    var signature = {"kwargs": {"d": 4, "e": 5}, "args": create_array("self", "a", "b", "c", "d", "e")};
    var arguments = get_arguments(signature, args, kwargs);
    var self = arguments["self"];
    var a = arguments["a"];
    var b = arguments["b"];
    var c = arguments["c"];
    var d = arguments["d"];
    var e = arguments["e"];
    return a + b + c + d + e;
}

A.METHOD = A__METHOD;
A = create_class("A", parents, A);
a = get_attribute(A, "__call__")(create_array(), {});
console.log(get_attribute(get_attribute(a, "METHOD"), "__call__")(create_array(1, 2, 3), {}));
console.log(get_attribute(get_attribute(a, "METHOD"), "__call__")(create_array(1, 2, 3, 6, 7), {}));
