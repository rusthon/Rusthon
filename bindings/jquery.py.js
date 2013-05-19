var J, __J_attrs, __J_parents;
__J_attrs = {};
__J_parents = create_array();
var __J____init__ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
set_attribute(self, j, jQuery(arg));
}

J.__init__ = __J____init__;
var __J__add = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, j);
o = j.add(arg);
var __args_0, __kwargs_0;
__args_0 = create_array(o);
__kwargs_0 = {};
return get_attribute(J, "__call__")(__args_0, __kwargs_0);
}

J.add = __J__add;
var __J__addClass = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "klass")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var klass = arguments['klass'];
j = get_attribute(self, j);
o = j.addClass(klass);
var __args_1, __kwargs_1;
__args_1 = create_array(o);
__kwargs_1 = {};
return get_attribute(J, "__call__")(__args_1, __kwargs_1);
}

J.addClass = __J__addClass;
var __J__after = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, j);
o = j.after(arg);
var __args_2, __kwargs_2;
__args_2 = create_array(o);
__kwargs_2 = {};
return get_attribute(J, "__call__")(__args_2, __kwargs_2);
}

J.after = __J__after;
var __J__animate = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "properties", "duration", "easing", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var properties = arguments['properties'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.animate(properties, duration, easing, complete);
var __args_3, __kwargs_3;
__args_3 = create_array(o);
__kwargs_3 = {};
return get_attribute(J, "__call__")(__args_3, __kwargs_3);
}

J.animate = __J__animate;
var __J__append = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, j);
o = j.append(arg);
var __args_4, __kwargs_4;
__args_4 = create_array(o);
__kwargs_4 = {};
return get_attribute(J, "__call__")(__args_4, __kwargs_4);
}

J.append = __J__append;
var __J__appendTo = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, j);
o = j.appendTo(arg);
var __args_5, __kwargs_5;
__args_5 = create_array(o);
__kwargs_5 = {};
return get_attribute(J, "__call__")(__args_5, __kwargs_5);
}

J.appendTo = __J__appendTo;
var __J__attr = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = get_attribute(self, j);
j.attr(key);
j.attr(key, value);
}

J.attr = __J__attr;
var __J__before = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "arg")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var arg = arguments['arg'];
j = get_attribute(self, j);
o = j.before(arg);
var __args_6, __kwargs_6;
__args_6 = create_array(o);
__kwargs_6 = {};
return get_attribute(J, "__call__")(__args_6, __kwargs_6);
}

J.before = __J__before;
var __J__bind = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event_type", "event_data", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event_type = arguments['event_type'];
var event_data = arguments['event_data'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.bind(event_type, event_data, adapt_arguments(handler));
var __args_7, __kwargs_7;
__args_7 = create_array(o);
__kwargs_7 = {};
return get_attribute(J, "__call__")(__args_7, __kwargs_7);
}

J.bind = __J__bind;
var __J__blur = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.blur(adapt_arguments(handler));
var __args_8, __kwargs_8;
__args_8 = create_array(o);
__kwargs_8 = {};
return get_attribute(J, "__call__")(__args_8, __kwargs_8);
}

J.blur = __J__blur;
var __J__change = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.change(adapt_arguments(handler));
var __args_9, __kwargs_9;
__args_9 = create_array(o);
__kwargs_9 = {};
return get_attribute(J, "__call__")(__args_9, __kwargs_9);
}

J.change = __J__change;
var __J__children = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, j);
o = j.children(selector);
var __args_10, __kwargs_10;
__args_10 = create_array(o);
__kwargs_10 = {};
return get_attribute(J, "__call__")(__args_10, __kwargs_10);
}

J.children = __J__children;
var __J__click = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.click(adapt_arguments(handler));
var __args_11, __kwargs_11;
__args_11 = create_array(o);
__kwargs_11 = {};
return get_attribute(J, "__call__")(__args_11, __kwargs_11);
}

