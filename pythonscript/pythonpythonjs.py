def create_object():
    object = JSObject()
    object.__class__ = klass
    object.__dict__ = JSObject()

    init = get_attribute(object, '__init__')
    if init:
        # unamed arguments from the instantiation call
        # equivalent to arguments[1:] in python
        args = arguments.___slice(1)
        # XXX: dummy assign is to bypass a bug in pythonjs
        o = init.apply(None, args)
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
        name = toString(object)
        if name == '[object Function]':
            return object
    attr = object.___get(attribute)
    if attr:
        return attr
    __dict__ = object.__dict__
    if __dict__:
        attr = get_attribute(__dict__, attribute)
        if attr:
            return attr
    __class__ = object.__class__
    if __class__:
        __dict__ = __class__.__dict__
        attr = __dict__.___get(attribute)
        if attr:
            name = toString(attr)
            if name == '[object Function]':
                def method():
                    o = arguments.___insert(0, object)
                    r = attr.apply(None, arguments)
                    return r
                return method
            return attr
    return None


def set_attribute(object, attr, value):
    __dict__ = object.__dict__
    __dict__.___set(attr, value)
