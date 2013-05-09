Animator = {};
parents = create_array();
var Animator____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "func", "delay", "loop")};
var arguments = get_arguments(signature, args, kwargs);
var loop = arguments["loop"];
var delay = arguments["delay"];
var func = arguments["func"];
var self = arguments["self"];
set_attribute(self, "func", func);
set_attribute(self, "delay", delay);
set_attribute(self, "loop", loop);
}

Animator.__init__ = Animator____init__;
var Animator__run = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var delay, func;
delay = get_attribute(self, "delay");
func = get_attribute(self, "func");
if(get_attribute(self, "loop")) {
set_attribute(self, "id", setInterval(adapt_arguments(func), delay));
}
else {
setTimeout(adapt_arguments(func), delay);
}

}

Animator.run = Animator__run;
var Animator__stop = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var id;
id = get_attribute(self, "id");
clearInterval(id);
}

Animator.stop = Animator__stop;
Animator = create_class("Animator", parents, Animator);
ABC = get_attribute(str, "__call__")(create_array("azertyuiopQSDFGHJKLMwxcvbnAZERTYUIOPqsdfghjklmWXCVBN "), {});
ProgressiveText = {};
parents = create_array();
var ProgressiveText____init__ = function(args, kwargs) {
var signature = {"kwargs": {"callback": undefined, "delay": 3000}, "args": create_array("self", "selector", "text", "callback", "delay")};
var arguments = get_arguments(signature, args, kwargs);
var delay = arguments["delay"];
var callback = arguments["callback"];
var text = arguments["text"];
var selector = arguments["selector"];
var self = arguments["self"];
set_attribute(self, "delay", delay);
set_attribute(self, "text", text);
set_attribute(self, "length", get_attribute(len, "__call__")(create_array(text), {}));
var element;
element = get_attribute(J, "__call__")(create_array(selector), {});
get_attribute(get_attribute(element, "html"), "__call__")(create_array(""), {});
var __iterator__ = get_attribute(text, "__iter__")(create_array(), {});
try {
var i = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
get_attribute(get_attribute(element, "append"), "__call__")(create_array("<span>a</span>"), {});
var i = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

set_attribute(self, "elements", get_attribute(J, "__call__")(create_array(selector + " span"), {}));
}

ProgressiveText.__init__ = ProgressiveText____init__;
var ProgressiveText__start = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
set_attribute(self, "animation", get_attribute(Animator, "__call__")(create_array(get_attribute(self, "update"), get_attribute(self, "delay"), true), {}));
get_attribute(get_attribute(get_attribute(self, "animation"), "run"), "__call__")(create_array(), {});
}

ProgressiveText.start = ProgressiveText__start;
var ProgressiveText__update = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
var to_update;
to_update = false;
var __iterator__ = get_attribute(get_attribute(range, "__call__")(create_array(get_attribute(self, "length")), {}), "__iter__")(create_array(), {});
try {
var index = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
var element, char, expected;
element = get_attribute(get_attribute(get_attribute(self, "elements"), "get"), "__call__")(create_array(index), {});
char = get_attribute(get_attribute(element, "html"), "__call__")(create_array(), {});
expected = get_attribute(get_attribute(get_attribute(self, "text"), "get"), "__call__")(create_array(index), {});
if(char != expected) {
var novo;
novo = get_attribute(get_attribute(ABC, "get"), "__call__")(create_array(get_attribute(get_attribute(ABC, "index"), "__call__")(create_array(char), {}) + 1), {});
get_attribute(get_attribute(element, "html"), "__call__")(create_array(novo), {});
to_update = true;
}
else {

}

var index = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

if(!to_update) {
get_attribute(get_attribute(get_attribute(self, "animation"), "stop"), "__call__")(create_array(), {});
}
else {

}

}

ProgressiveText.update = ProgressiveText__update;
ProgressiveText = create_class("ProgressiveText", parents, ProgressiveText);
get_attribute(get_attribute(get_attribute(ProgressiveText, "__call__")(create_array("#héllo", get_attribute(str, "__call__")(create_array("Hello World"), {})), {}), "start"), "__call__")(create_array(), {});
