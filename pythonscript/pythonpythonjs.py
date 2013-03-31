# FIX a "bug" in Javascript new Array where new Array(number) creates a list of undefined
def create_array():
    JS('array = new Array()')
    for i in arguments.length:
        JS('array.push(arguments[i])')
    return array


def adapt_arguments(handler):
    def func():
        handler(Array.prototype.slice.call(arguments))
    return func


def create_object():
    object = JSObject()
    object.__class__ = klass
    object.__dict__ = JSObject()

    init = get_attribute(object, '__init__')
    if init:
        init.apply(None, arguments)
    return object


def create_class(class_name, parents, attrs):
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
        for i in bases.length:
            base = JS('bases[i]')
            attr = get_attribute(base, attribute)
            if attr:
                return attr
    return None


def set_attribute(object, attr, value):
    __dict__ = object.__dict__
    JS('__dict__[attr] = value')


def get_arguments(parameters, args, kwargs):
    out = JSObject()
    if parameters.args.length:
        argslength = parameters.args.length
    else:
        argslength = 0
    kwargslength = JS('Object.keys(parameters.kwargs).length')
    j = 0
    for i in argslength:
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
