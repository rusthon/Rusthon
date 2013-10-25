with javascript:
    def call_callback(callback):
    	with python:
    		callback('one', 'two', 'three')


class SuperClass:

    def callback(self, foo, bar, baz):
        print foo
        print bar
        print baz
        print "viva l'algerie"

call_callback(SuperClass().callback)
