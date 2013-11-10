__NULL_OBJECT__ = Object.create( null )


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


#def create_class(class_name, parents, attrs, props):
#    """Create a PythonScript class"""
#    if attrs.__metaclass__:
#        var(metaclass)
#        metaclass = attrs.__metaclass__
#        attrs.__metaclass__ = None
#        return metaclass([class_name, parents, attrs])
#    var(klass)
#    klass = JSObject()
#    klass.__bases__ = parents
#    klass.__name__ = class_name
#    klass.__dict__ = attrs
#    klass.__properties__ = props
#
#    def __call__():
#        """Create a PythonScript object"""
#        JS('var object')
#        object = JSObject()
#        object.__class__ = klass
#        object.__dict__ = JSObject()
#        JS('var init')
#        init = get_attribute(object, '__init__')
#        if init:
#            init.apply(None, arguments)
#        return object
#    __call__.pythonscript_function = True
#    klass.__call__ = __call__
#    return klass


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
    #if attribute == '__contains__': ## DO NOT TOUCH Object.prototype !!
    #    attribute = '__CONTAINS__'  ## we need this ugly hack because we have added javascript Object.prototype.__contains__

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
        
    #if attribute in object:  ## in test not allowed with javascript-string
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
            __get__ = get_attribute(attr, '__get__')  ## what are data descriptors?
            if __get__:
                return __get__([object, __class__])  ## TODO - we need JSObject here?
        bases = __class__.__bases__
        for i in jsrange(bases.length):
            var(base, attr)
            base = bases[i]
            attr = get_attribute(base, attribute)
            if attr:
                __get__ = get_attribute(attr, '__get__')
                if __get__:
                    return __get__([object, __class__])  ## TODO - we need JSObject here?
    # Check object.__dict__ for attr and its bases if it a class
    # in the case if the descriptor is found return it
    __dict__ = object.__dict__
    bases = object.__bases__
    if __dict__:
        attr = __dict__[attribute]
        if attr != None:
            if bases:
                __get__ = get_attribute(attr, '__get__')  ## TODO - we need JSObject here?
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
                    return __get__([object, __class__])  ## TODO - we need JSObject here?

    if __class__:

        if attribute in __class__.__properties__:  ## @property decorators
            return __class__.__properties__[ attribute ]['get']( [object], JSObject() )

        __dict__ = __class__.__dict__
        attr = __dict__[attribute]
        #if attr:
        if attribute in __dict__:
            if JS("{}.toString.call(attr) === '[object Function]'"):
                def method():
                    var(args)
                    args =  Array.prototype.slice.call(arguments)
                    if (JS('args[0] instanceof Array') and JS("{}.toString.call(args[1]) === '[object Object]'") and args.length == 2):
                        pass
                    else:
                        # in the case where the method was submitted to javascript code
                        # put the arguments in order to be processed by PythonJS
                        args = [args, JSObject()]
                    args[0].splice(0, 0, object)
                    return attr.apply(None, args)
                method.is_wrapper = True

                object[attribute] = method  ## cache method - we assume that methods do not change

                return method
            else:
                return attr

        bases = __class__.__bases__

        for base in bases:
            attr = _get_upstream_attribute(base, attribute)
            if attr:
                if JS("{}.toString.call(attr) === '[object Function]'"):
                    def method():
                        var(args)
                        args =  Array.prototype.slice.call(arguments)
                        if (JS('args[0] instanceof Array') and JS("{}.toString.call(args[1]) === '[object Object]'") and args.length == 2):
                            pass
                        else:
                            # in the case where the method was submitted to javascript code
                            # put the arguments in order to be processed by PythonJS
                            args = [args, JSObject()]

                        args[0].splice(0, 0, object)
                        return attr.apply(None, args)
                    method.is_wrapper = True

                    object[attribute] = method  ## cache method - we assume that methods do not change

                    return method
                else:
                    return attr

        for base in bases:  ## upstream property getters come before __getattr__
            var( prop )
            prop = _get_upstream_property(base, attribute)
            if prop:
                return prop['get']( [object], JSObject() )

        if '__getattr__' in __dict__:
            return __dict__['__getattr__']( [object, attribute], JSObject() )

        for base in bases:
            var( f )
            f = _get_upstream_attribute(base, '__getattr__')
            if f:
                return f( [object, attribute], JSObject() )


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

def _get_upstream_attribute(base, attr):
    if attr in base.__dict__:
        return base.__dict__[ attr ]
    for parent in base.__bases__:
        return _get_upstream_attribute(parent, attr)

def _get_upstream_property(base, attr):
    if attr in base.__properties__:
        return base.__properties__[ attr ]
    for parent in base.__bases__:
        return _get_upstream_property(parent, attr)

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
        bases = __class__.__bases__
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

##set_attribute.pythonscript_function = True  ## let this get wrapped


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

    # if the caller did not specify supplemental positional arguments e.g. *args in the signature
    # raise an error
    if args.length > signature.args.length:
        if signature.vararg:
            pass
        else:
            print 'ERROR args:', args, 'kwargs:', kwargs, 'sig:', signature
            raise TypeError("Supplemental positional arguments provided but signature doesn't accept them")

    j = 0
    while j < signature.args.length:
        name = signature.args[j]
        if name in kwargs:
            # value is provided as a keyword argument
            out[name] = kwargs[name]
        elif j < args.length:
            # value is positional and within the signature length
            out[name] = args[j]
        elif name in signature.kwargs:
            # value is not found before and is in signature.length
            out[name] = signature.kwargs[name]
        j += 1

    args = args.slice(j)  ## note that if this fails because args is not an array, then a pythonjs function was called from javascript in a bad way.

    if signature.vararg:
        out[signature.vararg] = args
    if signature.varkwarg:
        out[signature.varkwarg] = kwargs
    return out

##get_arguments.pythonscript_function = True  ## this was not required

