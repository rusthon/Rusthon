J = {};
parents = create_array();
var J____init__ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
set_attribute(self, "j", jQuery(arg));
}

J.__init__ = J____init__;
var J__add = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.add(arg);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.add = J__add;
var J__addClass = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "klass")};
var arguments = get_arguments(signature, args, kwargs);
var klass = arguments["klass"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.addClass(klass);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.addClass = J__addClass;
var J__after = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.after(arg);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.after = J__after;
var J__animate = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "properties", "duration", "easing", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var easing = arguments["easing"];
var duration = arguments["duration"];
var properties = arguments["properties"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.animate(properties, duration, easing, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.animate = J__animate;
var J__append = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.append(arg);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.append = J__append;
var J__appendTo = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.appendTo(arg);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.appendTo = J__appendTo;
var J__attr = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var key = arguments["key"];
var self = arguments["self"];
j = get_attribute(self, "j");
if(value == undefined) {
j.attr(key);
}
else {
j.attr(key, value);
}

}

J.attr = J__attr;
var J__before = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "arg")};
var arguments = get_arguments(signature, args, kwargs);
var arg = arguments["arg"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.before(arg);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.before = J__before;
var J__bind = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "event_type", "event_data", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var event_data = arguments["event_data"];
var event_type = arguments["event_type"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.bind(event_type, event_data, adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.bind = J__bind;
var J__blur = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.blur(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.blur = J__blur;
var J__change = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.change(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.change = J__change;
var J__children = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "selector")};
var arguments = get_arguments(signature, args, kwargs);
var selector = arguments["selector"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.children(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.children = J__children;
var J__click = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.click(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.click = J__click;
var J__clone = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "with_data_and_events")};
var arguments = get_arguments(signature, args, kwargs);
var with_data_and_events = arguments["with_data_and_events"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.clone(with_data_and_events);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.clone = J__clone;
var J__contents = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.contents();
return get_attribute(J, "__call__")(create_array(o), {});
}

J.contents = J__contents;
var J__css = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "name", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var name = arguments["name"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.css(name, value);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.css = J__css;
var J__data = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "key", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var key = arguments["key"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.data(key, value);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.data = J__data;
var J__double_click = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.dbclick(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.double_click = J__double_click;
var J__delay = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "time", "queue_name")};
var arguments = get_arguments(signature, args, kwargs);
var queue_name = arguments["queue_name"];
var time = arguments["time"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.delay(time, queue_name);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.delay = J__delay;
var J__dequeue = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "queue_name")};
var arguments = get_arguments(signature, args, kwargs);
var queue_name = arguments["queue_name"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.dequeue(queue_name);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.dequeue = J__dequeue;
var J__detach = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "selector")};
var arguments = get_arguments(signature, args, kwargs);
var selector = arguments["selector"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.detach(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.detach = J__detach;
var J__each = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.each(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.each = J__each;
var J__end = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.end(handler);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.end = J__end;
var J__eq = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index")};
var arguments = get_arguments(signature, args, kwargs);
var index = arguments["index"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.eq(index);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.eq = J__eq;
var J__error = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.error(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.error = J__error;
var J__fade_in = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.fadeIn(duration, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.fade_in = J__fade_in;
var J__fade_out = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.fadeOut(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.fade_out = J__fade_out;
var J__fadeTo = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "opacity", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var opacity = arguments["opacity"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.fade_to(duration, opacity, adapt_arguments(complete));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.fadeTo = J__fadeTo;
var J__fade_toggle = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "easing", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var easing = arguments["easing"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.fade_toggle(duration, easing, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.fade_toggle = J__fade_toggle;
var J__filter = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "selector")};
var arguments = get_arguments(signature, args, kwargs);
var selector = arguments["selector"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.filter(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.filter = J__filter;
var J__finish = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "queue")};
var arguments = get_arguments(signature, args, kwargs);
var queue = arguments["queue"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.finish(queue);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.finish = J__finish;
var J__first = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.first();
return get_attribute(J, "__call__")(create_array(o), {});
}

J.first = J__first;
var J__focus = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.focus(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.focus = J__focus;
var J__focus_in = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.focusIn(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.focus_in = J__focus_in;
var J__focus_out = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.focusOut(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.focus_out = J__focus_out;
var J__get = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "index")};
var arguments = get_arguments(signature, args, kwargs);
var index = arguments["index"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.get(index);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.get = J__get;
var J__has_class = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "name")};
var arguments = get_arguments(signature, args, kwargs);
var name = arguments["name"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.has_class(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.has_class = J__has_class;
var J__height = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.height(value);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.height = J__height;
var J__hide = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.hide(duration, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.hide = J__hide;
var J__hover = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.hover(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.hover = J__hover;
var J__html = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var self = arguments["self"];
j = get_attribute(self, "j");
if(value != undefined) {
o = j.html(value);
}
else {
o = j.html();
}

return o;
}

J.html = J__html;
var J__index = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "selector")};
var arguments = get_arguments(signature, args, kwargs);
var selector = arguments["selector"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.index(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.index = J__index;
var J__inner_height = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.innerHeight();
return get_attribute(J, "__call__")(create_array(o), {});
}

J.inner_height = J__inner_height;
var J__inner_width = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.innerWidth();
return get_attribute(J, "__call__")(create_array(o), {});
}

J.inner_width = J__inner_width;
var J__insert_after = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "target")};
var arguments = get_arguments(signature, args, kwargs);
var target = arguments["target"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.insertAfter(target);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.insert_after = J__insert_after;
var J__insert_before = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "target")};
var arguments = get_arguments(signature, args, kwargs);
var target = arguments["target"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.insertBefore(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.insert_before = J__insert_before;
var J__is_ = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "name")};
var arguments = get_arguments(signature, args, kwargs);
var name = arguments["name"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.is(selector);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.is_ = J__is_;
var J__keydown = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.keydown(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.keydown = J__keydown;
var J__keypress = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.keypress(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.keypress = J__keypress;
var J__keyup = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.keyup(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.keyup = J__keyup;
var J__last = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.last(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.last = J__last;
var J__on = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var event = arguments["event"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.on(event, adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.on = J__on;
var J__load = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "url", "data", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var data = arguments["data"];
var url = arguments["url"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.load(url, data, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.load = J__load;
var J__select = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.select(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.select = J__select;
var J__show = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.show(duration, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.show = J__show;
var J__siblings = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "selector")};
var arguments = get_arguments(signature, args, kwargs);
var selector = arguments["selector"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.select(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.siblings = J__siblings;
var J__size = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.size();
return get_attribute(J, "__call__")(create_array(o), {});
}

J.size = J__size;
var J__slice = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "start", "end")};
var arguments = get_arguments(signature, args, kwargs);
var end = arguments["end"];
var start = arguments["start"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.slice(start, end);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.slice = J__slice;
var J__slide_down = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.slideDown(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.slide_down = J__slide_down;
var J__slide_toggle = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.slideToggle(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.slide_toggle = J__slide_toggle;
var J__slide_up = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.slideUp(duration, adapt_arguments(complete));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.slide_up = J__slide_up;
var J__stop = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
var arguments = get_arguments(signature, args, kwargs);
var jump_to_end = arguments["jump_to_end"];
var clear_queue = arguments["clear_queue"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.stop(clear_queue, jump_to_end);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.stop = J__stop;
var J__submit = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "clear_queue", "jump_to_end")};
var arguments = get_arguments(signature, args, kwargs);
var jump_to_end = arguments["jump_to_end"];
var clear_queue = arguments["clear_queue"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.submit(clear_queue, jump_to_end);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.submit = J__submit;
var J__text = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "text")};
var arguments = get_arguments(signature, args, kwargs);
var text = arguments["text"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.text(text);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.text = J__text;
var J__toggle = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "duration", "complete")};
var arguments = get_arguments(signature, args, kwargs);
var complete = arguments["complete"];
var duration = arguments["duration"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.toggle(duration, complete);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.toggle = J__toggle;
var J__toggle_class = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "class_name")};
var arguments = get_arguments(signature, args, kwargs);
var class_name = arguments["class_name"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.toggleClass(class_name);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.toggle_class = J__toggle_class;
var J__trigger = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "event")};
var arguments = get_arguments(signature, args, kwargs);
var event = arguments["event"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.trigger(event);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.trigger = J__trigger;
var J__unbind = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "event", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var event = arguments["event"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.unbind(event, adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.unbind = J__unbind;
var J__value = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.val(value);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.value = J__value;
var J__width = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "value")};
var arguments = get_arguments(signature, args, kwargs);
var value = arguments["value"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.width(value);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.width = J__width;
var J__length = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self")};
var arguments = get_arguments(signature, args, kwargs);
var self = arguments["self"];
j = get_attribute(self, "j");
return j.length();
}

J.length = J__length;
var J__map = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "func")};
var arguments = get_arguments(signature, args, kwargs);
var func = arguments["func"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.map(func);
return get_attribute(J, "__call__")(create_array(o), {});
}

J.map = J__map;
var J__mousedown = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mousedown(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mousedown = J__mousedown;
var J__mouseenter = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mouseenter(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mouseenter = J__mouseenter;
var J__mouseleave = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mouseleave(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mouseleave = J__mouseleave;
var J__mousemove = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mousemove(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mousemove = J__mousemove;
var J__mouseout = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mouseout(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mouseout = J__mouseout;
var J__mouseover = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mouseover(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mouseover = J__mouseover;
var J__mouseup = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("self", "handler")};
var arguments = get_arguments(signature, args, kwargs);
var handler = arguments["handler"];
var self = arguments["self"];
j = get_attribute(self, "j");
o = j.mouseup(adapt_arguments(handler));
return get_attribute(J, "__call__")(create_array(o), {});
}

J.mouseup = J__mouseup;
J = create_class("J", parents, J);
var ajax = function(args, kwargs) {
var signature = {"kwargs": {}, "args": create_array("url", "settings")};
var arguments = get_arguments(signature, args, kwargs);
var settings = arguments["settings"];
var url = arguments["url"];
return jQuery.ajax(url, settings);
}

