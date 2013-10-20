var J, __J_attrs, __J_parents;
window["__J_attrs"] = Object();
window["__J_parents"] = create_array();
window["__J_properties"] = Object();
var __J___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J___init__";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
self["__dict__"]["j"] = jQuery(arg);
}
window["__J___init__"] = __J___init__ 

__J___init__.pythonscript_function = true;
window["__J_attrs"]["__init__"] = __J___init__;
var __J_add = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J_add";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = self["__dict__"]["j"];
o = j.add(arg);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_add"] = __J_add 

__J_add.pythonscript_function = true;
window["__J_attrs"]["add"] = __J_add;
var __J_add_class = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "klass")};
signature["function_name"] = "__J_add_class";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var klass = arguments['klass'];
j = self["__dict__"]["j"];
o = j.addClass(klass);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_add_class"] = __J_add_class 

__J_add_class.pythonscript_function = true;
window["__J_attrs"]["add_class"] = __J_add_class;
var __J_after = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J_after";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = self["__dict__"]["j"];
o = j.after(arg);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_after"] = __J_after 

__J_after.pythonscript_function = true;
window["__J_attrs"]["after"] = __J_after;
var __J_animate = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "properties", "duration", "easing", "complete")};
signature["function_name"] = "__J_animate";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var properties = arguments['properties'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.animate(properties, duration, easing, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_animate"] = __J_animate 

__J_animate.pythonscript_function = true;
window["__J_attrs"]["animate"] = __J_animate;
var __J_append = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J_append";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = self["__dict__"]["j"];
o = j.append(arg);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_append"] = __J_append 

__J_append.pythonscript_function = true;
window["__J_attrs"]["append"] = __J_append;
var __J_append_to = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J_append_to";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = self["__dict__"]["j"];
o = j.appendTo(arg);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_append_to"] = __J_append_to 

__J_append_to.pythonscript_function = true;
window["__J_attrs"]["append_to"] = __J_append_to;
var __J_attr = function(args, kwargs) {
var j;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
signature["function_name"] = "__J_attr";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = self["__dict__"]["j"];
if(value == undefined) {
j.attr(key);
}
else {
j.attr(key, value);
}

}
window["__J_attr"] = __J_attr 

__J_attr.pythonscript_function = true;
window["__J_attrs"]["attr"] = __J_attr;
var __J_before = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "arg")};
signature["function_name"] = "__J_before";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = self["__dict__"]["j"];
o = j.before(arg);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_before"] = __J_before 

__J_before.pythonscript_function = true;
window["__J_attrs"]["before"] = __J_before;
var __J_bind = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "event_type", "event_data", "handler")};
signature["function_name"] = "__J_bind";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event_type = arguments['event_type'];
var event_data = arguments['event_data'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.bind(event_type, event_data, adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_bind"] = __J_bind 

__J_bind.pythonscript_function = true;
window["__J_attrs"]["bind"] = __J_bind;
var __J_blur = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_blur";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.blur(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_blur"] = __J_blur 

__J_blur.pythonscript_function = true;
window["__J_attrs"]["blur"] = __J_blur;
var __J_change = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_change";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.change(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_change"] = __J_change 

__J_change.pythonscript_function = true;
window["__J_attrs"]["change"] = __J_change;
var __J_children = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_children";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = self["__dict__"]["j"];
o = j.children(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_children"] = __J_children 

__J_children.pythonscript_function = true;
window["__J_attrs"]["children"] = __J_children;
var __J_click = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_click";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.click(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_click"] = __J_click 

__J_click.pythonscript_function = true;
window["__J_attrs"]["click"] = __J_click;
var __J_clone = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "with_data_and_events")};
signature["function_name"] = "__J_clone";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var with_data_and_events = arguments['with_data_and_events'];
j = self["__dict__"]["j"];
o = j.clone(with_data_and_events);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_clone"] = __J_clone 

__J_clone.pythonscript_function = true;
window["__J_attrs"]["clone"] = __J_clone;
var __J_contents = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "e")};
signature["function_name"] = "__J_contents";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var e = arguments['e'];
j = self["__dict__"]["j"];
o = j.contents();
return get_attribute(J, "__call__")([o], Object());
}
window["__J_contents"] = __J_contents 

