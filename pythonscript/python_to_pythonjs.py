#!/usr/bin/env python
import sys

from ast import Str
from ast import Expr
from ast import Call
from ast import Name
from ast import While
from ast import Assign
from ast import keyword
from ast import arguments
from ast import TryExcept
from ast import Attribute
from ast import FunctionDef

from ast import parse
from ast import NodeVisitor


class Writer(object):

    def __init__(self):
        self.level = 0
        self.buffers = list()

    def push(self):
        self.level += 1

    def pull(self):
        self.level -= 1

    def append(self, code):
        self.buffers.append(code)

    def write(self, code):
        for buffer in self.buffers:
            self._write(buffer)
        self.buffers = list()
        self._write(code)

    def _write(self, code):
        indentation = self.level * 4 * ' '
        print '%s%s' % (indentation, code)


writer = Writer()


class PythonToPythonJS(NodeVisitor):

    identifier = 0

    def visit_ClassDef(self, node):
        name = node.name
        writer.write('var(%s, __%s_attrs, __%s_parents)' % (name, name, name))
        writer.write('__%s_attrs = JSObject()' % name)
        writer.write('__%s_parents = JSArray()' % name)
        for base in node.bases:
            code = '__%s_parents.push(%s)' % (name, self.visit(base))
            writer.write(code)
        for item in node.body:
            if isinstance(item, FunctionDef):
                item_name = item.name
                item.name = '__%s_%s' % (name, item_name)
                self.visit(item)  # this will output the code for the function
                writer.write('__%s_attrs.%s = %s' % (name, item_name, item.name))
            elif isinstance(item, Assign):
                item_name = item.targets[0].id
                item.targets[0].id = '__%s_%s' % (name.id, item_name)
                self.visit(item)  # this will output the code for the assign
                writer.write('%s_attrs.%s = %s' % (name, item_name, item.targets[0].id))
        writer.write('%s = create_class("%s", __%s_parents, __%s_attrs)' % (name, name, name, name))

    def visit_If(self, node):
        writer.write('if %s:' % self.visit(node.test))
        writer.push()
        map(self.visit, node.body)
        writer.pull()
        if node.orelse:
            writer.write('else:')
            writer.push()
            map(self.visit, node.orelse)
            writer.pull()

    def visit_TryExcept(self, node):
        writer.write('try:')
        writer.push()
        map(self.visit, node.body)
        writer.pull()
        map(self.visit, node.handlers)

    def visit_Raise(self, node):
        writer.write('raise %s' % self.visit(node.type))

    def visit_ExceptHandler(self, node):
        if node.type and node.name:
            writer.write('except %s, %s:' % (self.visit(node.type), self.visit(node.name)))
        elif node.type and not node.name:
            writer.write('except %s:' % self.visit(node.type))
        else:
            writer.write('except:')
        writer.push()
        map(self.visit, node.body)
        writer.pull()

    def visit_Pass(self, node):
        writer.write('pass')

    def visit_Name(self, node):
        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def visit_Return(self, node):
        if node.value:
            return writer.write('return %s' % self.visit(node.value))
        return writer.write('return undefined')

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return '%s %s %s' % (left, op, right)

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Is(self, node):
        return 'is'

    def visit_Add(self, node):
        return '+'

    def visit_Sub(self, node):
        return '-'

    def visit_Lt(self, node):
        return '<'

    def visit_Gt(self, node):
        return '>'

    def visit_GtE(self, node):
        return '>='

    def visit_LtE(self, node):
        return '<='

    def visit_Compare(self, node):
        left = self.visit(node.left)
        ops = self.visit(node.ops[0])
        comparator = self.visit(node.comparators[0])
        return '%s %s %s' % (left, ops, comparator)

    def visit_Not(self, node):
        return ' not '

    def visit_UnaryOp(self, node):
        return self.visit(node.op) + self.visit(node.operand)

    def visit_Attribute(self, node):
        return 'get_attribute(%s, "%s")' % (self.visit(node.value), node.attr)

    def visit_Assign(self, node):
        attr = node.targets[0]
        if isinstance(attr, Attribute):
            code = 'set_attribute(%s, "%s", %s)' % (
                self.visit(attr.value),
                attr.attr,
                self.visit(node.value)
            )
            writer.write(code)
        else:
            writer.write('%s = %s' % (node.targets[0].id, self.visit(node.value)))

    def visit_Print(self, node):
        return 'print %s' % ', '.join(map(self.visit, node.values))

    def visit_Str(self, node):
        return '"%s"' % node.s

    def visit_Expr(self, node):
        writer.write(self.visit(node.value))

    def visit_Call(self, node):
        if hasattr(node.func, 'id') and node.func.id in ('JS', 'toString', 'JSObject', 'JSArray', 'var'):
            args = map(self.visit, node.args)
            kwargs = map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords)
            args.extend(kwargs)
            args = ', '.join(args)
            return '%s(%s)' % (node.func.id, args)
        else:
            args = ', '.join(map(self.visit, node.args))
            kwargs = ', '.join(map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords))
            args_name = '__args_%s' % self.identifier
            kwargs_name = '__kwargs_%s' % self.identifier
            writer.append('var(%s, %s)' % (args_name, kwargs_name))
            self.identifier += 1
            writer.append('%s = JSArray(%s)' % (args_name, args))
            if node.starargs:
                writer.append('%s.push.apply(%s, %s)' % (args_name, args_name, self.visit(node.starargs)))
            writer.append('%s = JSObject(%s)' % (kwargs_name, kwargs))
            if node.kwargs:
                kwargs = self.visit(node.kwargs)
                code = "JS('for (var name in %s) { %s[name] = %s[name]; }')" % (kwargs, kwargs_name, kwargs)
                writer.append(code)
            return 'get_attribute(%s, "__call__")(%s, %s)' % (self.visit(node.func), args_name, kwargs_name)

    def visit_FunctionDef(self, node):
        writer.write('def %s(args, kwargs):' % node.name)
        writer.push()

        # new pythonjs' python function arguments handling
        # create the structure representing the functions arguments
        # first create the defaultkwargs JSObject
        writer.write('var(signature, arguments)')
        L = len(node.args.defaults)
        kwargsdefault = map(lambda x: keyword(self.visit(x[0]), x[1]), zip(node.args.args[-L:], node.args.defaults))
        kwargsdefault = Call(
            Name('JSObject', None),
            [],
            kwargsdefault,
            None,
            None
        )
        args = Call(
            Name('JSArray', None),
            map(lambda x: Str(x.id), node.args.args),
            [],
            None,
            None
        )
        keywords = list([
            keyword(Name('kwargs', None), kwargsdefault),
            keyword(Name('args', None), args),
        ])
        if node.args.vararg:
            keywords.append(keyword(Name('vararg', None), Str(node.args.vararg)))
        if node.args.kwarg:
            keywords.append(keyword(Name('varkwarg', None), Str(node.args.kwarg)))

        prebody = list()

        # create a JS Object to store the value of each parameter
        signature = ', '.join(map(lambda x: '%s=%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
        writer.write('signature = JSObject(%s)' % signature)
        writer.write('arguments = get_arguments(signature, args, kwargs)')
        # # then for each argument assign its value
        for arg in node.args.args:
            writer.write("""JS("var %s = arguments['%s']")""" % (arg.id, arg.id))
        if node.args.vararg:
            writer.write("""JS("var %s arguments['%s']")""" % (node.args.vararg, node.args.vararg))
            # turn it into a list
            expr = '%s = get_attribute(list, "__call__")(create_array(%s), {});'
            expr = expr % (node.args.vararg, node.args.vararg)
            writer.write(expr)
        if node.args.kwarg:
            writer.write("""JS('var %s = arguments["%s"]')""" % (node.args.kwarg, node.args.kwarg))
            expr = '%s = get_attribute(dict, "__call__")(create_array(%s), {});'
            expr = expr % (node.args.kwarg, node.args.kwarg)
            writer.write(expr)

        map(self.visit, node.body)
        writer.pull()

        # apply decorators
        for decorator in reversed(node.decorator_list):
            writer.write('%s = %s(create_array(%s))' % (node.name, self.visit(decorator), node.name))

    def visit_For(self, node):
        writer.write('var(__iterator__, %s)' % node.target.id)
        writer.write('__iterator__ = get_attribute(get_attribute(%s, "__iter__"), "__call__")(JSArray(), JSObject())' % self.visit(node.iter))
        writer.write('try:')
        writer.push()
        writer.write('%s = get_attribute(__iterator__, "next")(JSArray(), JSObject())' % node.target.id)
        writer.write('while True:')
        writer.push()
        map(writer.write, map(self.visit, node.body))
        writer.write('%s = get_attribute(__iterator__, "next")(JSArray(), JSObject())' % node.target.id)
        writer.pull()
        writer.pull()
        writer.write('except StopIteration:')
        writer.push()
        writer.write('pass')
        writer.pull()
        return ''

    def visit_While(self, node):
        writer.write('while %s:' % self.visit(node.test))
        writer.push()
        map(self.visit, node.body)
        writer.pull()


def main():
    input = parse(sys.stdin.read())
    tree = parse(input)
    PythonToPythonJS().visit(tree)


if __name__ == '__main__':
    main()
