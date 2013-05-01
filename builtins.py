def range(num):
    """Emulates Python's range function"""
    JS('var i')
    JS('var r')
    i = 0
    r = list()
    while i < num:
        r.append(i)
        i = i + 1
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


class list:

    def __init__(self):
        self.js_object = JSArray()

    def append(self, obj):
        JS('var __array')
        __array = self.js_object
        JS('__array.push(obj)')

    def extend(self, other):
        for obj in other:
            self.append(obj)

    def insert(self, index, obj):
        JS('var __array')
        __array = self.js_object
        JS('__array.splice(index, 0, obj)')

    def remove(self, obj):
        JS('var __array')
        index = self.index(obj)
        __array = self.js_object
        JS('__array.splice(index, 1)')

    def pop(self):
        JS('var __array')
        __array = self.js_object
        return JS('__array.pop()')

    def index(self, obj):
        JS('var __array')
        __array = self.js_object
        return JS('__array.indexOf(obj)')

    def count(self, obj):
        i = 0
        for other in self:
            if other == obj:
                i = i + 1
        return i

    def reverse(self):
        JS('var __array')
        __array = self.js_object
        self.js_object = JS('__array.reverse()')

    def shift(self):
        JS('var __array')
        __array = self.js_object
        return JS('__array.shift()')

    def slice(self, start, end):
        JS('var __array')
        __array = self.js_object
        return JS('__array.slice(start, end)')

    def __iter__(self):
        return Iterator(self, 0)

    def get(self, index):
        JS('var __array')
        __array = self.js_object
        return JS('__array[index]')

    def set(self, index, value):
        JS('var __array')
        __array = self.js_object
        JS('__array[index] = value')

    def __len__(self):
        JS('var __array')
        __array = self.js_object
        return JS('__array.length')


class dict:

    def __init__(self):
        self.js_object = JSObject()

    def get(self, key, d):
        JS('var __dict')
        __dict = self.js_object
        if JS('__dict[key]'):
            return JS('__dict[key]')
        return d

    def set(self, key, value):
        JS('var __dict')
        __dict = self.js_object
        JS('__dict[key] = value')

    def __len__(self):
        JS('var __dict')
        __dict = self.js_object
        return JS('Object.keys(__dict).length')

    def keys(self):
        JS('var __dict')
        __dict = self.js_object
        __keys = JS('Object.keys(__dict)')
        JS('var out')
        out = list()
        out.js_object = __keys
        return out


class str(list):

    def __init__(self, jsstring):
        list.__init__(self)
        var(char)
        for i in range(JS('jsstring.length')):
            char = JS('jsstring.charAt(i)')
            self.append(char)
