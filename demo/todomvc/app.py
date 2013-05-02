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


### START APP #########################################################~