__J_contents.pythonscript_function = true;
window["__J_attrs"]["contents"] = __J_contents;
var __J_css = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "name", "value")};
signature["function_name"] = "__J_css";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
var value = arguments['value'];
j = self["__dict__"]["j"];
o = j.css(name, value);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_css"] = __J_css 

__J_css.pythonscript_function = true;
window["__J_attrs"]["css"] = __J_css;
var __J_data = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "key", "value")};
signature["function_name"] = "__J_data";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = self["__dict__"]["j"];
o = j.data(key, value);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_data"] = __J_data 

__J_data.pythonscript_function = true;
window["__J_attrs"]["data"] = __J_data;
var __J_double_click = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_double_click";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.dbclick(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_double_click"] = __J_double_click 

__J_double_click.pythonscript_function = true;
window["__J_attrs"]["double_click"] = __J_double_click;
var __J_delay = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "time", "queue_name")};
signature["function_name"] = "__J_delay";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var time = arguments['time'];
var queue_name = arguments['queue_name'];
j = self["__dict__"]["j"];
o = j.delay(time, queue_name);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_delay"] = __J_delay 

__J_delay.pythonscript_function = true;
window["__J_attrs"]["delay"] = __J_delay;
var __J_dequeue = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "queue_name")};
signature["function_name"] = "__J_dequeue";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue_name = arguments['queue_name'];
j = self["__dict__"]["j"];
o = j.dequeue(queue_name);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_dequeue"] = __J_dequeue 

__J_dequeue.pythonscript_function = true;
window["__J_attrs"]["dequeue"] = __J_dequeue;
var __J_detach = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_detach";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = self["__dict__"]["j"];
o = j.detach(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_detach"] = __J_detach 

__J_detach.pythonscript_function = true;
window["__J_attrs"]["detach"] = __J_detach;
var __J_each = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_each";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
"Iterate over a jQuery object, executing a function for each matched element that takes index and element (js object) as argument";
j = self["__dict__"]["j"];
o = j.each(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_each"] = __J_each 

__J_each.pythonscript_function = true;
window["__J_attrs"]["each"] = __J_each;
var __J_end = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_end";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.end(handler);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_end"] = __J_end 

__J_end.pythonscript_function = true;
window["__J_attrs"]["end"] = __J_end;
var __J_eq = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__J_eq";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = self["__dict__"]["j"];
o = j.eq(index);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_eq"] = __J_eq 

__J_eq.pythonscript_function = true;
window["__J_attrs"]["eq"] = __J_eq;
var __J_error = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_error";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.error(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_error"] = __J_error 

__J_error.pythonscript_function = true;
window["__J_attrs"]["error"] = __J_error;
var __J_fade_in = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_fade_in";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.fadeIn(duration, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_fade_in"] = __J_fade_in 

__J_fade_in.pythonscript_function = true;
window["__J_attrs"]["fade_in"] = __J_fade_in;
var __J_fade_out = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_fade_out";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.fadeOut(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_fade_out"] = __J_fade_out 

__J_fade_out.pythonscript_function = true;
window["__J_attrs"]["fade_out"] = __J_fade_out;
var __J_fadeTo = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "opacity", "complete")};
signature["function_name"] = "__J_fadeTo";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var opacity = arguments['opacity'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.fade_to(duration, opacity, adapt_arguments(complete));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_fadeTo"] = __J_fadeTo 

__J_fadeTo.pythonscript_function = true;
window["__J_attrs"]["fadeTo"] = __J_fadeTo;
var __J_fade_toggle = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "easing", "complete")};
signature["function_name"] = "__J_fade_toggle";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.fade_toggle(duration, easing, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_fade_toggle"] = __J_fade_toggle 

__J_fade_toggle.pythonscript_function = true;
window["__J_attrs"]["fade_toggle"] = __J_fade_toggle;
var __J_filter = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_filter";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = self["__dict__"]["j"];
o = j.filter(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_filter"] = __J_filter 

__J_filter.pythonscript_function = true;
window["__J_attrs"]["filter"] = __J_filter;
var __J_finish = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "queue")};
signature["function_name"] = "__J_finish";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue = arguments['queue'];
j = self["__dict__"]["j"];
o = j.finish(queue);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_finish"] = __J_finish 

