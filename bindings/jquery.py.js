J = Object();
parents = new Array();
var J____init__ = function(self, arg) {
set_attribute(self, "j", jQuery(arg));

}
J.__init__ = J____init__;
var J__add = function(self, arg) {
j = get_attribute(self, "j");
o = j.add(arg);
return get_attribute(J, "__call__")(o);
}
J.add = J__add;
var J__addClass = function(self, klass) {
j = get_attribute(self, "j");
o = j.addClass(klass);
return get_attribute(J, "__call__")(o);
}
J.addClass = J__addClass;
var J__after = function(self, arg) {
j = get_attribute(self, "j");
o = j.after(arg);
return get_attribute(J, "__call__")(o);
}
J.after = J__after;
var J__animate = function(self, properties, duration, easing, complete) {
j = get_attribute(self, "j");
o = j.animate(properties, duration, easing, complete);
return get_attribute(J, "__call__")(o);
}
J.animate = J__animate;
var J__append = function(self, arg) {
j = get_attribute(self, "j");
o = j.append(arg);
return get_attribute(J, "__call__")(o);
}
J.append = J__append;
var J__appendTo = function(self, arg) {
j = get_attribute(self, "j");
o = j.appendTo(arg);
return get_attribute(J, "__call__")(o);
}
J.appendTo = J__appendTo;
var J__attr = function(self, arg) {
j = get_attribute(self, "j");
o = j.attr(arg);
return get_attribute(J, "__call__")(o);
}
J.attr = J__attr;
var J__before = function(self, arg) {
j = get_attribute(self, "j");
o = j.before(arg);
return get_attribute(J, "__call__")(o);
}
J.before = J__before;
var J__bind = function(self, event_type, event_data, handler) {
j = get_attribute(self, "j");
o = j.bind(event_type, event_data, handler);
return get_attribute(J, "__call__")(o);
}
J.bind = J__bind;
var J__blur = function(self, handler) {
j = get_attribute(self, "j");
o = j.blur(handler);
return get_attribute(J, "__call__")(o);
}
J.blur = J__blur;
var J__change = function(self, handler) {
j = get_attribute(self, "j");
o = j.change(handler);
return get_attribute(J, "__call__")(o);
}
J.change = J__change;
var J__children = function(self, selector) {
j = get_attribute(self, "j");
o = j.children(selector);
return get_attribute(J, "__call__")(o);
}
J.children = J__children;
var J__click = function(self, handler) {
j = get_attribute(self, "j");
o = j.click(handler);
return get_attribute(J, "__call__")(o);
}
J.click = J__click;
var J__clone = function(self, with_data_and_events) {
j = get_attribute(self, "j");
o = j.clone(with_data_and_events);
return get_attribute(J, "__call__")(o);
}
J.clone = J__clone;
var J__contents = function(self) {
j = get_attribute(self, "j");
o = j.contents();
return get_attribute(J, "__call__")(o);
}
J.contents = J__contents;
var J__css = function(self, name, value) {
j = get_attribute(self, "j");
o = j.css(name);
return get_attribute(J, "__call__")(o);
}
J.css = J__css;
var J__data = function(self, key, value) {
j = get_attribute(self, "j");
o = j.data(key, value);
return get_attribute(J, "__call__")(o);
}
J.data = J__data;
var J__double_click = function(self, handler) {
j = get_attribute(self, "j");
o = j.dbclick(handler);
return get_attribute(J, "__call__")(o);
}
J.double_click = J__double_click;
var J__delay = function(self, time, queue_name) {
j = get_attribute(self, "j");
o = j.delay(time, queue_name);
return get_attribute(J, "__call__")(o);
}
J.delay = J__delay;
var J__dequeue = function(self, queue_name) {
j = get_attribute(self, "j");
o = j.dequeue(queue_name);
return get_attribute(J, "__call__")(o);
}
J.dequeue = J__dequeue;
var J__detach = function(self, selector) {
j = get_attribute(self, "j");
o = j.detach(selector);
return get_attribute(J, "__call__")(o);
}
J.detach = J__detach;
var J__each = function(self, handler) {
j = get_attribute(self, "j");
o = j.each(handler);
return get_attribute(J, "__call__")(o);
}
J.each = J__each;
var J__end = function(self, handler) {
j = get_attribute(self, "j");
o = j.end();
return get_attribute(J, "__call__")(o);
}
J.end = J__end;
var J__eq = function(self, index) {
j = get_attribute(self, "j");
o = j.eq(index);
return get_attribute(J, "__call__")(o);
}
J.eq = J__eq;
var J__error = function(self, handler) {
j = get_attribute(self, "j");
o = j.error(handler);
return get_attribute(J, "__call__")(o);
}
J.error = J__error;
var J__fade_in = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.fadeIn(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.fade_in = J__fade_in;
var J__fade_out = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.fadeOut(handler);
return get_attribute(J, "__call__")(o);
}
J.fade_out = J__fade_out;
var J__fadeTo = function(self, duration, opacity, complete) {
j = get_attribute(self, "j");
o = j.fade_to(handler);
return get_attribute(J, "__call__")(o);
}
J.fadeTo = J__fadeTo;
var J__fade_toggle = function(self, duration, easing, complete) {
j = get_attribute(self, "j");
o = j.fade_toggle(duration, easing, complete);
return get_attribute(J, "__call__")(o);
}
J.fade_toggle = J__fade_toggle;
var J__filter = function(self, selector) {
j = get_attribute(self, "j");
o = j.filter(selector);
return get_attribute(J, "__call__")(o);
}
J.filter = J__filter;
var J__finish = function(self, queue) {
j = get_attribute(self, "j");
o = j.finish(queue);
return get_attribute(J, "__call__")(o);
}
J.finish = J__finish;
var J__first = function(self) {
j = get_attribute(self, "j");
o = j.first();
return get_attribute(J, "__call__")(o);
}
J.first = J__first;
var J__focus = function(self, handler) {
j = get_attribute(self, "j");
o = j.focus(handler);
return get_attribute(J, "__call__")(o);
}
J.focus = J__focus;
var J__focus_in = function(self, handler) {
j = get_attribute(self, "j");
o = j.focus_in(handler);
return get_attribute(J, "__call__")(o);
}
J.focus_in = J__focus_in;
var J__focus_out = function(self, handler) {
j = get_attribute(self, "j");
o = j.filter(selector);
return get_attribute(J, "__call__")(o);
}
J.focus_out = J__focus_out;
var J__get = function(self, index) {
j = get_attribute(self, "j");
o = j.get(index);
return get_attribute(J, "__call__")(o);
}
J.get = J__get;
var J__has_class = function(self, name) {
j = get_attribute(self, "j");
o = j.has_class(selector);
return get_attribute(J, "__call__")(o);
}
J.has_class = J__has_class;
var J__height = function(self, value) {
j = get_attribute(self, "j");
o = j.height(value);
return get_attribute(J, "__call__")(o);
}
J.height = J__height;
var J__hide = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.hide(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.hide = J__hide;
var J__hover = function(self, handler) {
j = get_attribute(self, "j");
o = j.hover(handler);
return get_attribute(J, "__call__")(o);
}
J.hover = J__hover;
var J__html = function(self, value) {
j = get_attribute(self, "j");
o = j.html(value);
return get_attribute(J, "__call__")(o);
}
J.html = J__html;
var J__index = function(self, selector) {
j = get_attribute(self, "j");
o = j.index(selector);
return get_attribute(J, "__call__")(o);
}
J.index = J__index;
var J__inner_height = function(self) {
j = get_attribute(self, "j");
o = j.innerHeight();
return get_attribute(J, "__call__")(o);
}
J.inner_height = J__inner_height;
var J__inner_width = function(self) {
j = get_attribute(self, "j");
o = j.innerWidth();
return get_attribute(J, "__call__")(o);
}
J.inner_width = J__inner_width;
var J__insert_after = function(self, target) {
j = get_attribute(self, "j");
o = j.insertAfter(target);
return get_attribute(J, "__call__")(o);
}
J.insert_after = J__insert_after;
var J__insert_before = function(self, target) {
j = get_attribute(self, "j");
o = j.insertBefore(selector);
return get_attribute(J, "__call__")(o);
}
J.insert_before = J__insert_before;
var J__is_ = function(self, name) {
j = get_attribute(self, "j");
o = j.is(selector);
return get_attribute(J, "__call__")(o);
}
J.is_ = J__is_;
var J__keydown = function(self, handler) {
j = get_attribute(self, "j");
o = j.keydown(handler);
return get_attribute(J, "__call__")(o);
}
J.keydown = J__keydown;
var J__keypress = function(self, handler) {
j = get_attribute(self, "j");
o = j.keypress(handler);
return get_attribute(J, "__call__")(o);
}
J.keypress = J__keypress;
var J__keyup = function(self, handler) {
j = get_attribute(self, "j");
o = j.keyup(handler);
return get_attribute(J, "__call__")(o);
}
J.keyup = J__keyup;
var J__last = function(self, handler) {
j = get_attribute(self, "j");
o = j.last(handler);
return get_attribute(J, "__call__")(o);
}
J.last = J__last;
var J__on = function(self, event, handler) {
j = get_attribute(self, "j");
o = j.on(event, handler);
return get_attribute(J, "__call__")(o);
}
J.on = J__on;
var J__load = function(self, url, data, complete) {
j = get_attribute(self, "j");
o = j.load(url, data, complete);
return get_attribute(J, "__call__")(o);
}
J.load = J__load;
var J__select = function(self, handler) {
j = get_attribute(self, "j");
o = j.select(handler);
return get_attribute(J, "__call__")(o);
}
J.select = J__select;
var J__show = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.show(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.show = J__show;
var J__siblings = function(self, selector) {
j = get_attribute(self, "j");
o = j.select(handler);
return get_attribute(J, "__call__")(o);
}
J.siblings = J__siblings;
var J__size = function(self) {
j = get_attribute(self, "j");
o = j.size();
return o;
}
J.size = J__size;
var J__slice = function(self, start, end) {
j = get_attribute(self, "j");
o = j.slice(start, end);
return get_attribute(J, "__call__")(o);
}
J.slice = J__slice;
var J__slide_down = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.slideDown(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.slide_down = J__slide_down;
var J__slide_toggle = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.slideToggle(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.slide_toggle = J__slide_toggle;
var J__slide_up = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.slideUp(duration, complete);
return get_attribute(J, "__call__")(o);
}
J.slide_up = J__slide_up;
var J__stop = function(self, clear_queue, jump_to_end) {
j = get_attribute(self, "j");
o = j.stop(clear_queue, jump_to_end);
return get_attribute(J, "__call__")(o);
}
J.stop = J__stop;
var J__submit = function(self, clear_queue, jump_to_end) {
j = get_attribute(self, "j");
o = j.submit(handler);
return o;
}
J.submit = J__submit;
var J__text = function(self, text) {
j = get_attribute(self, "j");
o = j.text(text);
return o;
}
J.text = J__text;
var J__toggle = function(self, duration, complete) {
j = get_attribute(self, "j");
o = j.toggle(duration, complete);
return o;
}
J.toggle = J__toggle;
var J__toggle_class = function(self, class_name) {
j = get_attribute(self, "j");
o = j.toggle_class(class_name);
return o;
}
J.toggle_class = J__toggle_class;
var J__trigger = function(self, event) {
j = get_attribute(self, "j");
o = j.trigger(event);
return o;
}
J.trigger = J__trigger;
var J__unbind = function(self, event, handler) {
j = get_attribute(self, "j");
o = j.unbind(event, handler);
return o;
}
J.unbind = J__unbind;
var J__value = function(self, value) {
j = get_attribute(self, "j");
o = j.val(value);
return o;
}
J.value = J__value;
var J__width = function(self, value) {
j = get_attribute(self, "j");
o = j.width(value);
return get_attribute(J, "__call__")(o);
}
J.width = J__width;
var J__length = function(self) {
j = get_attribute(self, "j");
return j.length();
}
J.length = J__length;
var J__map = function(self, func) {
j = get_attribute(self, "j");
o = j.map(func);
return get_attribute(J, "__call__")(o);
}
J.map = J__map;
var J__mousedown = function(self, handler) {
j = get_attribute(self, "j");
o = j.mousedown(handler);
return get_attribute(J, "__call__")(o);
}
J.mousedown = J__mousedown;
var J__mouseenter = function(self, handler) {
j = get_attribute(self, "j");
o = j.mouseenter(handler);
return get_attribute(J, "__call__")(o);
}
J.mouseenter = J__mouseenter;
var J__mouseleave = function(self, handler) {
j = get_attribute(self, "j");
o = j.mouseleave(handler);
return get_attribute(J, "__call__")(o);
}
J.mouseleave = J__mouseleave;
var J__mousemove = function(self, handler) {
j = get_attribute(self, "j");
o = j.mousemove(handler);
return get_attribute(J, "__call__")(o);
}
J.mousemove = J__mousemove;
var J__mouseout = function(self, handler) {
j = get_attribute(self, "j");
o = j.mouseout(handler);
return get_attribute(J, "__call__")(o);
}
J.mouseout = J__mouseout;
var J__mouseover = function(self, handler) {
j = get_attribute(self, "j");
o = j.mouseover(handler);
return get_attribute(J, "__call__")(o);
}
J.mouseover = J__mouseover;
var J__mouseup = function(self, handler) {
j = get_attribute(self, "j");
o = j.mouseup(handler);
return get_attribute(J, "__call__")(o);
}
J.mouseup = J__mouseup;
J = create_class("J", parents, J);
var ajax = function(url, settings) {
return jQuery(url, settings);
}

