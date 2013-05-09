### PROGRESSIVE TEXT ######################################################

class Animator:

    def __init__(self, func, delay, loop):
        self.func = func
        self.delay = delay
        self.loop = loop

    def run(self):
        var(delay, func)
        delay = self.delay
        func = self.func
        if self.loop:
            self.id = JS('setInterval(adapt_arguments(func), delay)')
        else:
            JS('setTimeout(adapt_arguments(func), delay)')

    def stop(self):
        var(id)
        id = self.id
        JS('clearInterval(id)')

ABC = str('azertyuiopQSDFGHJKLMwxcvbnAZERTYUIOPqsdfghjklmWXCVBN ')


class ProgressiveText:

    def __init__(self, selector, text, callback=None, delay=3000):
        self.delay = delay
        self.text = text
        self.length = len(text)
        var(element)
        element = J(selector)
        element.html('')
        for i in text:
            element.append('<span>a</span>')
        self.elements = J(selector + ' span')

    def start(self):
        self.animation = Animator(self.update, self.delay, True)
        self.animation.run()

    def update(self):
        var(to_update)
        to_update = False
        for index in range(self.length):
            var(element, char, expected)
            element = self.elements.get(index)
            char = element.html()
            expected = self.text.get(index)
            if char != expected:
                var(novo)
                novo = ABC.get(ABC.index(char) + 1)
                element.html(novo)
                to_update = True
        if not to_update:
            self.animation.stop()

### END PROGRESSIVE TEXT ##############################################

ProgressiveText("#héllo", str('Hello World')).start()
