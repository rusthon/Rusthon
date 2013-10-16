from pythonjs import JS
from pythonjs import var
from pythonjs import Array
from pythonjs import JSObject
from pythonjs import arguments


def jsrange(num):
    """Emulates Python's range function"""
    var(i, r)
    i = 0
    r = []
    while i < num:
        r.push(i)
        i = i + 1
    return r


def create_array():
    """Used to fix a bug/feature of Javascript where new Array(number)
    created a array with number of undefined elements which is not
    what we want"""
    var(array)
    array = []
    for i in jsrange(arguments.length):
        array.push(arguments[i])
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
        return metaclass([class_name, parents, attrs])
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
    __call__.pythonscript_function = True
    klass.__call__ = __call__
    return klass


def get_attribute(object, attribute):
    """Retrieve an attribute, method, property, or wrapper function.

    method are actually functions which are converted to methods by
    prepending their arguments with the current object. Properties are
    not functions!

    DOM support:
        http://stackoverflow.com/questions/14202699/document-createelement-not-working
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof

    Direct JavaScript Calls:
        if an external javascript function is found, and it was not a wrapper that was generated here,
        check the function for a 'cached_wrapper' attribute, if none is found then generate a new
        wrapper, cache it on the function, and return the wrapper.
    """
    if attribute == '__call__':
        if JS("{}.toString.call(object) === '[object Function]'"):
            if JS("object.pythonscript_function === true"):
                return object
            elif JS("object.is_wrapper !== undefined"):
                return object
            else:
                JS("var cached = object.cached_wrapper")
                if cached:
                    return cached
                else:
                    def wrapper(args,kwargs): return object.apply(None, args)
                    wrapper.is_wrapper = True
                    object.cached_wrapper = wrapper
                    return wrapper

    var(attr)
    attr = object[attribute]

    if JS("object instanceof HTMLDocument"):
        #print 'DYNAMIC wrapping HTMLDocument'
        if JS("typeof(attr) === 'function'"):
            def wrapper(args,kwargs): return attr.apply(object, args)
            wrapper.is_wrapper = True
            return wrapper
        else:
            return attr
    elif JS("object instanceof HTMLElement"):
        #print 'DYNAMIC wrapping HTMLElement'
        if JS("typeof(attr) === 'function'"):
            def wrapper(args,kwargs): return attr.apply(object, args)
            wrapper.is_wrapper = True
            return wrapper
        else:
            return attr
        
    if attr is not None:  ## what about cases where attr is None?
        if JS("typeof(attr) === 'function' && attr.pythonscript_function === undefined && attr.is_wrapper === undefined"):
            ## to avoid problems with other generated wrapper funcs not marked with:
            ## F.pythonscript_function or F.is_wrapper, we could check if object has these props:
            ## bases, __name__, __dict__, __call__
            #print 'wrapping something external', object, attribute

            def wrapper(args,kwargs): return attr.apply(object, args)  ## THIS IS CORRECT
            #def wrapper(args,kwargs): return attr.call(object, args)  ## this is not correct
            wrapper.is_wrapper = True
            return wrapper
        else:
            return attr

    var(__class__, __dict__, __get__, bases)

    # Check object.__class__.__dict__ for data descriptors named attr
    __class__ = object.__class__
    if __class__:
        __dict__ = __class__.__dict__
        attr = __dict__[attribute]
        if attr:
            __get__ = get_attribute(attr, '__get__')
            if __get__:
                return __get__([object, __class__])
        bases = __class__.bases
        for i in jsrange(bases.length):
            var(base, attr)
            base = bases[i]
            attr = get_attribute(base, attribute)
            if attr:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__([object, __class__])
    # Check object.__dict__ for attr and its bases if it a class
    # in the case if the descriptor is found return it
    __dict__ = object.__dict__
    bases = object.__bases__
    if __dict__:
        attr = __dict__[attribute]
        if attr != None:
            if bases:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__([None, __class__])
            return attr

    if bases:
        for i in jsrange(bases.length):
            var(base, attr)
            base = bases[i]
            attr = get_attribute(base, attribute)
            if attr:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__([object, __class__])

    if __class__:
        var(__dict__)
        __dict__ = __class__.__dict__
        attr = __dict__[attribute]
        if attr:
            if JS("{}.toString.call(attr) === '[object Function]'"):
                def method():
                    var(args)
                    args = arguments
                    if args.length > 0:
                        args[0].splice(0, 0, object)
                    else:
                        args = [object]
                    return attr.apply(None, args)
                method.is_wrapper = True
                return method
            else:
                return attr

        bases = __class__.bases
        for i in jsrange(bases.length):
            var(base, attr)
            base = bases[i]
            attr = get_attribute(base, attribute)
            if attr:
                if JS("{}.toString.call(attr) === '[object Function]'"):
                    def method():
                        var(args)
                        args = arguments
                        if(args.length > 0):
                            args[0].splice(0, 0, object)
                        else:
                            args = [object]
                        return attr.apply(None, args)
                    method.is_wrapper = True
                    return method
                else:
                    return attr

    if JS('object instanceof Array'):
        if attribute == '__getitem__':
            def wrapper(args,kwargs): return object[ args[0] ]
            wrapper.is_wrapper = True
            return wrapper
        elif attribute == '__setitem__':
            def wrapper(args,kwargs): object[ args[0] ] = args[1]
            wrapper.is_wrapper = True
            return wrapper

    elif attribute == '__getitem__':  ## this should be a JSObject - or anything else - is this always safe?
        def wrapper(args,kwargs): return object[ args[0] ]
        wrapper.is_wrapper = True
        return wrapper
    elif attribute == '__setitem__':
        def wrapper(args,kwargs): object[ args[0] ] = args[1]
        wrapper.is_wrapper = True
        return wrapper

    return None  # XXX: raise AttributeError instead