J.click = __J__click;
var __J__clone = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "with_data_and_events")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var with_data_and_events = arguments['with_data_and_events'];
j = get_attribute(self, j);
o = j.clone(with_data_and_events);
var __args_12, __kwargs_12;
__args_12 = create_array(o);
__kwargs_12 = {};
return get_attribute(J, "__call__")(__args_12, __kwargs_12);
}

J.clone = __J__clone;
var __J__contents = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
o = j.contents();
var __args_13, __kwargs_13;
__args_13 = create_array(o);
__kwargs_13 = {};
return get_attribute(J, "__call__")(__args_13, __kwargs_13);
}

J.contents = __J__contents;
var __J__css = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.css(name, value);
var __args_14, __kwargs_14;
__args_14 = create_array(o);
__kwargs_14 = {};
return get_attribute(J, "__call__")(__args_14, __kwargs_14);
}

J.css = __J__css;
var __J__data = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var key = arguments['key'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.data(key, value);
var __args_15, __kwargs_15;
__args_15 = create_array(o);
__kwargs_15 = {};
return get_attribute(J, "__call__")(__args_15, __kwargs_15);
}

J.data = __J__data;
var __J__double_click = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.dbclick(adapt_arguments(handler));
var __args_16, __kwargs_16;
__args_16 = create_array(o);
__kwargs_16 = {};
return get_attribute(J, "__call__")(__args_16, __kwargs_16);
}

J.double_click = __J__double_click;
var __J__delay = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "time", "queue_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var time = arguments['time'];
var queue_name = arguments['queue_name'];
j = get_attribute(self, j);
o = j.delay(time, queue_name);
var __args_17, __kwargs_17;
__args_17 = create_array(o);
__kwargs_17 = {};
return get_attribute(J, "__call__")(__args_17, __kwargs_17);
}

J.delay = __J__delay;
var __J__dequeue = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "queue_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue_name = arguments['queue_name'];
j = get_attribute(self, j);
o = j.dequeue(queue_name);
var __args_18, __kwargs_18;
__args_18 = create_array(o);
__kwargs_18 = {};
return get_attribute(J, "__call__")(__args_18, __kwargs_18);
}

J.dequeue = __J__dequeue;
var __J__detach = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, j);
o = j.detach(selector);
var __args_19, __kwargs_19;
__args_19 = create_array(o);
__kwargs_19 = {};
return get_attribute(J, "__call__")(__args_19, __kwargs_19);
}

J.detach = __J__detach;
var __J__each = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.each(adapt_arguments(handler));
var __args_20, __kwargs_20;
__args_20 = create_array(o);
__kwargs_20 = {};
return get_attribute(J, "__call__")(__args_20, __kwargs_20);
}

J.each = __J__each;
var __J__end = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.end(handler);
var __args_21, __kwargs_21;
__args_21 = create_array(o);
__kwargs_21 = {};
return get_attribute(J, "__call__")(__args_21, __kwargs_21);
}

J.end = __J__end;
var __J__eq = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = get_attribute(self, j);
o = j.eq(index);
var __args_22, __kwargs_22;
__args_22 = create_array(o);
__kwargs_22 = {};
return get_attribute(J, "__call__")(__args_22, __kwargs_22);
}

J.eq = __J__eq;
var __J__error = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.error(adapt_arguments(handler));
var __args_23, __kwargs_23;
__args_23 = create_array(o);
__kwargs_23 = {};
return get_attribute(J, "__call__")(__args_23, __kwargs_23);
}

J.error = __J__error;
var __J__fade_in = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.fadeIn(duration, complete);
var __args_24, __kwargs_24;
__args_24 = create_array(o);
__kwargs_24 = {};
return get_attribute(J, "__call__")(__args_24, __kwargs_24);
}

J.fade_in = __J__fade_in;
var __J__fade_out = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.fadeOut(duration, adapt_arguments(complete));
var __args_25, __kwargs_25;
__args_25 = create_array(o);
__kwargs_25 = {};
return get_attribute(J, "__call__")(__args_25, __kwargs_25);
}

