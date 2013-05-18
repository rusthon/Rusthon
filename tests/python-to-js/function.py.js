var function = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("a", "b", "c", "d")};
var arguments = get_arguments(signature, args, kwargs);
var d = arguments["d"];
var c = arguments["c"];
var b = arguments["b"];
var a = arguments["a"];
return a + b + c + d;
}

console.log(get_attribute(function, "__call__")(create_array(1, 2, 3, 4), {}));
