def jsrange(num):
    """Emulates Python's range function"""
    var(i, r)
    i = 0
    r = JS('[]')
    while i < num:
        r.push(i)
        i = i + 1
    return r


def create_array():
    """Used to fix a bug/feature of Javascript where new Array(number)
    created a array with number of undefined elements which is not
    what we want"""
    JS('var array = new Array()')
    for i in jsrange(arguments.length):
        JS('array.push(arguments[i])')
    return array


def adapt_arguments(handler):
    """Useful to transform Javascript arguments to Python arguments"""
    def func():
        handler(Array.prototype.slice.call(arguments))
    return func


def create_class(class_name, parents, attrs):
    """Create a PythonScript class"""
    if attrs.__metaclass__:
        var(metaclass)
        metaclass = attrs.__metaclass__
        attrs.__metaclass__ = None
        return metaclass(JS('[class_name, parents, attrs]'))
    var(klass)
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
    var(attr)
    JS('attr = object[attribute]')
    if attr:
        return attr
    var(__class__, __dict__, __get__, bases)
    # Check object.__class__.__dict__ for data descriptors named attr
    __class__ = object.__class__
    if __class__:
        __dict__ = __class__.__dict__
        attr = JS('__dict__[attribute]')
        if attr:
            __get__ = get_attribute(attr, '__get__')
            if __get__:
                return __get__(JS('[object, __class__]'))
        bases = __class__.bases
        for i in jsrange(bases.length):
            var(base, attr)
            JS('base = bases[i]')
            attr = get_attribute(base, attribute)
            if attr:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__(JS('[object, __class__]'))
    # Check object.__dict__ for attr and its bases if it a class
    # in the case if the descriptor is found return it
    __dict__ = object.__dict__
    bases = object.__bases__
    if __dict__:
        attr = JS('__dict__[attribute]')
        if attr != None:
            if bases:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__(JS('[undefined, __class__]'))
            return attr
    if bases:
        for i in jsrange(bases.length):
            var(base, attr)
            JS('base = bases[i]')
            attr = get_attribute(base, attribute)
            if attr:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__(JS('[object, __class__]'))
    if __class__:
        JS('var __dict__ = __class__.__dict__')
        attr = JS('__dict__[attribute]')
        if attr:
            if JS("{}.toString.call(attr) === '[object Function]'"):
                def method():
                    var(args)
                    args = arguments
                    if args.length > 0:
                        JS('args[0]').splice(0, 0, object)
                    else:
                        args = JSArray(object)
                    return attr.apply(None, args)
                return method
            return attr
        bases = __class__.bases
        for i in jsrange(bases.length):
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
    return None  # XXX: raise AttributeError instead


def set_attribute(object, attribute, value):
    """Set an attribute on an object by updating its __dict__ property"""
    var(__dict__, __class__)
    __class__  = object.__class__
    if __class__:
        var(attr, bases)
        __dict__ = __class__.__dict__
        attr = JS('__dict__[attribute]')
        if attr != None:
            __set__ = get_attribute(attr, '__set__')
            if __set__:
                __set__(JS('[object, value]'))
                return
        bases = __class__.bases
        for i in jsrange(bases.length):
            var(base)
            base = JS('bases[i]')
            attr = get_attribute(base, attribute)
            if attr:
                __set__ = get_attribute(attr, '__set__')
                if __set__:
                    __set__(JS('[object, value]'))
                    return
    __dict__ = object.__dict__
    if __dict__:
        JS('__dict__[attribute] = value')
    else:
        JS('object[attribute] = value')


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
    for i in jsrange(argslength):
        arg = JS('signature.args[j]')
        if kwargs:
            kwarg = JS('kwargs[arg]')
            if kwarg:
                JS('out[arg] = kwarg')
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


def type(args, kwargs):
    var(class_name, parents, attrs)
    class_name = JS('args[0]')
    parents = JS('args[1]')
    attrs = JS('args[2]')
    return create_class(class_name, parents, attrs)


def getattr(args, kwargs):
    var(object, attribute)
    object = JS('args[0]')
    attribute = JS('args[1]')
    return get_attribute(object, attribute)


def setattr(args, kwargs):
    var(object, attribute, value)
    object = JS('args[0]')
    attribute = JS('args[1]')
    value = JS('args[2]')
    return set_attribute(object, attribute, value)
