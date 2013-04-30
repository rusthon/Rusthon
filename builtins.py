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
        if self.index >= len(self.obj):
            raise StopIteration
        item = self.obj[self.index]
        self.index = self.index + 1
        return item


class list:

    def __init__(self):
        self.js_object = JSArray()

    def append(self, obj):
        array = self.js_object
        JS('array.push(obj)')

    def extend(self, other):
        for obj in other:
            self.append(obj)

    def insert(self, index, obj):
        array = self.js_object
        JS('array.splice(index, 0, obj)')

    def remove(self, obj):
        index = self.index(obj)
        array = self.js_object
        JS('array.splice(index, 1)')

    def pop(self):
        array = self.js_object
        return JS('array.pop()')

    def index(self, obj):
        array = self.js_object
        return JS('array.indexOf(obj)')

    def count(self, obj):
        i = 0
        for other in self:
            if other == obj:
                i = i + 1
        return i

    def reverse(self):
        array = self.js_object
        self.js_object = JS('array.reverse()')

    def shift(self):
        array = self.js_object
        return JS('array.shift()')

    def slice(self, start, end):
        array = self.js_object
        return JS('array.slice(start, end)')

    def __iter__(self):
        return Iterator(self, 0)