__J_finish.pythonscript_function = true;
window["__J_attrs"]["finish"] = __J_finish;
var __J_find = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_find";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
var j, o;
j = self["__dict__"]["j"];
o = j.find(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_find"] = __J_find 

__J_find.pythonscript_function = true;
window["__J_attrs"]["find"] = __J_find;
var __J_first = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__J_first";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = self["__dict__"]["j"];
o = j.first();
return get_attribute(J, "__call__")([o], Object());
}
window["__J_first"] = __J_first 

__J_first.pythonscript_function = true;
window["__J_attrs"]["first"] = __J_first;
var __J_focus = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_focus";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.focus(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_focus"] = __J_focus 

__J_focus.pythonscript_function = true;
window["__J_attrs"]["focus"] = __J_focus;
var __J_focus_in = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_focus_in";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.focusIn(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_focus_in"] = __J_focus_in 

__J_focus_in.pythonscript_function = true;
window["__J_attrs"]["focus_in"] = __J_focus_in;
var __J_focus_out = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_focus_out";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.focusOut(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_focus_out"] = __J_focus_out 

__J_focus_out.pythonscript_function = true;
window["__J_attrs"]["focus_out"] = __J_focus_out;
var __J_get = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "index")};
signature["function_name"] = "__J_get";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = self["__dict__"]["j"];
o = j.get(index);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_get"] = __J_get 

__J_get.pythonscript_function = true;
window["__J_attrs"]["get"] = __J_get;
var __J_has_class = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "name")};
signature["function_name"] = "__J_has_class";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = self["__dict__"]["j"];
o = j.has_class(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_has_class"] = __J_has_class 

__J_has_class.pythonscript_function = true;
window["__J_attrs"]["has_class"] = __J_has_class;
var __J_height = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__J_height";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = self["__dict__"]["j"];
o = j.height(value);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_height"] = __J_height 

__J_height.pythonscript_function = true;
window["__J_attrs"]["height"] = __J_height;
var __J_hide = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_hide";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.hide(duration, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_hide"] = __J_hide 

__J_hide.pythonscript_function = true;
window["__J_attrs"]["hide"] = __J_hide;
var __J_hover = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_hover";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.hover(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_hover"] = __J_hover 

__J_hover.pythonscript_function = true;
window["__J_attrs"]["hover"] = __J_hover;
var __J_html = function(args, kwargs) {
var j;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__J_html";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = self["__dict__"]["j"];
if(value != undefined) {
o = j.html(value);
}
else {
o = j.html();
}

return o;
}
window["__J_html"] = __J_html 

__J_html.pythonscript_function = true;
window["__J_attrs"]["html"] = __J_html;
var __J_index = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_index";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = self["__dict__"]["j"];
o = j.index(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_index"] = __J_index 

__J_index.pythonscript_function = true;
window["__J_attrs"]["index"] = __J_index;
var __J_inner_height = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__J_inner_height";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = self["__dict__"]["j"];
o = j.innerHeight();
return get_attribute(J, "__call__")([o], Object());
}
window["__J_inner_height"] = __J_inner_height 

__J_inner_height.pythonscript_function = true;
window["__J_attrs"]["inner_height"] = __J_inner_height;
var __J_inner_width = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__J_inner_width";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = self["__dict__"]["j"];
o = j.innerWidth();
return get_attribute(J, "__call__")([o], Object());
}
window["__J_inner_width"] = __J_inner_width 

__J_inner_width.pythonscript_function = true;
window["__J_attrs"]["inner_width"] = __J_inner_width;
var __J_insert_after = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "target")};
signature["function_name"] = "__J_insert_after";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = self["__dict__"]["j"];
o = j.insertAfter(target);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_insert_after"] = __J_insert_after 

__J_insert_after.pythonscript_function = true;
window["__J_attrs"]["insert_after"] = __J_insert_after;
var __J_insert_before = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "target")};
signature["function_name"] = "__J_insert_before";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = self["__dict__"]["j"];
o = j.insertBefore(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_insert_before"] = __J_insert_before 

__J_insert_before.pythonscript_function = true;
window["__J_attrs"]["insert_before"] = __J_insert_before;
var __J_is_ = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "name")};
signature["function_name"] = "__J_is_";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = self["__dict__"]["j"];
o = j.is(selector);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_is_"] = __J_is_ 

__J_is_.pythonscript_function = true;
window["__J_attrs"]["is_"] = __J_is_;
var __J_keydown = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_keydown";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.keydown(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_keydown"] = __J_keydown 

