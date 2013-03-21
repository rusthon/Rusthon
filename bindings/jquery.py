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
