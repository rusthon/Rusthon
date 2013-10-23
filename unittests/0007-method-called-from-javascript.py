with javascript:
    JS('var call_callback = function(callback) {')
    callback('one', 'two', 'three')
    JS('}')


class SuperClass:

    def callback(self, foo, bar, baz):
        print foo
        print bar
        print baz
        print "viva l'algerie"

call_callback(SuperClass().callback)