J.fade_out = __J__fade_out;
var __J__fadeTo = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "opacity", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var opacity = arguments['opacity'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.fade_to(duration, opacity, adapt_arguments(complete));
var __args_26, __kwargs_26;
__args_26 = create_array(o);
__kwargs_26 = {};
return get_attribute(J, "__call__")(__args_26, __kwargs_26);
}

J.fadeTo = __J__fadeTo;
var __J__fade_toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "easing", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var easing = arguments['easing'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.fade_toggle(duration, easing, complete);
var __args_27, __kwargs_27;
__args_27 = create_array(o);
__kwargs_27 = {};
return get_attribute(J, "__call__")(__args_27, __kwargs_27);
}

J.fade_toggle = __J__fade_toggle;
var __J__filter = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, j);
o = j.filter(selector);
var __args_28, __kwargs_28;
__args_28 = create_array(o);
__kwargs_28 = {};
return get_attribute(J, "__call__")(__args_28, __kwargs_28);
}

J.filter = __J__filter;
var __J__finish = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "queue")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var queue = arguments['queue'];
j = get_attribute(self, j);
o = j.finish(queue);
var __args_29, __kwargs_29;
__args_29 = create_array(o);
__kwargs_29 = {};
return get_attribute(J, "__call__")(__args_29, __kwargs_29);
}

J.finish = __J__finish;
var __J__first = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
o = j.first();
var __args_30, __kwargs_30;
__args_30 = create_array(o);
__kwargs_30 = {};
return get_attribute(J, "__call__")(__args_30, __kwargs_30);
}

J.first = __J__first;
var __J__focus = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.focus(adapt_arguments(handler));
var __args_31, __kwargs_31;
__args_31 = create_array(o);
__kwargs_31 = {};
return get_attribute(J, "__call__")(__args_31, __kwargs_31);
}

J.focus = __J__focus;
var __J__focus_in = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.focusIn(adapt_arguments(handler));
var __args_32, __kwargs_32;
__args_32 = create_array(o);
__kwargs_32 = {};
return get_attribute(J, "__call__")(__args_32, __kwargs_32);
}

J.focus_in = __J__focus_in;
var __J__focus_out = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.focusOut(adapt_arguments(handler));
var __args_33, __kwargs_33;
__args_33 = create_array(o);
__kwargs_33 = {};
return get_attribute(J, "__call__")(__args_33, __kwargs_33);
}

J.focus_out = __J__focus_out;
var __J__get = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "index")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var index = arguments['index'];
j = get_attribute(self, j);
o = j.get(index);
var __args_34, __kwargs_34;
__args_34 = create_array(o);
__kwargs_34 = {};
return get_attribute(J, "__call__")(__args_34, __kwargs_34);
}

J.get = __J__get;
var __J__has_class = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = get_attribute(self, j);
o = j.has_class(selector);
var __args_35, __kwargs_35;
__args_35 = create_array(o);
__kwargs_35 = {};
return get_attribute(J, "__call__")(__args_35, __kwargs_35);
}

J.has_class = __J__has_class;
var __J__height = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.height(value);
var __args_36, __kwargs_36;
__args_36 = create_array(o);
__kwargs_36 = {};
return get_attribute(J, "__call__")(__args_36, __kwargs_36);
}

J.height = __J__height;
var __J__hide = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.hide(duration, complete);
var __args_37, __kwargs_37;
__args_37 = create_array(o);
__kwargs_37 = {};
return get_attribute(J, "__call__")(__args_37, __kwargs_37);
}

J.hide = __J__hide;
var __J__hover = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.hover(adapt_arguments(handler));
var __args_38, __kwargs_38;
__args_38 = create_array(o);
__kwargs_38 = {};
return get_attribute(J, "__call__")(__args_38, __kwargs_38);
}

J.hover = __J__hover;
var __J__html = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.html(value);
o = j.html();
return o;
}

