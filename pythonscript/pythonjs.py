#!/usr/bin/env python
"""
Emulate Javascript object in Python those object will be converted to their Javascript equivalent by PythonScript compiler also functions can be converted to Javascript functions but only positional arguments are converted.

At least the following doesn't work

- functions don't take keyword arguments
- args, **kwargs is not supported
- assignements support only one target
"""
import sys
from types import GeneratorType

from ast import Str
from ast import parse
from ast import NodeVisitor


class JSGenerator(NodeVisitor):

    def visit_Module(self, node):
        return '\n'.join(map(self.visit, node.body))

    def visit_TryExcept(self, node):
        out = 'try {\n'
        out += '\n'.join(map(self.visit, node.body))
        out += '\n}\n'
        out += 'catch(__exception__) {\n'
        out += '\n'.join(map(self.visit, node.handlers))
        out += '\n}\n'
        return out

    def visit_Raise(self, node):
        return 'throw %s;' % self.visit(node.type)

    def visit_ExceptHandler(self, node):
        return '\n'.join(map(self.visit, node.body))

    def visit_FunctionDef(self, node):
        args = self.visit(node.args)
        buffer = 'var %s = function(%s) {\n' % (
            node.name,
            ', '.join(args),
        )
        body = list()
        for child in node.body:
            # simple test to drop triple quote comments
            if hasattr(child, 'value'):
                if isinstance(child.value, Str):
                    continue
            if isinstance(child, GeneratorType):
                for sub in child:
                    body.append(self.visit(sub))
            else:
                body.append(self.visit(child))
        buffer += '\n'.join(body)
        buffer += '\n}\n'
        return buffer

    def visit_arguments(self, node):
        out = []
        for name in [self.visit(arg) for arg in node.args]:
            out.append(name)
        return out

    def visit_Name(self, node):
        if node.id == 'None':
            return 'undefined'
        if node.id == 'True':
            return 'true'
        if node.id == 'False':
            return 'false'
        return node.id

    def visit_Attribute(self, node):
        name = self.visit(node.value)
        attr = node.attr
        return '%s.%s' % (name, attr)

    def visit_Print(self, node):
        args = [self.visit(e) for e in node.values]
        s = 'console.log(%s);' % ', '.join(args)
        return s

    def visit_keyword(self, node):
        if isinstance(node.arg, basestring):
            return node.arg, self.visit(node.value)
        return self.visit(node.arg), self.visit(node.value)

    def visit_Call(self, node):
        name = self.visit(node.func)
        if name == 'JSObject':
            if node.keywords:
                kwargs = map(self.visit, node.keywords)
                f = lambda x: '"%s": %s' % (x[0], x[1])
                out = ', '.join(map(f, kwargs))
            else:
                out = ''
            return '{%s}' % out
        if name == 'var':
            args = map(self.visit, node.args)
            out = ', '.join(args)
            return 'var %s' % out
        if name == 'JSArray':
            if node.args:
                args = map(self.visit, node.args)
                out = ', '.join(args)
            else:
                out = ''
            return 'create_array(%s)' % out
        elif name == 'JS':
            return node.args[0].s
        else:
            if node.args:
                args = [self.visit(e) for e in node.args]
                args = ', '.join(args)
            else:
                args = ''
            return '%s(%s)' % (name, args)

    def visit_While(self, node):
        body = '\n'.join(map(self.visit, node.body))
        return 'while(%s) {\n%s\n}' % (self.visit(node.test), body)

    def visit_Str(self, node):
        return '"%s"' % node.s

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return '%s %s %s' % (left, op, right)

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

    def visit_Assign(self, node):
        target = self.visit(node.targets[0])  # XXX: support only one target
        value = self.visit(node.value)
        code = '%s = %s;' % (target, value)
        return code

    def visit_Expr(self, node):
        # XXX: this is UGLY
        s = self.visit(node.value)
        if not s.endswith(';'):
            s += ';'
        return s

    def visit_Return(self, node):
        if node.value:
            return 'return %s;' % self.visit(node.value)
        return 'return undefined;'

    def visit_Pass(self, node):
        return ''

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Num(self, node):
        return str(node.n)

    def visit_Is(self, node):
        return '==='

    def visit_Compare(self, node):
        left = self.visit(node.left)
        ops = self.visit(node.ops[0])
        comparator = self.visit(node.comparators[0])
        return '%s %s %s' % (left, ops, comparator)

    def visit_Not(self, node):
        return '!'

    def visit_UnaryOp(self, node):
        return self.visit(node.op) + self.visit(node.operand)

    def visit_If(self, node):
        test = self.visit(node.test)
        body = '\n'.join(map(self.visit, node.body)) + '\n'
        orelse = '\n'.join(map(self.visit, node.orelse)) + '\n'
        if orelse:
            return 'if(%s) {\n%s}\nelse {\n%s}\n' % (test, body, orelse)
        return 'if(%s) {\n%s}\n' % (test, body)

    def visit_For(self, node):
        target = node.target.id
        iter = self.visit(node.iter)
        # iter is the python iterator
        init_iter = 'var iter = %s;\n' % iter
        # backup iterator and affect value of the next element to the target
        pre = 'var backup = %s;\n%s = iter[%s];\n' % (target, target, target)
        # replace the replace target with the javascript iterator
        post = '%s = backup;\n' % target
        body = '\n'.join(map(self.visit, node.body)) + '\n'
        body = pre + body + post
        for_block = init_iter + 'for (var %s=0; %s < iter.length; %s++) {\n%s}\n' % (target, target, target, body)
        return for_block


def main():
    input = parse(sys.stdin.read())
    tree = parse(input)
    print JSGenerator().visit(tree)


if __name__ == '__main__':
    main()