__J_keydown.pythonscript_function = true;
window["__J_attrs"]["keydown"] = __J_keydown;
var __J_keypress = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_keypress";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.keypress(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_keypress"] = __J_keypress 

__J_keypress.pythonscript_function = true;
window["__J_attrs"]["keypress"] = __J_keypress;
var __J_keyup = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_keyup";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.keyup(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_keyup"] = __J_keyup 

__J_keyup.pythonscript_function = true;
window["__J_attrs"]["keyup"] = __J_keyup;
var __J_last = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_last";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.last(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_last"] = __J_last 

__J_last.pythonscript_function = true;
window["__J_attrs"]["last"] = __J_last;
var __J_on = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "event", "handler")};
signature["function_name"] = "__J_on";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.on(event, adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_on"] = __J_on 

__J_on.pythonscript_function = true;
window["__J_attrs"]["on"] = __J_on;
var __J_load = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "url", "data", "complete")};
signature["function_name"] = "__J_load";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var url = arguments['url'];
var data = arguments['data'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.load(url, data, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_load"] = __J_load 

__J_load.pythonscript_function = true;
window["__J_attrs"]["load"] = __J_load;
var __J_select = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_select";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.select(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_select"] = __J_select 

__J_select.pythonscript_function = true;
window["__J_attrs"]["select"] = __J_select;
var __J_show = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_show";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.show(duration, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_show"] = __J_show 

__J_show.pythonscript_function = true;
window["__J_attrs"]["show"] = __J_show;
var __J_siblings = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "selector")};
signature["function_name"] = "__J_siblings";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = self["__dict__"]["j"];
o = j.select(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_siblings"] = __J_siblings 

__J_siblings.pythonscript_function = true;
window["__J_attrs"]["siblings"] = __J_siblings;
var __J_size = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__J_size";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = self["__dict__"]["j"];
o = j.size();
return get_attribute(J, "__call__")([o], Object());
}
window["__J_size"] = __J_size 

__J_size.pythonscript_function = true;
window["__J_attrs"]["size"] = __J_size;
var __J_slice = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "start", "end")};
signature["function_name"] = "__J_slice";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
j = self["__dict__"]["j"];
o = j.slice(start, end);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_slice"] = __J_slice 

__J_slice.pythonscript_function = true;
window["__J_attrs"]["slice"] = __J_slice;
var __J_slide_down = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_slide_down";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.slideDown(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_slide_down"] = __J_slide_down 

__J_slide_down.pythonscript_function = true;
window["__J_attrs"]["slide_down"] = __J_slide_down;
var __J_slide_toggle = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_slide_toggle";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.slideToggle(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_slide_toggle"] = __J_slide_toggle 

__J_slide_toggle.pythonscript_function = true;
window["__J_attrs"]["slide_toggle"] = __J_slide_toggle;
var __J_slide_up = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_slide_up";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.slideUp(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_slide_up"] = __J_slide_up 

__J_slide_up.pythonscript_function = true;
window["__J_attrs"]["slide_up"] = __J_slide_up;
var __J_stop = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "clear_queue", "jump_to_end")};
signature["function_name"] = "__J_stop";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = self["__dict__"]["j"];
o = j.stop(clear_queue, jump_to_end);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_stop"] = __J_stop 

__J_stop.pythonscript_function = true;
window["__J_attrs"]["stop"] = __J_stop;
var __J_submit = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "clear_queue", "jump_to_end")};
signature["function_name"] = "__J_submit";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = self["__dict__"]["j"];
o = j.submit(clear_queue, jump_to_end);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_submit"] = __J_submit 

__J_submit.pythonscript_function = true;
window["__J_attrs"]["submit"] = __J_submit;
var __J_text = function(args, kwargs) {
var j;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "text")};
signature["function_name"] = "__J_text";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var text = arguments['text'];
j = self["__dict__"]["j"];
if(text != undefined) {
o = get_attribute(J, "__call__")([j.text(text)], Object());
}
else {
o = j.text();
}

return o;
}
window["__J_text"] = __J_text 

__J_text.pythonscript_function = true;
window["__J_attrs"]["text"] = __J_text;
var __J_toggle = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "duration", "complete")};
signature["function_name"] = "__J_toggle";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = self["__dict__"]["j"];
o = j.toggle(duration, complete);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_toggle"] = __J_toggle 

