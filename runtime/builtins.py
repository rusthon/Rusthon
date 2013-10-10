from pythonjs import JS
from pythonjs import var
from pythonjs import JSArray
from pythonjs import JSObject


def range(num):
    """Emulates Python's range function"""
    var(i, r)
    i = 0
    r = list()
    while i < num:
        r.append(i)
        i += 1
    return r


class StopIteration:
    pass


def len(obj):
    return obj.__len__()


def next(obj):
    return obj.next()


def map(func, objs):
    out = list()
    out.js_object = map(func, objs.js_object)
    return out


class Iterator:

    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def next(self):
        index = self.index
        length = len(self.obj)
        if index == length:
            raise StopIteration
        item = self.obj.get(self.index)
        self.index = self.index + 1
        return item



class tuple:
    def __init__(self, js_object=None):
        self.js_object = JSArray()
        if JS('js_object instanceof Array'):
            arr = self.js_object
            i = 0; length = JS('js_object.length')
            while i < length:
                JS('arr.push( js_object[i] )')
                i += 1
        elif js_object:
            raise TypeError

    def __getitem__(self, index):
        __array = self.js_object
        return JS('__array[index]')

    def __iter__(self):
        return Iterator(self, 0)

    def __len__(self):
        var(__array)
        __array = self.js_object
        return JS('__array.length')

    def index(self, obj):
        __array = self.js_object
        return JS('__array.indexOf(obj)')

    def count(self, obj):
        i = 0
        for other in self:
            if other == obj:
                i = i + 1
        return i

    def get(self, index): ## used by Iterator
        __array = self.js_object
        return JS('__array[index]')

class list:

    def __init__(self, js_object=None):
        if js_object:
            self.js_object = js_object
        else:
            self.js_object = JSArray()

    def __getitem__(self, index):
        __array = self.js_object
        return JS('__array[index]')

    def __setitem__(self, index, value):
        __array = self.js_object
        JS('__array[index] = value')

    def append(self, obj):
        var(__array)
        __array = self.js_object
        JS('__array.push(obj)')

    def extend(self, other):
        for obj in other:
            self.append(obj)

    def insert(self, index, obj):
        var(__array)
        __array = self.js_object
        JS('__array.splice(index, 0, obj)')

    def remove(self, obj):
        var(__array)
        index = self.index(obj)
        __array = self.js_object
        JS('__array.splice(index, 1)')

    def pop(self):
        var(__array)
        __array = self.js_object
        return JS('__array.pop()')

    def index(self, obj):
        var(__array)
        __array = self.js_object
        return JS('__array.indexOf(obj)')

    def count(self, obj):
        i = 0
        for other in self:
            if other == obj:
                i = i + 1
        return i

    def reverse(self):
        var(__array)
        __array = self.js_object
        self.js_object = JS('__array.reverse()')

    def shift(self):
        var(__array)
        __array = self.js_object
        return JS('__array.shift()')

    def slice(self, start, end):
        var(__array)
        __array = self.js_object
        return JS('__array.slice(start, end)')

    def __iter__(self):
        return Iterator(self, 0)

    def get(self, index):
        var(__array)
        __array = self.js_object
        return JS('__array[index]')

    def set(self, index, value):
        var(__array)
        __array = self.js_object
        JS('__array[index] = value')

    def __len__(self):
        var(__array)
        __array = self.js_object
        return JS('__array.length')