def set_attribute(object, attribute, value):
    """Set an attribute on an object by updating its __dict__ property"""
    var(__dict__, __class__)
    __class__ = object.__class__
    if __class__:
        var(attr, bases)
        __dict__ = __class__.__dict__
        attr = __dict__[attribute]
        if attr != None:
            __set__ = get_attribute(attr, '__set__')
            if __set__:
                __set__([object, value])
                return
        bases = __class__.bases
        for i in jsrange(bases.length):
            var(base)
            base = bases[i]
            attr = get_attribute(base, attribute)
            if attr:
                __set__ = get_attribute(attr, '__set__')
                if __set__:
                    __set__([object, value])
                    return
    __dict__ = object.__dict__
    if __dict__:
        __dict__[attribute] = value
    else:
        object[attribute] = value
set_attribute.pythonscript_function = True


def get_arguments(signature, args, kwargs):
    """Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve
    the actual parameters.

    This will set default keyword arguments and retrieve positional arguments
    in kwargs if their called as such"""
    if args is None:
        args = []
    if kwargs is None:
        kwargs = JSObject()
    out = JSObject()
    if signature.args.length:
        argslength = signature.args.length
    else:
        argslength = 0

    if args.length > signature.args.length:
        print 'ERROR args:', args, 'kwargs:', kwargs, 'sig:', signature
        raise TypeError('function called with wrong number of arguments')

    j = 0
    while j < argslength:
        arg = JS('signature.args[j]')
        if kwargs:
            kwarg = kwargs[arg]
            #if kwarg is not None:  ## what about cases where the caller wants None
            if arg in kwargs:       ## TODO, JSObject here should be created with Object.create(null) so that the "in" test will not conflict with internal props like: "constructor", "hasOwnProperty", etc.
                out[arg] = kwarg
            elif j < args.length:
                out[arg] = args[j]
            elif arg in signature.kwargs:
                out[arg] = signature.kwargs[arg]
            else:
                print 'ERROR args:', args, 'kwargs:', kwargs, 'sig:', signature, j
                raise TypeError('function called with wrong number of arguments')
        elif j < args.length:
            out[arg] = args[j]
        elif arg in signature.kwargs:
            out[arg] = signature.kwargs[arg]
        else:
            print 'ERROR args:', args, 'kwargs:', kwargs, 'sig:', signature, j
            raise TypeError('function called with wrong number of arguments')
        j += 1

    args = args.slice(j)
    if signature.vararg:
        out[signature.vararg] = args
    if signature.varkwarg:
        out[signature.varkwarg] = kwargs
    return out
get_arguments.pythonscript_function = True

def type(args, kwargs):
    var(class_name, parents, attrs)
    class_name = args[0]
    parents = args[1]
    attrs = args[2]
    return create_class(class_name, parents, attrs)
type.pythonscript_function = True

def getattr(args, kwargs):
    var(object, attribute)
    object = args[0]
    attribute = args[1]
    return get_attribute(object, attribute)


def setattr(args, kwargs):
    var(object, attribute, value)
    object = args[0]
    attribute = args[1]
    value = args[2]
    return set_attribute(object, attribute, value)


def issubclass(args, kwargs):
    var(C, B, base)
    C = args[0]
    B = args[1]
    if C is B:
        return True
    for index in jsrange(C.bases.length):
        base = C.bases[index]
        if issubclass([base, B], JSObject()):
            return True
    return False


def isinstance(args, kwargs):
    var(object_class, object, klass)
    object = args[0]
    klass = args[1]
    object_class = object.__class__
    if object_class is None:
        return False
    return issubclass(create_array(object_class, klass))


# not part of Python, but it's here because it's easier to write
# in PythonJS

def json_to_pythonscript(json):
    var(jstype, item, output)
    jstype = JS('typeof json')
    if jstype == 'number':
        return json
    if jstype == 'string':
        return json
    if JS("Object.prototype.toString.call(json) === '[object Array]'"):
        output = list.__call__([])
        var(append)
        for item in json:
            append = get_attribute(output, 'append')
            append([json_to_pythonscript(item)])
        return output
    # else it's a map
    output = dict.__call__([])
    for key in JS('Object.keys(json)'):
        set = get_attribute(output, 'set')
        set([key, json_to_pythonscript(json[key])])
    return output
