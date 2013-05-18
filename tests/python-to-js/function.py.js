var function = function(args, kwargs) {
var signature = {"kwargs": {"e": 5, "f": 6}, "args": create_array("a", "b", "c", "d", "e", "f")};
var arguments = get_arguments(signature, args, kwargs);
var a = arguments["a"];
var b = arguments["b"];
var c = arguments["c"];
var d = arguments["d"];
var e = arguments["e"];
var f = arguments["f"];
return a + b + c + d + e + f;
}

console.log(get_attribute(function, "__call__")(create_array(1, 2, 3, 4), {}));
console.log(get_attribute(function, "__call__")(create_array(1, 2, 3, 4, 7, 8), {}));
