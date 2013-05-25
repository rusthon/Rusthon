var J, __J_attrs, __J_parents;
__J_attrs = {};
__J_parents = create_array();
var __J___init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
set_attribute(self, "j", jQuery(arg));
}

__J_attrs.__init__ = __J___init__;
var __J_add = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, "j");
o = j.add(arg);
var __args_0, __kwargs_0;
__args_0 = create_array(o);
__kwargs_0 = {};
return get_attribute(J, "__call__")(__args_0, __kwargs_0);
}

__J_attrs.add = __J_add;
var __J_addClass = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "klass")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var klass = arguments['klass'];
j = get_attribute(self, "j");
o = j.addClass(klass);
var __args_1, __kwargs_1;
__args_1 = create_array(o);
__kwargs_1 = {};
return get_attribute(J, "__call__")(__args_1, __kwargs_1);
}

__J_attrs.addClass = __J_addClass;
var __J_after = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, "j");
o = j.after(arg);
var __args_2, __kwargs_2;
__args_2 = create_array(o);
__kwargs_2 = {};
return get_attribute(J, "__call__")(__args_2, __kwargs_2);
}

__J_attrs.after = __J_after;
var __J_animate = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "properties", "duration", "easing", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var properties = arguments['properties'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.animate(properties, duration, easing, complete);
var __args_3, __kwargs_3;
__args_3 = create_array(o);
__kwargs_3 = {};
return get_attribute(J, "__call__")(__args_3, __kwargs_3);
}

__J_attrs.animate = __J_animate;
var __J_append = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, "j");
o = j.append(arg);
var __args_4, __kwargs_4;
__args_4 = create_array(o);
__kwargs_4 = {};
return get_attribute(J, "__call__")(__args_4, __kwargs_4);
}

__J_attrs.append = __J_append;
var __J_appendTo = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, "j");
o = j.appendTo(arg);
var __args_5, __kwargs_5;
__args_5 = create_array(o);
__kwargs_5 = {};
return get_attribute(J, "__call__")(__args_5, __kwargs_5);
}

__J_attrs.appendTo = __J_appendTo;
var __J_attr = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = get_attribute(self, "j");
if(value == undefined) {
j.attr(key);
}
else {
j.attr(key, value);
}

}

__J_attrs.attr = __J_attr;
var __J_before = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, "j");
o = j.before(arg);
var __args_6, __kwargs_6;
__args_6 = create_array(o);
__kwargs_6 = {};
return get_attribute(J, "__call__")(__args_6, __kwargs_6);
}

__J_attrs.before = __J_before;
var __J_bind = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event_type", "event_data", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event_type = arguments['event_type'];
var event_data = arguments['event_data'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.bind(event_type, event_data, adapt_arguments(handler));
var __args_7, __kwargs_7;
__args_7 = create_array(o);
__kwargs_7 = {};
return get_attribute(J, "__call__")(__args_7, __kwargs_7);
}

__J_attrs.bind = __J_bind;
var __J_blur = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.blur(adapt_arguments(handler));
var __args_8, __kwargs_8;
__args_8 = create_array(o);
__kwargs_8 = {};
return get_attribute(J, "__call__")(__args_8, __kwargs_8);
}

__J_attrs.blur = __J_blur;
var __J_change = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.change(adapt_arguments(handler));
var __args_9, __kwargs_9;
__args_9 = create_array(o);
__kwargs_9 = {};
return get_attribute(J, "__call__")(__args_9, __kwargs_9);
}

__J_attrs.change = __J_change;
var __J_children = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, "j");
o = j.children(selector);
var __args_10, __kwargs_10;
__args_10 = create_array(o);
__kwargs_10 = {};
return get_attribute(J, "__call__")(__args_10, __kwargs_10);
}

__J_attrs.children = __J_children;
var __J_click = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.click(adapt_arguments(handler));
var __args_11, __kwargs_11;
__args_11 = create_array(o);
__kwargs_11 = {};
return get_attribute(J, "__call__")(__args_11, __kwargs_11);
}

