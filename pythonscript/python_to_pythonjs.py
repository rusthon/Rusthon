from ast import Str
from ast import Expr
from ast import Call
from ast import Name
from ast import Assign
from ast import keyword
from ast import arguments
from ast import Attribute
from ast import FunctionDef
from ast import NodeTransformer


class PythonToPythonJS(NodeTransformer):

    def visit_ClassDef(self, node):
        name = Name(node.name, None)
        yield Expr(Assign([name], Call(Name('JSObject', None), None, None, None, None)))
        yield Expr(Assign([Name('parents', None)], Call(Name('JSArray', Name), None, None, None, None)))
        if node.bases:
            yield Expr(
                Call(
                    Attribute(
                        Name('parents', None),
                        'push',
                        None
                    ),
                    node.bases,
                    None,
                    None,
                    None
                )
            )
        for item in node.body:
            if isinstance(item, FunctionDef):
                item_name = item.name
                item.name = closure_name = '%s__%s' % (node.name, item_name)
                for i in self.visit(item):
                    yield i
                yield Expr(Assign([Attribute(name, item_name, None)], Name(closure_name, None)))
            elif isinstance(item, Assign):
                item_name = item.targets[0].id
                item.targets[0].id = closure_name = '%s__%s' % (name.id, item_name)
                yield item
                yield Expr(Assign([Attribute(name, item_name, None)], Name(closure_name, None)))
        yield Expr(Assign([name], Call(Name('create_class', None), [Str(node.name), Name('parents', None), Name(name.id, None)], None, None, None)))

    def visit_Attribute(self, node):
        return Call(Name('get_attribute', None), [self.visit(node.value), Str(node.attr)], None, None, None)

    def visit_Expr(self, node):  # FIXME: is it useful
        return Expr(self.visit(node.value))

    def visit_Assign(self, node):
        attr = node.targets[0]
        if isinstance(attr, Attribute):
            return Expr(Call(Name('set_attribute', None), [attr.value, Str(attr.attr), node.value], None, None, None))
        else:
            return Expr(self.generic_visit(node))

    def visit_Call(self, node):
        if hasattr(node.func, 'id') and node.func.id in ('JS', 'toString', 'dict'):
            return self.generic_visit(node)
        return Call(
            Call(
                Name('get_attribute', None),
                [self.visit(node.func), Str('__call__')],
                None,
                None,
                None,
            ),
            [
                Call(
                    Name('JSArray', None),
                    node.args,
                    None,
                    None,
                    None
                ),
                Call(
                    Name('JSObject', None),
                    None,
                    map(lambda x: keyword(Name(x.arg, None), x.value), node.keywords),
                    None,
                    None
                ),
            ],
            None,
            None,
            None,
        )

    def visit_FunctionDef(self, node):
        # new body is old body processed by PythonToPythonJS
        # prepended by the python arguments handling
        body = map(self.visit, node.body)
        # new pythonjs' python function arguments handling
        # create the structure representing the functions arguments
        # first create the defaultkwargs JSObject
        l = len(node.args.defaults)

        kwargsdefault = map(lambda x: keyword(x[0], x[1]), zip(node.args.args[-l:], node.args.defaults))
        kwargsdefault = Call(
            Name('JSObject', None),
            None,
            kwargsdefault,
            None,
            None
        )
        args = Call(
            Name('JSArray', None),
            map(lambda x: Str(x.id), node.args.args),
            None,
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
        body.insert(
            0,
            Expr(
                Assign(
                    [Name('parameters', None)],
                    Call(
                        Name('JSObject', None),
                        None,
                        keywords,
                        None,
                        None
                    )
                )
            )
        )
        # retrieve the actual value for each argument, cf. pythonpythonjs
        body.insert(
            1,
            Expr(
                Assign(
                    [Name('parameters', None)],
                    Call(
                        Name('get_arguments', None),
                        [Name('parameters', None), Name('args', None), Name('kwargs', None)],
                        None,
                        None,
                        None
                    )
                )
            )
        )
        # then for each argument assign its value
        for arg in node.args.args:
            body.insert(
                2,
                Expr(
                    Assign(
                        [arg],
                        Call(
                            Name('JS', None),
                            [Str('parameters["%s"]' % arg.id)],
                            None,
                            None,
                            None
                        )
                    )
                )
            )
        if node.args.vararg:
            body.insert(
                    2,
                    Expr(
                        Call(
                            Name('JS', None),
                            [Str('%s = parameters["%s"]' % (node.args.vararg, node.args.vararg))],
                            None,
                            None,
                            None
                    )
                )
            )
        if node.args.kwarg:
            body.insert(
                    2,
                    Expr(
                        Call(
                            Name('JS', None),
                            [Str('%s = parameters["%s"]' % (node.args.kwarg, node.args.kwarg))],
                            None,
                            None,
                            None
                    )
                )
            )

        # process arguments to build python keyword arguments handling
        # in pythonjs, python functions takes two parameters args and kwargs
        args = arguments([Name('args', None), Name('kwargs', None)], None, None, None)
        yield FunctionDef(
            node.name,
            args,
            body,
            None
        )

        for decorator in reversed(node.decorator_list):
            yield Assign(
                [Name(node.name, None)],
                Call(
                    decorator,
                    [
                        Call(
                            Name('JS', None),
                            [Str('new Array(%s)' % node.name)],
                            None,
                            None,
                            None
                        )
                    ],
                    None,
                    None,
                    None
                )
            )
