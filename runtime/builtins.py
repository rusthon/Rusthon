_PythonJS_UID = 0


with javascript:
    def _JSNew(T):
        return JS("new T")

    ## This can not be trusted because Object.hasOwnProperty will fail on an empty object with
    ## TypeError: Cannot convert object to primitive value
    ## It was not a good idea in the first place to try to use Javascript's "in" operator to
    ## test if something had an attribute, because if something was a string that throws an error
    ## note: Object.hasOwnProperty always returns false with strings and numbers.
    #def _create_empty_object(arr):
    #        o = Object.create(null)
    #        for i in arr:
    #            o[ i ] = True
    #        return o

def int(a):
    with javascript:
        if instanceof(a, String):
            return window.parseInt(a)
        else:
            return Math.round(a)

def float(a):
    with javascript:
        if instanceof(a, String):
            return window.parseFloat(a)
        else:
            return a

def str(s):
    return ''+s

def _setup_str_prototype():
    '''
    Extend JavaScript String.prototype with methods that implement the Python str API.
    The decorator @String.prototype.[name] assigns the function to the prototype,
    and ensures that the special 'this' variable will work.
    '''
    with javascript:

        @String.prototype.__getitem__
        def func(idx):
            return this[ idx ]

        @String.prototype.__len__
        def func():
            return this.length

        @String.prototype.startswith
        def func(a):
            if this.substring(0, a.length) == a:
                return True
            else:
                return False

        @String.prototype.endswith
        def func(a):
            if this.substring(this.length-a.length, this.length) == a:
                return True
            else:
                return False

        @String.prototype.join
        def func(a):
            out = ''
            if instanceof(a, Array):
                arr = a
            else:
                arr = a.__dict__.js_object
            i = 0
            for value in arr:
                out += value
                i += 1
                if i < arr.length:
                    out += this
            return out

        @String.prototype.upper
        def func():
            return this.toUpperCase()

        @String.prototype.lower
        def func():
            return this.toLowerCase()

        @String.prototype.index
        def func(a):
            return this.indexOf(a)

        @String.prototype.isdigit
        def func():
            digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for char in this:
                if char in digits: pass
                else: return False
            return True

_setup_str_prototype()

def _setup_array_prototype():

    with javascript:

        @Array.prototype.__contains__
        def func(a):
            if this.indexOf(a) == -1: return False
            else: return True

        @Array.prototype.__len__
        def func():
            return this.length

_setup_array_prototype()

#def _setup_object_prototype():  ## TODO fix code that had used with-javascript: if 'x' in ob
#
#    with javascript:
#
#        @Object.prototype.__contains__
#        def func(a):
#            if JS("a in this"):  ## JS() so that we don't call __contains__ again
#                return True
#            else:
#                return False
#
#_setup_object_prototype()  ## this is not safe with external libraries like ace.js


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

def min( lst ):
    a = None
    for value in lst:
        if a is None: a = value
        elif value < a: a = value
    return a

def max( lst ):
    a = None
    for value in lst:
        if a is None: a = value
        elif value > a: a = value
    return a

def abs( num ):
    return JS('Math.abs(num)')

def ord( char ):
    return JS('char.charCodeAt(0)')

def chr( num ):
    return JS('String.fromCharCode(num)')

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
            if isinstance( js_object, list):
                self.js_object = js_object.js_object.slice(0)
            elif isinstance( js_object, tuple):
                self.js_object = js_object.js_object.slice(0)
            elif isinstance( js_object, array):
                arr = JSArray()
                for v in js_object:
                    with javascript:
                        arr.push( v )
                self.js_object = arr
            else:
                raise TypeError
        elif js_object:
            raise TypeError

        self[...] = self.js_object  ## self.js_object is deprecated

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

    def __contains__(self, value):
        arr = self.js_object
        with javascript:
            if arr.indexOf(value) == -1:
                return False
            else:
                return True