__J_attrs.click = __J_click;
var __J_clone = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "with_data_and_events")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var with_data_and_events = arguments['with_data_and_events'];
j = get_attribute(self, "j");
o = j.clone(with_data_and_events);
var __args_12, __kwargs_12;
__args_12 = create_array(o);
__kwargs_12 = {};
return get_attribute(J, "__call__")(__args_12, __kwargs_12);
}

__J_attrs.clone = __J_clone;
var __J_contents = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "e")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var e = arguments['e'];
j = get_attribute(self, "j");
o = j.contents();
var __args_13, __kwargs_13;
__args_13 = create_array(o);
__kwargs_13 = {};
return get_attribute(J, "__call__")(__args_13, __kwargs_13);
}

__J_attrs.contents = __J_contents;
var __J_css = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
var value = arguments['value'];
j = get_attribute(self, "j");
o = j.css(name, value);
var __args_14, __kwargs_14;
__args_14 = create_array(o);
__kwargs_14 = {};
return get_attribute(J, "__call__")(__args_14, __kwargs_14);
}

__J_attrs.css = __J_css;
var __J_data = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = get_attribute(self, "j");
o = j.data(key, value);
var __args_15, __kwargs_15;
__args_15 = create_array(o);
__kwargs_15 = {};
return get_attribute(J, "__call__")(__args_15, __kwargs_15);
}

__J_attrs.data = __J_data;
var __J_double_click = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.dbclick(adapt_arguments(handler));
var __args_16, __kwargs_16;
__args_16 = create_array(o);
__kwargs_16 = {};
return get_attribute(J, "__call__")(__args_16, __kwargs_16);
}

__J_attrs.double_click = __J_double_click;
var __J_delay = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "time", "queue_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var time = arguments['time'];
var queue_name = arguments['queue_name'];
j = get_attribute(self, "j");
o = j.delay(time, queue_name);
var __args_17, __kwargs_17;
__args_17 = create_array(o);
__kwargs_17 = {};
return get_attribute(J, "__call__")(__args_17, __kwargs_17);
}

__J_attrs.delay = __J_delay;
var __J_dequeue = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "queue_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue_name = arguments['queue_name'];
j = get_attribute(self, "j");
o = j.dequeue(queue_name);
var __args_18, __kwargs_18;
__args_18 = create_array(o);
__kwargs_18 = {};
return get_attribute(J, "__call__")(__args_18, __kwargs_18);
}

__J_attrs.dequeue = __J_dequeue;
var __J_detach = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, "j");
o = j.detach(selector);
var __args_19, __kwargs_19;
__args_19 = create_array(o);
__kwargs_19 = {};
return get_attribute(J, "__call__")(__args_19, __kwargs_19);
}

__J_attrs.detach = __J_detach;
var __J_each = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.each(adapt_arguments(handler));
var __args_20, __kwargs_20;
__args_20 = create_array(o);
__kwargs_20 = {};
return get_attribute(J, "__call__")(__args_20, __kwargs_20);
}

__J_attrs.each = __J_each;
var __J_end = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.end(handler);
var __args_21, __kwargs_21;
__args_21 = create_array(o);
__kwargs_21 = {};
return get_attribute(J, "__call__")(__args_21, __kwargs_21);
}

__J_attrs.end = __J_end;
var __J_eq = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = get_attribute(self, "j");
o = j.eq(index);
var __args_22, __kwargs_22;
__args_22 = create_array(o);
__kwargs_22 = {};
return get_attribute(J, "__call__")(__args_22, __kwargs_22);
}

__J_attrs.eq = __J_eq;
var __J_error = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.error(adapt_arguments(handler));
var __args_23, __kwargs_23;
__args_23 = create_array(o);
__kwargs_23 = {};
return get_attribute(J, "__call__")(__args_23, __kwargs_23);
}

__J_attrs.error = __J_error;
var __J_fade_in = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.fadeIn(duration, complete);
var __args_24, __kwargs_24;
__args_24 = create_array(o);
__kwargs_24 = {};
return get_attribute(J, "__call__")(__args_24, __kwargs_24);
}

