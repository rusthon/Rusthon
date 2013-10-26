with javascript:  # should be a pure javascript function
                  # it emulates jQuery.click behavior
    def call_callback(callback):
        callback(1,2,3)


def callback(foo, bar, baz):
    print foo
    print bar
    print baz

call_callback(callback)
