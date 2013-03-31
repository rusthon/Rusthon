class J:

    def __init__(self, arg):
        self.j = JS("jQuery(arg)")

    def add(self, arg):
        j = self.j
        o = JS('j.add(arg)')
        return J(o)

    def addClass(self, klass):
        j = self.j
        o = JS('j.addClass(klass)')
        return J(o)

    def after(self, arg):
        j = self.j
        o = JS('j.after(arg)')
        return J(o)

    def animate(self, properties, duration, easing, complete):
        j = self.j
        o = JS('j.animate(properties, duration, easing, complete)')
        return J(o)

    def append(self, arg):
        j = self.j
        o = JS('j.append(arg)')
        return J(o)

    def appendTo(self, arg):
        j = self.j
        o = JS('j.appendTo(arg)')
        return J(o)

    def attr(self, arg):
        j = self.j
        o = JS('j.attr(arg)')
        return J(o)

    def before(self, arg):
        j = self.j
        o = JS('j.before(arg)')
        return J(o)

    def bind(self, event_type, event_data, handler):
        j = self.j
        o = JS('j.bind(event_type, event_data, adapt_arguments(handler))')
        return J(o)

    def blur(self, handler):
        j = self.j
        o = JS('j.blur(adapt_arguments(handler))')
        return J(o)

    def change(self, handler):
        j = self.j
        o = JS('j.change(adapt_arguments(handler))')
        return J(o)

    def children(self, selector):
        j = self.j
        o = JS('j.children(selector)')
        return J(o)

    def click(self, handler):
        j = self.j
        o = JS('j.click(adapt_arguments(handler))')
        return J(o)

    def clone(self, with_data_and_events):
        j = self.j
        o = JS('j.clone(with_data_and_events)')
        return J(o)

    def contents(self):
        j = self.j
        o = JS('j.contents()')
        return J(o)

    def css(self, name, value):
        j = self.j
        o = JS('j.css(name, value)')
        return J(o)

    def data(self, key, value):
        j = self.j
        o = JS('j.data(key, value)')
        return J(o)

    def double_click(self, handler):
        j = self.j
        o = JS('j.dbclick(adapt_arguments(handler))')
        return J(o)

    def delay(self, time, queue_name):
        j = self.j
        o = JS('j.delay(time, queue_name)')
        return J(o)

    def dequeue(self, queue_name):
        j = self.j
        o = JS('j.dequeue(queue_name)')
        return J(o)

    def detach(self, selector):
        j = self.j
        o = JS('j.detach(selector)')
        return J(o)

    def each(self, handler):
        j = self.j
        o = JS('j.each(adapt_arguments(handler))')
        return J(o)

    def end(self, handler):
        j = self.j
        o = JS('j.end(handler)')
        return J(o)

    def eq(self, index):
        j = self.j
        o = JS('j.eq(index)')
        return J(o)

    def error(self, handler):
        j = self.j
        o = JS('j.error(adapt_arguments(handler))')
        return J(o)

    def fade_in(self, duration, complete):
        j = self.j
        o = JS('j.fadeIn(duration, complete)')
        return J(o)

    def fade_out(self, duration, complete):
        j = self.j
        o = JS('j.fadeOut(duration, adapt_arguments(complete))')
        return J(o)

    def fadeTo(self, duration, opacity, complete):
        j = self.j
        o = JS('j.fade_to(duration, opacity, adapt_arguments(complete))')
        return J(o)

    def fade_toggle(self, duration, easing, complete):
        j = self.j
        o = JS('j.fade_toggle(duration, easing, complete)')
        return J(o)

    def filter(self, selector):
        j = self.j
        o = JS('j.filter(selector)')
        return J(o)

    def finish(self, queue):
        j = self.j
        o = JS('j.finish(queue)')
        return J(o)

    def first(self, ):
        j = self.j
        o = JS('j.first()')
        return J(o)

    def focus(self, handler):
        j = self.j
        o = JS('j.focus(adapt_arguments(handler))')
        return J(o)

    def focus_in(self, handler):
        j = self.j
        o = JS('j.focusIn(adapt_arguments(handler))')
        return J(o)

    def focus_out(self, handler):
        j = self.j
        o = JS('j.focusOut(adapt_arguments(handler))')
        return J(o)

    def get(self, index):
        j = self.j
        o = JS('j.get(index)')
        return J(o)

    def has_class(self, name):
        j = self.j
        o = JS('j.has_class(selector)')
        return J(o)

    def height(self, value):
        j = self.j
        o = JS('j.height(value)')
        return J(o)

    def hide(self, duration, complete):
        j = self.j
        o = JS('j.hide(duration, complete)')
        return J(o)

    def hover(self, handler):
        j = self.j
        o = JS('j.hover(adapt_arguments(handler))')
        return J(o)

    def html(self, value):
        j = self.j
        o = JS('j.html(value)')
        return J(o)

    def index(self, selector):
        j = self.j
        o = JS('j.index(selector)')
        return J(o)

    def inner_height(self):
        j = self.j
        o = JS('j.innerHeight()')
        return J(o)

    def inner_width(self):
        j = self.j
        o = JS('j.innerWidth()')
        return J(o)

    def insert_after(self, target):
        j = self.j
        o = JS('j.insertAfter(target)')
        return J(o)

    def insert_before(self, target):
        j = self.j
        o = JS('j.insertBefore(selector)')
        return J(o)

    def is_(self, name):
        j = self.j
        o = JS('j.is(selector)')
        return J(o)

    def keydown(self, handler):
        j = self.j
        o = JS('j.keydown(adapt_arguments(handler))')
        return J(o)

    def keypress(self, handler):
        j = self.j
        o = JS('j.keypress(adapt_arguments(handler))')
        return J(o)

    def keyup(self, handler):
        j = self.j
        o = JS('j.keyup(adapt_arguments(handler))')
        return J(o)

    def last(self, handler):
        j = self.j
        o = JS('j.last(adapt_arguments(handler))')
        return J(o)

    def on(self, event, handler):
        j = self.j
        o = JS('j.on(event, adapt_arguments(handler))')
        return J(o)

    def load(self, url, data, complete):
        j = self.j
        o = JS('j.load(url, data, complete)')
        return J(o)

    def select(self, handler):
        j = self.j
        o = JS('j.select(adapt_arguments(handler))')
        return J(o)

    def show(self, duration, complete):
        j = self.j
        o = JS('j.show(duration, complete)')
        return J(o)

    def siblings(self, selector):
        j = self.j
        o = JS('j.select(adapt_arguments(handler))')
        return J(o)

    def size(self):
        j = self.j
        o = JS('j.size()')
        return J(o)

    def slice(self, start, end):
        j = self.j
        o = JS('j.slice(start, end)')
        return J(o)

    def slide_down(self, duration, complete):
        j = self.j
        o = JS('j.slideDown(duration, complete)')
        return J(o)

    def slide_toggle(self, duration, complete):
        j = self.j
        o = JS('j.slideToggle(duration, complete)')
        return J(o)

    def slide_up(self, duration, complete):
        j = self.j
        o = JS('j.slideUp(duration, complete)')
        return J(o)

    def stop(self, clear_queue, jump_to_end):
        j = self.j
        o = JS('j.stop(clear_queue, jump_to_end)')
        return J(o)

    def submit(self, clear_queue, jump_to_end):
        j = self.j
        o = JS('j.submit(clear_queue, jump_to_end)')
        return J(o)

    def text(self, text):
        j = self.j
        o = JS('j.text(text)')
        return J(o)

    def toggle(self, duration, complete):
        j = self.j
        o = JS('j.toggle(duration, complete)')
        return J(o)

    def toggle_class(self, class_name):
        j = self.j
        o = JS('j.toggleClass(class_name)')
        return J(o)

    def trigger(self, event):
        j = self.j
        o = JS('j.trigger(event)')
        return J(o)

    def unbind(self, event, handler):
        j = self.j
        o = JS('j.unbind(event, adapt_arguments(handler))')
        return J(o)

    def value(self, value):
        j = self.j
        o = JS('j.val(value)')
        return J(o)

    def width(self, value):
        j = self.j
        o = JS('j.width(value)')
        return J(o)

    def length(self):
        j = self.j
        return JS('j.length()')

    def map(self, func):
        j = self.j
        o = JS('j.map(func)')
        return J(o)

    def mousedown(self, handler):
        j = self.j
        o = JS('j.mousedown(adapt_arguments(handler))')
        return J(o)

    def mouseenter(self, handler):
        j = self.j
        o = JS('j.mouseenter(adapt_arguments(handler))')
        return J(o)

    def mouseleave(self, handler):
        j = self.j
        o = JS('j.mouseleave(adapt_arguments(handler))')
        return J(o)

    def mousemove(self, handler):
        j = self.j
        o = JS('j.mousemove(adapt_arguments(handler))')
        return J(o)

    def mouseout(self, handler):
        j = self.j
        o = JS('j.mouseout(adapt_arguments(handler))')
        return J(o)

    def mouseover(self, handler):
        j = self.j
        o = JS('j.mouseover(adapt_arguments(handler))')
        return J(o)

    def mouseup(self, handler):
        j = self.j
        o = JS('j.mouseup(adapt_arguments(handler))')
        return J(o)


def ajax(url, settings):
    return JS("jQuery.ajax(url, settings)")
        
