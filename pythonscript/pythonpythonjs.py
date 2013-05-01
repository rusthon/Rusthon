def create_array():
    """Used to fix a bug/feature of Javascript where new Array(number)
    created a array with number of undefined elements which is not
    what we want"""
    JS('var array = new Array()')
    for i in range(arguments.length):
        JS('array.push(arguments[i])')
    return array


def range(num):
    """Emulates Python's range function"""
    i = 0
    r = JS('[]')
    while i < num:
        r.push(i)
        i = i + 1
    return r


def adapt_arguments(handler):
    """Useful to transform callback arguments to positional arguments"""
    def func():
        handler(Array.prototype.slice.call(arguments))
    return func


def create_class(class_name, parents, attrs):
    """Create a PythonScript class"""
    JS('var klass')
    klass = JSObject()
    klass.bases = parents
    klass.__name__ = class_name
    klass.__dict__ = attrs

    def __call__():
        """Create a PythonScript object"""
        JS('var object')
        object = JSObject()
        object.__class__ = klass
        object.__dict__ = JSObject()
        JS('var init')
        init = get_attribute(object, '__init__')
        if init:
            init.apply(None, arguments)
        return object
    klass.__call__ = __call__
    return klass


def get_attribute(object, attribute):
    """Retrieve an attribute, method or property

    method are actually functions which are converted to methods by
    prepending their arguments with the current object. Properties are
    not functions!"""
    if attribute == '__call__':
        if JS("{}.toString.call(object) === '[object Function]'"):
            return object
    JS('var attr = object[attribute]')
    if attr:
        return attr
    JS('var __dict__ = object.__dict__')
    if __dict__:
        attr = JS('__dict__[attribute]')
        if attr != None:
            return attr
    JS('var __class__ = object.__class__')
    if __class__:
        JS('var __dict__ = __class__.__dict__')
        attr = JS('__dict__[attribute]')
        if attr:
            if JS("{}.toString.call(attr) === '[object Function]'"):
                def method():
                    JS('var args = arguments')
                    if(args.length>0):
                        JS('args[0]').splice(0, 0, object)
                    else:
                        args = JSArray(object)
                    return attr.apply(None, args)
                return method
            return attr
        JS('var bases = __class__.bases')
        for i in range(bases.length):
            JS('var base = bases[i]')
            JS('var attr = get_attribute(base, attribute)')
            if attr:
                if JS("{}.toString.call(attr) === '[object Function]'"):
                    def method():
                        JS('var args = arguments')
                        if(args.length>0):
                            JS('args[0]').splice(0, 0, object)
                        else:
                            args = JSArray(object)
                        return attr.apply(None, args)
                    return method

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
    if signature.args.length:
        argslength = signature.args.length
    else:
        argslength = 0
    kwargslength = JS('Object.keys(signature.kwargs).length')
    j = 0
    for i in range(argslength):
        arg = JS('signature.args[j]')
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
    if signature.vararg:
        JS("out[signature.vararg] = args")
    if signature.varkwarg:
        JS("out[signature.varkwarg] = kwargs")
    return out