class dict:
    # http://stackoverflow.com/questions/10892322/javascript-hashtable-use-object-key
    # using a function as a key is allowed, but would waste memory because it gets converted to a string
    # http://stackoverflow.com/questions/10858632/are-functions-valid-keys-for-javascript-object-properties
    UID = 0
    def __init__(self, js_object=None):
        if js_object:
            if JS("js_object instanceof Array"):
                self.js_object = JS('Object.create(null)')
                i = 0
                while i < js_object.length:
                    JS('var key = js_object[i]["key"]')
                    JS('var value = js_object[i]["value"]')
                    self.set(key, value)
                    i += 1
            else:
                self.js_object = js_object
        else:
            self.js_object = JSObject()

    def get(self, key, _default=None):
        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            JS('var uid = "@"+key.uid') ## gotcha - what if "@undefined" was in __dict ?
            if JS('uid in __dict'):
                return JS('__dict[uid]')
        elif JS("typeof(key) === 'function'"):
            JS('var uid = "@"+key.uid')
            if JS('uid in __dict'):
                return JS('__dict[uid]')
        else:
            if JS('key in __dict'):
                return JS('__dict[key]')

        return _default

    def set(self, key, value):
        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            if JS("key.uid === undefined"):
                uid = self.UID
                JS("key.uid = uid")
                self.UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        elif JS("typeof(key) === 'function'"):
            if JS("key.uid === undefined"):
                uid = self.UID
                JS("key.uid = uid")
                self.UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        else:
            JS('__dict[key] = value')

    def __len__(self):
        __dict = self.js_object
        return JS('Object.keys(__dict).length')

    def __getitem__(self, key):
        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            JS('var uid = key.uid')
            return JS('__dict["@"+uid]')  ## "@" is needed so that integers can also be used as keys
        elif JS("typeof(key) === 'function'"):
            JS('var uid = key.uid')
            return JS('__dict["@"+uid]')  ## "@" is needed so that integers can also be used as keys
        else:
            return JS('__dict[key]')

    def __setitem__(self, key, value):
        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            if JS("key.uid === undefined"):
                uid = self.UID
                JS("key.uid = uid")
                self.UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        elif JS("typeof(key) === 'function'"):
            if JS("key.uid === undefined"):
                uid = self.UID
                JS("key.uid = uid")
                self.UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        else:
            JS('__dict[key] = value')

    def keys(self):
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')
        out = list()
        out.js_object = __keys
        return out

    def values(self):
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')
        out = list()
        i = 0
        while i < __keys.length:
            out.append( JS('__dict[ __keys[i] ]') )
            i += 1
        return out


class str:

    def __init__(self, jsstring):
        self.jsstring = jsstring

    def __iter__(self):
        return Iterator(self.jsstring, 0)


class array:
    ## note that class-level dicts can only be used after the dict class has been defined above
    typecodes = {
        'c': 1, # char
        'b': 1, # signed char
        'B': 1, # unsigned char
        'u': 2, # unicode
        'h': 2, # signed short
        'H': 2, # unsigned short
        'i': 4, # signed int
        'I': 4, # unsigned int
        'l': 4, # signed long
        'L': 4, # unsigned long
        'f': 4, # float
        'd': 8, # double
    }
    typecode_names = {
        'c': 'Int8',
        'b': 'Int8',
        'B': 'Uint8',
        'u': 'Uint16',
        'h': 'Int16',
        'H': 'Uint16',
        'i': 'Int32',
        'I': 'Uint32',
        #'l': 'TODO',
        #'L': 'TODO',
        'f': 'Float32',
        'd': 'Float64'
    }
    def __init__(self, typecode, initializer=None, little_endian=False):
        self.typecode = typecode
        self.little_endian = little_endian
        size = 0
        if initializer:
            length = len(initializer)
            print 'array.initalizer length', length
            print 'array.typecode', typecode
            print 'array.type size', self.typecodes[ typecode ]
            size = length * self.typecodes[ typecode ]
        else: size = 0
        self.size = size
        print 'array.init bytes', size
        buff = JS('new ArrayBuffer(size)')
        self.dataview = JS('new DataView(buff)')
        self.buffer = buff
        self.fromlist( initializer )

    def fromlist(self, lst):
        print 'array.fromlist->', lst
        length = len(lst)
        step = self.typecodes[ self.typecode ]
        size = length * step

        dataview = self.dataview
        func_name = 'set'+self.typecode_names[ self.typecode ]
        print 'func name->', func_name
        func = JS('dataview[func_name].bind(dataview)')
        print 'func->', func
        if size <= self.size:
            i = 0; offset = 0
            while i < length:
                item = lst[i]
                print '  item->', item
                print '  index', i
                print '  offset', offset
                #JS('func.apply(dataview, [offset, item])')
                #JS('func.call(dataview, offset, item)')
                JS('func(offset,item)')
                offset += step
                i += 1
        else:
            raise TypeError

    def __getitem__(self, index):
        step = self.typecodes[ self.typecode ]
        offset = step * index

        dataview = self.dataview
        func_name = 'get'+self.typecode_names[ self.typecode ]
        func = JS('dataview[func_name].bind(dataview)')

        if offset < self.size:
            return JS('func(offset)')
        else:
            raise IndexError

    def __setitem__(self, index, value):
        step = self.typecodes[ self.typecode ]
        offset = step * index

        dataview = self.dataview
        func_name = 'set'+self.typecode_names[ self.typecode ]
        func = JS('dataview[func_name].bind(dataview)')

        if offset < self.size:
            JS('func(offset, value)')
        else:
            raise IndexError
