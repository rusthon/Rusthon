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
        if js_object:
            self.js_object = js_object
        else:
            self.js_object = JSArray()

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
        #self.js_object = JS('Object.create(null)')
        if js_object:
            self.js_object = js_object
        else:
            self.js_object = JSObject()

    def get(self, key, d):
        var(__dict)
        __dict = self.js_object
        if JS('__dict[key]'):
            return JS('__dict[key]')
        return d

    def set(self, key, value):
        var(__dict)
        __dict = self.js_object
        JS('__dict[key] = value')

    def __len__(self):
        var(__dict)
        __dict = self.js_object
        return JS('Object.keys(__dict).length')

    def keys(self):
        var(__dict, out)
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')
        out = list()
        out.js_object = __keys
        return out

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


class str:

    def __init__(self, jsstring):
        self.jsstring = jsstring

    def __iter__(self):
        return Iterator(self.jsstring, 0)