__J_attrs.fade_in = __J_fade_in;
var __J_fade_out = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.fadeOut(duration, adapt_arguments(complete));
var __args_25, __kwargs_25;
__args_25 = create_array(o);
__kwargs_25 = {};
return get_attribute(J, "__call__")(__args_25, __kwargs_25);
}

__J_attrs.fade_out = __J_fade_out;
var __J_fadeTo = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "opacity", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var opacity = arguments['opacity'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.fade_to(duration, opacity, adapt_arguments(complete));
var __args_26, __kwargs_26;
__args_26 = create_array(o);
__kwargs_26 = {};
return get_attribute(J, "__call__")(__args_26, __kwargs_26);
}

__J_attrs.fadeTo = __J_fadeTo;
var __J_fade_toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "easing", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.fade_toggle(duration, easing, complete);
var __args_27, __kwargs_27;
__args_27 = create_array(o);
__kwargs_27 = {};
return get_attribute(J, "__call__")(__args_27, __kwargs_27);
}

__J_attrs.fade_toggle = __J_fade_toggle;
var __J_filter = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, "j");
o = j.filter(selector);
var __args_28, __kwargs_28;
__args_28 = create_array(o);
__kwargs_28 = {};
return get_attribute(J, "__call__")(__args_28, __kwargs_28);
}

__J_attrs.filter = __J_filter;
var __J_finish = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "queue")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue = arguments['queue'];
j = get_attribute(self, "j");
o = j.finish(queue);
var __args_29, __kwargs_29;
__args_29 = create_array(o);
__kwargs_29 = {};
return get_attribute(J, "__call__")(__args_29, __kwargs_29);
}

__J_attrs.finish = __J_finish;
var __J_find = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
var j, o;
j = get_attribute(self, "j");
o = j.find(selector);
var __args_30, __kwargs_30;
__args_30 = create_array(o);
__kwargs_30 = {};
return get_attribute(J, "__call__")(__args_30, __kwargs_30);
}

__J_attrs.find = __J_find;
var __J_first = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, "j");
o = j.first();
var __args_31, __kwargs_31;
__args_31 = create_array(o);
__kwargs_31 = {};
return get_attribute(J, "__call__")(__args_31, __kwargs_31);
}

__J_attrs.first = __J_first;
var __J_focus = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.focus(adapt_arguments(handler));
var __args_32, __kwargs_32;
__args_32 = create_array(o);
__kwargs_32 = {};
return get_attribute(J, "__call__")(__args_32, __kwargs_32);
}

__J_attrs.focus = __J_focus;
var __J_focus_in = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.focusIn(adapt_arguments(handler));
var __args_33, __kwargs_33;
__args_33 = create_array(o);
__kwargs_33 = {};
return get_attribute(J, "__call__")(__args_33, __kwargs_33);
}

__J_attrs.focus_in = __J_focus_in;
var __J_focus_out = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.focusOut(adapt_arguments(handler));
var __args_34, __kwargs_34;
__args_34 = create_array(o);
__kwargs_34 = {};
return get_attribute(J, "__call__")(__args_34, __kwargs_34);
}

__J_attrs.focus_out = __J_focus_out;
var __J_get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = get_attribute(self, "j");
o = j.get(index);
var __args_35, __kwargs_35;
__args_35 = create_array(o);
__kwargs_35 = {};
return get_attribute(J, "__call__")(__args_35, __kwargs_35);
}

__J_attrs.get = __J_get;
var __J_has_class = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = get_attribute(self, "j");
o = j.has_class(selector);
var __args_36, __kwargs_36;
__args_36 = create_array(o);
__kwargs_36 = {};
return get_attribute(J, "__call__")(__args_36, __kwargs_36);
}

__J_attrs.has_class = __J_has_class;
var __J_height = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, "j");
o = j.height(value);
var __args_37, __kwargs_37;
__args_37 = create_array(o);
__kwargs_37 = {};
return get_attribute(J, "__call__")(__args_37, __kwargs_37);
}

