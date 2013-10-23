#!/usr/bin/env python
import sys
from types import GeneratorType

from ast import Str
from ast import Name
from ast import Tuple
from ast import parse
from ast import Attribute
from ast import NodeVisitor


class JSGenerator(NodeVisitor):
    def visit_In(self, node):
        return ' in '

    def visit_AugAssign(self, node):
        a = '%s %s= %s' %(self.visit(node.target), self.visit(node.op), self.visit(node.value))
        return a

    def visit_Module(self, node):
        return '\n'.join(map(self.visit, node.body))

    def visit_Tuple(self, node):
        return '[%s]' % ', '.join(map(self.visit, node.elts))

    def visit_List(self, node):
        return '[%s]' % ', '.join(map(self.visit, node.elts))

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

    def visit_Yield(self, node):
        return 'yield %s' % self.visit(node.value)

    def visit_ImportFrom(self, node):
        # print node.module
        # print node.names[0].name
        # print node.level
        return ''

    def visit_ExceptHandler(self, node):
        out = ''
        if node.type:
            out = 'if (__exception__ == %s || isinstance([__exception__, %s])) {\n' % (self.visit(node.type), self.visit(node.type))
        if node.name:
            out += 'var %s = __exception__;\n' % self.visit(node.name)
        out += '\n'.join(map(self.visit, node.body)) + '\n'
        if node.type:
            out += '}\n'
        return out

    def visit_Lambda(self, node):
        args = [self.visit(a) for a in node.args.args]
        return '(function (%s) {%s})' %(','.join(args), self.visit(node.body))


    def visit_FunctionDef(self, node):
        if not hasattr(self, '_function_stack'):  ## track nested functions ##
            self._function_stack = []

        self._function_stack.append( node.name )

        args = self.visit(node.args)
        buffer = 'var %s = function(%s) {\n' % (
            node.name,
            ', '.join(args),
        )
        body = list()
        for child in node.body:
            # simple test to drop triple quote comments
            #if hasattr(child, 'value'):
            #    if isinstance(child.value, Str):
            #        continue
            if isinstance(child, Str):
                continue

            if isinstance(child, GeneratorType):
                for sub in child:
                    body.append(self.visit(sub))
            else:
                body.append(self.visit(child))
        buffer += '\n'.join(body)
        buffer += '\n}\n'

        if node.name == self._function_stack[0]:  ## to be safe do not export nested functions
            buffer += 'window["%s"] = %s \n' % (node.name, node.name)  ## export to global namespace so Closure will not remove them

        assert node.name == self._function_stack.pop()
        return buffer

    def visit_Subscript(self, node):
        return '%s[%s]' % (self.visit(node.value), self.visit(node.slice.value))

    def visit_arguments(self, node):
        out = []
        for name in [self.visit(arg) for arg in node.args]:
            out.append(name)
        return out

    def visit_Name(self, node):
        if node.id == 'None':
            return 'undefined'
        elif node.id == 'True':
            return 'true'
        elif node.id == 'False':
            return 'false'
        elif node.id == 'null':
            return 'null'
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
        if name == 'instanceof':  ## this gets used by "with javascript:" blocks to test if an instance is a JavaScript type
            args = map(self.visit, node.args)
            if len(args) == 2:
                return '%s instanceof %s' %tuple(args)
            else:
                raise SyntaxError( args )

        #elif name == 'new':
        #    args = map(self.visit, node.args)
        #    if len(args) == 1:
        #        return ' new %s' %args[0]
        #    else:
        #        raise SyntaxError( args )

        elif name == 'JSObject':
            if node.keywords:
                kwargs = map(self.visit, node.keywords)
                f = lambda x: '"%s": %s' % (x[0], x[1])
                out = ', '.join(map(f, kwargs))
                return '{%s}' % out
            else:
                return 'Object()'
        elif name == 'var':
            args = map(self.visit, node.args)
            out = ', '.join(args)
            return 'var %s' % out
        elif name == 'JSArray':
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
                args = ', '.join([e for e in args if e])
            else:
                args = ''
            return '%s(%s)' % (name, args)

    def visit_While(self, node):
        body = '\n'.join(map(self.visit, node.body))
        return 'while(%s) {\n%s\n}' % (self.visit(node.test), body)

    def visit_Str(self, node):
        return '"%s"' % node.s.replace('\n', '\\n')

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return '%s %s %s' % (left, op, right)

    def visit_Mult(self, node):
        return '*'

    def visit_Add(self, node):
        return '+'

    def visit_Sub(self, node):
        return '-'

    def visit_Div(self, node):
        return '/'

    def visit_Mod(self, node):
        return '%'

    def visit_Lt(self, node):
        return '<'

    def visit_Gt(self, node):
        return '>'

    def visit_GtE(self, node):
        return '>='

    def visit_LtE(self, node):
        return '<='

    def visit_LShift(self, node):
        return '<<'
    def visit_RShift(self, node):
        return '>>'
    def visit_BitXor(self, node):
        return '^'
    def visit_BitOr(self, node):
        return '|'
    def visit_BitAnd(self, node):
        return '&'


    def visit_Assign(self, node):
        # XXX: I'm not sure why it is a list since, mutiple targets are inside a tuple
        target = node.targets[0]
        if isinstance(target, Tuple):
            raise NotImplementedError
        else:
            target = self.visit(target)
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
        if isinstance(node.value, Tuple):
            return 'return [%s];' % ', '.join(map(self.visit, node.value.elts))
        if node.value:
            return 'return %s;' % self.visit(node.value)
        return 'return undefined;'

    def visit_Pass(self, node):
        return '/*pass*/'

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Num(self, node):
        return str(node.n)

    def visit_Is(self, node):
        return '==='

    def visit_Compare(self, node):
        comp = [ self.visit(node.left) ]
        for i in range( len(node.ops) ):
            comp.append( self.visit(node.ops[i]) )
            comp.append( self.visit(node.comparators[i]) )
        return ' '.join( comp )

    def visit_Not(self, node):
        return '!'

    def visit_IsNot(self, node):
        return '!=='

    def visit_UnaryOp(self, node):
        return self.visit(node.op) + self.visit(node.operand)


    def visit_And(self, node):
        return ' && '

    def visit_Or(self, node):
        return ' || '

    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        return op.join( [self.visit(v) for v in node.values] )

    def visit_If(self, node):
        test = self.visit(node.test)
        body = '\n'.join(map(self.visit, node.body)) + '\n'
        orelse = '\n'.join(map(self.visit, node.orelse)) + '\n'
        if not orelse.isspace():
            return 'if(%s) {\n%s}\nelse {\n%s}\n' % (test, body, orelse)
        return 'if(%s) {\n%s}\n' % (test, body)

    def visit_Dict(self, node):
        a = []
        for i in range( len(node.keys) ):
            k = self.visit( node.keys[ i ] )
            v = self.visit( node.values[i] )
            a.append( '%s:%s'%(k,v) )
        b = ','.join( a )
        return '{ %s }' %b


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

    def visit_Continue(self, node):
        return 'continue'


def main(script):
    input = parse(script)
    tree = parse(input)
    return JSGenerator().visit(tree)


def command():
    print( main(sys.stdin.read()) )

if __name__ == '__main__':
    command()
