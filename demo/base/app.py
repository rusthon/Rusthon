### FRAMEWORK STUFF ###################################################


class Messaging:
    """Class for sending message which allows for loose coupling of
    component in the app.

    Example usage:

    .. code-block:: python

       messaging = Messaging()
       messaging.subscribe(something, 'boot:done')
       messaging.publish(boot, 'boot:done')
    """

    def __init__(self):
        self.omni = list()
        self.channels = dict()

    def publish(self, sender, channel, param=None):
        print 'publish', sender, channel, param
        for receiver in self.omni:
            receiver(sender, channel, param)
        channel = self.channels.get(channel, None)
        if channel:
            channel = self.channels.get(channel)
            for receiver in channel:
                receiver(sender, channel, param)

    def subscribe(self, receiver, channel=None):
        print 'subscribe', channel
        if not channel:
            self.omni.append(receiver)
        else:
            receivers = self.channels.get(channel)
            if receivers:
                receivers.append(receiver)
            else:
                receivers = list()
                receivers.append(receiver)
                self.channels.set(channel, receivers)


class Node:
    """Node in a state machine"""

    def __init__(self, app):
        self.app = app
        self.transitions = dict()

    def transition(self, message, end):
        """Change state on ``message`` to ``end``"""
        self.transitions.set(message, end)

    def on_leave(self, next, sender, message, param=None):
        print 'on_leave empty', next, sender, message, param

    def on_enter(self, before, sender, message, param=None):
        print 'on_enter empty', before, sender, message, param


class Machinima:
    """State machine"""

    def __init__(self, name):
        self.name = name
        self.node = None

    def handle(self, sender, message, param=None):
        print 'handle', sender, message, param
        end = self.node.transitions.get(message)
        if end:
            self.node.on_leave(next, sender, message, param)
            end.on_enter(self.node, sender, message, param)
            self.node = end

    def start(self):
        self.node.on_enter(None, None, None, None)


class Animator:

    def __init__(self, func, delay, loop):
        self.func = func
        self.delay = delay
        self.loop = loop

    def start(self):
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


class Application:

    def __init__(self):
        self.messaging = Messaging()
        self.machinima = Machinima('main')
        self.messaging.subscribe(self.machinima.handle)

### END FRAMEWORK STUFF ###################################################

### PROGRESSIVE TEXT ######################################################

ABC = str('azertyuiopQSDFGHJKLMwxcvbnAZERTYUIOPqsdfghjklmWXCVBN  ')


class ProgressiveText:

    def __init__(self, selector, text, callback=None, delay=50):
        self.callback = callback
        self.delay = delay
        self.text = text
        self.length = len(text)
        var(element)
        element = J(selector)
        element.html('')
        self.element = element
        for i in text:
            element.append('<span>a</span>')
        self.elements = J(selector + ' span')

    def start(self):
        self.running = True
        self.animation = Animator(self.update, self.delay, True)
        self.animation.start()

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
            if self.callback:
                self.callback(self)

### END PROGRESSIVE TEXT ##############################################

### START APP #########################################################~


link = J('#link')
playground = J('#playground')


class Block:

    def __init__(self, action, helpline, href):
        block = J('<div></div>')
        playground.append(block.j)
        block.click(self.show)
        self.action = action
        self.helpline = helpline
        self.href = href

    def show(self):
        ProgressiveText('#action', self.action, delay=75).start()
        ProgressiveText('#helpline', self.helpline, delay=100).start()
        link.attr('href', self.href)


def hightlight_title(progressive):
    progressive.element.toggle_class('hightlight-title')


def hightlight_helpline(progressive):
    progressive.element.toggle_class('hightlight-helpline')


class Wooooot(Application):

    def __init__(self):
        Application.__init__(self)

        ProgressiveText('#title', str('Wooooot'), hightlight_title, 100).start()
        ProgressiveText('#helpline', str('computer hacks'), hightlight_helpline, 200).start()


Wooooot()