class list:

    def __init__(self, js_object=None):
        if js_object:
            if JS('js_object instanceof Array'):
                self.js_object = js_object
            elif isinstance(js_object, list) or isinstance(js_object, tuple) or isinstance(js_object, array):
                self.js_object = JSArray()
                for v in js_object:
                    self.append( v )
            else:
                raise TypeError
        else:
            self.js_object = JSArray()

        self[...] = self.js_object  ## self.js_object is deprecated


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

    def __contains__(self, value):
        arr = self.js_object
        with javascript:
            if arr.indexOf(value) == -1:
                return False
            else:
                return True

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

        jsob = self.js_object
        with javascript:
            self[...] = jsob

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
        global _PythonJS_UID

        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            if JS("key.uid === undefined"):
                uid = _PythonJS_UID
                JS("key.uid = uid")
                _PythonJS_UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        elif JS("typeof(key) === 'function'"):
            if JS("key.uid === undefined"):
                uid = _PythonJS_UID
                JS("key.uid = uid")
                _PythonJS_UID += 1
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
        global _PythonJS_UID

        __dict = self.js_object
        if JS("typeof(key) === 'object'"):
            if JS("key.uid === undefined"):
                uid = _PythonJS_UID
                JS("key.uid = uid")
                _PythonJS_UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        elif JS("typeof(key) === 'function'"):
            if JS("key.uid === undefined"):
                uid = _PythonJS_UID
                JS("key.uid = uid")
                _PythonJS_UID += 1
            JS('var uid = key.uid')
            JS('__dict["@"+uid] = value')
        else:
            JS('__dict[key] = value')

    def keys(self):
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')  ## the problem with this is that keys are coerced into strings
        out = list()
        out.js_object = __keys
        return out

    def pop(self, key, d=None):
        v = self.get(key, None)
        if v is None:
            return d
        else:
            js_object = self.js_object
            JS("delete js_object[key]")
            return v
        

    def values(self):
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')
        out = list()
        i = 0
        while i < __keys.length:
            out.append( JS('__dict[ __keys[i] ]') )
            i += 1
        return out

    def __contains__(self, value):
        with javascript:
            keys = Object.keys(self[...])  ## the problem with this is that keys are coerced into strings
            if typeof(value) == 'object':
                key = '@'+value.uid
            else:
                key = ''+value  ## convert to string

            if keys.indexOf( key ) == -1:
                return False
            else:
                return True

