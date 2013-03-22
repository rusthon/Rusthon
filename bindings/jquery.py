class J:

    def __init__(self, arg):
        self.j = JS("jQuery(arg)")

    def add(self, arg):
        j = self.j
        o = JS('j.add(arg)')
        return J(o)

    def add(self, arg):
        j = self.j
        o = JS('j.addBack(arg)')
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
        o = JS('j.bind(event_type, event_data, handler)')
        return J(o)

    def blur(self, handler):
        j = self.j
        o = JS('j.blur(handler)')
        return J(o)

    def change(self, handler):
        j = self.j
        o = JS('j.change(handler)')
        return J(o)

    def children(self, selector):
        j = self.j
        o = JS('j.children(selector)')
        return J(o)

    def click(self, handler):
        j = self.j
        o = JS('j.click(handler)')
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
        o = JS('j.css(name)')
        return o

    def data(self, key, value):
        j = self.j
        o = JS('j.data(key, value)')
        return o

    def double_click(self, handler):
        j = self.j
        o = JS('j.dbclick(handler)')
        return o

    def delay(self, time, queue_name):
        j = self.j
        o = JS('j.delay(time, queue_name)')
        return o

    def delay(self, time, queue_name):
        j = self.j
        o = JS('j.delay(time, queue_name)')
        return o

    def dequeue(self, queue_name):
        j = self.j
        o = JS('j.dequeue(queue_name)')
        return o

    def dequeue(self, queue_name):
        j = self.j
        o = JS('j.dequeue(queue_name)')
        return o

    def dequeue(self, queue_name):
        j = self.j
        o = JS('j.dequeue(queue_name)')
        return o

    def dequeue(self, queue_name):
        j = self.j
        o = JS('j.dequeue(queue_name)')
        return o

    def detach(self, selector):
        j = self.j
        o = JS('j.detach(selector)')
        return o

    def die(self, event_type, handler):
        j = self.j
        o = JS('j.detach(event_type, handler)')
        return o

    def each(self, handler):
        j = self.j
        o = JS('j.each(handler)')
        return o

    def end(self, handler):
        j = self.j
        o = JS('j.end()')
        return o

    def eq(self, index):
        j = self.j
        o = JS('j.eq(index)')
        return o

    def error(self, handler):
        j = self.j
        o = JS('j.error(handler)')
        return o
