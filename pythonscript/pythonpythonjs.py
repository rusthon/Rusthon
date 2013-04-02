def create_array():
    """Used to fix a bug/feature of Javascript where new Array(number)
    created a array with number of undefined elements which is not
    what we want"""
    JS('array = new Array()')
    for i in range(arguments.length):
        JS('array.push(arguments[i])')
    return array


def range(num):
    """Emulates Python's range function"""
    i = 1
    r = JS('[0]')
    while i < num:
        r.push(i)
        i = i + 1
    return r

def adapt_arguments(handler):
    """Useful to transform callback arguments to positional arguments"""
    def func():
        handler(Array.prototype.slice.call(arguments))
    return func


def create_object():
    """Create a PythonScript object"""
    object = JSObject()
    object.__class__ = klass
    object.__dict__ = JSObject()

    init = get_attribute(object, '__init__')
    if init:
        init.apply(None, arguments)
    return object


def create_class(class_name, parents, attrs):
    """Create a PythonScript class"""
    klass = JSObject()
    klass.bases = parents
    klass.__name__ = class_name
    klass.__dict__ = attrs

    def __call__():
        args = arguments.___insert(0, klass)
        return create_object.apply(None, args)
    klass.__call__ = create_object
    return klass


def get_attribute(object, attribute):
    """Retrieve an attribute, method or property

    method are actually functions which are converted to methods by
    prepending their arguments with the current object. Properties are
    not functions!"""
    if attribute == '__call__':
        if JS("{}.toString.call(object) === '[object Function]'"):
            return object
    attr = JS('object[attribute]')
    if attr:
        return attr
    __dict__ = object.__dict__
    if __dict__:
        attr = JS('__dict__[attribute]')
        if attr:
            return attr
    __class__ = object.__class__
    if __class__:
        __dict__ = __class__.__dict__
        attr = JS('__dict__[attribute]')
        if attr:
            if JS("{}.toString.call(attr) === '[object Function]'"):
                def method():
                    JS('arguments[0]').splice(0, 0, object)
                    return attr.apply(None, arguments)
                return method
            return attr
        bases = __class__.bases
        for i in range(bases.length):
            base = JS('bases[i]')
            attr = get_attribute(base, attribute)
            if attr:
                return attr
    return None


def set_attribute(object, attr, value):
    """Set an attribute on an object by updating its __dict__ property"""
    __dict__ = object.__dict__
    JS('__dict__[attr] = value')


def get_arguments(signature, args, kwargs):
    """Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve
    the actual parameters.

    This will set default keyword arguments and retrieve positional arguments
    in kwargs if their called as such"""
    out = JSObject()
    if parameters.args.length:
        argslength = parameters.args.length
    else:
        argslength = 0
    kwargslength = JS('Object.keys(parameters.kwargs).length')
    j = 0
    for i in range(argslength):
        arg = JS('parameters.args[j]')
        if kwargs:
            kwarg = JS('kwargs[arg]')
            if kwarg:
                JS('out[arg] = kwarg')
                JS('delete kwargs[arg]')
            else:
                JS('out[arg] = args[j]')
                j = j + 1
        else:
            JS('out[arg] = args[j]')
            j = j + 1
    args = args.slice(j)
    if parameters.vararg:
        JS("out[parameters.vararg] = args")
    if parameters.varkwarg:
        JS("out[parameters.varkwarg] = kwargs")
    return out