__J_toggle.pythonscript_function = true;
window["__J_attrs"]["toggle"] = __J_toggle;
var __J_toggle_class = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "class_name")};
signature["function_name"] = "__J_toggle_class";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var class_name = arguments['class_name'];
j = self["__dict__"]["j"];
o = j.toggleClass(class_name);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_toggle_class"] = __J_toggle_class 

__J_toggle_class.pythonscript_function = true;
window["__J_attrs"]["toggle_class"] = __J_toggle_class;
var __J_trigger = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "event")};
signature["function_name"] = "__J_trigger";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
j = self["__dict__"]["j"];
o = j.trigger(event);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_trigger"] = __J_trigger 

__J_trigger.pythonscript_function = true;
window["__J_attrs"]["trigger"] = __J_trigger;
var __J_unbind = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "event", "handler")};
signature["function_name"] = "__J_unbind";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.unbind(event, adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_unbind"] = __J_unbind 

__J_unbind.pythonscript_function = true;
window["__J_attrs"]["unbind"] = __J_unbind;
var __J_value = function(args, kwargs) {
var j;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__J_value";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = self["__dict__"]["j"];
if(value === undefined) {
o = j.val();
}
else {
o = j.val(value);
}

return o;
}
window["__J_value"] = __J_value 

__J_value.pythonscript_function = true;
window["__J_attrs"]["value"] = __J_value;
var __J_width = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "value")};
signature["function_name"] = "__J_width";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = self["__dict__"]["j"];
o = j.width(value);
return get_attribute(J, "__call__")([o], Object());
}
window["__J_width"] = __J_width 

__J_width.pythonscript_function = true;
window["__J_attrs"]["width"] = __J_width;
var __J_length = function(args, kwargs) {
var j;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self")};
signature["function_name"] = "__J_length";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = self["__dict__"]["j"];
return j.length();
}
window["__J_length"] = __J_length 

__J_length.pythonscript_function = true;
window["__J_attrs"]["length"] = __J_length;
var __J_map = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "func")};
signature["function_name"] = "__J_map";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var func = arguments['func'];
j = self["__dict__"]["j"];
o = j.map(adapt_arguments(func));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_map"] = __J_map 

__J_map.pythonscript_function = true;
window["__J_attrs"]["map"] = __J_map;
var __J_mousedown = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mousedown";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mousedown(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mousedown"] = __J_mousedown 

__J_mousedown.pythonscript_function = true;
window["__J_attrs"]["mousedown"] = __J_mousedown;
var __J_mouseenter = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mouseenter";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mouseenter(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mouseenter"] = __J_mouseenter 

__J_mouseenter.pythonscript_function = true;
window["__J_attrs"]["mouseenter"] = __J_mouseenter;
var __J_mouseleave = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mouseleave";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mouseleave(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mouseleave"] = __J_mouseleave 

__J_mouseleave.pythonscript_function = true;
window["__J_attrs"]["mouseleave"] = __J_mouseleave;
var __J_mousemove = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mousemove";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mousemove(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mousemove"] = __J_mousemove 

__J_mousemove.pythonscript_function = true;
window["__J_attrs"]["mousemove"] = __J_mousemove;
var __J_mouseout = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mouseout";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mouseout(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mouseout"] = __J_mouseout 

__J_mouseout.pythonscript_function = true;
window["__J_attrs"]["mouseout"] = __J_mouseout;
var __J_mouseover = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mouseover";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mouseover(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mouseover"] = __J_mouseover 

__J_mouseover.pythonscript_function = true;
window["__J_attrs"]["mouseover"] = __J_mouseover;
var __J_mouseup = function(args, kwargs) {
var j, o;
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("self", "handler")};
signature["function_name"] = "__J_mouseup";
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = self["__dict__"]["j"];
o = j.mouseup(adapt_arguments(handler));
return get_attribute(J, "__call__")([o], Object());
}
window["__J_mouseup"] = __J_mouseup 

__J_mouseup.pythonscript_function = true;
window["__J_attrs"]["mouseup"] = __J_mouseup;
J = create_class("J", window["__J_parents"], window["__J_attrs"], window["__J_properties"]);
var ajax = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": Object(), "args": create_array("url", "settings")};
signature["function_name"] = "ajax";
arguments = get_arguments(signature, args, kwargs);
var url = arguments['url'];
var settings = arguments['settings'];
return jQuery.ajax(url, settings);
}
window["ajax"] = ajax 

ajax.pythonscript_function = true;
