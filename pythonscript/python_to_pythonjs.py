#!/usr/bin/env python
import os, sys, pickle
from types import GeneratorType

from ast import Str
from ast import Call
from ast import Name
from ast import Tuple
from ast import Assign
from ast import keyword
from ast import Subscript
from ast import Attribute
from ast import FunctionDef

from ast import parse
from ast import NodeVisitor

if sys.version_info.major == 3:
    import io
    StringIO = io.StringIO
else:
    from cStringIO import StringIO as StringIO


class Writer(object):

    def __init__(self):
        self.level = 0
        self.buffers = list()
        self.output = StringIO()

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
        self.output.write('%s%s\n' % (indentation, code))

    def getvalue(self):
        s = self.output.getvalue()
        self.output = StringIO()
        return s

writer = Writer()

MINI_STDLIB = {
    'time': {
        'time': 'function time() { return new Date().getTime() / 1000.0; }'
    },
    'random': {
        'random': 'var random = Math.random'
    }
}
class PythonToPythonJS(NodeVisitor):

    identifier = 0

    def __init__(self, module=None, module_path=None):
        super(PythonToPythonJS, self).__init__()
        self._classes = dict()    ## class name : [method names]
        self._inline_classes = dict()  ## class name : [attribute names]
        self._catch_attributes = None
        self._names = set()
        self._instances = dict()  ## instance name : class name
        self._decorator_properties = dict()
        self._decorator_class_props = dict()

        self._module = module
        self._module_path = module_path
        assert os.path.isdir( module_path )

    def save_module(self):
        if self._module and self._module_path:
            a = dict(
                classes = self._classes,
                inline_classes = self._inline_classes,
                decorator_class_props = self._decorator_class_props,
            )
            pickle.dump( a, open(os.path.join(self._module_path, self._module+'.module'), 'wb') )

    def visit_ImportFrom(self, node):
        if node.module in MINI_STDLIB:
            for n in node.names:
                if n.name in MINI_STDLIB[ node.module ]:
                    writer.write( 'JS("%s")' %MINI_STDLIB[node.module][n.name] )

        elif self._module_path and node.module+'.module' in os.listdir(self._module_path):
            f = open( os.path.join(self._module_path, node.module+'.module'), 'rb' )
            a = pickle.load( f ); f.close()
            self._classes.update( a['classes'] )
            self._inline_classes.update( a['inline_classes'] )
            self._decorator_class_props.update( a['decorator_class_props'] )

    def visit_Assert(self, node):
        ## hijacking "assert isinstance(a,A)" as a type system ##
        if isinstance( node.test, Call ) and node.test.func.id == 'isinstance':
            a,b = node.test.args
            if b.id in self._classes:
                self._instances[ a.id ] = b.id

    def visit_Tuple(self, node):
        ## TODO how to deal with tuples
        return '(%s)' % ', '.join(map(self.visit, node.elts))

    def visit_List(self, node):
        return 'get_attribute(list, "__call__")(create_array([%s]), Object())' % ', '.join(map(self.visit, node.elts))

    def visit_In(self, node):
        return ' in '

    def visit_AugAssign(self, node):
        a = '%s %s= %s' %(self.visit(node.target), self.visit(node.op), self.visit(node.value))
        writer.write(a)

    def visit_Yield(self, node):
        return 'yield %s' % self.visit(node.value)

    def _gen_getattr_helper(self, class_name, func_name):
        '''
        This helper is used to emulate how Python works, __getattr__ is only supposed
        to be called when the attribute is not found on the instance.
        '''
        a = [
            'def __%s____getattr_helper(args, kwargs):' %class_name,
            '  var(signature, arguments)',
            '  signature = JSObject(kwargs=JSObject(), args=JSArray("self", "name"))',
            '  arguments = get_arguments(signature, args, kwargs)',
            '''  JS("var self = arguments['self']")''',
            '''  JS("var name = arguments['name']")''',
            '  if name in get_attribute(self, "__dict__"):',
            '    return get_attribute(getattr, "__call__")( JSArray(self,name), JSObject() )',
            '  else:',
            '    return %s( [self, name] )' %func_name
        ]
        return '\n'.join(a)

    def visit_ClassDef(self, node):
        name = node.name
        self._classes[ name ] = list()  ## method names
        self._catch_attributes = None
        self._decorator_properties = dict() ## property names :  {'get':func, 'set':func}
        self._decorator_class_props[ name ] = self._decorator_properties
        self._instances[ 'self' ] = name

        for dec in node.decorator_list:
            if isinstance(dec, Name) and dec.id == 'inline':
                self._catch_attributes = set()

        writer.write('var(%s, __%s_attrs, __%s_parents)' % (name, name, name))
        writer.write('__%s_attrs = JSObject()' % name)
        writer.write('__%s_parents = JSArray()' % name)
        for base in node.bases:
            code = '__%s_parents.push(%s)' % (name, self.visit(base))
            writer.write(code)
        for item in node.body:
            if isinstance(item, FunctionDef):
                self._classes[ name ].append( item.name )
                item_name = item.name
                item.original_name = item.name
                item.name = '__%s_%s' % (name, item_name)

                self.visit(item)  # this will output the code for the function

                if item_name in self._decorator_properties:
                    pass
                else:
                    writer.write('__%s_attrs["%s"] = %s' % (name, item_name, item.name))

                if item_name == '__getattr__':
                    writer.write( self._gen_getattr_helper(name, item.name) )

            elif isinstance(item, Assign):
                item_name = item.targets[0].id
                item.targets[0].id = '__%s_%s' % (name.id, item_name)
                self.visit(item)  # this will output the code for the assign
                writer.write('%s_attrs["%s"] = %s' % (name, item_name, item.targets[0].id))

        if self._catch_attributes:
            self._inline_classes[ name ] = self._catch_attributes

        self._catch_attributes = None
        self._decorator_properties = None
        self._instances.pop('self')

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
        name = self.visit(node.value)
        if name in self._instances:  ## support '.' operator overloading
            klass = self._instances[ name ]
            if '__getattr__' in self._classes[ klass ]:
                if klass in self._inline_classes:  ## static attribute
                    if node.attr in self._inline_classes[klass]:
                        #return '''JS('%s.__dict__["%s"]')''' %(name, node.attr)  ## this is not ClosureCompiler compatible
                        return '''JS('%s["__dict__"]["%s"]')''' %(name, node.attr)
                    elif node.attr in self._classes[ klass ]: ## method
                        return '''JS('__%s_attrs["%s"]')''' %(klass, node.attr)
                    elif klass in self._decorator_class_props and node.attr in self._decorator_class_props[klass]:
                        getter = self._decorator_class_props[klass][node.attr]['get']
                        return '''JS('%s( [%s] )')''' %(getter, name)
                    else:
                        return '''JS('__%s___getattr__( [%s, "%s"] )')''' %(klass, name, node.attr)

                else:  ## dynamic python style
                    return '__%s____getattr_helper( [%s, "%s"] )' % (klass, name, node.attr)
            else:
                if klass in self._inline_classes:  ## static attribute
                    if node.attr in self._inline_classes[klass]:
                        return '''JS('%s["__dict__"]["%s"]')''' %(name, node.attr)
                    elif node.attr in self._classes[ klass ]: ## method
                        return '''JS('__%s_attrs["%s"]')''' %(klass, node.attr)
                    elif klass in self._decorator_class_props and node.attr in self._decorator_class_props[klass]:
                        getter = self._decorator_class_props[klass][node.attr]['get']
                        return '''JS('%s( [%s] )')''' %(getter, name)
                    else:
                        return '''JS('__%s___getattr__( [%s, "%s"] )')''' %(klass, name, node.attr)

                elif klass in self._decorator_class_props and node.attr in self._decorator_class_props[klass]:
                    getter = self._decorator_class_props[klass][node.attr]['get']
                    return '''JS('%s( [%s] )')''' %(getter, name)

                else:
                    return 'get_attribute(%s, "%s")' % (name, node.attr)
        else:
            return 'get_attribute(%s, "%s")' % (name, node.attr)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Subscript(self, node):
        name = self.visit(node.value)
        if name in self._instances:  ## support x[y] operator overloading
            klass = self._instances[ name ]
            if '__getitem__' in self._classes[ klass ]:
                return '__%s___getitem__( [%s, %s] )' % (klass, name, self.visit(node.slice))
            else:
                return 'get_attribute(%s, "__getitem__")([%s], JSObject())' % (
                    self.visit(node.value),
                    self.visit(node.slice),
                )
        else:
            return 'get_attribute(%s, "__getitem__")([%s], JSObject())' % (
                self.visit(node.value),
                self.visit(node.slice),
            )

    def visit_Slice(self, node):
        return "get_attribute(Slice, '__call__')([%s, %s, %s], JSObject())" % (self.visit(node.lower), self.visit(node.upper), self.visit(node.step))

    def visit_Assign(self, node):
        # XXX: support only one target for subscripts
        target = node.targets[0]
        if isinstance(target, Subscript):
            code = "get_attribute(get_attribute('%s', '__setitem__'), '__call__')([%s, %s], JSObject())"
            code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))
            writer.write(code)
        elif isinstance(target, Attribute):
            name = self.visit(target.value)
            if name == 'self' and isinstance(self._catch_attributes, set):
                self._catch_attributes.add( target.attr )

            fallback = True
            if name in self._instances:  ## support '.' operator overloading
                klass = self._instances[ name ]
                if klass in self._decorator_class_props and target.attr in self._decorator_class_props[klass]:
                    setter = self._decorator_class_props[klass][target.attr].get( 'set', None )
                    if setter:
                        #writer.write( '''JS('%s( [%s, %s] )')''' %(setter, name, self.visit(node.value)) )  ## can not nest have nested JS() calls
                        writer.write( '%s( [%s, %s] )' %(setter, name, self.visit(node.value)) )
                        fallback = False


            if fallback:
                code = 'set_attribute(%s, "%s", %s)' % (
                    name,
                    target.attr,
                    self.visit(node.value)
                )
                writer.write(code)

        elif isinstance(target, Name):

            if isinstance(node.value, Call) and hasattr(node.value.func, 'id') and node.value.func.id in self._classes:
                self._instances[ target.id ] = node.value.func.id  ## keep track of instances
            elif target.id in self._instances:
                self._instances.pop( target.id )

            if isinstance(node.value, Name):
                name = self.visit(node.value)
                if name in self._instances: self._instances[ target.id ] = self._instances[ name ]
                writer.write('%s = %s' % (target.id, name))
            else:
                writer.write('%s = %s' % (target.id, self.visit(node.value)))

        else:  # it's a Tuple
            id = self.identifier
            self.identifier += 1
            r = '__r_%s' % id
            writer.write('var(%s)' % r)
            writer.write('%s = %s' % (r, self.visit(node.value)))
            for i, target in enumerate(target.elts):
                if isinstance(target, Attribute):
                    code = 'set_attribute(%s, "%s", %s[%s])' % (
                        self.visit(target.value),
                        target.attr,
                        r,
                        i
                    )
                    writer.write(code)
                else:
                    writer.write('%s = %s[%s]' % (target.id, r, i))

    def visit_Print(self, node):
        writer.write('print %s' % ', '.join(map(self.visit, node.values)))

    def visit_Str(self, node):
        return '"%s"' % node.s

    def visit_Expr(self, node):
        writer.write(self.visit(node.value))

    def visit_Call(self, node):
        if hasattr(node.func, 'id') and node.func.id in ('JS', 'toString', 'JSObject', 'JSArray', 'var'):
            args = list( map(self.visit, node.args) ) ## map in py3 returns an iterator not a list
            if node.func.id == 'var':
                for k in node.keywords:
                    self._instances[ k.arg ] = k.value.id
                    args.append( k.arg )
            else:
                kwargs = map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords)
                args.extend(kwargs)
            args = ', '.join(args)
            return '%s(%s)' % (node.func.id, args)
        else:

            call_has_args = len(node.args) or len(node.keywords) or node.starargs or node.kwargs

            if call_has_args:
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

            name = self.visit(node.func)
            if call_has_args:
                return 'get_attribute(%s, "__call__")(%s, %s)' % (name, args_name, kwargs_name)
            elif name in self._classes:
                return 'get_attribute(%s, "__call__")( JSArray(), JSObject() )' %name
            else:
                return '%s()' %name

    def visit_FunctionDef(self, node):
        property_decorator = None
        decorators = []
        for decorator in reversed(node.decorator_list):
            if isinstance(decorator, Name) and decorator.id == 'property':
                property_decorator = decorator
                n = node.name + '__getprop__'
                self._decorator_properties[ node.original_name ] = dict( get=n, set=None )
                node.name = n

            elif isinstance(decorator, Attribute) and isinstance(decorator.value, Name) and decorator.value.id in self._decorator_properties:
                if decorator.attr == 'setter':
                    if self._decorator_properties[ decorator.value.id ]['set']:
                        raise SyntaxError('user error - the same decorator.setter is used more than once!')
                    n = node.name + '__setprop__'
                    self._decorator_properties[ decorator.value.id ]['set'] = n
                    node.name = n
                elif decorator.attr == 'deleter':
                    raise NotImplementedError
                else:
                    raise RuntimeError

            else:
                decorators.append( decorator )


        writer.write('def %s(args, kwargs):' % node.name)
        writer.push()

        if len(node.args.defaults) or len(node.args.args) or node.args.vararg or node.args.kwarg:
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

            #prebody = list()  ## NOT USED?

            # create a JS Object to store the value of each parameter
            signature = ', '.join(map(lambda x: '%s=%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
            writer.write('signature = JSObject(%s)' % signature)
            writer.write('arguments = get_arguments(signature, args, kwargs)')
            # # then for each argument assign its value
            for arg in node.args.args:
                writer.write("""JS("var %s = arguments['%s']")""" % (arg.id, arg.id))
            if node.args.vararg:
                writer.write("""JS("var %s = arguments['%s']")""" % (node.args.vararg, node.args.vararg))
                # turn it into a list
                expr = '%s = get_attribute(list, "__call__")(create_array(%s), {});'
                expr = expr % (node.args.vararg, node.args.vararg)
                writer.write(expr)
            if node.args.kwarg:
                writer.write("""JS('var %s = arguments["%s"]')""" % (node.args.kwarg, node.args.kwarg))
                expr = '%s = get_attribute(dict, "__call__")(create_array(%s), {});'
                expr = expr % (node.args.kwarg, node.args.kwarg)
                writer.write(expr)

        #map(self.visit, node.body)
        for child in node.body:
            # simple test to drop triple quote comments
            if hasattr(child, 'value'):
                if isinstance(child.value, Str):
                    continue
            if isinstance(child, GeneratorType):
                for sub in child:
                    self.visit(sub)
            else:
                self.visit(child)

        writer.pull()

        # apply decorators
        for decorator in decorators:
            writer.write('%s = %s(create_array(%s))' % (node.name, self.visit(decorator), node.name))

    def visit_For(self, node):
        writer.write('var(__iterator__, %s)' % node.target.id)
        writer.write('__iterator__ = get_attribute(get_attribute(%s, "__iter__"), "__call__")(JSArray(), JSObject())' % self.visit(node.iter))
        writer.write('try:')
        writer.push()
        writer.write('%s = get_attribute(__iterator__, "next")(JSArray(), JSObject())' % node.target.id)
        writer.write('while True:')
        writer.push()
        map(self.visit, node.body)
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



def main(script):
    input = parse(script)
    PythonToPythonJS().visit(input)
    return writer.getvalue()


def command():
    module = module_path = None

    data = sys.stdin.read()
    if data.startswith('#!'):
        header = data[ 2 : data.index('\n') ]
        data = data[ data.index('\n')+1 : ]
        if ';' in header:
            module_path, module = header.split(';')
        else:
            module_path = header

    compiler = PythonToPythonJS( module=module, module_path=module_path )
    compiler.visit( parse(data) )
    compiler.save_module()
    output = writer.getvalue()
    print( output )  ## pipe to stdout


if __name__ == '__main__':
    command()