__J_attrs.height = __J_height;
var __J_hide = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.hide(duration, complete);
var __args_38, __kwargs_38;
__args_38 = create_array(o);
__kwargs_38 = {};
return get_attribute(J, "__call__")(__args_38, __kwargs_38);
}

__J_attrs.hide = __J_hide;
var __J_hover = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.hover(adapt_arguments(handler));
var __args_39, __kwargs_39;
__args_39 = create_array(o);
__kwargs_39 = {};
return get_attribute(J, "__call__")(__args_39, __kwargs_39);
}

__J_attrs.hover = __J_hover;
var __J_html = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, "j");
if(value != undefined) {
o = j.html(value);
}
else {
o = j.html();
}

return o;
}

__J_attrs.html = __J_html;
var __J_index = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, "j");
o = j.index(selector);
var __args_40, __kwargs_40;
__args_40 = create_array(o);
__kwargs_40 = {};
return get_attribute(J, "__call__")(__args_40, __kwargs_40);
}

__J_attrs.index = __J_index;
var __J_inner_height = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, "j");
o = j.innerHeight();
var __args_41, __kwargs_41;
__args_41 = create_array(o);
__kwargs_41 = {};
return get_attribute(J, "__call__")(__args_41, __kwargs_41);
}

__J_attrs.inner_height = __J_inner_height;
var __J_inner_width = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, "j");
o = j.innerWidth();
var __args_42, __kwargs_42;
__args_42 = create_array(o);
__kwargs_42 = {};
return get_attribute(J, "__call__")(__args_42, __kwargs_42);
}

__J_attrs.inner_width = __J_inner_width;
var __J_insert_after = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "target")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = get_attribute(self, "j");
o = j.insertAfter(target);
var __args_43, __kwargs_43;
__args_43 = create_array(o);
__kwargs_43 = {};
return get_attribute(J, "__call__")(__args_43, __kwargs_43);
}

__J_attrs.insert_after = __J_insert_after;
var __J_insert_before = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "target")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = get_attribute(self, "j");
o = j.insertBefore(selector);
var __args_44, __kwargs_44;
__args_44 = create_array(o);
__kwargs_44 = {};
return get_attribute(J, "__call__")(__args_44, __kwargs_44);
}

__J_attrs.insert_before = __J_insert_before;
var __J_is_ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = get_attribute(self, "j");
o = j.is(selector);
var __args_45, __kwargs_45;
__args_45 = create_array(o);
__kwargs_45 = {};
return get_attribute(J, "__call__")(__args_45, __kwargs_45);
}

__J_attrs.is_ = __J_is_;
var __J_keydown = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.keydown(adapt_arguments(handler));
var __args_46, __kwargs_46;
__args_46 = create_array(o);
__kwargs_46 = {};
return get_attribute(J, "__call__")(__args_46, __kwargs_46);
}

__J_attrs.keydown = __J_keydown;
var __J_keypress = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.keypress(adapt_arguments(handler));
var __args_47, __kwargs_47;
__args_47 = create_array(o);
__kwargs_47 = {};
return get_attribute(J, "__call__")(__args_47, __kwargs_47);
}

__J_attrs.keypress = __J_keypress;
var __J_keyup = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.keyup(adapt_arguments(handler));
var __args_48, __kwargs_48;
__args_48 = create_array(o);
__kwargs_48 = {};
return get_attribute(J, "__call__")(__args_48, __kwargs_48);
}

__J_attrs.keyup = __J_keyup;
var __J_last = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.last(adapt_arguments(handler));
var __args_49, __kwargs_49;
__args_49 = create_array(o);
__kwargs_49 = {};
return get_attribute(J, "__call__")(__args_49, __kwargs_49);
}

__J_attrs.last = __J_last;
var __J_on = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.on(event, adapt_arguments(handler));
var __args_50, __kwargs_50;
__args_50 = create_array(o);
__kwargs_50 = {};
return get_attribute(J, "__call__")(__args_50, __kwargs_50);
}

__J_attrs.on = __J_on;
var __J_load = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "url", "data", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var url = arguments['url'];
var data = arguments['data'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.load(url, data, complete);
var __args_51, __kwargs_51;
__args_51 = create_array(o);
__kwargs_51 = {};
return get_attribute(J, "__call__")(__args_51, __kwargs_51);
}

