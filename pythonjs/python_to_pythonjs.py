#!/usr/bin/env python
import os, sys, pickle
from types import GeneratorType

import ast
from ast import Str
from ast import Call
from ast import Name
from ast import Tuple
from ast import Assign
from ast import keyword
from ast import Subscript
from ast import Attribute
from ast import FunctionDef
from ast import BinOp
from ast import Pass
from ast import Global
from ast import With

from ast import parse
from ast import NodeVisitor

if sys.version_info.major == 3:
    import io
    StringIO = io.StringIO
else:
    from cStringIO import StringIO as StringIO

try:
    _log_file = open('/tmp/python_to_pythonjs.log', 'wb')
except:
    _log_file = None
def log(txt):
    if _log_file:
        _log_file.write( str(txt)+'\n' )
        _log_file.flush()


GLOBAL_VARIABLE_SCOPE = False              ## Python style
if '--global-variable-scope' in sys.argv:  ## JavaScript style
    GLOBAL_VARIABLE_SCOPE = True
    log('not using python style variable scope')


class Writer(object):

    def __init__(self):
        self.level = 0
        self.buffers = list()
        self.output = StringIO()
        self.with_javascript = False

    def is_at_global_level(self):
        return self.level == 0

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
        if self.with_javascript:
            if not code.endswith(':'):  ## will this rule always catch: while, and if/else blocks?
                if not code.startswith('print '):
                    if not code.startswith('var('):
                        if not code == 'pass':
                            code = """JS('''%s''')"""%code
        s = '%s%s\n' % (indentation, code)
        #self.output.write(s.encode('utf-8'))
        self.output.write(s)

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

class Typedef(object):
    # http://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
    _opmap = dict(
        __add__ = '+',
        __iadd__ = '+=',
        __sub__ = '-',
        __isub__ = '-=',
        __mul__ = '*',
        __imul__ = '*=',
        __div__ = '/',
        __idiv__ = '/=',
        __mod__ = '%',
        __imod__ = '%=',
        __lshift__ = '<<',
        __ilshift__ = '<<=',
        __rshift__ = '>>',
        __irshift__ = '>>=',
        __and__ = '&',
        __iand__ = '&=',
        __xor__ = '^',
        __ixor__ = '^=',
        __or__ = '|',
        __ior__ = '|=',
    )

    def __init__(self, **kwargs):
        for name in kwargs.keys():
            setattr( self, name, kwargs[name] )

        self.operators = dict()
        for name in self.methods:
            if name in self._opmap:
                op = self._opmap[ name ]
                self.operators[ op ] = self.get_pythonjs_function_name( name )

    def get_pythonjs_function_name(self, name):
        assert name in self.methods
        return '__%s_%s' %(self.name, name) ## class name

    def check_for_parent_with(self, method=None, property=None, operator=None, class_attribute=None):
        log('check_for_parent_with: %s'%locals())
        log('self.parents: %s'%self.parents)

        for parent_name in self.parents:
            typedef = self.compiler.get_typedef( class_name=parent_name )
            if method and method in typedef.methods:
                return typedef
            elif property and property in typedef.properties:
                return typedef
            elif operator and typedef.operators:
                return typedef
            elif class_attribute in typedef.class_attributes:
                return typedef
            elif typedef.parents:
                res = typedef.check_for_parent_with(
                    method=method, 
                    property=property, 
                    operator=operator,
                    class_attribute=class_attribute
                )
                if res:
                    return res

