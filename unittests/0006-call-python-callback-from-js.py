with javascript:
    JS('var call_callback = function(callback) {')
    callback(1,2,3)
    JS('}')


def callback(foo, bar, baz):
    print foo
    print bar
    print baz

call_callback(callback)
