#!/usr/bin/env python
"""
Emulate Javascript object in Python those object will be converted to their Javascript equivalent by PythonScript compiler also functions can be converted to Javascript functions but only positional arguments are converted.

At least the following doesn't work

- print(foo.bar) doesn't work
- call without statement doesn't work do always assign things
- functions don't take keyword arguments
- args, **kwargs is not supported
- assignements support only one target
"""
import sys
from ast import parse
from ast import NodeVisitor


class JSObject(dict):

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def length(self):
        return len(self)


class JSArray(list):

    def push(self, value):
        self.append(value)

    def length(self):
        return len(self)


class JSGenerator(NodeVisitor):

    def generic_visit(self, node):
        return super(JSGenerator, self).generic_visit(node)

    def visit(self, node):
        return super(JSGenerator, self).visit(node)

    def visit_Module(self, node):
        return '\n'.join(map(self.visit, node.body))

    def visit_FunctionDef(self, node):
        args = self.visit(node.args)  # FIXME: support kwargs
        buffer = 'var %s = function(%s) {\n' % (
            node.name,
            ', '.join(args),
        )
        body = map(self.visit, node.body)
        buffer += '\n'.join(body)
        buffer += '\n}\n'
        return buffer

    def visit_arguments(self, node):
        out = []
        for name in [self.visit(arg) for arg in node.args]:
            out.append(name)  # FIXME: support kwargs
        return out

    def visit_Name(self, node):
        if node.id == 'None':
            return 'undefined'
        if node.id == 'JSObject':
            return 'Object'
        if node.id == 'JSArray':
            return 'new Array'
        return node.id

    def visit_Attribute(self, node):
        name = self.visit(node.value)
        attr = node.attr
        return '%s.%s' % (name, attr)

    def visit_Print(self, node):
        args = [self.visit(e) for e in node.values]
        s = 'console.log(%s)' % ' + '.join(args)
        return s

    def visit_keyword(self, node):
        return node.arg, self.visit(node.value)

    def visit_Call(self, node):
        name = self.visit(node.func)
        if name.endswith('___get'):
            object = node.func.value.id
            arg = node.args[0].id
            return '%s[%s]' % (object, arg)
        elif name.endswith('___set'):
            object = node.func.value.id
            key = node.args[0].id
            value = node.args[1].id
            return '%s[%s] = %s' % (object, key, value)
        elif name.endswith('___insert'):
            object = node.func.value.id
            pos = node.args[0].n
            item = node.args[1].id
            return 'Array.prototype.splice.apply(%s, [%s, 0, %s])' % (object, pos, item)
        elif name.endswith('___slice'):
            object = node.func.value.id
            start = node.args[0].n
            if len(node.args) > 1:
                end = node.args[1].n
                return 'Array.prototype.slice.call(%s).slice(%s, %s)' % (object, start, end)
            return 'Array.prototype.slice.call(%s).slice(%s)' % (object, start)
        elif name == 'dict':
            kwargs = map(self.visit, node.keywords)
            f = lambda x: '"%s": %s' % (x[0], x[1])
            out = ', '.join(map(f, kwargs))
            return '{%s}' % out
        elif name == 'JS':
            return node.args[0].s
        elif name == 'toString':
            return 'Object().toString.call(%s)' % self.visit(node.args[0])
        else:
            if node.args:
                args = [self.visit(e) for e in node.args]
                args = ', '.join(args)
            else:
                args = ''
            return '%s(%s)' % (name, args)

    def visit_Str(self, node):
        return '"%s"' % node.s

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return '%s %s %s' % (left, op, right)

    def visit_Add(self, node):
        return '+'

    def visit_Assign(self, node):
        target = self.visit(node.targets[0])  # XXX: support only one target
        value = self.visit(node.value)
        code = '%s = %s' % (target, value)
        return code

    def visit_Expr(self, node):
        return self.visit(node.value) + ';'

    def visit_Return(self, node):
        return 'return %s;' % self.visit(node.value)

    def visit_Pass(self, node):
        return ''

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Num(self, node):
        return str(node.n)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        ops = self.visit(node.ops[0])
        comparator = self.visit(node.comparators[0])
        return '%s %s %s' % (left, ops, comparator)

    def visit_If(self, node):
        test = self.visit(node.test)
        body = '\n'.join(map(self.visit, node.body))
        orelse = '\n'.join(map(self.visit, node.orelse))
        if orelse:
            return 'if(%s) {\n%s}\nelse {\n%s}\n' % (test, body, orelse)
        return 'if(%s) {\n%s}\n' % (test, body)

    def visit_For(self, node):
        target = node.target.id
        num = self.visit(node.iter.args[0])
        body = '\n'.join(map(self.visit, node.body)) + '\n'
        return 'for (%s=0; %s<%s; %s++) {\n%s}\n' % (target, target, num, target, body)


def main():
    input = parse(sys.stdin.read())
    tree = parse(input)
    print JSGenerator().visit(tree)


if __name__ == '__main__':
    main()