J.html = __J__html;
var __J__index = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, j);
o = j.index(selector);
var __args_39, __kwargs_39;
__args_39 = create_array(o);
__kwargs_39 = {};
return get_attribute(J, "__call__")(__args_39, __kwargs_39);
}

J.index = __J__index;
var __J__inner_height = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
o = j.innerHeight();
var __args_40, __kwargs_40;
__args_40 = create_array(o);
__kwargs_40 = {};
return get_attribute(J, "__call__")(__args_40, __kwargs_40);
}

J.inner_height = __J__inner_height;
var __J__inner_width = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
o = j.innerWidth();
var __args_41, __kwargs_41;
__args_41 = create_array(o);
__kwargs_41 = {};
return get_attribute(J, "__call__")(__args_41, __kwargs_41);
}

J.inner_width = __J__inner_width;
var __J__insert_after = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "target")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = get_attribute(self, j);
o = j.insertAfter(target);
var __args_42, __kwargs_42;
__args_42 = create_array(o);
__kwargs_42 = {};
return get_attribute(J, "__call__")(__args_42, __kwargs_42);
}

J.insert_after = __J__insert_after;
var __J__insert_before = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "target")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var target = arguments['target'];
j = get_attribute(self, j);
o = j.insertBefore(selector);
var __args_43, __kwargs_43;
__args_43 = create_array(o);
__kwargs_43 = {};
return get_attribute(J, "__call__")(__args_43, __kwargs_43);
}

J.insert_before = __J__insert_before;
var __J__is_ = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var name = arguments['name'];
j = get_attribute(self, j);
o = j.is(selector);
var __args_44, __kwargs_44;
__args_44 = create_array(o);
__kwargs_44 = {};
return get_attribute(J, "__call__")(__args_44, __kwargs_44);
}

J.is_ = __J__is_;
var __J__keydown = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.keydown(adapt_arguments(handler));
var __args_45, __kwargs_45;
__args_45 = create_array(o);
__kwargs_45 = {};
return get_attribute(J, "__call__")(__args_45, __kwargs_45);
}

J.keydown = __J__keydown;
var __J__keypress = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.keypress(adapt_arguments(handler));
var __args_46, __kwargs_46;
__args_46 = create_array(o);
__kwargs_46 = {};
return get_attribute(J, "__call__")(__args_46, __kwargs_46);
}

J.keypress = __J__keypress;
var __J__keyup = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.keyup(adapt_arguments(handler));
var __args_47, __kwargs_47;
__args_47 = create_array(o);
__kwargs_47 = {};
return get_attribute(J, "__call__")(__args_47, __kwargs_47);
}

J.keyup = __J__keyup;
var __J__last = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.last(adapt_arguments(handler));
var __args_48, __kwargs_48;
__args_48 = create_array(o);
__kwargs_48 = {};
return get_attribute(J, "__call__")(__args_48, __kwargs_48);
}

J.last = __J__last;
var __J__on = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.on(event, adapt_arguments(handler));
var __args_49, __kwargs_49;
__args_49 = create_array(o);
__kwargs_49 = {};
return get_attribute(J, "__call__")(__args_49, __kwargs_49);
}

J.on = __J__on;
var __J__load = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "url", "data", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var url = arguments['url'];
var data = arguments['data'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.load(url, data, complete);
var __args_50, __kwargs_50;
__args_50 = create_array(o);
__kwargs_50 = {};
return get_attribute(J, "__call__")(__args_50, __kwargs_50);
}

J.load = __J__load;
var __J__select = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.select(adapt_arguments(handler));
var __args_51, __kwargs_51;
__args_51 = create_array(o);
__kwargs_51 = {};
return get_attribute(J, "__call__")(__args_51, __kwargs_51);
}

J.select = __J__select;
var __J__show = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.show(duration, complete);
var __args_52, __kwargs_52;
__args_52 = create_array(o);
__kwargs_52 = {};
return get_attribute(J, "__call__")(__args_52, __kwargs_52);
}

