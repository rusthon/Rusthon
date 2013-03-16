from ast import Str
from ast import Expr
from ast import Call
from ast import Name
from ast import Assign
from ast import Attribute
from ast import FunctionDef
from ast import NodeTransformer


class PythonScriptTransformer(NodeTransformer):

    def visit_ClassDef(self, node):
        name = Name(node.name, None)
        yield Assign([name], Call(Name('JSObject', None), None, None, None, None))
        yield Assign([Name('parents', None)], Call(Name('JSArray', Name), None, None, None, None))  # Bases not supported
        for item in node.body:
            if isinstance(item, FunctionDef):
                item_name = item.name
                item.name = closure_name = '%s__%s' % (node.name, item_name)
            elif isinstance(item, Assign):
                item_name = item.targets[0].id
                item.targets[0].id = closure_name = '%s__%s' % (name.id, item_name)
            yield self.generic_visit(item)
            yield Assign([Attribute(name, item_name, None)], Name(closure_name, None))
        yield Assign([name], Call(Name('create_class', None), [Str(node.name), Name('parents', None), Name(name.id, None)], None, None, None))

    def visit_Attribute(self, node):
        return Call(Name('get_attribute', None), [node.value, Str(node.attr)], None, None, None)

    def visit_Assign(self, node):
        attr = node.targets[0]
        if isinstance(attr, Attribute):
            return Expr(Call(Name('set_attribute', None), [attr.value, Str(attr.attr), node.value], None, None, None))
        else:
            return self.generic_visit(node)

    def visit_Call(self, node):
        if hasattr(node.func, 'id') and node.func.id == 'JS':
            return self.generic_visit(node)
        return Call(
            Call(
                Name('get_attribute', None),
                [self.visit(node.func), Str('__call__')],
                None,
                None,
                None,
            ),
            node.args,
            None,
            None,
            None,
        )
