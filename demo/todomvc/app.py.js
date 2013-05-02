Messaging = {};
parents = create_array();
var Messaging____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
set_attribute(self, "omni", get_attribute(list, "__call__")(create_array(), {}));
set_attribute(self, "channels", get_attribute(dict, "__call__")(create_array(), {}));
}

Messaging.__init__ = Messaging____init__;
var Messaging__publish = function(args, kwargs) {
var signature = {"kwargs": {"param": undefined}, "args": create_array("self", "sender", "channel", "param")};
var arguments = get_arguments(signature, args, kwargs);
var param = arguments["param"];
var channel = arguments["channel"];
var sender = arguments["sender"];
var self = arguments["self"];
console.log("publish", sender, channel, param);
var __iterator__ = get_attribute(get_attribute(self, "omni"), "__iter__")(create_array(), {});
try {
var receiver = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
get_attribute(receiver, "__call__")(create_array(sender, channel, param), {});
var receiver = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

channel = get_attribute(get_attribute(get_attribute(self, "channels"), "get"), "__call__")(create_array(channel, undefined), {});
if(channel) {
channel = get_attribute(get_attribute(get_attribute(self, "channels"), "get"), "__call__")(create_array(channel), {});
var __iterator__ = get_attribute(channel, "__iter__")(create_array(), {});
try {
var receiver = get_attribute(__iterator__, "next")(create_array(), {});
while(true) {
get_attribute(receiver, "__call__")(create_array(sender, channel, param), {});
var receiver = get_attribute(__iterator__, "next")(create_array(), {});
}
}
catch(__exception__) {

}

}
else {

}

}

Messaging.publish = Messaging__publish;
var Messaging__subscribe = function(args, kwargs) {
var signature = {"kwargs": {"channel": undefined}, "args": create_array("self", "receiver", "channel")};
var arguments = get_arguments(signature, args, kwargs);
var channel = arguments["channel"];
var receiver = arguments["receiver"];
var self = arguments["self"];
console.log("subscribe", channel);
if(!channel) {
get_attribute(get_attribute(get_attribute(self, "omni"), "append"), "__call__")(create_array(receiver), {});
}
else {
receivers = get_attribute(get_attribute(get_attribute(self, "channels"), "get"), "__call__")(create_array(channel), {});
if(receivers) {
get_attribute(get_attribute(receivers, "append"), "__call__")(create_array(receiver), {});
}
else {
receivers = get_attribute(list, "__call__")(create_array(), {});
get_attribute(get_attribute(receivers, "append"), "__call__")(create_array(receiver), {});
get_attribute(get_attribute(get_attribute(self, "channels"), "set"), "__call__")(create_array(channel, receivers), {});
}

}

}

Messaging.subscribe = Messaging__subscribe;
Messaging = create_class("Messaging", parents, Messaging);
Node = {};
parents = create_array();
var Node____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "app")};
var arguments = get_arguments(signature, args, kwargs);
var app = arguments["app"];
var self = arguments["self"];
set_attribute(self, "app", app);
set_attribute(self, "transitions", get_attribute(dict, "__call__")(create_array(), {}));
}

Node.__init__ = Node____init__;
var Node__transition = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "message", "end")};
var arguments = get_arguments(signature, args, kwargs);
var end = arguments["end"];
var message = arguments["message"];
var self = arguments["self"];
get_attribute(get_attribute(get_attribute(self, "transitions"), "set"), "__call__")(create_array(message, end), {});
}

Node.transition = Node__transition;
var Node__on_leave = function(args, kwargs) {
var signature = {"kwargs": {"param": undefined}, "args": create_array("self", "next", "sender", "message", "param")};
var arguments = get_arguments(signature, args, kwargs);
var param = arguments["param"];
var message = arguments["message"];
var sender = arguments["sender"];
var next = arguments["next"];
var self = arguments["self"];
console.log("on_leave empty", next, sender, message, param);
}

Node.on_leave = Node__on_leave;
var Node__on_enter = function(args, kwargs) {
var signature = {"kwargs": {"param": undefined}, "args": create_array("self", "before", "sender", "message", "param")};
var arguments = get_arguments(signature, args, kwargs);
var param = arguments["param"];
var message = arguments["message"];
var sender = arguments["sender"];
var before = arguments["before"];
var self = arguments["self"];
console.log("on_enter empty", before, sender, message, param);
}

Node.on_enter = Node__on_enter;
Node = create_class("Node", parents, Node);
Machinima = {};
parents = create_array();
var Machinima____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "name")};
var arguments = get_arguments(signature, args, kwargs);
var name = arguments["name"];
var self = arguments["self"];
set_attribute(self, "name", name);
set_attribute(self, "node", undefined);
}

Machinima.__init__ = Machinima____init__;
var Machinima__handle = function(args, kwargs) {
var signature = {"kwargs": {"param": undefined}, "args": create_array("self", "sender", "message", "param")};
var arguments = get_arguments(signature, args, kwargs);
var param = arguments["param"];
var message = arguments["message"];
var sender = arguments["sender"];
var self = arguments["self"];
console.log("handle", sender, message, param);
end = get_attribute(get_attribute(get_attribute(get_attribute(self, "node"), "transitions"), "get"), "__call__")(create_array(message), {});
if(end) {
get_attribute(get_attribute(get_attribute(self, "node"), "on_leave"), "__call__")(create_array(next, sender, message, param), {});
get_attribute(get_attribute(end, "on_enter"), "__call__")(create_array(get_attribute(self, "node"), sender, message, param), {});
set_attribute(self, "node", end);
}
else {

}

}

Machinima.handle = Machinima__handle;
var Machinima__start = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
get_attribute(get_attribute(get_attribute(self, "node"), "on_enter"), "__call__")(create_array(undefined, undefined, undefined, undefined), {});
}

Machinima.start = Machinima__start;
Machinima = create_class("Machinima", parents, Machinima);
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
var Animator__start = function(args, kwargs) {
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

Animator.start = Animator__start;
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
Application = {};
parents = create_array();
var Application____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
set_attribute(self, "messaging", get_attribute(Messaging, "__call__")(create_array(), {}));
set_attribute(self, "machinima", get_attribute(Machinima, "__call__")(create_array("main"), {}));
get_attribute(get_attribute(get_attribute(self, "messaging"), "subscribe"), "__call__")(create_array(get_attribute(get_attribute(self, "machinima"), "handle")), {});
}

Application.__init__ = Application____init__;
Application = create_class("Application", parents, Application);
