with javascript:
    def call_callback(callback):
    	callback(1,2,3)


def callback(foo, bar, baz):
    print foo
    print bar
    print baz

call_callback(callback)
