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
        'float32':4,
        'float16':2,
        'float8' :1,
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
        'float8' : 'Int8'
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