__J_attrs.load = __J_load;
var __J_select = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.select(adapt_arguments(handler));
var __args_52, __kwargs_52;
__args_52 = create_array(o);
__kwargs_52 = {};
return get_attribute(J, "__call__")(__args_52, __kwargs_52);
}

__J_attrs.select = __J_select;
var __J_show = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.show(duration, complete);
var __args_53, __kwargs_53;
__args_53 = create_array(o);
__kwargs_53 = {};
return get_attribute(J, "__call__")(__args_53, __kwargs_53);
}

__J_attrs.show = __J_show;
var __J_siblings = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, "j");
o = j.select(adapt_arguments(handler));
var __args_54, __kwargs_54;
__args_54 = create_array(o);
__kwargs_54 = {};
return get_attribute(J, "__call__")(__args_54, __kwargs_54);
}

__J_attrs.siblings = __J_siblings;
var __J_size = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, "j");
o = j.size();
var __args_55, __kwargs_55;
__args_55 = create_array(o);
__kwargs_55 = {};
return get_attribute(J, "__call__")(__args_55, __kwargs_55);
}

__J_attrs.size = __J_size;
var __J_slice = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
j = get_attribute(self, "j");
o = j.slice(start, end);
var __args_56, __kwargs_56;
__args_56 = create_array(o);
__kwargs_56 = {};
return get_attribute(J, "__call__")(__args_56, __kwargs_56);
}

__J_attrs.slice = __J_slice;
var __J_slide_down = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.slideDown(duration, adapt_arguments(complete));
var __args_57, __kwargs_57;
__args_57 = create_array(o);
__kwargs_57 = {};
return get_attribute(J, "__call__")(__args_57, __kwargs_57);
}

__J_attrs.slide_down = __J_slide_down;
var __J_slide_toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.slideToggle(duration, adapt_arguments(complete));
var __args_58, __kwargs_58;
__args_58 = create_array(o);
__kwargs_58 = {};
return get_attribute(J, "__call__")(__args_58, __kwargs_58);
}

__J_attrs.slide_toggle = __J_slide_toggle;
var __J_slide_up = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.slideUp(duration, adapt_arguments(complete));
var __args_59, __kwargs_59;
__args_59 = create_array(o);
__kwargs_59 = {};
return get_attribute(J, "__call__")(__args_59, __kwargs_59);
}

__J_attrs.slide_up = __J_slide_up;
var __J_stop = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = get_attribute(self, "j");
o = j.stop(clear_queue, jump_to_end);
var __args_60, __kwargs_60;
__args_60 = create_array(o);
__kwargs_60 = {};
return get_attribute(J, "__call__")(__args_60, __kwargs_60);
}

__J_attrs.stop = __J_stop;
var __J_submit = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = get_attribute(self, "j");
o = j.submit(clear_queue, jump_to_end);
var __args_61, __kwargs_61;
__args_61 = create_array(o);
__kwargs_61 = {};
return get_attribute(J, "__call__")(__args_61, __kwargs_61);
}

__J_attrs.submit = __J_submit;
var __J_text = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "text")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var text = arguments['text'];
j = get_attribute(self, "j");
o = j.text(text);
var __args_62, __kwargs_62;
__args_62 = create_array(o);
__kwargs_62 = {};
return get_attribute(J, "__call__")(__args_62, __kwargs_62);
}

__J_attrs.text = __J_text;
var __J_toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, "j");
o = j.toggle(duration, complete);
var __args_63, __kwargs_63;
__args_63 = create_array(o);
__kwargs_63 = {};
return get_attribute(J, "__call__")(__args_63, __kwargs_63);
}

__J_attrs.toggle = __J_toggle;
var __J_toggle_class = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "class_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var class_name = arguments['class_name'];
j = get_attribute(self, "j");
o = j.toggleClass(class_name);
var __args_64, __kwargs_64;
__args_64 = create_array(o);
__kwargs_64 = {};
return get_attribute(J, "__call__")(__args_64, __kwargs_64);
}

