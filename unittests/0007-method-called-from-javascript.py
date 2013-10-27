with javascript:  # should be a pure javascript function
                  # it emulates jQuery.click behavior
    def call_callback(callback):
        callback(1,2,3)


class SuperClass:

    def callback(self, foo, bar, baz):
        print foo
        print bar
        print baz
        print "viva l'algerie"

call_callback(SuperClass().callback)