J.show = __J__show;
var __J__siblings = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "selector")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var selector = arguments['selector'];
j = get_attribute(self, j);
o = j.select(adapt_arguments(handler));
var __args_53, __kwargs_53;
__args_53 = create_array(o);
__kwargs_53 = {};
return get_attribute(J, "__call__")(__args_53, __kwargs_53);
}

J.siblings = __J__siblings;
var __J__size = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
o = j.size();
var __args_54, __kwargs_54;
__args_54 = create_array(o);
__kwargs_54 = {};
return get_attribute(J, "__call__")(__args_54, __kwargs_54);
}

J.size = __J__size;
var __J__slice = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var start = arguments['start'];
var end = arguments['end'];
j = get_attribute(self, j);
o = j.slice(start, end);
var __args_55, __kwargs_55;
__args_55 = create_array(o);
__kwargs_55 = {};
return get_attribute(J, "__call__")(__args_55, __kwargs_55);
}

J.slice = __J__slice;
var __J__slide_down = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.slideDown(duration, adapt_arguments(complete));
var __args_56, __kwargs_56;
__args_56 = create_array(o);
__kwargs_56 = {};
return get_attribute(J, "__call__")(__args_56, __kwargs_56);
}

J.slide_down = __J__slide_down;
var __J__slide_toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.slideToggle(duration, adapt_arguments(complete));
var __args_57, __kwargs_57;
__args_57 = create_array(o);
__kwargs_57 = {};
return get_attribute(J, "__call__")(__args_57, __kwargs_57);
}

J.slide_toggle = __J__slide_toggle;
var __J__slide_up = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.slideUp(duration, adapt_arguments(complete));
var __args_58, __kwargs_58;
__args_58 = create_array(o);
__kwargs_58 = {};
return get_attribute(J, "__call__")(__args_58, __kwargs_58);
}

J.slide_up = __J__slide_up;
var __J__stop = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = get_attribute(self, j);
o = j.stop(clear_queue, jump_to_end);
var __args_59, __kwargs_59;
__args_59 = create_array(o);
__kwargs_59 = {};
return get_attribute(J, "__call__")(__args_59, __kwargs_59);
}

J.stop = __J__stop;
var __J__submit = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var clear_queue = arguments['clear_queue'];
var jump_to_end = arguments['jump_to_end'];
j = get_attribute(self, j);
o = j.submit(clear_queue, jump_to_end);
var __args_60, __kwargs_60;
__args_60 = create_array(o);
__kwargs_60 = {};
return get_attribute(J, "__call__")(__args_60, __kwargs_60);
}

J.submit = __J__submit;
var __J__text = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "text")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var text = arguments['text'];
j = get_attribute(self, j);
o = j.text(text);
var __args_61, __kwargs_61;
__args_61 = create_array(o);
__kwargs_61 = {};
return get_attribute(J, "__call__")(__args_61, __kwargs_61);
}

J.text = __J__text;
var __J__toggle = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var duration = arguments['duration'];
var complete = arguments['complete'];
j = get_attribute(self, j);
o = j.toggle(duration, complete);
var __args_62, __kwargs_62;
__args_62 = create_array(o);
__kwargs_62 = {};
return get_attribute(J, "__call__")(__args_62, __kwargs_62);
}

J.toggle = __J__toggle;
var __J__toggle_class = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "class_name")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var class_name = arguments['class_name'];
j = get_attribute(self, j);
o = j.toggleClass(class_name);
var __args_63, __kwargs_63;
__args_63 = create_array(o);
__kwargs_63 = {};
return get_attribute(J, "__call__")(__args_63, __kwargs_63);
}

J.toggle_class = __J__toggle_class;
var __J__trigger = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
j = get_attribute(self, j);
o = j.trigger(event);
var __args_64, __kwargs_64;
__args_64 = create_array(o);
__kwargs_64 = {};
return get_attribute(J, "__call__")(__args_64, __kwargs_64);
}