__J_attrs.toggle_class = __J_toggle_class;
var __J_trigger = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
j = get_attribute(self, "j");
o = j.trigger(event);
var __args_65, __kwargs_65;
__args_65 = create_array(o);
__kwargs_65 = {};
return get_attribute(J, "__call__")(__args_65, __kwargs_65);
}

__J_attrs.trigger = __J_trigger;
var __J_unbind = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.unbind(event, adapt_arguments(handler));
var __args_66, __kwargs_66;
__args_66 = create_array(o);
__kwargs_66 = {};
return get_attribute(J, "__call__")(__args_66, __kwargs_66);
}

__J_attrs.unbind = __J_unbind;
var __J_value = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, "j");
o = j.val(value);
var __args_67, __kwargs_67;
__args_67 = create_array(o);
__kwargs_67 = {};
return get_attribute(J, "__call__")(__args_67, __kwargs_67);
}

__J_attrs.value = __J_value;
var __J_width = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, "j");
o = j.width(value);
var __args_68, __kwargs_68;
__args_68 = create_array(o);
__kwargs_68 = {};
return get_attribute(J, "__call__")(__args_68, __kwargs_68);
}

__J_attrs.width = __J_width;
var __J_length = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, "j");
return j.length();
}

__J_attrs.length = __J_length;
var __J_map = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "func")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var func = arguments['func'];
j = get_attribute(self, "j");
o = j.map(func);
var __args_69, __kwargs_69;
__args_69 = create_array(o);
__kwargs_69 = {};
return get_attribute(J, "__call__")(__args_69, __kwargs_69);
}

__J_attrs.map = __J_map;
var __J_mousedown = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mousedown(adapt_arguments(handler));
var __args_70, __kwargs_70;
__args_70 = create_array(o);
__kwargs_70 = {};
return get_attribute(J, "__call__")(__args_70, __kwargs_70);
}

__J_attrs.mousedown = __J_mousedown;
var __J_mouseenter = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mouseenter(adapt_arguments(handler));
var __args_71, __kwargs_71;
__args_71 = create_array(o);
__kwargs_71 = {};
return get_attribute(J, "__call__")(__args_71, __kwargs_71);
}

__J_attrs.mouseenter = __J_mouseenter;
var __J_mouseleave = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mouseleave(adapt_arguments(handler));
var __args_72, __kwargs_72;
__args_72 = create_array(o);
__kwargs_72 = {};
return get_attribute(J, "__call__")(__args_72, __kwargs_72);
}

__J_attrs.mouseleave = __J_mouseleave;
var __J_mousemove = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mousemove(adapt_arguments(handler));
var __args_73, __kwargs_73;
__args_73 = create_array(o);
__kwargs_73 = {};
return get_attribute(J, "__call__")(__args_73, __kwargs_73);
}

__J_attrs.mousemove = __J_mousemove;
var __J_mouseout = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mouseout(adapt_arguments(handler));
var __args_74, __kwargs_74;
__args_74 = create_array(o);
__kwargs_74 = {};
return get_attribute(J, "__call__")(__args_74, __kwargs_74);
}

__J_attrs.mouseout = __J_mouseout;
var __J_mouseover = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mouseover(adapt_arguments(handler));
var __args_75, __kwargs_75;
__args_75 = create_array(o);
__kwargs_75 = {};
return get_attribute(J, "__call__")(__args_75, __kwargs_75);
}

__J_attrs.mouseover = __J_mouseover;
var __J_mouseup = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, "j");
o = j.mouseup(adapt_arguments(handler));
var __args_76, __kwargs_76;
__args_76 = create_array(o);
__kwargs_76 = {};
return get_attribute(J, "__call__")(__args_76, __kwargs_76);
}

__J_attrs.mouseup = __J_mouseup;
J = create_class("J", __J_parents, __J_attrs);
var ajax = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("url", "settings")};
arguments = get_arguments(signature, args, kwargs);
var url = arguments['url'];
var settings = arguments['settings'];
return jQuery.ajax(url, settings);
}