# DEPRECATED - see _setup_str_prototype
#class str:
#
#    def __init__(self, jsstring):
#        self.jsstring = jsstring
#
#    def __iter__(self):
#        return Iterator(self.jsstring, 0)


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
        'float32':4,
        'float16':2,
        'float8' :1,

        'int32'  :4,
        'uint32' :4,
        'int16'  :2,
        'uint16' :2,
        'int8'  :1,
        'uint8' :1,
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
        'd': 'Float64',

        'float32': 'Float32',
        'float16': 'Int16',
        'float8' : 'Int8',

        'int32'  : 'Int32',
        'uint32' : 'Uint32',
        'int16'  : 'Int16',
        'uint16' : 'Uint16',
        'int8'   : 'Int8',
        'uint8'  : 'Uint8',

    }
    def __init__(self, typecode, initializer=None, little_endian=False):
        self.typecode = typecode
        self.itemsize = self.typecodes[ typecode ]
        self.little_endian = little_endian

        if initializer:
            self.length = len(initializer)
            self.bytes = self.length * self.itemsize

            if self.typecode == 'float8':
                self._scale = max( [abs(min(initializer)), max(initializer)] )
                self._norm_get = self._scale / 127  ## half 8bits-1
                self._norm_set = 1.0 / self._norm_get
            elif self.typecode == 'float16':
                self._scale = max( [abs(min(initializer)), max(initializer)] )
                self._norm_get = self._scale / 32767  ## half 16bits-1
                self._norm_set = 1.0 / self._norm_get

        else:
            self.length = 0
            self.bytes = 0
        
        size = self.bytes
        buff = JS('new ArrayBuffer(size)')
        self.dataview = JS('new DataView(buff)')
        self.buffer = buff
        self.fromlist( initializer )

    def __len__(self):
        return self.length

    def __contains__(self, value):
        #lst = self.to_list()
        #return value in lst  ## this old style is deprecated
        arr = self.to_array()
        with javascript:
            if arr.indexOf(value) == -1: return False
            else: return True

    def __getitem__(self, index):
        step = self.itemsize
        offset = step * index

        dataview = self.dataview
        func_name = 'get'+self.typecode_names[ self.typecode ]
        func = JS('dataview[func_name].bind(dataview)')

        if offset < self.bytes:
            value = JS('func(offset)')
            if self.typecode == 'float8':
                value = value * self._norm_get
            elif self.typecode == 'float16':
                value = value * self._norm_get
            return value
        else:
            raise IndexError

    def __setitem__(self, index, value):
        step = self.itemsize
        if index < 0: index = self.length + index -1  ## TODO fixme
        offset = step * index

        dataview = self.dataview
        func_name = 'set'+self.typecode_names[ self.typecode ]
        func = JS('dataview[func_name].bind(dataview)')

        if offset < self.bytes:
            if self.typecode == 'float8':
                value = value * self._norm_set
            elif self.typecode == 'float16':
                value = value * self._norm_set

            JS('func(offset, value)')
        else:
            raise IndexError

    def __iter__(self):
        return Iterator(self, 0)

    def get(self, index):
        return self[ index ]

    def fromlist(self, lst):
        length = len(lst)
        step = self.itemsize
        typecode = self.typecode
        size = length * step
        dataview = self.dataview
        func_name = 'set'+self.typecode_names[ typecode ]
        func = JS('dataview[func_name].bind(dataview)')
        if size <= self.bytes:
            i = 0; offset = 0
            while i < length:
                item = lst[i]
                if typecode == 'float8':
                    item *= self._norm_set
                elif typecode == 'float16':
                    item *= self._norm_set

                JS('func(offset,item)')
                offset += step
                i += 1
        else:
            raise TypeError

    def resize(self, length):
        buff = self.buffer
        source = JS('new Uint8Array(buff)')

        new_size = length * self.itemsize
        new_buff = JS('new ArrayBuffer(new_size)')
        target = JS('new Uint8Array(new_buff)')
        JS('target.set(source)')

        self.length = length
        self.bytes = new_size
        self.buffer = new_buff
        self.dataview = JS('new DataView(new_buff)')

    def append(self, value):
        length = self.length
        self.resize( self.length + 1 )
        self[ length ] = value

    def extend(self, lst):  ## TODO optimize
        for value in lst:
            self.append( value )

    def to_array(self):
        arr = JSArray()
        i = 0
        while i < self.length:
            item = self[i]
            JS('arr.push( item )')
            i += 1
        return arr

    def to_list(self):
        #return list( js_object=self.to_array() )  ## TODO fixme
        lst = list()
        lst.js_object = self.to_array()
        return lst

    def to_ascii(self):
        string = ''
        arr = self.to_array()
        i = 0; length = arr.length
        while i < length:
            JS('var num = arr[i]')
            JS('var char = String.fromCharCode(num)')
            string += char
            i += 1
        return string


# JSON stuff

def _to_pythonjs(json):
    var(jstype, item, output)
    jstype = JS('typeof json')
    if jstype == 'number':
        return json
    if jstype == 'string':
        return json
    if JS("Object.prototype.toString.call(json) === '[object Array]'"):
        output = list()
        raw = list()
        raw.js_object = json
        var(append)
        append = output.append
        for item in raw:
            append(_to_pythonjs(item))
        return output
    # else it's a map
    output = dict()
    var(set)
    set = output.set
    keys = list()
    keys.js_object = JS('Object.keys(json)')
    for key in keys:
        set(key, _to_pythonjs(JS("json[key]")))
    return output

def json_to_pythonjs(json):
    return _to_pythonjs(JSON.parse(json))

# inverse function

def _to_json(pythonjs):
    if isinstance(pythonjs, list):
        r = JSArray()
        for i in pythonjs:
            r.push(_to_json(i))
    elif isinstance(pythonjs, dict):
        var(r)
        r = JSObject()
        for key in pythonjs.keys():
            value = _to_json(pythonjs.get(key))
            key = _to_json(key)
            with javascript:
                r[key] = value
    else:
        r = pythonjs
    return r


def pythonjs_to_json(pythonjs):
    return JSON.stringify(_to_json(pythonjs))