J.trigger = __J__trigger;
var __J__unbind = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var event = arguments['event'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.unbind(event, adapt_arguments(handler));
var __args_65, __kwargs_65;
__args_65 = create_array(o);
__kwargs_65 = {};
return get_attribute(J, "__call__")(__args_65, __kwargs_65);
}

J.unbind = __J__unbind;
var __J__value = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.val(value);
var __args_66, __kwargs_66;
__args_66 = create_array(o);
__kwargs_66 = {};
return get_attribute(J, "__call__")(__args_66, __kwargs_66);
}

J.value = __J__value;
var __J__width = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "value")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var value = arguments['value'];
j = get_attribute(self, j);
o = j.width(value);
var __args_67, __kwargs_67;
__args_67 = create_array(o);
__kwargs_67 = {};
return get_attribute(J, "__call__")(__args_67, __kwargs_67);
}

J.width = __J__width;
var __J__length = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
j = get_attribute(self, j);
return j.length();
}

J.length = __J__length;
var __J__map = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "func")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var func = arguments['func'];
j = get_attribute(self, j);
o = j.map(func);
var __args_68, __kwargs_68;
__args_68 = create_array(o);
__kwargs_68 = {};
return get_attribute(J, "__call__")(__args_68, __kwargs_68);
}

J.map = __J__map;
var __J__mousedown = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mousedown(adapt_arguments(handler));
var __args_69, __kwargs_69;
__args_69 = create_array(o);
__kwargs_69 = {};
return get_attribute(J, "__call__")(__args_69, __kwargs_69);
}

J.mousedown = __J__mousedown;
var __J__mouseenter = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mouseenter(adapt_arguments(handler));
var __args_70, __kwargs_70;
__args_70 = create_array(o);
__kwargs_70 = {};
return get_attribute(J, "__call__")(__args_70, __kwargs_70);
}

J.mouseenter = __J__mouseenter;
var __J__mouseleave = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mouseleave(adapt_arguments(handler));
var __args_71, __kwargs_71;
__args_71 = create_array(o);
__kwargs_71 = {};
return get_attribute(J, "__call__")(__args_71, __kwargs_71);
}

J.mouseleave = __J__mouseleave;
var __J__mousemove = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mousemove(adapt_arguments(handler));
var __args_72, __kwargs_72;
__args_72 = create_array(o);
__kwargs_72 = {};
return get_attribute(J, "__call__")(__args_72, __kwargs_72);
}

J.mousemove = __J__mousemove;
var __J__mouseout = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mouseout(adapt_arguments(handler));
var __args_73, __kwargs_73;
__args_73 = create_array(o);
__kwargs_73 = {};
return get_attribute(J, "__call__")(__args_73, __kwargs_73);
}

J.mouseout = __J__mouseout;
var __J__mouseover = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mouseover(adapt_arguments(handler));
var __args_74, __kwargs_74;
__args_74 = create_array(o);
__kwargs_74 = {};
return get_attribute(J, "__call__")(__args_74, __kwargs_74);
}

J.mouseover = __J__mouseover;
var __J__mouseup = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("self", "handler")};
arguments = get_arguments(signature, args, kwargs);
var self = arguments['self'];
var handler = arguments['handler'];
j = get_attribute(self, j);
o = j.mouseup(adapt_arguments(handler));
var __args_75, __kwargs_75;
__args_75 = create_array(o);
__kwargs_75 = {};
return get_attribute(J, "__call__")(__args_75, __kwargs_75);
}

J.mouseup = __J__mouseup;
J = create_class("J", __J_parents, __J__attrs);
var ajax = function(args, kwargs) {
var signature, arguments;
signature = {"kwargs": {}, "args": create_array("url", "settings")};
arguments = get_arguments(signature, args, kwargs);
var url = arguments['url'];
var settings = arguments['settings'];
return jQuery.ajax(url, settings);
}