class PythonToPythonJS(NodeVisitor):

    identifier = 0

    def __init__(self, module=None, module_path=None):
        super(PythonToPythonJS, self).__init__()
        self._classes = dict()    ## class name : [method names]
        self._class_parents = dict()  ## class name : parents
        self._instance_attributes = dict()  ## class name : [attribute names]
        self._class_attributes = dict()
        self._catch_attributes = None
        self._names = set() ## not used?
        self._instances = dict()  ## instance name : class name
        self._decorator_properties = dict()
        self._decorator_class_props = dict()
        self._function_return_types = dict()
        self._return_type = None
        self._module = module
        self._module_path = module_path
        self._with_js = False
        self._typedefs = dict()  ## class name : typedef  (not pickled)

        self._globals = dict()
        self._global_typed_lists = dict()  ## global name : set  (if len(set)==1 then we know it is a typed list)
        self._global_typed_dicts = dict()
        self._global_typed_tuples = dict()

        self._custom_operators = {}

        self.setup_builtins()

    def preprocess_custom_operators(self, data):
        '''
        custom operators must be defined before they are used
        '''
        code = []
        for line in data.splitlines():
            if line.strip().startswith('@custom_operator'):
                l = line.replace('"', "'")
                a,b,c = l.split("'")
                op = b.decode('utf-8')
                self._custom_operators[ op ] = None
            else:
                for op in self._custom_operators:
                    op = op.encode('utf-8')
                    line = line.replace(op, '|"%s"|'%op)

            code.append( line )

        data = '\n'.join( code )
        return data

    def setup_builtins(self):
        self._classes['dict'] = set(['__getitem__', '__setitem__'])
        self._classes['list'] = set(['__getitem__', '__setitem__'])
        self._classes['tuple'] = set(['__getitem__', '__setitem__'])
        self._builtins = set(['dict', 'list', 'tuple'])

    def get_typedef(self, instance=None, class_name=None):
        assert instance or class_name
        if isinstance(instance, Name) and instance.id in self._instances:
            class_name = self._instances[ instance.id ]

        if class_name:
            #assert class_name in self._classes
            if class_name not in self._classes:
                log('ERROR: class name not in self._classes: %s'%class_name)
                log('self._classes: %s'%self._classes)
                raise RuntimeError('class name: %s - not found in self._classes - node:%s '%(class_name, instance))

            if class_name not in self._typedefs:
                self._typedefs[ class_name ] = Typedef(
                    name = class_name,
                    methods = self._classes[ class_name ],
                    #properties = self._decorator_class_props[ class_name ],
                    #attributes = self._instance_attributes[ class_name ],
                    #class_attributes = self._class_attributes[ class_name ],
                    #parents = self._class_parents[ class_name ],
                    properties = self._decorator_class_props.get(  class_name, set()),
                    attributes = self._instance_attributes.get(    class_name, set()),
                    class_attributes = self._class_attributes.get( class_name, set()),
                    parents = self._class_parents.get(             class_name, set()),

                    compiler = self,
                )
            return self._typedefs[ class_name ]

    def save_module(self):
        if self._module and self._module_path:
            a = dict(
                classes = self._classes,
                instance_attributes = self._instance_attributes,
                class_attributes = self._class_attributes,
                decorator_class_props = self._decorator_class_props,
                function_return_types = self._function_return_types,
                class_parents = self._class_parents,
            )
            pickle.dump( a, open(os.path.join(self._module_path, self._module+'.module'), 'wb') )

    def _check_for_module(self, name):
        if self._module_path and name+'.module' in os.listdir(self._module_path):
            return True
        else:
            return False

    def _load_module(self, name):
        f = open( os.path.join(self._module_path, name+'.module'), 'rb' )
        a = pickle.load( f ); f.close()
        return a

    def visit_Import(self, node):
        for alias in node.names:
            writer.write( '## import: %s :: %s' %(a.name,a.asname) )
            raise SyntaxError('import with a namespace is not support yet, use "from module import *" instead')

    def visit_ImportFrom(self, node):
        if node.module in MINI_STDLIB:
            for n in node.names:
                if n.name in MINI_STDLIB[ node.module ]:
                    writer.write( 'JS("%s")' %MINI_STDLIB[node.module][n.name] )

        elif self._check_for_module( node.module ):
            if node.names[0].name == '*':
                a = self._load_module( node.module )
                self._classes.update( a['classes'] )
                self._class_attributes.update( a['class_attributes'] )
                self._instance_attributes.update( a['instance_attributes'] )
                self._decorator_class_props.update( a['decorator_class_props'] )
                self._function_return_types.update( a['function_return_types'] )
                self._class_parents.update( a['class_parents'] )
            else:
                raise SyntaxError('only "from module import *" is allowed')

            writer.write('## import from: %s :: %s' %(node.module, [ (a.name,a.asname) for a in node.names]))

    def visit_Assert(self, node):
        ## hijacking "assert isinstance(a,A)" as a type system ##
        if isinstance( node.test, Call ) and isinstance(node.test.func, Name) and node.test.func.id == 'isinstance':
            a,b = node.test.args
            if b.id in self._classes:
                self._instances[ a.id ] = b.id

    def visit_Dict(self, node):
        node.returns_type = 'dict'
        #keys = [x.s for x in node.keys]
        #values = map(self.visit, node.values)
        #a = [ '%s=%s'%x for x in zip(keys, values) ]
        #b = 'JSObject(%s)' %', '.join(a)
        #return 'get_attribute(dict, "__call__")([], JSObject(js_object=%s))' %b
        a = []
        for i in range( len(node.keys) ):
            k = self.visit( node.keys[ i ] )
            v = self.visit( node.values[i] )
            if self._with_js:
                a.append( '%s:%s'%(k,v) )
            else:
                a.append( 'JSObject(key=%s, value=%s)'%(k,v) )
        if self._with_js:
            b = ','.join( a )
            return '{ %s }' %b
        else:
            b = '[%s]' %', '.join(a)
            return 'get_attribute(dict, "__call__")([], JSObject(js_object=%s))' %b

    def visit_Tuple(self, node):
        node.returns_type = 'tuple'
        a = '[%s]' % ', '.join(map(self.visit, node.elts))
        return 'get_attribute(tuple, "__call__")([], JSObject(js_object=%s))' %a

    def visit_List(self, node):
        node.returns_type = 'list'
        a = '[%s]' % ', '.join(map(self.visit, node.elts))
        if self._with_js:
            return a
        else:
            return 'get_attribute(list, "__call__")([], JSObject(js_object=%s))' %a

    def visit_ListComp(self, node):
        node.returns_type = 'list'
        writer.write('var(__comprehension__)')
        writer.write('__comprehension__ = JSArray()')

        length = len( node.generators )
        a = ['idx%s'%i for i in range(length)]
        writer.write('var( %s )' %','.join(a) )
        a = ['iter%s'%i for i in range(length)]
        writer.write('var( %s )' %','.join(a) )
        a = ['get%s'%i for i in range(length)]
        writer.write('var( %s )' %','.join(a) )

        generators = list( node.generators )
        self._gen_comp( generators, node )

        return 'get_attribute(list, "__call__")([], JSObject(js_object=__comprehension__))'


    def _gen_comp(self, generators, node):
        gen = generators.pop()
        if len(gen.ifs): raise NotImplementedError  ## TODO
        id = len(generators)
        assert isinstance(gen.target, Name)
        writer.write('idx%s = 0'%id)
        writer.write('iter%s = %s' %(id, self.visit(gen.iter)) )
        writer.write('get%s = get_attribute(iter%s, "__getitem__")'%(id,id) )
        writer.write('while idx%s < get_attribute(len, "__call__")([iter%s], JSObject()):' %(id,id) )
        writer.push()

        writer.write('var(%s)'%gen.target.id)
        writer.write('%s=get%s( [idx%s], JSObject() )' %(gen.target.id, id,id) )

        if generators:
            self._gen_comp( generators, node )
        else:
            writer.write('__comprehension__.push( %s )' %self.visit(node.elt) )

        writer.write('idx%s+=1' %id )
        writer.pull()

    def visit_In(self, node):
        return ' in '

    def visit_NotIn(self, node):
        #return ' not in '
        raise RuntimeError('"not in" is only allowed in if-test: see method - visit_Compare')

    def visit_AugAssign(self, node):
        target = self.visit( node.target )
        op = '%s=' %self.visit( node.op )

        typedef = self.get_typedef( node.target )
        if typedef and op in typedef.operators:
            func = typedef.operators[ op ]
            a = '%s( [%s, %s] )' %(func, target, self.visit(node.value))
            writer.write( a )
        else:
            ## TODO extra checks to make sure the operator type is valid in this context
            a = '%s %s %s' %(target, op, self.visit(node.value))
            writer.write(a)

    def visit_Yield(self, node):
        return 'yield %s' % self.visit(node.value)


    def visit_ClassDef(self, node):
        name = node.name
        log('ClassDef: %s'%name)
        self._classes[ name ] = list()  ## method names
        self._class_parents[ name ] = set()
        self._class_attributes[ name ] = set()
        self._catch_attributes = None
        self._decorator_properties = dict() ## property names :  {'get':func, 'set':func}
        self._decorator_class_props[ name ] = self._decorator_properties
        self._instances[ 'self' ] = name

        #for dec in node.decorator_list:  ## TODO class decorators
        #    if isinstance(dec, Name) and dec.id == 'inline':  ## @inline class decorator is DEPRECATED
        #        self._catch_attributes = set()
        ## always catch attributes ##
        self._catch_attributes = set()
        self._instance_attributes[ name ] = self._catch_attributes


        writer.write('var(%s, __%s_attrs, __%s_parents)' % (name, name, name))
        writer.write('window["__%s_attrs"] = JSObject()' % name)
        writer.write('window["__%s_parents"] = JSArray()' % name)
        writer.write('window["__%s_properties"] = JSObject()' % name)

        for base in node.bases:
            code = 'window["__%s_parents"].push(%s)' % (name, self.visit(base))
            writer.write(code)
            if isinstance(base, Name):
                self._class_parents[ name ].add( base.id )
            else:
                raise NotImplementedError

        for item in node.body:
            if isinstance(item, FunctionDef):
                log('  method: %s'%item.name)

                if item.name == '__contains__':  ## this is required because we added Object.prototype.__contains__
                    item.name = item.name.upper()

                self._classes[ name ].append( item.name )
                item_name = item.name
                item.original_name = item.name
                item.name = '__%s_%s' % (name, item_name)

                self.visit(item)  # this will output the code for the function

                if item_name in self._decorator_properties:
                    pass
                else:
                    writer.write('window["__%s_attrs"]["%s"] = %s' % (name, item_name, item.name))

            elif isinstance(item, Assign) and isinstance(item.targets[0], Name):
                item_name = item.targets[0].id
                item.targets[0].id = '__%s_%s' % (name, item_name)
                self.visit(item)  # this will output the code for the assign
                writer.write('window["__%s_attrs"]["%s"] = %s' % (name, item_name, item.targets[0].id))
                self._class_attributes[ name ].add( item_name )  ## should this come before self.visit(item) ??
            elif isinstance(item, Pass):
                pass
            elif isinstance(item, ast.Expr) and isinstance(item.value, Str):  ## skip doc strings
                pass
            else:
                raise NotImplementedError( item )

        for prop_name in self._decorator_properties:
            getter = self._decorator_properties[prop_name]['get']
            writer.write('window["__%s_properties"]["%s"] = %s' %(name, prop_name, getter))

        self._catch_attributes = None
        self._decorator_properties = None
        self._instances.pop('self')

        writer.write('%s = create_class("%s", window["__%s_parents"], window["__%s_attrs"], window["__%s_properties"])' % (name, name, name, name, name))

    def visit_And(self, node):
        return ' and '

    def visit_Or(self, node):
        return ' or '

    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        return op.join( [self.visit(v) for v in node.values] )

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
        if self._with_js:
            if node.id == 'True':
                return 'true'
            elif node.id == 'False':
                return 'false'

        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def visit_Return(self, node):
        if node.value:
            if isinstance(node.value, Call) and isinstance(node.value.func, Name) and node.value.func.id in self._classes:
                self._return_type = node.value.func.id
            elif isinstance(node.value, Name) and node.value.id == 'self' and 'self' in self._instances:
                self._return_type = self._instances['self']

            writer.write('return %s' % self.visit(node.value))

        else:
            writer.write('return')  ## empty return

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)

        if op == '|':
            if isinstance(node.right, Str):
                self._custom_op_hack = (node.right.s, left)
                return ''
            elif hasattr(self, '_custom_op_hack') and isinstance(node.left, BinOp):
                op,left_operand = self._custom_op_hack
                right_operand = self.visit(node.right)
                #return '%s( %s, %s )' %(op, left_operand, right_operand)
                if op.decode('utf-8') in self._custom_operators:  ## swap name to python function
                    op = self._custom_operators[ op.decode('utf-8') ]
                return '%s( [%s, %s], JSObject() )' %(op, left_operand, right_operand)

        if isinstance(node.left, Name):
            typedef = self.get_typedef( node.left )
            if typedef and op in typedef.operators:
                func = typedef.operators[ op ]
                node.operator_overloading = func
                return '''JS('%s( [%s, %s], JSObject() )')''' %(func, left, right)  ## TODO double check this without wrapping in JS()

        return '%s %s %s' % (left, op, right)

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Is(self, node):
        return 'is'

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
        comp = [ left ]
        for i in range( len(node.ops) ):
            if isinstance(node.ops[i], ast.In) or isinstance(node.ops[i], ast.NotIn):
                if comp[-1] == left:
                    comp.pop()
                else:
                    comp.append( ' and ' )

                if isinstance(node.ops[i], ast.NotIn):
                    comp.append( ' not (')

                a = ( self.visit(node.comparators[i]), left )
                if self._with_js:
                    ## this makes "if 'x' in Array" work like Python: "if 'x' in list" - TODO fix this for js-objects
                    ## note javascript rules are confusing: "1 in [1,2]" is true, this is because a "in test" in javascript tests for an index
                    ## TODO double check this code
                    comp.append( '%s in %s or' %(a[1], a[0]) )  ## this is ugly, will break with Arrays
                    comp.append( 'Object.hasOwnProperty.call(%s, "__contains__") and' %a[0])
                    comp.append( "%s['__contains__'](%s)" %a )
                else:
                    comp.append( "get_attribute(get_attribute(%s, '__contains__'), '__call__')([%s], JSObject())" %a )

                if isinstance(node.ops[i], ast.NotIn):
                    comp.append( ' )')  ## it is not required to enclose NotIn

            else:
                comp.append( self.visit(node.ops[i]) )
                comp.append( self.visit(node.comparators[i]) )
        return ' '.join( comp )

    def visit_Not(self, node):
        return ' not '

    def visit_IsNot(self, node):
        return ' is not '

    def visit_UnaryOp(self, node):
        return self.visit(node.op) + self.visit(node.operand)

    def visit_Attribute(self, node):
        node_value = self.visit(node.value)

        if self._with_js:
            return '%s.%s' %(node_value, node.attr)
        typedef = None
        if isinstance(node.value, Name):
            typedef = self.get_typedef( instance=node.value )
        elif hasattr(node.value, 'returns_type'):
            typedef = self.get_typedef( class_name=node.value.returns_type )

        if typedef:
            if node.attr in typedef.properties:
                getter = typedef.properties[ node.attr ]['get']
                if getter in self._function_return_types:
                    node.returns_type = self._function_return_types[getter]
                return '%s( [%s], JSObject() )' %(getter, node_value)

            elif node.attr in typedef.class_attributes and not typedef.check_for_parent_with( class_attribute=node.attr ) and node_value != 'self':
                ## This optimization breaks when a subclass redefines a class attribute,
                ## but we need it for inplace assignment operators, this is safe only when
                ## other parent classes have not defined the same class attribute.
                ## This is also not safe when node_value is "self".
                return "%s['__class__']['__dict__']['%s']" %(node_value, node.attr)

            elif node.attr in typedef.attributes:
                return "%s['__dict__']['%s']" %(node_value, node.attr)

            elif '__getattr__' in typedef.methods:
                func = typedef.get_pythonjs_function_name( '__getattr__' )
                return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

            elif typedef.check_for_parent_with( property=node.attr ):
                parent = typedef.check_for_parent_with( property=node.attr )
                getter = parent.properties[ node.attr ]['get']
                if getter in self._function_return_types:
                    node.returns_type = self._function_return_types[getter]
                return '%s( [%s], JSObject() )' %(getter, node_value)

            elif typedef.check_for_parent_with( class_attribute=node.attr ):
                #return 'get_attribute(%s, "%s")' % (node_value, node.attr)  ## get_attribute is broken with grandparent class attributes
                if node.attr in typedef.class_attributes:
                    ## this might not be always correct
                    return "%s['__class__']['__dict__']['%s']" %(node_value, node.attr)
                else:
                    parent = typedef.check_for_parent_with( class_attribute=node.attr )
                    return "window['__%s_attrs']['%s']" %(parent.name, node.attr)

            elif typedef.check_for_parent_with( method='__getattr__' ):
                parent = typedef.check_for_parent_with( method='__getattr__' )
                func = parent.get_pythonjs_function_name( '__getattr__' )
                return '%s([%s, "%s"], JSObject())' %(func, node_value, node.attr)

            else:
                return 'get_attribute(%s, "%s")' % (node_value, node.attr)  ## TODO - double check this
        else:
            return 'get_attribute(%s, "%s")' % (node_value, node.attr)      ## TODO - double check this


    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Subscript(self, node):
        name = self.visit(node.value)

        if isinstance(node.slice, ast.Ellipsis):
            return '%s["wrapped"]' %name

        elif self._with_js:
            return '%s[ %s ]' %(name, self.visit(node.slice))

        elif name in self._instances:  ## support x[y] operator overloading
            klass = self._instances[ name ]
            if '__getitem__' in self._classes[ klass ]:
                return '__%s___getitem__([%s, %s], JSObject())' % (klass, name, self.visit(node.slice))
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

    def visit_Slice(self, node):  ## TODO - test this
        return "get_attribute(Slice, '__call__')([%s, %s, %s], JSObject())" % (self.visit(node.lower), self.visit(node.upper), self.visit(node.step))

    def visit_Assign(self, node):
        # XXX: support only one target for subscripts
        target = node.targets[0]
        if isinstance(target, Subscript):
            if isinstance(target.slice, ast.Ellipsis):
                code = '%s["wrapped"] = %s' %(self.visit(target.value), self.visit(node.value))
            elif self._with_js:
                code = '%s[ %s ] = %s'
                code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))
            else:
                code = "get_attribute(get_attribute(%s, '__setitem__'), '__call__')([%s, %s], JSObject())"
                code = code % (self.visit(target.value), self.visit(target.slice.value), self.visit(node.value))

            writer.write(code)

        elif isinstance(target, Attribute):
            target_value = self.visit(target.value)  ## target.value may have "returns_type" after being visited
            typedef = None
            if isinstance(target.value, Name):
                if target.value.id == 'self' and isinstance(self._catch_attributes, set):
                    self._catch_attributes.add( target.attr )
                typedef = self.get_typedef( instance=target.value )
            elif hasattr(target.value, 'returns_type'):
                typedef = self.get_typedef( class_name=target.value.returns_type )

            if self._with_js:
                writer.write( '%s.%s=%s' %(target_value, target.attr, self.visit(node.value)) )
            elif typedef and target.attr in typedef.properties and 'set' in typedef.properties[ target.attr ]:
                setter = typedef.properties[ target.attr ]['set']
                writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )
            elif typedef and target.attr in typedef.class_attributes:
                writer.write( '''%s['__class__']['__dict__']['%s'] = %s''' %(target_value, target.attr, self.visit(node.value)))
            elif typedef and target.attr in typedef.attributes:
                writer.write( '''%s['__dict__']['%s'] = %s''' %(target_value, target.attr, self.visit(node.value)))

            elif typedef and typedef.parents:
                parent_prop = typedef.check_for_parent_with( property=target.attr )
                parent_classattr = typedef.check_for_parent_with( class_attribute=target.attr )
                parent_setattr = typedef.check_for_parent_with( method='__setattr__' )
                if parent_prop and 'set' in parent_prop.properties[target.attr]:
                    setter = parent_prop.properties[target.attr]['set']
                    writer.write( '%s( [%s, %s], JSObject() )' %(setter, target_value, self.visit(node.value)) )
                elif parent_classattr:
                    writer.write( "window['__%s_attrs']['%s'] = %s" %(parent_classattr.name, target.attr, self.visit(node.value)) )
                elif parent_setattr:
                    func = parent_setattr.get_pythonjs_function_name( '__setattr__' )
                    writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )

                elif '__setattr__' in typedef.methods:
                    func = typedef.get_pythonjs_function_name( '__setattr__' )
                    writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )

                else:
                    code = 'set_attribute(%s, "%s", %s)' % (
                        target_value,
                        target.attr,
                        self.visit(node.value)
                    )
                    writer.write(code)

            elif typedef and '__setattr__' in typedef.methods:
                func = typedef.get_pythonjs_function_name( '__setattr__' )
                log('__setattr__ in instance typedef.methods - func:%s target_value:%s target_attr:%s' %(func, target_value, target_attr))
                writer.write( '%s([%s, "%s", %s], JSObject() )' %(func, target_value, target.attr, self.visit(node.value)) )


            else:
                code = 'set_attribute(%s, "%s", %s)' % (
                    target_value,
                    target.attr,
                    self.visit(node.value)
                )
                writer.write(code)

        elif isinstance(target, Name):
            node_value = self.visit( node.value )  ## node.value may have extra attributes after being visited

            if isinstance(node.value, Call) and hasattr(node.value.func, 'id') and node.value.func.id in self._classes:
                self._instances[ target.id ] = node.value.func.id  ## keep track of instances
            elif isinstance(node.value, Call) and isinstance(node.value.func, Name) and node.value.func.id in self._function_return_types:
                self._instances[ target.id ] = self._function_return_types[ node.value.func.id ]
            elif isinstance(node.value, Call) and isinstance(node.value.func, Attribute) and isinstance(node.value.func.value, Name) and node.value.func.value.id in self._instances:
                typedef = self.get_typedef( node.value.func.value )
                method = node.value.func.attr
                if method in typedef.methods:
                    func = typedef.get_pythonjs_function_name( method )
                    if func in self._function_return_types:
                        self._instances[ target.id ] = self._function_return_types[ func ]
                    else:
                        writer.write('## %s - unknown return type for: %s' % (typedef.name, func))
                else:
                    writer.write('## %s - not a method: %s' %(typedef.name, method))

            elif isinstance(node.value, Name) and node_value in self._instances:  ## if this is a simple copy: "a = b" and "b" is known to be of some class
                self._instances[ target.id ] = self._instances[ node_value ]
            elif isinstance(node.value, BinOp) and hasattr(node.value, 'operator_overloading') and node.value.operator_overloading in self._function_return_types:
                self._instances[ target.id ] = self._function_return_types[ node.value.operator_overloading ]
            elif hasattr(node.value, 'returns_type'):
                self._instances[ target.id ] = node.value.returns_type
            elif target.id in self._instances:
                self._instances.pop( target.id )

            if target.id in self._instances:
                type = self._instances[ target.id ]
                if writer.is_at_global_level():
                    self._globals[ target.id ] = type
                    if type == 'list':
                        self._global_typed_lists[ target.id ] = set()
                    elif type == 'tuple':
                        self._global_typed_tuples[ target.id ] = set()
                    elif type == 'dict':
                        self._global_typed_dicts[ target.id ] = set()

                    writer.write('%s = %s' % (target.id, node_value))
                else:
                    writer.write('%s = %s' % (target.id, node_value))
            else:
                writer.write('%s = %s' % (target.id, node_value))

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
        if self._with_js:
            return '"%s"' %node.s
        else:
            return '"""%s"""' % node.s

    def visit_Expr(self, node):
        writer.write(self.visit(node.value))

    def visit_Call(self, node):
        if self._with_js:
            args = list( map(self.visit, node.args) )
            if isinstance(node.func, Name) and node.func.id == 'new':
                assert len(args) == 1
                return ' new %s' %args[0]

            elif isinstance(node.func, Name) and node.func.id == 'JS':  ## avoids nested JS
                assert len(args) == 1
                return node.args[0].s  ## string literal
            else:
                a = ','.join(args)
                return '%s( %s )' %( self.visit(node.func), a )

        if isinstance(node.func, Name) and node.func.id in ('JS', 'toString', 'JSObject', 'JSArray', 'var', 'instanceof', 'typeof'):
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

            ## check if pushing to a global typed list ##
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, Name) and node.func.value.id in self._globals:
                gtype = self._globals[ node.func.value.id ]
                if gtype == 'list' and node.func.attr == 'append':
                    if isinstance(node.args[0], Name):
                        if node.args[0].id in self._instances:
                            gset = self._global_typed_lists[ node.func.value.id ]
                            gset.add( self._instances[node.args[0].id])
                            if len(gset) != 1:
                                raise SyntaxError('global lists can only contain one type: instance "%s" is different' %node.args[0].id)
                        else:
                            raise SyntaxError('global lists can only contain one type: instance "%s" is unknown' %node.args[0].id)

            call_has_args_only = len(node.args) and not (len(node.keywords) or node.starargs or node.kwargs)
            call_has_args = len(node.args) or len(node.keywords) or node.starargs or node.kwargs
            name = self.visit(node.func)

            if call_has_args_only:  ## lambda only supports simple args for now.
                args = ', '.join(map(self.visit, node.args))

            elif call_has_args:
                args = ', '.join(map(self.visit, node.args))
                kwargs = ', '.join(map(lambda x: '%s=%s' % (x.arg, self.visit(x.value)), node.keywords))
                args_name = '__args_%s' % self.identifier
                kwargs_name = '__kwargs_%s' % self.identifier

                writer.append('var(%s, %s)' % (args_name, kwargs_name))
                self.identifier += 1

                if name in ('list', 'tuple'):
                    writer.append( '%s = JS("%s.__dict__.js_object")' % (args_name, args))
                else:
                    writer.append('%s = JSArray(%s)' % (args_name, args))

                if node.starargs:
                    writer.append('%s.push.apply(%s, %s.__dict__.js_object)' % (args_name, args_name, self.visit(node.starargs)))
                writer.append('%s = JSObject(%s)' % (kwargs_name, kwargs))

                if node.kwargs:
                    kwargs = self.visit(node.kwargs)
                    code = "JS('for (var name in %s) { %s[name] = %s.__dict__.js_object[name]; }')" % (kwargs, kwargs_name, kwargs)
                    writer.append(code)

            if call_has_args_only:
                return 'get_attribute(%s, "__call__")([%s], JSObject())' % (name, args)

            elif call_has_args:
                if name == 'dict':
                    return 'get_attribute(%s, "__call__")(%s, JSObject(js_object=%s))' % (name, args_name, kwargs_name)
                elif name in ('list', 'tuple'):
                    return 'get_attribute(%s, "__call__")([], JSObject(js_object=%s))' % (name, args_name)
                else:
                    return 'get_attribute(%s, "__call__")(%s, %s)' % (name, args_name, kwargs_name)

            elif name in self._classes or name in self._builtins:
                return 'get_attribute(%s, "__call__")( JSArray(), JSObject() )' %name

            else:
                ## this a slightly dangerous optimization,
                ## because if the user is trying to create an instance of some class
                ## and that class is define in an external binding,
                ## and they forgot to put "from mylibrary import *" in their script (an easy mistake to make)
                ## then this fails to call __call__ to initalize the instance,
                ## and throws a confusing error:
                ## Uncaught TypeError: Property 'SomeClass' of object [object Object] is not a function 
                ## TODO - remove this optimization, or provide the user with a better error message.
                return '%s( JSArray(), JSObject() )' %name

    def visit_Lambda(self, node):
        args = [self.visit(a) for a in node.args.args]
        if self._with_js:
            return '(function (%s) {%s})' %(','.join(args), self.visit(node.body))
        else:
            return 'lambda %s: %s' %(','.join(args), self.visit(node.body))

    def visit_FunctionDef(self, node):
        property_decorator = None
        decorators = []
        with_js_decorators = []
        for decorator in reversed(node.decorator_list):
            log('@decorator: %s' %decorator)
            if self._with_js:  ## decorators are special in with-js mode
                with_js_decorators.append( self.visit( decorator ) )

            elif isinstance(decorator, Name) and decorator.id == 'property':
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

            elif isinstance(decorator, Call) and decorator.func.id == 'custom_operator':
                assert len(decorator.args) == 1
                assert isinstance( decorator.args[0], Str )
                op = decorator.args[0].s.decode('utf-8')
                if op not in self._custom_operators:
                    raise RuntimeError( op, self._custom_operators )
                self._custom_operators[ op ] = node.name

            else:
                decorators.append( decorator )

        log('function: %s'%node.name)
        if self._with_js:
            if node.args.defaults:
                raise SyntaxError( 'pure javascript functions can not take keyword arguments')
            elif node.args.vararg:
                raise SyntaxError( 'pure javascript functions can not take variable arguments (*args)' )
            elif node.args.kwarg:
                raise SyntaxError( 'pure javascript functions can not take variable keyword arguments (**kwargs)' )

            args = [ a.id for a in node.args.args ]
            writer.write( 'def %s( %s ):' % (node.name, ','.join(args)) )

        else:
            writer.write('def %s(args, kwargs):' % node.name)
        writer.push()

        ## the user will almost always want to use Python-style variable scope,
        ## this is kept here as an option to be sure we are compatible with the
        ## old-style code in runtime/pythonpythonjs.py and runtime/builtins.py
        if not GLOBAL_VARIABLE_SCOPE:
            local_vars = set()
            global_vars = set()
            for n in node.body:
                if isinstance(n, Assign) and isinstance(n.targets[0], Name):  ## assignment to local
                    local_vars.add( n.targets[0].id )
                elif isinstance(n, Global):
                    global_vars.update( n.names )
                elif isinstance(n, With) and isinstance( n.context_expr, Name ) and n.context_expr.id == 'javascript':
                    for c in n.body:
                        if isinstance(c, Assign) and isinstance(c.targets[0], Name):  ## assignment to local
                            local_vars.add( c.targets[0].id )

            if local_vars-global_vars:
                a = ','.join( local_vars-global_vars )
                writer.write('var(%s)' %a)



        if not self._with_js and (len(node.args.defaults) or len(node.args.args) or node.args.vararg or node.args.kwarg):
            # First check the arguments are well formed 
            # ie. that this function is not a callback of javascript code
            writer.write("""if (JS('args instanceof Array') and JS("{}.toString.call(kwargs) === '[object Object]'") and arguments.length == 2):""")
            # XXX: there is bug in the underlying translator preventing me to write the condition
            # in a more readble way... something to do with brakects...
            writer.push()
            writer.write('pass')  # do nothing if it's not called from javascript
            writer.pull()
            writer.write('else:')
            writer.push()
            # If it's the case, move use ``arguments`` to ``args`` 
            writer.write('args = Array.prototype.slice.call(arguments)')
            # This means you can't pass keyword argument from javascript but we already knew that
            writer.write('kwargs = JSObject()')
            writer.pull()
            # done with pythonjs function used as callback of Python code 

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

            # create a JS Object to store the value of each parameter
            signature = ', '.join(map(lambda x: '%s=%s' % (self.visit(x.arg), self.visit(x.value)), keywords))
            writer.write('signature = JSObject(%s)' % signature)
            writer.write('signature["function_name"] = "%s"' %node.name)
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
        else:
            log('(function has no arguments)')

        self._return_type = None
        map(self.visit, node.body)

        if self._return_type:
            self._function_return_types[ node.name ] = self._return_type

        writer.pull()
        ## note, in javascript function.name is a non-standard readonly attribute,
        ## the compiler creates anonymous functions with name set to an empty string.
        writer.write('%s.NAME = "%s"' %(node.name,node.name))

        writer.write( '%s.args_signature = [%s]' %(node.name, ','.join(['"%s"'%n.id for n in node.args.args])) )
        defaults = ['%s:%s'%(self.visit(x[0]), self.visit(x[1])) for x in zip(node.args.args[-len(node.args.defaults):], node.args.defaults) ]
        writer.write( '%s.kwargs_signature = {%s}' %(node.name, ','.join(defaults)) )

        if self._with_js and with_js_decorators:
            for dec in with_js_decorators:
                if '.prototype.' in dec:
                    ## these with-js functions are assigned to a some objects prototype,
                    ## here we assume that they depend on the special "this" variable,
                    ## therefore this function can not be marked as f.pythonscript_function,
                    ## because we need get_attribute(f,'__call__') to dynamically bind "this"
                    writer.write( '%s=%s'%(dec,node.name) )
                else:  ## TODO fix with-javascript decorators
                    writer.write( '%s = get_attribute(%s,"__call__")( [%s], {} )' %(node.name, dec, node.name))

        ## Gotcha, this broke calling a "with javascript:" defined function from pythonjs, 
        ## because get_attribute thought it was dealing with a pythonjs function and was
        ## calling the function in the normal pythonjs way, ie. func( [args], {} )
        #elif self._with_js:  ## this is just an optimization so we can avoid making wrappers at runtime
        #    writer.write('%s.pythonscript_function=true'%node.name)

        if not self._with_js:
            writer.write('%s.pythonscript_function=True'%node.name)

        # apply decorators
        for decorator in decorators:
            assert not self._with_js
            writer.write('%s = get_attribute(%s,"__call__")( [%s], {} )' % (node.name, self.visit(decorator), node.name))

    def visit_Continue(self, node):
        if self._with_js:
            writer.write('continue')
        else:
            writer.write('%s = get_attribute(__iterator__, "next")(JSArray(), JSObject())' % self._for_iterator_target)
            writer.write('continue')
        return ''

    def visit_For(self, node):
        if self._with_js:
            writer.write('for %s in %s:' %(self.visit(node.target),self.visit(node.iter)))
            writer.push()
            map(self.visit, node.body)
            writer.pull()
        else:

            ## TODO else remove node.target.id from self._instances
            if isinstance(node.iter, Name) and node.iter.id in self._global_typed_lists:
                self._instances[ node.target.id ] = list( self._global_typed_lists[ node.iter.id ] )[0]

            self._for_iterator_target = node.target.id  ## this could break with nested for loops
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

    def visit_With(self, node):
        if isinstance( node.context_expr, Name ) and node.context_expr.id == 'javascript':
            self._with_js = True
            writer.with_javascript = True
            map(self.visit, node.body)
            writer.with_javascript = False
            self._with_js = False
        elif isinstance( node.context_expr, Name ) and node.context_expr.id == 'python':
            if not self._with_js:
                raise SyntaxError('"with python:" is only used inside of a "with javascript:" block')
            self._with_js = False
            writer.with_javascript = False
            map(self.visit, node.body)
            writer.with_javascript = True
            self._with_js = True


def main(script):
    input = parse(script)
    PythonToPythonJS().visit(input)
    return writer.getvalue()


def command():
    module = module_path = None

    data = sys.stdin.read()
    #data = data.decode('utf-8')
    #open('/tmp/testunicode.txt', 'wb').write(data.encode('utf-8'))

    if data.startswith('#!'):
        header = data[ 2 : data.index('\n') ]
        data = data[ data.index('\n')+1 : ]
        if ';' in header:
            module_path, module = header.split(';')
        else:
            module_path = header

    compiler = PythonToPythonJS( module=module, module_path=module_path )

    data = compiler.preprocess_custom_operators( data )
    compiler.visit( parse(data) )

    compiler.save_module()
    output = writer.getvalue()
    print( output )  ## pipe to stdout


if __name__ == '__main__':
    command()
