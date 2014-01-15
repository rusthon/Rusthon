// Python to Javascript translation engine

;(function(){

var js,$pos,res,$op

var $operators = {
    "//=":"ifloordiv",">>=":"irshift","<<=":"ilshift",
    "**=":"ipow","**":"pow","//":"floordiv","<<":"lshift",">>":"rshift",
    "+=":"iadd","-=":"isub","*=":"imul","/=":"itruediv",
    "%=":"imod","&=":"iand","|=":"ior","^=":"ixor",
    "+":"add","-":"sub","*":"mul",
    "/":"truediv","%":"mod","&":"and","|":"or","~":"invert",
    "^":"xor","<":"lt",">":"gt",
    "<=":"le",">=":"ge","==":"eq","!=":"ne",
    "or":"or","and":"and", "in":"in", //"not":"not",
    "is":"is","not_in":"not_in","is_not":"is_not" // fake
    }

var $oplist = []
for(var attr in $operators){$oplist.push(attr)}

// operators weight for precedence
var $op_order = [['or'],['and'],
    ['in','not_in'],
    ['<','<=','>','>=','!=','==','is','is_not'],
    ['|','^','&'],
    ['+'],
    ['-'],
    ['/','//','%'],
    ['*'],
    ['**']
]

var $op_weight={}
var $weight=1
for (var $i=0;$i<$op_order.length;$i++){
    for(var $j=0;$j<$op_order[$i].length;$j++){
        $op_weight[$op_order[$i][$j]]=$weight
    }
    $weight++
}

var $augmented_assigns = {
    "//=":"ifloordiv",">>=":"irshift","<<=":"ilshift",
    "**=":"ipow","+=":"iadd","-=":"isub","*=":"imul","/=":"itruediv",
    "%=":"imod",
    "&=":"iand","|=":"ior","^=":"ixor"
}

function $_SyntaxError(context,msg,indent){
    console.log('syntax error '+msg)
    var ctx_node = context
    while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
    var tree_node = ctx_node.node
    var module = tree_node.module
    var line_num = tree_node.line_num
    __BRYTHON__.line_info = [line_num,module]
    if(indent===undefined){
        if(msg.constructor===Array){__BRYTHON__.$SyntaxError(module,msg[0],$pos)}
        if(msg==="Triple string end not found"){
            // add an extra argument : used in interactive mode to
            // prompt for the rest of the triple-quoted string
            __BRYTHON__.$SyntaxError(module,'invalid syntax : triple string end not found',$pos)
        }
        __BRYTHON__.$SyntaxError(module,'invalid syntax',$pos)
    }else{throw __BRYTHON__.$IndentationError(module,msg,$pos)}
}

var $first_op_letter = []
for($op in $operators){
    if($first_op_letter.indexOf($op.charAt(0))==-1){
        $first_op_letter.push($op.charAt(0))
    }
}

function $Node(type){
    this.type = type
    this.children=[]
    this.add = function(child){
        this.children.push(child)
        child.parent = this
    }
    this.insert = function(pos,child){
        this.children.splice(pos,0,child)
        child.parent = this
    }
    this.toString = function(){return "<object 'Node'>"} 
    this.show = function(indent){
        var res = ''
        if(this.type==='module'){
            for(var i=0;i<this.children.length;i++){
                res += this.children[i].show(indent)
            }
        }else{
            indent = indent || 0
            for(var i=0;i<indent;i++){res+=' '}
            res += this.context
            if(this.children.length>0){res += '{'}
            res +='\n'
            for(var i=0;i<this.children.length;i++){
                res += '['+i+'] '+this.children[i].show(indent+4)
            }
            if(this.children.length>0){
                for(var i=0;i<indent;i++){res+=' '}
                res+='}\n'
            }
        }
        return res
   }
    this.to_js = function(indent){
        this.res = []
        this.unbound = []
        if(this.type==='module'){
            for(var i=0;i<this.children.length;i++){
                this.res.push(this.children[i].to_js(indent))
                this.children[i].js_index = this.res.length+0
            }
        }else{
            indent = indent || 0
            var ctx_js = this.context.to_js(indent)
            if(ctx_js){ // empty for "global x"
                for(var i=0;i<indent;i++){this.res.push(' ')}
                this.res.push(ctx_js)
                this.js_index = this.res.length+0
                if(this.children.length>0){this.res.push('{')}
                this.res.push('\n')
                for(var i=0;i<this.children.length;i++){
                    this.res.push(this.children[i].to_js(indent+4))
                    this.children[i].js_index = this.res.length+0
                }
                if(this.children.length>0){
                    for(var i=0;i<indent;i++){this.res.push(' ')}
                    this.res.push('}\n')
                }
            }
        }
        if(this.unbound.length>0){
            console.log('unbound '+this.unbound+' res length '+this.res.length)
            for(var i=0;i<this.res.length;i++){
                console.log('['+i+'] '+this.res[i])
            }
        }
        for(var i=0;i<this.unbound.length;i++){
            console.log('  '+this.unbound[i]+' '+this.res[this.unbound[i]])
        }
        return this.res.join('')
    }
    this.transform = function(rank){
        var res = ''
        if(this.type==='module'){
            // module doc string
            this.doc_string = $get_docstring(this)
            var i=0
            while(i<this.children.length){
                var node = this.children[i]
                this.children[i].transform(i)
                i++
            }
        }else{
            var elt=this.context.tree[0]
            if(elt.transform !== undefined){
                elt.transform(this,rank)
            }
            var i=0
            while(i<this.children.length){
                this.children[i].transform(i)
                i++
            }
        }
    }
    this.get_ctx = function(){return this.context}
}

var $loop_id=0

function $AbstractExprCtx(context,with_commas){
    this.type = 'abstract_expr'
    // allow expression with comma-separted values, or a single value ?
    this.with_commas = with_commas
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(abstract_expr '+with_commas+') '+this.tree}
    this.to_js = function(){
        if(this.type==='list'){return '['+$to_js(this.tree)+']'}
        else{return $to_js(this.tree)}
    }
}

function $AssertCtx(context){
    this.type = 'assert'
    this.toString = function(){return '(assert) '+this.tree}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.transform = function(node,rank){
        if(this.tree[0].type==='list_or_tuple'){
            // form "assert condition,message"
            var condition = this.tree[0].tree[0]
            var message = this.tree[0].tree[1]
        }else{
            var condition = this.tree[0]
            var message = null
        }
        // transform "assert cond" into "if not cond: throw AssertionError"
        var new_ctx = new $ConditionCtx(node.context,'if')
        var not_ctx = new $NotCtx(new_ctx)
        not_ctx.tree = [condition]
        node.context = new_ctx
        var new_node = new $Node('expression')
        var js = 'throw AssertionError("AssertionError")'
        if(message !== null){
            js = 'throw AssertionError(str('+message.to_js()+'))'
        }
        new $NodeJSCtx(new_node,js)
        node.add(new_node)
    }
}

function $AssignCtx(context){
    // context is the left operand of assignment
    this.type = 'assign'
    // replace parent by this in parent tree
    context.parent.tree.pop()
    context.parent.tree.push(this)
    this.parent = context.parent
    this.tree = [context]
    
    
    if(context.type=='expr' && context.tree[0].type=='call'){
        $_SyntaxError(context,["can't assign to function call "])
    }
    
    // An assignment in a function creates a local variable. If it was
    // referenced before, replace the statement where it was defined by an
    // UnboundLocalError
    if(context.type=='list_or_tuple'){
        for(var i=0;i<context.tree.length;i++){
            var assigned = context.tree[i].tree[0]
            if(assigned.type=='id'){
                var scope = $get_scope(this)
                if(scope.ntype=='def' || scope.ntype=='generator'){
                    $check_unbound(assigned,scope,assigned.value)
                }
            }else if(assigned.type=='call'){
                $_SyntaxError(context,["can't assign to function call"])
            }
        }
    }else if(context.type=='assign'){
        for(var i=0;i<context.tree.length;i++){
            var assigned = context.tree[i].tree[0]
            if(assigned.type=='id'){
                var scope = $get_scope(this)
                if(scope.ntype=='def' || scope.ntype=='generator'){
                    $check_unbound(assigned,scope,assigned.value)
                }
            }
        }
    }else{
        var assigned = context.tree[0]
        if(assigned && assigned.type=='id'){
            var scope = $get_scope(this)
            if(scope.ntype=='def' || scope.ntype=='generator'){
                $check_unbound(assigned,scope,assigned.value)
            }
        }
    }
    
    this.toString = function(){return '(assign) '+this.tree[0]+'='+this.tree[1]}
    this.transform = function(node,rank){
        // rank is the rank of this line in node
        var left = this.tree[0]
        while(left.type==='assign'){ 
            // chained assignment : x=y=z
            // transform current node to "y=z"
            // and add a new node "x=y"
            var new_node = new $Node('expression')
            var node_ctx = new $NodeCtx(new_node)
            node_ctx.tree = [left]
            node.parent.insert(rank+1,new_node)
            this.tree[0] = left.tree[1]
            left = this.tree[0]
        }
        var left_items = null
        if(left.type==='expr' && left.tree.length>1){
            var left_items = left.tree
        }else if(left.type==='expr' && 
            (left.tree[0].type==='list_or_tuple'||left.tree[0].type==='target_list')){
            var left_items = left.tree[0].tree
        }else if(left.type==='target_list'){
            var left_items = left.tree
        }else if(left.type==='list_or_tuple'){
            var left_items = left.tree
        }
        var right = this.tree[1]
        if(left_items===null){
            return
        }
        var right_items = null
        if(right.type==='list'||right.type==='tuple'||
            (right.type==='expr' && right.tree.length>1)){
                var right_items = right.tree
        }
        if(right_items!==null){ // form x,y=a,b
            if(right_items.length>left_items.length){
                throw Error('ValueError : too many values to unpack (expected '+left_items.length+')')
            }else if(right_items.length<left_items.length){
                throw Error('ValueError : need more than '+right_items.length+' to unpack')
            }
            var new_nodes = []
            // replace original line by dummy line : the next one might also
            // be a multiple assignment
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,'void(0)')
            new_nodes.push(new_node)
            
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,'var $temp'+$loop_num+'=[]')
            new_nodes.push(new_node)

            for(var i=0;i<right_items.length;i++){
                var js = '$temp'+$loop_num+'.push('+right_items[i].to_js()+')'
                var new_node = new $Node('expression')
                new $NodeJSCtx(new_node,js)
                new_nodes.push(new_node)
            }
            for(var i=0;i<left_items.length;i++){
                var new_node = new $Node('expression')
                var context = new $NodeCtx(new_node) // create ordinary node
                left_items[i].parent = context
                var assign = new $AssignCtx(left_items[i]) // assignment to left operand
                assign.tree[1] = new $JSCode('$temp'+$loop_num+'['+i+']')
                new_nodes.push(new_node)
            }
            node.parent.children.splice(rank,1) // remove original line
            for(var i=new_nodes.length-1;i>=0;i--){
                node.parent.insert(rank,new_nodes[i])
            }
            $loop_num++
        }else{ // form x,y=a
            // evaluate right argument (it might be a function call)
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,'var $right=iter('+right.to_js()+');var $counter=-1')
            var new_nodes = [new_node]
            
            var try_node = new $Node('expression')
            // we must set line_num and module to generate __BRYTHON__.line_info
            try_node.line_num = node.parent.children[rank].line_num
            try_node.module = node.parent.children[rank].module
            new $NodeJSCtx(try_node,'try')
            new_nodes.push(try_node)
                
            for(var i=0;i<left_items.length;i++){
                var new_node = new $Node('expression')
                new $NodeJSCtx(new_node,'$counter++')
                try_node.add(new_node)
                
                var new_node = new $Node('expression')
                var context = new $NodeCtx(new_node) // create ordinary node
                left_items[i].parent = context
                var assign = new $AssignCtx(left_items[i]) // assignment to left operand
                assign.tree[1] = new $JSCode('__builtins__.next($right)')
                try_node.add(new_node)
            }

            var catch_node = new $Node('expression')
            new $NodeJSCtx(catch_node,'catch($err'+$loop_num+')')
            new_nodes.push(catch_node)
            
            var catch_node1 = new $Node('expression')
            var js = 'if($err'+$loop_num+'.__name__=="StopIteration")'
            js += '{__BRYTHON__.$pop_exc();throw ValueError("need more than "+$counter+" value"+'
            js += '($counter>1 ? "s" : "")+" to unpack")}else{throw $err'+$loop_num+'};'
            new $NodeJSCtx(catch_node1,js)
            catch_node.add(catch_node1)
            
            // add a test to see if iterator is exhausted
            var exhausted = new $Node('expression')
            js = 'var $exhausted=true;try{__builtins__.next($right);$exhausted=false}'
            js += 'catch(err){if(err.__name__=="StopIteration"){__BRYTHON__.$pop_exc()}}'
            js += 'if(!$exhausted){throw ValueError('
            js += '"too many values to unpack (expected "+($counter+1)+")")}'
            new $NodeJSCtx(exhausted,js)
            new_nodes.push(exhausted)
            
            node.parent.children.splice(rank,1) // remove original line
            for(var i=new_nodes.length-1;i>=0;i--){
                node.parent.insert(rank,new_nodes[i])
            }
            $loop_num++
        }
    }
    this.to_js = function(){
        if(this.parent.type==='call'){ // like in foo(x=0)
            return '__BRYTHON__.$Kw('+this.tree[0].to_js()+','+this.tree[1].to_js()+')'
        }else{ // assignment
            var left = this.tree[0]
            if(left.type==='expr'){
                left=left.tree[0]
            }
            var right = this.tree[1]
            if(left.type==='attribute'){ // assign to attribute
                left.func = 'setattr'
                var res = left.to_js()
                left.func = 'getattr'
                res = res.substr(0,res.length-1) // remove trailing )
                res += ','+right.to_js()+');None;'
                return res
            }else if(left.type==='sub'){ // assign to item
                left.func = 'setitem' // just for to_js()
                var res = left.to_js()
                res = res.substr(0,res.length-1) // remove trailing )
                left.func = 'getitem' // restore default function
                res += ','+right.to_js()+');None;'
                return res
            }
            var scope = $get_scope(this)
            if(scope.ntype==="module"){
                var res = 'var '+left.to_js()
                //if(scope.module!=='__main__'){res = 'var '+res}
                if(left.to_js().charAt(0)!='$'){
                    res += '=$globals["'+left.to_js()+'"]'
                }
                res += '='+right.to_js()+';None;'
                return res
            }else if(scope.ntype==='def'||scope.ntype==="generator"){
                // assignment in a function : depends if variable is local
                // or global
                if(scope.globals && scope.globals.indexOf(left.value)>-1){
                    return left.to_js()+'=$globals["'+left.to_js()+'"]='+right.to_js()
                }else{ // local to scope : prepend 'var'
                    var scope_id = scope.context.tree[0].id
                    var locals = __BRYTHON__.scope[scope_id].locals
                    if(locals.indexOf(left.to_js())===-1){
                        locals.push(left.to_js())
                    }
                    var res = 'var '+left.to_js()+'='
                    res += '$locals["'+left.to_js()+'"]='
                    res += right.to_js()+';None;'
                    return res
                }
            }else if(scope.ntype==='class'){
                // assignment in a class : creates a class attribute
                left.is_left = true // used in to_js() for ids
                var attr = left.to_js()
                // Store the JS code in attribute 'in_class'
                // In the case of a chained assignment inside a class, eg
                //    class foo:
                //        a = b = 0
                // the assignment is split into "b = 0" then "a = b"
                // In the second assignment, the JS rendering of b must be
                // the same as in the first assignment, ie "$class.b"
                left.in_class = '$class.'+attr
                return '$class.'+attr+'='+right.to_js()
            }
        }
    }
}

function $AttrCtx(context){
    this.type = 'attribute'
    this.value = context.tree[0]
    this.parent = context
    context.tree.pop()
    context.tree.push(this)
    this.tree = []
    this.func = 'getattr' // becomes setattr for an assignment 
    this.toString = function(){return '(attr) '+this.value+'.'+this.name}
    this.to_js = function(){
        var name = this.name
        return this.func+'('+this.value.to_js()+',"'+name+'")'
    }
}

function $BodyCtx(context){
    // inline body for def, class, if, elif, else, try...
    // creates a new node, child of context node
    var ctx_node = context.parent
    while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
    var tree_node = ctx_node.node
    var body_node = new $Node('expression')
    tree_node.insert(0,body_node)
    return new $NodeCtx(body_node)
}

function $BreakCtx(context){
    // used for the keyword "break"
    // a flag is associated to the enclosing "for" or "while" loop
    // if the loop exits with a break, this flag is set to true
    // so that the "else" clause of the loop, if present, is executed
    
    
    this.type = 'break'
    this.toString = function(){return 'break '}
    this.parent = context
    context.tree.push(this)

    // get loop context
    var ctx_node = context
    while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
    var tree_node = ctx_node.node
    var loop_node = tree_node.parent
    while(true){
        if(loop_node.type==='module'){
            // "break" is not inside a loop
            $_SyntaxError(context,'break outside of a loop')
        }else{
            var ctx = loop_node.context.tree[0]
            if(ctx.type==='for' || (ctx.type==='condition' && ctx.token==='while')){
                this.loop_ctx = ctx
                break
            }else if(['def','generator','class'].indexOf(ctx.type)>-1){
                // "break" must not be inside a def or class, even if they are
                // enclosed in a loop
                $_SyntaxError(context,'break outside of a loop')        
            }else{
                loop_node=loop_node.parent
            }
        }
    }

    this.to_js = function(){
        return 'var $no_break'+this.loop_ctx.loop_num+'=false;break'
    }
}

function $CallArgCtx(context){
    this.type = 'call_arg'
    this.toString = function(){return 'call_arg '+this.tree}
    this.parent = context
    this.start = $pos
    this.tree = []
    context.tree.push(this)
    this.expect='id'
    this.to_js = function(){return $to_js(this.tree)}
}

function $CallCtx(context){
    this.type = 'call'
    this.func = context.tree[0]
    if(this.func!==undefined){ // undefined for lambda
        this.func.parent = this
    }
    this.parent = context
    if(context.type!='class'){
        context.tree.pop()
        context.tree.push(this)
    }else{
        // class parameters
        context.args = this
    }
    this.tree = []
    this.start = $pos

    this.toString = function(){return '(call) '+this.func+'('+this.tree+')'}

    this.to_js = function(){
        if(this.tree.length>0){
            if(this.tree[this.tree.length-1].tree.length==0){
                // from "foo(x,)"
                this.tree.pop()
            }
        }
        if(this.func!==undefined && 
            ['eval','exec'].indexOf(this.func.value)>-1){
            // get module
            var ctx_node = this
            while(ctx_node.parent!==undefined){ctx_node=ctx_node.parent}
            var module = ctx_node.node.module
            arg = this.tree[0].to_js()
            var ns = ''
            var _name = module+',exec_'+Math.random().toString(36).substr(2,8)
            if(this.tree.length>1){
                var arg2 = this.tree[1]
                if(arg2.tree!==undefined&&arg2.tree.length>0){
                    arg2 = arg2.tree[0]
                }
                if(arg2.tree!==undefined&&arg2.tree.length>0){
                    arg2 = arg2.tree[0]
                }
                if(arg2.type==='call'){
                    if(arg2.func.value==='globals'){
                        // exec in globals
                        ns = 'globals'
                        _name = module
                    }
                }else if(arg2.type==='id'){
                    ns = arg2.value
                }
            }
            __BRYTHON__.$py_module_path[_name] = __BRYTHON__.$py_module_path[module]
            // replace by the result of an anonymous function with a try/except clause
            var res = '(function(){try{'
            // insert globals and locals in the function
            res += '\nfor(var $attr in $globals){eval("var "+$attr+"=$globals[$attr]")};'
            res += '\nfor(var $attr in $locals){eval("var "+$attr+"=$locals[$attr]")};'
            // if an argument namespace is passed, insert it
            if(ns!=='' && ns!=='globals'){
                res += '\nfor(var $i=0;$i<'+ns+'.$keys.length;$i++){'
                res += 'eval("var "+'+ns+'.$keys[$i]+"='+ns+'.$values[$i]")};'
            }
            // execute the Python code and return its result
            // the namespace built inside the function will be in
            // __BRYTHON__.scope[_name].__dict__
            res += 'var $jscode = __BRYTHON__.py2js('+arg+',"'+_name+'").to_js();'
            res += 'if(__BRYTHON__.debug>1){console.log($jscode)};'
            res += 'var $res = eval($jscode);'
            res += 'if($res===undefined){return None};return $res'
            res += '}catch(err){throw __BRYTHON__.exception(err)}'
            res += '})()'
            if(ns==='globals'){
                // copy the execution namespace in module and global namespace
                res += ';for(var $attr in __BRYTHON__.scope["'+_name+'"].__dict__)'
                res += '{window[$attr]=$globals[$attr]='
                res += '__BRYTHON__.scope["'+_name+'"].__dict__[$attr]}'
            }else if(ns !=''){
                // use specified namespace
                res += ';for(var $attr in __BRYTHON__.scope["'+_name+'"].__dict__)'
                res += '{__builtins__.dict.$dict.__setitem__('+ns+',$attr,__BRYTHON__.scope["'+_name+'"].__dict__[$attr])}'            
            }else{
                // namespace not specified copy the execution namespace in module namespace
                res += ';for(var $attr in __BRYTHON__.scope["'+_name+'"].__dict__){'
                // check that $attr is a valid identifier
                res += '\nif($attr.search(/[\.]/)>-1){continue}\n'
                res += 'eval("var "+$attr+"='
                res += '$globals[$attr]='
                res += '__BRYTHON__.scope[\\"'+_name+'\\"].__dict__[$attr]")}'
            }
            return res
        }else if(this.func!==undefined && this.func.value === 'classmethod'){
            return 'classmethod($class,'+$to_js(this.tree)+')'
        }else if(this.func!==undefined && this.func.value ==='locals'){
            var scope = $get_scope(this),mod = $get_module(this)
            if(scope !== null && (scope.ntype==='def'||scope.ntype=='generator')){
                return 'locals("'+scope.context.tree[0].id+'","'+mod.module+'")'
            }
        }else if(this.func!==undefined && this.func.value ==='globals'){
            var ctx_node = this
            while(ctx_node.parent!==undefined){ctx_node=ctx_node.parent}
            var module = ctx_node.node.module
            return 'globals("'+module+'")'
        }else if(this.func!==undefined && this.func.value ==='dir'){
            if(this.tree.length==0){
                // dir() : pass arguments (null,module name)
                var mod=$get_module(this)
                return 'dir(null,"'+mod.module+'")'                
            }
        }else if(this.func!==undefined && this.func.value=='$$super'){
            if(this.tree.length==0){
                // super() called with no argument : if inside a class, add the
                // class parent as first argument
                var scope = $get_scope(this)
                if(scope.ntype=='def' || scope.ntype=='generator'){
                    if(scope.parent && scope.parent.context.tree[0].type=='class'){
                        new $IdCtx(this,scope.parent.context.tree[0].name)
                    }
                }
            }
        }
        else if(this.func!==undefined && this.func.type=='unary'){
            // form " -(x+2) "
            var op = this.func.op
            if(op=='+'){return $to_js(this.tree)}
            else if(op=='-'){return 'getattr('+$to_js(this.tree)+',"__neg__")()'}
            else if(op=='~'){return 'getattr('+$to_js(this.tree)+',"__invert__")()'}
        }
        if(this.tree.length>0){
            return 'getattr('+this.func.to_js()+',"__call__")('+$to_js(this.tree)+')'
        }else{return 'getattr('+this.func.to_js()+',"__call__")()'}
    }
}

function $ClassCtx(context){
    this.type = 'class'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.expect = 'id'
    this.toString = function(){return '(class) '+this.name+' '+this.tree+' args '+this.args}
    this.transform = function(node,rank){
        
        // for an unknown reason, code like
        //
        // for base in foo:
        //    class Int:
        //        A=9
        //
        // generates the class declaration twice. To avoid this we use
        // a flag this.transformed
        if(this.transformed){return}
        // doc string
        this.doc_string = $get_docstring(node)

        // insert "$class = new Object"
        var instance_decl = new $Node('expression')
        new $NodeJSCtx(instance_decl,'var $class = {$def_line:__BRYTHON__.line_info}')
        node.insert(0,instance_decl)

        // return $class at the end of class definition
        var ret_obj = new $Node('expression')
        new $NodeJSCtx(ret_obj,'return $class')
        node.insert(node.children.length,ret_obj) 
       
        // close function and run it
        var run_func = new $Node('expression')
        new $NodeJSCtx(run_func,')()')
        node.parent.insert(rank+1,run_func)

        // add doc string
        rank++
        js = '$'+this.name+'.__doc__='+(this.doc_string || 'None')
        var ds_node = new $Node('expression')
        new $NodeJSCtx(ds_node,js)
        node.parent.insert(rank+1,ds_node)       

        // add attribute __module__
        rank++
        js = '$'+this.name+'.__module__="'+$get_module(this).module+'"'
        var mod_node = new $Node('expression')
        new $NodeJSCtx(mod_node,js)
        node.parent.insert(rank+1,mod_node)  

        // class constructor
        var scope = $get_scope(this)
        if(scope.ntype==="module"||scope.ntype!=='class'){
            js = 'var '+this.name
        }else{
            js = 'var '+this.name+' = $class.'+this.name
        }
        js += '=__BRYTHON__.$class_constructor("'+this.name+'",$'+this.name
        if(this.args!==undefined){ // class def has arguments
            var arg_tree = this.args.tree,args=[],kw=[]

                for(var i=0;i<arg_tree.length;i++){
                    if(arg_tree[i].tree[0].type=='kwarg'){kw.push(arg_tree[i].tree[0])}
                    else{args.push(arg_tree[i].to_js())}
                }
                js += ',tuple(['+args.join(',')+']),['
                // add the names - needed to raise exception if a value is undefined
                for(var i=0;i<args.length;i++){
                    js += '"'+args[i].replace(new RegExp('"','g'),'\\"')+'"'
                    if(i<args.length-1){js += ','}
                }
                js += ']'

                js+=',['
                for(var i=0;i<kw.length;i++){
                    js+='["'+kw[i].tree[0].value+'",'+kw[i].tree[1].to_js()+']'
                    if(i<kw.length-1){js+=','}
                }
                js+=']'

        }else{ // form "class foo:"
            js += ',tuple([]),[],[]'
        }
        js += ')'
        var cl_cons = new $Node('expression')
        new $NodeJSCtx(cl_cons,js)
        node.parent.insert(rank+2,cl_cons)
        
        // if class is defined at module level, add to module namespace
        if(scope.ntype==='module'){
            js = '__BRYTHON__.scope["'+scope.module+'"].__dict__["'
            js += this.name+'"]='+this.name
            var w_decl = new $Node('expression')
            new $NodeJSCtx(w_decl,js)
            node.parent.insert(rank+3,w_decl)
            rank++
        }
        // end by None for interactive interpreter
        var end_node = new $Node('expression')
        new $NodeJSCtx(end_node,'None;')
        node.parent.insert(rank+3,end_node)

        this.transformed = true
                
    }
    this.to_js = function(){
        return 'var $'+this.name+'=(function()'
    }
}

function $CompIfCtx(context){
    this.type = 'comp_if'
    context.parent.intervals.push($pos)
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(comp if) '+this.tree}
    this.to_js = function(){return $to_js(this.tree)}
}

function $ComprehensionCtx(context){
    this.type = 'comprehension'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(comprehension) '+this.tree}
    this.to_js = function(){
        var intervals = []
        for(var i=0;i<this.tree.length;i++){
            intervals.push(this.tree[i].start)
        }
        return intervals
    }
}

function $CompForCtx(context){
    this.type = 'comp_for'
    context.parent.intervals.push($pos)
    this.parent = context
    this.tree = []
    this.expect = 'in'
    context.tree.push(this)
    this.toString = function(){return '(comp for) '+this.tree}
    this.to_js = function(){return $to_js(this.tree)}
}

function $CompIterableCtx(context){
    this.type = 'comp_iterable'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(comp iter) '+this.tree}
    this.to_js = function(){return $to_js(this.tree)}
}

function $ConditionCtx(context,token){
    this.type = 'condition'
    this.token = token
    this.parent = context
    this.tree = []
    if(token==='while'){this.loop_num=$loop_num;$loop_num++}
    context.tree.push(this)
    this.toString = function(){return this.token+' '+this.tree}
    this.to_js = function(){
        var tok = this.token
        if(tok==='elif'){tok='else if'}
        // in a "while" loop, insert a flag initially set to false
        // if the loop exits with a "break" this flag will be set to
        // true so that an optional "else" clause will not be run
        if(tok==='while'){tok = 'var $no_break'+this.loop_num+'=true;'+tok}
        if(this.tree.length==1){
            var res = tok+'(bool('+$to_js(this.tree)+'))'
        }else{ // syntax "if cond : do_something" in the same line
            var res = tok+'(bool('+this.tree[0].to_js()+'))'
            if(this.tree[1].tree.length>0){
                res += '{'+this.tree[1].to_js()+'}'
            }
        }
        return res
    }
}

function $DecoratorCtx(context){
    this.type = 'decorator'
    this.parent = context
    context.tree.push(this)
    this.tree = []
    this.toString = function(){return '(decorator) '+this.tree}
    this.transform = function(node,rank){
        var func_rank=rank+1,children=node.parent.children
        var decorators = [this.tree]
        while(true){
            if(func_rank>=children.length){$_SyntaxError(context)}
            else if(children[func_rank].context.tree[0].type==='decorator'){
                decorators.push(children[func_rank].context.tree[0].tree)
                children.splice(func_rank,1)
            }else{break}
        }
        // Associate a random variable name to each decorator
        // In a code such as 
        // class Cl(object):
        //      def __init__(self):
        //          self._x = None
        //    
        //      @property
        //      def x(self):
        //          return self._x
        //    
        //      @x.setter
        //      def x(self, value):
        //          self._x = value
        //
        // we can't replace the decorated methods by something like
        //
        //      def x(self):
        //          return self._x
        //      x = property(x)      # [1]
        //
        //      def x(self,value):   # [2]
        //          self._x = value
        //      x = x.setter(x)      # [3]
        //
        // because when we want to use x.setter in [3], x is no longer the one
        // defined in [1] : it has been reset by the function declaration in [2]
        // The technique used here is to replace these lines by :
        //
        //      $vth93h6g = property # random variable name
        //      def x(self):
        //          return self._x
        //      x = $vth93h6g(x)
        //    
        //      $h3upb5s8 = x.setter
        //      def x(self, value):
        //          self._x = value
        //      x = $h3upb5s8(x)
        //
        this.dec_ids = []
        for(var i=0;i<decorators.length;i++){
            this.dec_ids.push('$'+Math.random().toString(36).substr(2,8))
        }
        var obj = children[func_rank].context.tree[0]
        // add a line after decorated element
        var callable = children[func_rank].context
        var res = obj.name+'=',tail=''
        var scope = $get_scope(this)
        if(scope !==null && scope.ntype==='class'){
            res = '$class.'+obj.name+'='
        }
        for(var i=0;i<decorators.length;i++){
            var dec = this.dec_ids[i] //$to_js(decorators[i]);
            res += dec+'('
            if (decorators[i][0].tree[0].value == 'classmethod') { res+= '$class,'}
            tail +=')'
        }
        res += (scope.ntype ==='class' ? '$class.' : '')
        res += obj.name+tail
        var decor_node = new $Node('expression')
        new $NodeJSCtx(decor_node,res)
        node.parent.children.splice(func_rank+1,0,decor_node)
        this.decorators = decorators
    }
    this.to_js = function(){
        var res = ''
        for(var i=0;i<this.decorators.length;i++){
            res += this.dec_ids[i]+'='+$to_js(this.decorators[i])+';'
        }
        return res
    }
}
function $DefCtx(context){
    this.type = 'def'
    this.name = null
    this.parent = context
    this.tree = []
    this.id = Math.random().toString(36).substr(2,8)
    __BRYTHON__.scope[this.id] = this
    this.locals = []
    context.tree.push(this)

    // store id of enclosing functions
    this.enclosing = []
    var scope = $get_scope(this)
    while(true){
        if(scope.ntype=='def' || scope.ntype=='generator'){
            this.enclosing.push(scope.context.tree[0].id)
            scope = $get_scope(scope.context.tree[0])
        }else{break}
    }
        
    this.set_name = function(name){
        this.name = name
        // if function is defined inside another function, add the name
        // to local names
        var scope = $get_scope(this)
        if(scope.ntype=='def' || scope.ntype=='generator'){
            if(scope.context.tree[0].locals.indexOf(name)==-1){
                scope.context.tree[0].locals.push(name)
            }
        }
    }
    
    this.toString = function(){return 'def '+this.name+'('+this.tree+')'}
    this.transform = function(node,rank){
        // already transformed ?
        if(this.transformed!==undefined){return}
        // search doc string
        this.doc_string = $get_docstring(node)
        this.rank = rank // save rank if we must add generator declaration
        // if function inside a class, the first argument represents
        // the instance
        var scope = $get_scope(this)
        var required = ''
        var defaults = [],defs=[],defs1=[]
        var after_star = []
        var other_args = null
        var other_kw = null
        var env = []
        for(var i=0;i<this.tree[0].tree.length;i++){
            var arg = this.tree[0].tree[i]
            if(arg.type==='func_arg_id'){
                if(arg.tree.length===0){
                    if(other_args==null){
                        required+='"'+arg.name+'",'
                    }else{
                        after_star.push('"'+arg.name+'"')
                    }
                }else{
                    defaults.push('"'+arg.name+'"')
                    defs.push(arg.name+' = '+$to_js(arg.tree))
                    defs1.push(arg.name+':'+$to_js(arg.tree))
                    if(arg.tree[0].type==='expr' 
                        && arg.tree[0].tree[0].type==='id'){
                        env.push(arg.tree[0].tree[0].value)
                    }                        
                }
            }else if(arg.type==='func_star_arg'&&arg.op==='*'){other_args='"'+arg.name+'"'}
            else if(arg.type==='func_star_arg'&&arg.op==='**'){other_kw='"'+arg.name+'"'}
        }
        this.env = env
        this.defs = defs
        if(required.length>0){required=required.substr(0,required.length-1)}
        //if(defaults.length>0){defaults=defaults.substr(0,defaults.length-1)}

        var nodes = []
        // add lines of code to node children
        var js = 'var $locals = __BRYTHON__.scope["'+this.id+'"].__dict__={}'
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        nodes.push(new_node)

        // initialize default variables
        var js = 'for(var $var in $defaults){eval("var "+$var+"=$locals[$var]=$defaults[$var]")}'
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        nodes.push(new_node)
        
        for(var i=this.enclosing.length-1;i>=0;i--){
            var js = 'var $ns=__BRYTHON__.scope["'+this.enclosing[i]+'"].__dict__'
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,js)
            nodes.push(new_node)

            var js = 'for(var $var in $ns){$locals[$var]=$ns[$var]}'
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,js)
            nodes.push(new_node)
        }

        var js = 'var $ns=__BRYTHON__.$MakeArgs("'+this.name+'",arguments,['+required+'],'
        js += '['+defaults.join(',')+'],'+other_args+','+other_kw+',['+after_star.join(',')+'])'
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        nodes.push(new_node)

        var js = 'for(var $var in $ns){eval("var "+$var+"=$ns[$var]");'
        js += '$locals[$var]=$ns[$var]}'
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        nodes.push(new_node)

        for(var i=nodes.length-1;i>=0;i--){
            node.children.splice(0,0,nodes[i])
        }

        var def_func_node = new $Node('expression')
        new $NodeJSCtx(def_func_node,'return function()')

        // wrap function body in a try/catch
        var try_node = new $Node('expression')
        new $NodeJSCtx(try_node,'try')

        for(var i=0;i<node.children.length;i++){
            try_node.add(node.children[i])
        }

        def_func_node.add(try_node)

        var catch_node = new $Node('expression')
        var js = 'catch(err'+$loop_num+')'
        js += '{throw __BRYTHON__.exception(err'+$loop_num+')}'
        new $NodeJSCtx(catch_node,js)
        node.children = []
        def_func_node.add(catch_node)
        
        node.add(def_func_node)

        var ret_node = new $Node('expression')
        var txt = ')('
        for(var i=0;i<this.env.length;i++){
            if(scope.ntype=='class'){
                txt += '$class.'+this.env[i]+' != undefined ? '
                txt += '$class.'+this.env[i]+' : '
            }
            txt += this.env[i]
            if(i<this.env.length-1){txt += ','}
        }
        new $NodeJSCtx(ret_node,txt+')')
        node.parent.insert(rank+1,ret_node)
        
        var offset = 2
        
        // add function name
        js = this.name+'.__name__'
        if(scope.ntype==='class'){
            js = '$class.'+this.name+'.__name__'
        }
        js += '="'+this.name+'"'
        if(scope.ntype==='def'){
            // add to $locals
            js += ';$locals["'+this.name+'"]='+this.name
        }
        var name_decl = new $Node('expression')
        new $NodeJSCtx(name_decl,js)
        node.parent.children.splice(rank+offset,0,name_decl)
        offset++

        // if function is defined at module level, add to module scope
        if(scope.ntype==='module'){
            js = '$globals["'+this.name+'"]='+this.name
            js += ';'+this.name+".$type='function'"
            new_node = new $Node('expression')
            new $NodeJSCtx(new_node,js)
            node.parent.children.splice(rank+offset,0,new_node)
            offset++
        }
        // add attribute __module__
        var module = $get_module(this)
        var prefix = scope.ntype=='class' ? '$class.' : ''
        
        js = prefix+this.name+'.__module__ = "'+module.module+'"'
        new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        node.parent.children.splice(rank+offset,0,new_node)
        offset++
        
        // if doc string, add it as attribute __doc__
        js = prefix+this.name+'.__doc__='+(this.doc_string || 'None')
        new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        node.parent.children.splice(rank+offset,0,new_node)
        offset++

        // add attribute __code__
        js = prefix+this.name+'.__code__= {__class__:__BRYTHON__.$CodeDict}'
        js += ';None;' // end with None for interactive interpreter
        new_node = new $Node('expression')
        new $NodeJSCtx(new_node,js)
        node.parent.children.splice(rank+offset,0,new_node)
        offset++

        // define default values
        var default_node = new $Node('expression')
        new $NodeJSCtx(default_node,'var $defaults = {'+defs1.join(',')+'}')
        node.insert(0,default_node)
                
        this.transformed = true
    }
    this.add_generator_declaration = function(){
        // if generator, add line 'foo = __BRYTHON__.$generator($foo)'
        var scope = $get_scope(this)
        var node = this.parent.node
        if(this.type==='generator' && !this.declared){
            var offset = 2
            if(this.decorators !== undefined){offset++}
            js = '__BRYTHON__.$generator('
            if(scope.ntype==='class'){js += '$class.'}
            js += '$'+this.name+')'
            var gen_node = new $Node('expression')
            var ctx = new $NodeCtx(gen_node)
            var expr = new $ExprCtx(ctx,'id',false)
            var name_ctx = new $IdCtx(expr,this.name)
            var assign = new $AssignCtx(expr)
            var expr1 = new $ExprCtx(assign,'id',false)
            var js_ctx = new $NodeJSCtx(assign,js)
            expr1.tree.push(js_ctx)
            node.parent.insert(this.rank+offset,gen_node) 
            this.declared = true
        }
    }

    this.to_js = function(){
        var scope = $get_scope(this)
        var name = this.name
        if(this.type==='generator'){name='$'+name}
        if(scope.ntype==="module" || scope.ntype!=='class'){
            res = 'var '+name+'= (function ('
        }else{
            res = '$class.'+name+'= (function ('
        }
        for(var i=0;i<this.env.length;i++){
            res+=this.env[i]
            if(i<this.env.length-1){res+=','}
        }
        res += ')'
        return res
    }
}

function $DelCtx(context){
    this.type = 'del'
    this.parent = context
    context.tree.push(this)
    this.tree = []
    this.toString = function(){return 'del '+this.tree}
    this.to_js = function(){
        if(this.tree[0].type=='list_or_tuple'){
            var res = ''
            for(var i=0;i<this.tree[0].tree.length;i++){
                var subdel = new $DelCtx(context) // this adds an element to context.tree
                subdel.tree = [this.tree[0].tree[i]]
                res += subdel.to_js()+';'
                context.tree.pop() // remove the element from context.tree
            }
            this.tree = []
            return res
        }else{
            var expr = this.tree[0].tree[0]
            var scope = $get_scope(this)
            if(expr.type==='id'){
                var js = 'delete '+expr.to_js()+';'
                // remove name from dictionaries
                if(scope.ntype==='module'){
                    js+='delete $globals["'+expr.to_js()+'"]'
                }else if(scope.ntype==="def"||scope.ntype==="generator"){
                    if(scope.globals && scope.globals.indexOf(expr.to_js())>-1){
                        // global variable
                        js+='delete $globals["'+expr.to_js()+'"]'
                    }else{ // local variable
                        js+='delete $locals["'+expr.to_js()+'"]'
                    }
                }
                return js
            }else if(expr.type==='sub'){
                expr.func = 'delitem'
                js = expr.to_js()
                expr.func = 'getitem'
                return js
            }else{
                if(expr.type==='op'){
                    $_SyntaxError(this,["can't delete operator"])
                }else if(expr.type==='call'){
                    $_SyntaxError(this,["can't delete function call"])
                }else if(expr.type==='attribute'){
                    return 'delattr('+expr.value.to_js()+',"'+expr.name+'")'
                }else{
                    $_SyntaxError(this,["can't delete "+expr.type])
                }
            }
        }
    }
}

function $DictOrSetCtx(context){
    // the real type (dist or set) is set inside $transition
    // as attribute 'real'
    this.type = 'dict_or_set'
    this.real = 'dict_or_set'
    this.expect = 'id'
    this.closed = false
    this.start = $pos
    this.toString = function(){
        if(this.real==='dict'){return '(dict) {'+this.items+'}'}
        else if(this.real==='set'){return '(set) {'+this.tree+'}'}
        else{return '(dict_or_set) {'+this.tree+'}'}
    }
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){
        if(this.real==='dict'){
            var res = '__BRYTHON__.$dict(['
            for(var i=0;i<this.items.length;i+=2){
                res+='['+this.items[i].to_js()+','+this.items[i+1].to_js()+']'
                if(i<this.items.length-2){res+=','}
            }
            return res+'])'+$to_js(this.tree)
        }else if(this.real==='set_comp'){return 'set('+$to_js(this.items)+')'+$to_js(this.tree)}
        else if(this.real==='dict_comp'){
            var key_items = this.items[0].expression[0].to_js()
            var value_items = this.items[0].expression[1].to_js()
            return '__BRYTHON__.$dict('+$to_js(this.items)+')'+$to_js(this.tree)
        }else{return 'set(['+$to_js(this.items)+'])'+$to_js(this.tree)}
    }
}

function $DoubleStarArgCtx(context){
    this.type = 'double_star_arg'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '**'+this.tree}
    this.to_js = function(){return '__BRYTHON__.$pdict('+$to_js(this.tree)+')'}
}

function $ExceptCtx(context){
    this.type = 'except'
    this.parent = context
    context.tree.push(this)
    this.tree = []
    this.expect = 'id'
    this.toString = function(){return '(except) '}
    this.to_js = function(){
        // in method "transform" of $TryCtx instances, related
        // $ExceptCtx instances receive an attribute __name__
        if(this.tree.length===0){return 'else'}
        else if(this.tree.length===1 && this.tree[0].name==='Exception'){
            return 'else if(true)'
        }else{
            var res ='else if(__BRYTHON__.is_exc('+this.error_name+',['
            for(var i=0;i<this.tree.length;i++){
                res+=this.tree[i].to_js()
                if(i<this.tree.length-1){res+=','}
            }
            res +=']))'
            return res
        }
    }
}

function $ExprCtx(context,name,with_commas){
    this.type = 'expr'
    this.name = name
    // allow expression with comma-separted values, or a single value ?
    this.with_commas = with_commas
    this.expect = ',' // can be 'expr' or ','
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(expr '+with_commas+') '+this.tree}
    this.to_js = function(arg){
        if(this.type==='list'){return '['+$to_js(this.tree)+']'}
        else if(this.tree.length===1){return this.tree[0].to_js(arg)}
        else{return 'tuple('+$to_js(this.tree)+')'}
    }
}

function $ExprNot(context){ // used for 'x not', only accepts 'in' as next token
    this.type = 'expr_not'
    this.toString = function(){return '(expr_not)'}
    this.parent = context
    this.tree = []
    context.tree.push(this)
}

function $FloatCtx(context,value){
    this.type = 'float'
    this.value = value
    this.toString = function(){return 'float '+this.value}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){return 'float('+this.value+')'}
}

function $ForTarget(context){
    this.type = 'for_target'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return 'for_target'+' '+this.tree}
    this.to_js = function(){return $to_js(this.tree)}
}

function $ForExpr(context){
    this.type = 'for'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.loop_num = $loop_num
    this.toString = function(){return '(for) '+this.tree}
    this.transform = function(node,rank){
        var new_nodes = []
        
        // node to create a temporary variable set to iter(iterable)
        var new_node = new $Node('expression')
        var target = this.tree[0]
        var iterable = this.tree[1]
        this.loop_num = $loop_num
        new_node.line_num = node.line_num
        new_node.module = node.module
        var js = 'var $next'+$loop_num+'=getattr(iter('+iterable.to_js()
        js += '),"__next__")'
        new $NodeJSCtx(new_node,js)
        new_nodes.push(new_node)

        new_node = new $Node('expression')
        var js = 'var $no_break'+$loop_num+'=true;while(true)'
        new $NodeJSCtx(new_node,js)
        new_node.context.loop_num = $loop_num // used for "else" clauses
        new_nodes.push(new_node)

        // save original node children
        var children = node.children
        // replace original line by these 2 lines
        node.parent.children.splice(rank,1)
        for(var i=new_nodes.length-1;i>=0;i--){
            node.parent.insert(rank,new_nodes[i])
        }

        // add lines to get next item in iterator, or exit the loop
        // if __next__ raises StopIteration
        var try_node = new $Node('expression')
        new $NodeJSCtx(try_node,'try')
        node.insert(0,try_node)

        var iter_node = new $Node('expression')
        var context = new $NodeCtx(iter_node) // create ordinary node
        var target_expr = new $ExprCtx(context,'left',true)
        target_expr.tree = target.tree
        var assign = new $AssignCtx(target_expr) // assignment to left operand
        assign.tree[1] = new $JSCode('$next'+$loop_num+'()')
        try_node.add(iter_node)

        var catch_node = new $Node('expression')
        var js = 'catch($err){if(__BRYTHON__.is_exc($err,[__builtins__.StopIteration])){__BRYTHON__.$pop_exc();break}'
        js += 'else{throw($err)}}'
        new $NodeJSCtx(catch_node,js)
        node.insert(1,catch_node)

        // set new loop children
        node.parent.children[rank+1].children = children
        $loop_num++
    }
    this.to_js = function(){
        var iterable = this.tree.pop()
        return 'for '+$to_js(this.tree)+' in '+iterable.to_js()
    }
}

function $FromCtx(context){
    this.type = 'from'
    this.parent = context
    this.module = ''
    this.names = []
    this.aliases = {}
    context.tree.push(this)
    this.expect = 'module'
    this.toString = function(){
        var res = '(from) '+this.module+' (import) '+this.names 
        res += '(as)' + this.aliases
        return res
    }
    this.to_js = function(){
        var scope = $get_scope(this)
        var mod = $get_module(this).module
        if(mod.substr(0,13)==='__main__,exec'){mod='__main__'}
        var path = __BRYTHON__.$py_module_path[mod]
        var elts = path.split('/')
        elts.pop()
        path =elts.join('/')
        // temporarily add module path to __BRYTHON__.path
        var res = ''
        var indent = $get_node(this).indent
        var head = ''
        for(var i=0;i<indent;i++){head += ' '}

        if (this.module.charAt(0)=='.'){
            // intra-package reference : "from . import x"
            // get the name of current module
            var parent_module = $get_module(this).module
            // get the url of current module
            var parent_path = __BRYTHON__.$py_module_path[parent_module]
            // split it into parts
            var search_path_parts = parent_path.split('/')
            // remove as many parts as the number of leading dots
            var mod = this.module
            while(mod && mod.charAt(0)=='.'){
               search_path_parts.pop()
               mod = mod.substr(1)
            }
            if(mod){
               search_path_parts.push(mod)
            }
            var search_path = search_path_parts.join('/')
            res +="$mod=__BRYTHON__.$import_list_intra('"+this.module+"','"
            res += __BRYTHON__.$py_module_path[parent_module]
            res += "',["
            for(var i=0;i<this.names.length;i++){
                res += '"'+this.names[i]+'",'
            }
            res += '])\n'+head
            for(var i=0;i<this.names.length;i++){
                if(['def','class','module'].indexOf(scope.ntype)>-1){
                    res += 'var '
                }
                var alias = this.aliases[this.names[i]]||this.names[i]
                res += alias
                if(scope.ntype == 'def'){
                    res += '=$locals["'+alias+'"]'
                }else if(scope.ntype=='module'){
                    res += '=$globals["'+alias+'"]'
                }          
                res += '=getattr($mod,"'+this.names[i]+'")\n'
            }
        }else{
           if(this.names[0]=='*'){
             res += '__BRYTHON__.$import("'+this.module+'","'+mod+'")\n'
             res += head+'var $mod=__BRYTHON__.imported["'+this.module+'"]\n'
             res += head+'for(var $attr in $mod){\n'
             res +="if($attr.substr(0,1)!=='_')\n"+head+"{var $x = 'var '+$attr+'"
              if(scope.ntype==="module"){
                  res += '=__BRYTHON__.scope["'+scope.module+'"].__dict__["'+"'+$attr+'"+'"]'
              }
             res += '=$mod["'+"'+$attr+'"+'"]'+"'"+'\n'+head+'eval($x)}}'
           }else{
             res += '__BRYTHON__.$import_from("'+this.module+'",['
             for(var i=0;i<this.names.length;i++){
                 res += '"'+this.names[i]+'",'
             }
             res += '],"'+mod+'");\n'
             for(var i=0;i<this.names.length;i++){
                res += head+'try{var '+(this.aliases[this.names[i]]||this.names[i])
                if(scope.ntype==="module"){
                    res += '=$globals["'
                    res += this.aliases[this.names[i]]||this.names[i]
                    res += '"]'
                }
                res += '=getattr(__BRYTHON__.imported["'+this.module+'"],"'+this.names[i]+'")}\n'
                res += 'catch($err'+$loop_num+'){if($err'+$loop_num+'.__class__'
                res += '===__builtins__.AttributeError.$dict){$err'+$loop_num+'.__class__'
                res += '=__builtins__.ImportError.$dict};throw $err'+$loop_num+'};'
             }
           }
        }
        res += '\n'+head+'None;'
        return res
    }
}

function $FuncArgs(context){
    this.type = 'func_args'
    this.parent = context
    this.tree = []
    this.names = []
    context.tree.push(this)
    this.toString = function(){return 'func args '+this.tree}
    this.expect = 'id'
    this.has_default = false
    this.has_star_arg = false
    this.has_kw_arg = false
    this.to_js = function(){return $to_js(this.tree)}
}

function $FuncArgIdCtx(context,name){
    // id in function arguments
    // may be followed by = for default value
    this.type = 'func_arg_id'
    this.name = name
    this.parent = context
    this.parent.names.push(name)
    this.tree = []
    context.tree.push(this)
    // add to locals of function
    var ctx = context
    while(ctx.parent!==undefined){
        if(ctx.type==='def'){
            ctx.locals.push(name)
            break
        }
        ctx = ctx.parent
    }    
    this.toString = function(){return 'func arg id '+this.name +'='+this.tree}
    this.expect = '='
    this.to_js = function(){return this.name+$to_js(this.tree)}
}

function $FuncStarArgCtx(context,op){
    this.type = 'func_star_arg'
    this.op = op
    this.parent = context
    if(op=='*'){context.has_star_arg=true}
    else if(op=='**'){context.has_kw_arg=true}
    context.tree.push(this)
    this.set_name = function(name){
        this.name = name
        if(name=='$dummy'){return}
        // add to locals of function
        var ctx = context
        while(ctx.parent!==undefined){
            if(ctx.type==='def'){
                ctx.locals.push(name)
                break
            }
            ctx = ctx.parent
        }    
        
    }
    this.toString = function(){return '(func star arg '+this.op+') '+this.name}
}

function $GlobalCtx(context){
    this.type = 'global'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.expect = 'id'
    this.toString = function(){return 'global '+this.tree}
    this.transform = function(node,rank){
        var scope = $get_scope(this)
        if(scope.globals===undefined){scope.globals=[]}
        for(var i=0;i<this.tree.length;i++){
            scope.globals.push(this.tree[i].value)
        }
    }
    this.to_js = function(){return ''}
}

function $check_unbound(assigned,scope,varname){
    // check if the variable varname in context "assigned" was
    // referenced in the scope
    // If so, replace statement by UnboundLocalError
    if(scope.var2node && scope.var2node[varname]){
        if(scope.context.tree[0].locals.indexOf(varname)>-1){
            return
        }
        for(var i=0;i<scope.var2node[varname].length;i++){
            var ctx = scope.var2node[varname][i]
            if(ctx==assigned){
                delete scope.var2node[varname]
                break
            }else{
                while(ctx.parent){ctx=ctx.parent}
                var ctx_node = ctx.node
                var js = 'throw UnboundLocalError("local variable '+"'"
                js += varname+"'"+' referenced before assignment")'
                new $NodeJSCtx(ctx_node,js)                        
            }
        }
    }
    if(scope.context.tree[0].locals.indexOf(varname)==-1){
        scope.context.tree[0].locals.push(varname)
    }
}

function $IdCtx(context,value,minus){
    // minus is set if there is a unary minus before the id
    //console.log('id '+value+' context '+context+' target list ? '+(context.type=='target_list'))
    this.type = 'id'
    this.toString = function(){return '(id) '+this.value+':'+(this.tree||'')}
    this.value = value
    this.minus = minus
    this.parent = context
    this.tree = []
    context.tree.push(this)
    if(context.parent.type==='call_arg'){
        this.call_arg=true
    }

    var ctx = context
    while(ctx.parent!==undefined){
        if(['list_or_tuple','dict_or_set','call_arg','def','lambda'].indexOf(ctx.type)>-1){
            if(ctx.vars===undefined){ctx.vars=[value]}
            else if(ctx.vars.indexOf(value)===-1){ctx.vars.push(value)}
            if(this.call_arg&&ctx.type==='lambda'){
                if(ctx.locals===undefined){ctx.locals=[value]}
                else{ctx.locals.push(value)}
            }
        }
        ctx = ctx.parent
    }

    var scope = $get_scope(this)
    if(scope.ntype=='def' || scope.ntype=='generator'){
        // if variable is declared inside a comprehension, don't add it to function
        // namespace
        var _ctx=this.parent
        while(_ctx){
            if(_ctx.type=='list_or_tuple' && _ctx.is_comp()){return}
            _ctx = _ctx.parent
        }
        if(context.type=='target_list'){
            if(context.parent.type=='for'){
                // a "for" loop inside the function creates a local variable : 
                // check if it was not referenced before
                $check_unbound(this,scope,value)
            }else if(context.parent.type=='comp_for'){
                // Inside a comprehension
                // The variables of the same name in the returned elements before "for" 
                // are not referenced in the function block
                var comprehension = context.parent.parent.parent
                if(comprehension.parent && comprehension.parent.type=='call_arg'){
                    // for the form "func(x for x in iterable)"
                    comprehension = comprehension.parent
                }
                var remove = []
                if(scope.var2node && scope.var2node[value]){
                    for(var i=0;i<scope.var2node[value].length;i++){
                        var ctx = scope.var2node[value][i]
                        while(ctx.parent){
                            if(ctx===comprehension.parent){
                                remove.push(i)
                                break
                            }
                            ctx = ctx.parent
                        }
                    }
                }
                for(var i=remove.length-1;i>=0;i--){
                    scope.var2node[value].splice(i,1)
                }
            }
        }else if(context.type=='expr' && context.parent.type=='comp_if'){
            // form {x for x in foo if x>5} : don't put x in referenced names
            return
        }else if(context.type=='global'){
            if(scope.globals === undefined){
                scope.globals = [value]
            }else if(scope.globals.indexOf(value)==-1){
                scope.globals.push(value)
            }
        }else if(scope.globals===undefined || scope.globals.indexOf(value)==-1){
            // variable referenced in the function
            if(scope.var2node===undefined){
                scope.var2node = {}
                scope.var2node[value] = [this]
            }else if(scope.var2node[value]===undefined){
                scope.var2node[value] = [this]
            }else{
                scope.var2node[value].push(this)
            }
        }
    }
    
    this.transform = function(node,rank){
        // If the variable is used in a function, we store the current node 
        // context in a dictionary indexed by the variables
        // If later there is a local variable assigned with the same
        // name, the context will be replaced by raising the exception
        // "UnboundLocalError : local variable referenced before assignment"
        console.log('transform id '+value)
        var scope = $get_scope(this)
        if(scope.ntype==='def' || scope.ntype==='generator'){
            var flag = true
            var parent=this.parent
            while(parent){parent=parent.parent}
            if(this.parent.type==='expr' && this.parent.parent.type=='call_arg'){
                // left part of a keyword argument
                if(this.parent.parent.tree[0].type==='kwarg'){
                   var flag = false
                }
            }
            if(flag){
                console.log('add '+value+' to scope')
                var ctx = this.parent
                while(ctx.parent!==undefined){ctx=ctx.parent}
                var ctx_node = ctx.node
                if(scope.var2node===undefined){
                    scope.var2node = {value:[ctx_node]}
                }else if(scope.var2node[value]===undefined){
                    scope.var2node[value] = [ctx_node]
                }else{
                    scope.var2node[value].push(ctx_node)
                }            
            }
        }
    }
 
    this.to_js = function(arg){
        var val = this.value
        if(['print','eval','open'].indexOf(this.value)>-1){val = '$'+val}
        if(['locals','globals'].indexOf(this.value)>-1){
            if(this.parent.type==='call'){
                var scope = $get_scope(this)
                if(scope.ntype==="module"){new $StringCtx(this.parent,'"__main__"')}
                else{
                    var locals = scope.context.tree[0].locals
                    var res = '{'
                    for(var i=0;i<locals.length;i++){
                        res+="'"+locals[i]+"':"+locals[i]
                        if(i<locals.length-1){res+=','}
                    }
                    new $StringCtx(this.parent,res+'}')
                }
            }
        }
        var scope = $get_scope(this)
        if(scope.ntype=='class' && this.in_class){
            // If the id is used in a chained assignment inside a class body,
            // this instance is referenced in several assign nodes
            // If it the left part of an assignment, an attribute 'in_class'
            // has been set in method $to_js of $AssignCtx
            return this.in_class
        }
        if(scope.ntype==='class' && !this.is_left){
            // ids used in a class body (not inside a method) are resolved
            // in a specific way :
            // - if the id is used as the left part of a keyword argument
            //   (eg the id "x" in "foo(x=8)") it is left as is
            // - if this is the left part of an assignement, it is left as is
            // - otherwise, if the id matches a class attribute, it is resolved 
            //   as this class attribute, else it is left as is
            // example :
            // =============
            // x = 0
            // class foo:
            //   y = 1
            //   z = [x,y]
            //   A = foo(u=8)
            // ==============
            // y and u will be left as they are
            // x will be replaced by :
            //     ($class["x"]!==undefined ? $class["x"] : x)
            // y will be replaced by :
            //     ($class["y"]!==undefined ? $class["y"] : y)
            // at run time, the test will fail for x and will succeed for y
            var parent=this.parent
            while(parent){parent=parent.parent}
            if(this.parent.type==='expr' && this.parent.parent.type=='call_arg'){
                // left part of a keyword argument
                if(this.parent.parent.tree[0].type=='kwarg'){
                    return val+$to_js(this.tree,'')
                }
            }
            return '($class["'+val+'"] !==undefined ? $class["'+val+'"] : '+val+')'
        }
        
        return val+$to_js(this.tree,'')
    }
}

function $ImportCtx(context){
    this.type = 'import'
    this.toString = function(){return 'import '+this.tree}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.expect = 'id'
    this.to_js = function(){
        var scope = $get_scope(this)
        var mod = $get_module(this).module
        if(mod.substr(0,13)==='__main__,exec'){mod='__main__'}
        var path = __BRYTHON__.$py_module_path[mod]
        var elts = path.split('/')
        elts.pop()
        path =elts.join('/')
        var res = ''
        for(var i=0;i<this.tree.length;i++){
            res += '__BRYTHON__.$import('+this.tree[i].to_js()+');'
            var parts = this.tree[i].name.split('.')
            // $import returns an object
            // for "import a.b.c" this object has attributes
            // "a", "a.b" and "a.b.c", values are the matching modules
            for(j=0;j<parts.length;j++){
                if(j==0 && 
                    ['def','class'].indexOf(scope.ntype)>-1){
                    res += 'var '
                }else if(j==0 && scope.ntype==="module" && scope.module !=="__main__"){
                    res += 'var '
                }
                var key = parts.slice(0,j+1).join('.')
                var alias = key
                if(j==parts.length-1){alias = this.tree[i].alias}
                res += alias
                if(scope.ntype == 'def' || scope.ntype==="generator"){
                    res += '=$locals["'+alias+'"]'
                }else if(scope.ntype==="module"){
                    res += '=$globals["'+alias+'"]'
                }
                res += '=__BRYTHON__.scope["'+key+'"].__dict__;'
            }
        }
        // add None for interactive console
        res += 'None;'
        return res
    }
}

function $ImportedModuleCtx(context,name){
    this.type = 'imported module'
    this.toString = function(){return ' (imported module) '+this.name}
    this.parent = context
    this.name = name
    this.alias = name
    context.tree.push(this)
    this.to_js = function(){
        return '"'+this.name+'"'
    }
}

function $IntCtx(context,value){
    this.type = 'int'
    this.value = value
    this.toString = function(){return 'int '+this.value}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){return 'Number('+this.value+')'}
}

function $JSCode(js){
    this.js = js
    this.toString = function(){return this.js}
    this.to_js = function(){return this.js}
}

function $KwArgCtx(context){
    this.type = 'kwarg'
    this.toString = function(){return 'kwarg '+this.tree[0]+'='+this.tree[1]}
    this.parent = context.parent
    this.tree = [context.tree[0]]
    // operation replaces left operand
    context.parent.tree.pop()
    context.parent.tree.push(this)

    // put id in list of kwargs
    // used to avoid passing the id as argument of a list comprehension
    var value = this.tree[0].value
    var ctx = context
    while(ctx.parent!==undefined){
        if(['list_or_tuple','dict_or_set','call_arg','def','lambda'].indexOf(ctx.type)>-1){
            if(ctx.kwargs===undefined){ctx.kwargs=[value]}
            else if(ctx.kwargs.indexOf(value)===-1){ctx.kwargs.push(value)}
        }
        ctx = ctx.parent
    }

    // If the keyword argument occurs inside a function, remove the occurence
    // from referenced variables in the function
    var scope = $get_scope(this)
    if(scope.ntype=='def' || scope.ntype=='generator'){
        var ix = null,varname=context.tree[0].value
        //ui slider caused an issue in which scope.var2node[varname] is undefined
        // so lets check for that.
        if (scope.var2node[varname] !== undefined) {
           for(var i=0;i<scope.var2node[varname].length;i++){
             if(scope.var2node[varname][i]==context.tree[0]){
                ix = i
                break
             }
           }
           scope.var2node[varname].splice(ix,1)
        }
    }

    this.to_js = function(){
        var key = this.tree[0].to_js()
        if(key.substr(0,2)=='$$'){key=key.substr(2)}
        var res = '__BRYTHON__.$Kw("'+key+'",'
        res += $to_js(this.tree.slice(1,this.tree.length))+')'
        return res
    }
}

function $LambdaCtx(context){
    this.type = 'lambda'
    this.toString = function(){return '(lambda) '+this.args_start+' '+this.body_start}
    this.parent = context
    context.tree.push(this)
    this.tree = []
    this.args_start = $pos+6
    this.vars = []
    this.locals = []
    this.to_js = function(){
        var ctx_node = this
        while(ctx_node.parent!==undefined){ctx_node=ctx_node.parent}
        var module = ctx_node.node.module
        var src = document.$py_src[module]
        var qesc = new RegExp('"',"g") // to escape double quotes in arguments

        var args = src.substring(this.args_start,this.body_start).replace(qesc,'\\"')
        var body = src.substring(this.body_start+1,this.body_end).replace(qesc,'\\"')
        body = body.replace(/\n/g,' ')
        return '__BRYTHON__.$lambda("'+module+'",$globals,$locals,"'+args+'","'+body+'")'
    }
}

function $ListOrTupleCtx(context,real){
    // the real type (list or tuple) is set inside $transition
    // as attribute 'real'
    this.type = 'list_or_tuple'
    this.start = $pos
    this.real = real
    this.expect = 'id'
    this.closed = false
    this.toString = function(){
        if(this.real==='list'){return '(list) ['+this.tree+']'}
        else if(this.real==='list_comp'||this.real==='gen_expr'){
            return '('+this.real+') ['+this.intervals+'-'+this.tree+']'
        }else{return '(tuple) ('+this.tree+')'}
    }
    this.parent = context
    this.tree = []
    context.tree.push(this)
    
    this.is_comp = function(){
        return ['list_comp','gen_expr','dict_or_set_comp'].indexOf(this.real)>-1
    }
    this.get_src = function(){
        var ctx_node = this
        while(ctx_node.parent!==undefined){ctx_node=ctx_node.parent}
        var module = ctx_node.node.module
        return document.$py_src[module]
    }
    this.to_js = function(){
        if(this.real==='list'){return 'list.__call__(['+$to_js(this.tree)+'])'}
        else if(['list_comp','gen_expr','dict_or_set_comp'].indexOf(this.real)>-1){
            var src = this.get_src()
            var res = '__BRYTHON__.$mkdict($globals,$locals),'

            var qesc = new RegExp('"',"g") // to escape double quotes in arguments
            for(var i=1;i<this.intervals.length;i++){
                var txt = src.substring(this.intervals[i-1],this.intervals[i])
                txt = txt.replace(/\n/g,' ')
                txt = txt.replace(/\\/g,'\\\\')
                txt = txt.replace(qesc,'\\"')
                res += '"'+txt+'"'
                if(i<this.intervals.length-1){res+=','}
            }

            if(this.real==='list_comp'){return '__BRYTHON__.$list_comp('+res+')'}
            else if(this.real==='dict_or_set_comp'){
                if(this.expression.length===1){return '__BRYTHON__.$gen_expr('+res+')'}
                else{return '__BRYTHON__.$dict_comp('+res+')'}
            }else{return '__BRYTHON__.$gen_expr('+res+')'}
        }else if(this.real==='tuple'){
            if(this.tree.length===1 && this.has_comma===undefined){return this.tree[0].to_js()}
            else{return 'tuple(['+$to_js(this.tree)+'])'}
        }
    }
}

function $NodeCtx(node){
    this.node = node
    node.context = this
    this.tree = []
    this.type = 'node'
    this.toString = function(){return 'node '+this.tree}
    this.to_js = function(){
        if(this.tree.length>1){
            var new_node = new $Node('expression')
            var ctx = new $NodeCtx(new_node)
            ctx.tree = [this.tree[1]]
            new_node.indent = node.indent+4
            this.tree.pop()
            node.add(new_node)
        }
        return $to_js(this.tree)
    }
}

function $NodeJSCtx(node,js){ // used for raw JS code
    this.node = node
    node.context = this
    this.type = 'node_js'
    this.tree = [js]
    this.toString = function(){return 'js '+js}
    this.to_js = function(){return js}
}

function $NonlocalCtx(context){
    // for the moment keep this as alias for global 
    this.type = 'global'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.expect = 'id'
    this.toString = function(){return 'global '+this.tree}
    this.transform = function(node,rank){
        var scope = $get_scope(this)
        if(scope.globals===undefined){scope.globals=[]}
        for(var i=0;i<this.tree.length;i++){
            scope.globals.push(this.tree[i].value)
        }
    }
    this.to_js = function(){return ''}
}


function $NotCtx(context){
    this.type = 'not'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return 'not ('+this.tree+')'}
    this.to_js = function(){return '!bool('+$to_js(this.tree)+')'}
}

function $OpCtx(context,op){ // context is the left operand
    this.type = 'op'
    this.op = op
    this.toString = function(){return '(op '+this.op+')'+this.tree}
    this.parent = context.parent
    this.tree = [context]
    // operation replaces left operand
    context.parent.tree.pop()
    context.parent.tree.push(this)
    this.to_js = function(){
        if(this.op==='and'){
            var res ='__BRYTHON__.$test_expr(__BRYTHON__.$test_item('+this.tree[0].to_js()+')&&'
            res += '__BRYTHON__.$test_item('+this.tree[1].to_js()+'))'
            return res
        }else if(this.op==='or'){
            var res ='__BRYTHON__.$test_expr(__BRYTHON__.$test_item('+this.tree[0].to_js()+')||'
            res += '__BRYTHON__.$test_item('+this.tree[1].to_js()+'))'
            return res
        }else{
            var res = this.tree[0].to_js()
            if(this.op==="is"){
                res += '==='+this.tree[1].to_js()
            }else if(this.op==="is_not"){
                res += '!=='+this.tree[1].to_js()
            }else{
                res = 'getattr('+res+',"__'+$operators[this.op]+'__")'
                res += '('+this.tree[1].to_js()+')'
            }
            return res
        }
    }
}

function $PassCtx(context){
    this.type = 'pass'
    this.toString = function(){return '(pass)'}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){return 'void(0)'}
}

function $RaiseCtx(context){
    this.type = 'raise'
    this.toString = function(){return ' (raise) '+this.tree}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){
        if(this.tree.length===0){return '__BRYTHON__.$raise()'}
        var exc = this.tree[0]
        if(exc.type==='id'){return 'throw '+exc.value+'("")'}
        else if(exc.type==='expr' && exc.tree[0].type==='id'){
            return 'throw '+exc.tree[0].value+'("")'
        }else{
            // if raise had a 'from' clause, ignore it
            while(this.tree.length>1){this.tree.pop()}
            return 'throw '+$to_js(this.tree)
        }
    }
}

function $RawJSCtx(context,js){
    context.tree.push(this)
    this.parent = context
    this.toString = function(){return '(js) '+js}
    this.to_js = function(){return js}
}

function $ReturnCtx(context){ // subscription or slicing
    this.type = 'return'
    this.toString = function(){return 'return '+this.tree}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){return 'return '+$to_js(this.tree)}
}

function $SingleKwCtx(context,token){ // used for finally,else
    this.type = 'single_kw'
    this.token = token
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return this.token}
    this.to_js = function(){
        if(this.token==='finally'){return this.token}
        // For "else" we must check if the previous block was a loop
        // If so, check if the loop exited with a "break" to decide
        // if the block below "else" should be run
        var ctx_node = context
        while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
        var tree_node = ctx_node.node
        var parent = tree_node.parent
        for(var i=0;i<parent.children.length;i++){
            if(parent.children[i]===tree_node){
                if(i==0){$_SyntaxError(context,"block begins with 'else'")}
                var pctx = parent.children[i-1].context
                // get loop num : for a 'for' loop the previous node is a node_js
                if(pctx.type==='node_js'){var loop = pctx.loop_num}
                // for a 'while' loop it is a normal node
                else{var loop=pctx.tree[0].loop_num}
                // if 'else' inside a loop, translate it into a condition
                // on the 'no break' variable associated with the loop
                if(loop!==undefined){return 'if ($no_break'+loop+')'}
                else{break}
            }
        }
        return this.token
    }
}

function $StarArgCtx(context){
    this.type = 'star_arg'
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.toString = function(){return '(star arg) '+this.tree}
    this.to_js = function(){
        return '__BRYTHON__.$ptuple('+$to_js(this.tree)+')'
    }
}

function $StringCtx(context,value){
    this.type = 'str'
    this.toString = function(){return 'string '+(this.tree||'')}
    this.parent = context
    this.tree = [value] // may be extended if consecutive strings eg 'a' 'b'
    context.tree.push(this)
    this.to_js = function(){
        var res = ''
        for(var i=0;i<this.tree.length;i++){
            var value=this.tree[i]
            if(value.charAt(0)!='b'){
                res += value.replace(/\n/g,'\\n\\\n')
            }else{
                res += 'bytes('
                res += value.substr(1).replace(/\n/g,'\\n\\\n')
                res += ')'
            }
            if(i<this.tree.length-1){res+='+'}
        }
        return res
    }
}

function $SubCtx(context){ // subscription or slicing
    this.type = 'sub'
    this.func = 'getitem' // set to 'setitem' if assignment
    this.toString = function(){return '(sub) '+this.tree}
    this.value = context.tree[0]
    context.tree.pop()
    context.tree.push(this)
    this.parent = context
    this.tree = []
    this.to_js = function(){
        var res = 'getattr('+this.value.to_js()+',"__'+this.func+'__")('
        if(this.tree.length===1){
            return res+this.tree[0].to_js()+')'
        }else{
            res += 'slice('
            for(var i=0;i<this.tree.length;i++){
                if(this.tree[i].type==='abstract_expr'){res+='null'}
                else{res+=this.tree[i].to_js()}
                if(i<this.tree.length-1){res+=','}
            }
            return res+'))'
        }
    }
}

function $TargetCtx(context,name){ // exception
    this.toString = function(){return ' (target) '+this.name}
    this.parent = context
    this.name = name
    this.alias = null
    context.tree.push(this)
    this.to_js = function(){
        return '["'+this.name+'","'+this.alias+'"]'
    }
}

function $TargetListCtx(context){
    this.type = 'target_list'
    this.parent = context
    this.tree = []
    this.expect = 'id'
    context.tree.push(this)
    this.toString = function(){return '(target list) '+this.tree}
    this.to_js = function(){return $to_js(this.tree)}
}

function $TernaryCtx(context){
    this.type = 'ternary'
    this.parent = context.parent
    context.parent.tree.pop()
    context.parent.tree.push(this)
    context.parent = this
    this.tree = [context]
    this.toString = function(){return '(ternary) '+this.tree}
    this.to_js = function(){
        // build namespace
        var env = '{'
        var ids = $get_ids(this)
        for(var i=0;i<ids.length;i++){
            env += '"'+ids[i]+'":'+ids[i]
            if(i<ids.length-1){env+=','}
        }
        env+='}'
        var qesc = new RegExp('"',"g") // to escape double quotes in arguments
        var args = '"'+this.tree[1].to_js().replace(qesc,'\\"')+'","' // condition
        args += escape(this.tree[0].to_js())+'","' // result if true
        args += escape(this.tree[2].to_js()) // result if false
        return '__BRYTHON__.$ternary('+env+','+args+'")'
    }
}

function $TryCtx(context){
    this.type = 'try'
    this.parent = context
    context.tree.push(this)
    this.toString = function(){return '(try) '}
    this.transform = function(node,rank){
        if(node.parent.children.length===rank+1){
            $_SyntaxError(context,"missing clause after 'try' 1")
        }else{
            var next_ctx = node.parent.children[rank+1].context.tree[0]
            if(['except','finally','single_kw'].indexOf(next_ctx.type)===-1){
                $_SyntaxError(context,"missing clause after 'try' 2")
            }
        }
        // transform node into Javascript 'try' (necessary if
        // "try" inside a "for" loop
        // add a boolean $failed, used to run the 'else' clause
        new $NodeJSCtx(node,'$failed'+$loop_num+'=false;try')
        // insert new 'catch' clause
        var catch_node = new $Node('expression')
        new $NodeJSCtx(catch_node,'catch($err'+$loop_num+')')
        node.parent.insert(rank+1,catch_node)
        
        // fake line to start the 'else if' clauses
        var new_node = new $Node('expression')
        // set the boolean $failed to true
        new $NodeJSCtx(new_node,'var $failed'+$loop_num+'=true;if(false){void(0)}')
        catch_node.insert(0,new_node)
        
        var pos = rank+2
        var has_default = false // is there an "except:" ?
        var has_else = false // is there an "else" clause ?
        while(true){
            if(pos===node.parent.children.length){break}
            var ctx = node.parent.children[pos].context.tree[0]
            if(ctx.type==='except'){
                // move the except clauses below catch_node
                if(has_else){$_SyntaxError(context,"'except' or 'finally' after 'else'")}
                ctx.error_name = '$err'+$loop_num
                if(ctx.tree.length>0 && ctx.tree[0].alias!==null
                    && ctx.tree[0].alias!==undefined){
                    // syntax "except ErrorName as Alias"
                    var new_node = new $Node('expression')
                    var js = 'var '+ctx.tree[0].alias+'=__BRYTHON__.exception($err'+$loop_num+')'
                    new $NodeJSCtx(new_node,js)
                    node.parent.children[pos].insert(0,new_node)
                }
                catch_node.insert(catch_node.children.length,
                    node.parent.children[pos])
                if(ctx.tree.length===0){
                    if(has_default){$_SyntaxError(context,'more than one except: line')}
                    has_default=true
                }
                node.parent.children.splice(pos,1)
            }else if(ctx.type==='single_kw' && ctx.token==='finally'){
                if(has_else){$_SyntaxError(context,"'finally' after 'else'")}
                pos++
            }else if(ctx.type==='single_kw' && ctx.token==='else'){
                if(has_else){$_SyntaxError(context,"more than one 'else'")}
                has_else = true
                else_body = node.parent.children[pos]
                node.parent.children.splice(pos,1)
            }else{break}
        }
        if(!has_default){ 
            // if no default except: clause, add a line to throw the
            // exception if it was not caught
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,'else{throw $err'+$loop_num+'}')
            catch_node.insert(catch_node.children.length,new_node)
        }
        if(has_else){
            var else_node = new $Node('expression')
            new $NodeJSCtx(else_node,'if(!$failed'+$loop_num+')')
            for(var i=0;i<else_body.children.length;i++){
                else_node.add(else_body.children[i])
            }
            catch_node.insert(catch_node.children.length,else_node)
        }
        $loop_num++
    }
    this.to_js = function(){return 'try'}
}

function $UnaryCtx(context,op){
    this.type = 'unary'
    this.op = op
    this.toString = function(){return '(unary) '+this.op+' ['+this.tree+']'}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.to_js = function(){return this.op+$to_js(this.tree)}
}

function $WithCtx(context){
    this.type = 'with'
    this.parent = context
    context.tree.push(this)
    this.tree = []
    this.expect = 'as'
    this.toString = function(){return '(with) '}
    this.transform = function(node,rank){
        if(this.transformed){return} // used if inside a for loop
        if(this.tree[0].alias===null){this.tree[0].alias = '$temp'}
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,'catch($err'+$loop_num+')')
        var fbody = new $Node('expression')
        var js = 'if(!$ctx_manager_exit($err'+$loop_num+'.type,'
        js += '$err'+$loop_num+'.value,$err'+$loop_num+'.traceback))'
        js += '{throw $err'+$loop_num+'}'
        new $NodeJSCtx(fbody,js)
        new_node.add(fbody)
        node.parent.insert(rank+1,new_node)
        $loop_num++
        var new_node = new $Node('expression')
        new $NodeJSCtx(new_node,'finally')
        var fbody = new $Node('expression')
        new $NodeJSCtx(fbody,'$ctx_manager_exit(None,None,None)')
        new_node.add(fbody)
        node.parent.insert(rank+2,new_node)
        this.transformed = true
    }
    this.to_js = function(){
        var res = 'var $ctx_manager='+this.tree[0].to_js()
        res += '\nvar $ctx_manager_exit = getattr($ctx_manager,"__exit__")\n'
        if(this.tree[0].alias){
            res += 'var '+this.tree[0].alias+'='
        }
        res += 'getattr($ctx_manager,"__enter__")()'
        return res+'\ntry'
    }
}

function $YieldCtx(context){ // subscription or slicing
    this.type = 'yield'
    this.toString = function(){return '(yield) '+this.tree}
    this.parent = context
    this.tree = []
    context.tree.push(this)
    this.transform = function(node,rank){
        if(this.transformed!==undefined){return}
        var scope = $get_scope(node.context.tree[0])
        // change type of function to generator
        scope.context.tree[0].type = 'generator'
        this.transformed = true
        this.func_name = scope.context.tree[0].name
        scope.context.tree[0].add_generator_declaration()
    }
    this.to_js = function(){
        var scope = $get_scope(this)
        var res = ''
        if(scope.ntype==='generator'){
            scope = $get_scope(scope.context.tree[0])
            if(scope.ntype==='class'){res = '$class.'}
        }
        if(this.tree.length==1){
            return res+'$'+this.func_name+'.$iter.push('+$to_js(this.tree)+')'
        }else{ // form "yield from <expr>" : <expr> is this.tree[1]
            var indent = $ws($get_module(this).indent)
            res += '$subiter'+$loop_num+'=getattr(iter('+this.tree[1].to_js()+'),"__next__")\n'
            res += indent+'while(true){\n'+indent+$ws(4)
            res += 'try{$'+this.func_name+'.$iter.push('
            res += '$subiter'+$loop_num+'())}\n'
            res += indent+$ws(4)+'catch($err'+$loop_num+'){\n'
            res += indent+$ws(8)+'if($err'+$loop_num+'.__class__.$factory===__builtins__.StopIteration)'
            res += '{__BRYTHON__.$pop_exc();break}\n'
            res += indent+$ws(8)+'else{throw $err'+$loop_num+'}\n}\n}'
            $loop_num++
            return res
        }
    }
}


// used in loops
var $loop_num = 0
var $iter_num = 0 

function $add_line_num(node,rank){
    if(node.type==='module'){
        var i=0
        while(i<node.children.length){
            i += $add_line_num(node.children[i],i)
        }
    }else{
        var elt=node.context.tree[0],offset=1
        var flag = true
        // ignore lines added in transform()
        if(node.line_num===undefined){flag=false}
        // don't add line num before try,finally,else,elif
        if(elt.type==='condition' && elt.token==='elif'){flag=false}
        else if(elt.type==='except'){flag=false}
        else if(elt.type==='single_kw'){flag=false}
        if(flag){
            var js = '__BRYTHON__.line_info=['+node.line_num+',"'+node.module+'"];'
            // add a trailing None for interactive mode
            js += 'None;'
            var new_node = new $Node('expression')
            new $NodeJSCtx(new_node,js)
            node.parent.insert(rank,new_node)
            offset = 2
        }
        var i=0
        while(i<node.children.length){
            i += $add_line_num(node.children[i],i)
        }
        return offset
    }
}

function $augmented_assign(context,op){
    // in "foo += bar" context = foo, op = +
    // replace foo += bar by :
    // $temp = bar
    // if(!hasattr(foo,"__iadd__")){
    //     foo = foo.__add__(bar)
    // }else{
    //     foo.__iadd__(bar)
    // }
    
    var func = '__'+$operators[op]+'__'
    var ctx = context
    while(ctx.parent!==undefined){ctx=ctx.parent}
    var node = ctx.node
    var parent = node.parent
    for(var i=0;i<parent.children.length;i++){
        if(parent.children[i]===node){var rank = i;break}
    }

    // replace current node by "$temp = <placeholder>"
    // at the end of $aumented_assign, control will be
    // passed to the <placeholder> expression
    var new_node = new $Node('expression')
    var new_ctx = new $NodeCtx(new_node)
    var new_expr = new $ExprCtx(new_ctx,'id',false)
    var _id = new $IdCtx(new_expr,'$temp')
    var assign = new $AssignCtx(context)
    assign.tree[0] = _id
    _id.parent = assign

    var prefix = ''

    if(['+=','-=','*=','/='].indexOf(op)>-1 && 
        context.type=='expr' && context.tree[0].type=='id'){
        var scope = $get_scope(context)
        prefix='$locals'
        if(scope.ntype=='module'){prefix='$globals'}
        else if(['def','generator'].indexOf(scope.ntype)>-1){
            if(scope.globals && scope.globals.indexOf(context.tree[0].value)>-1){
                prefix = '$globals'
            }
        }
    }


    // insert shortcut node if op is += and both args are numbers
    var offset = 1
    if(prefix){
        var new_node = new $Node('expression')
        var js = 'if($temp.$fast_augm && '
        js += context.to_js()+'.$fast_augm){'
        js += context.to_js()+op+'$temp'
        js += ';'+prefix+'["'+context.tree[0].value+'"]='+context.to_js()
        js += '}'
        new $NodeJSCtx(new_node,js)
        parent.insert(rank+offset,new_node)
        offset++
    }
    // insert node 'if(!hasattr(foo,"__iadd__"))
    var new_node = new $Node('expression')
    var js = ''
    if(prefix){js += 'else '}
    js += 'if(!hasattr('+context.to_js()+',"'+func+'"))'
    new $NodeJSCtx(new_node,js)
    parent.insert(rank+offset,new_node)
    offset ++

    // create node for "foo = foo + bar"
    var aa1 = new $Node('expression')
    var ctx1 = new $NodeCtx(aa1)
    var expr1 = new $ExprCtx(ctx1,'clone',false)
    expr1.tree = context.tree
    for(var i=0;i<expr1.tree.length;i++){
        expr1.tree[i].parent = expr1
    }
    var assign1 = new $AssignCtx(expr1)
    var new_op = new $OpCtx(expr1,op.substr(0,op.length-1))
    new_op.parent = assign1
    new $RawJSCtx(new_op,'$temp')
    assign1.tree.push(new_op)
    expr1.parent.tree.pop()
    expr1.parent.tree.push(assign1)
    new_node.add(aa1)
    
    // create node for "else"
    var aa2 = new $Node('expression')
    new $NodeJSCtx(aa2,'else')
    parent.insert(rank+offset,aa2)

    // create node for "foo.__iadd__(bar)    
    var aa3 = new $Node('expression')
    var js3 = context.to_js()
    if(prefix){js3 += '='+prefix+'["'+context.to_js()+'"]'}
    js3 += '=getattr('+context.to_js()
    js3 += ',"'+func+'")($temp)'
    new $NodeJSCtx(aa3,js3)
    aa2.add(aa3)

    // return control to right term of "$temp = ?"    
    return new $AbstractExprCtx(assign)
}

function $clear_ns(ctx){
    // Function called when it turns out that the list or tuple is a comprehension
    // If the list is in a function, the names defined in the display so far must 
    // be removed from the function namespace
    var scope = $get_scope(ctx)
    if(scope.ntype=="def" || scope.ntype=="generator"){
        if(scope.var2node){
            for(var name in scope.var2node){
                var remove = []
                for(var j=0;j<scope.var2node[name].length;j++){
                    var elt = scope.var2node[name][j].parent
                    while(elt.parent){
                        if(elt===ctx){remove.push(j);break}
                        elt=elt.parent
                    }
                }
                for(var k=remove.length-1;k>=0;k--){
                    scope.var2node[name].splice(remove[k],1)
                }
                //if(scope.var2node[name].length==0){scope.var2node[name]==undefined}

            }
        }
    }
}

function $get_docstring(node){
    var doc_string='""'
    if(node.children.length>0){
        var firstchild = node.children[0]
        if(firstchild.context.tree && firstchild.context.tree[0].type=='expr'){
            if(firstchild.context.tree[0].tree[0].type=='str')
            doc_string = firstchild.context.tree[0].tree[0].to_js()
        }
    }
    return doc_string
}

function $get_scope(context){
    // return the $Node indicating the scope of context
    // null for the script or a def $Node
    var ctx_node = context.parent
    while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
    var tree_node = ctx_node.node
    var scope = null
    while(tree_node.parent && tree_node.parent.type!=='module'){
        var ntype = tree_node.parent.context.tree[0].type
        if(['def','class','generator'].indexOf(ntype)>-1){
            scope = tree_node.parent
            scope.ntype = ntype
            scope.elt = scope.context.tree[0]
            return scope
        }
        tree_node = tree_node.parent
    }
    scope = tree_node.parent || tree_node // module
    scope.ntype = "module"
    scope.elt = scope.module
    return scope
}

function $get_module(context){
    var ctx_node = context.parent
    while(ctx_node.type!=='node'){ctx_node=ctx_node.parent}
    var tree_node = ctx_node.node
    var scope = null
    while(tree_node.parent.type!=='module'){
        tree_node = tree_node.parent
    }
    scope = tree_node.parent // module
    scope.ntype = "module"
    return scope
}

function $get_node(context){
    var ctx = context
    while(ctx.parent){ctx=ctx.parent}
    return ctx.node
}

function $get_ids(ctx){
    var res = []
    if(ctx.type==='expr' &&
        ctx.tree[0].type==='list_or_tuple' &&
        ctx.tree[0].real==='list_comp'){return []}
    if(ctx.type==='id'){res.push(ctx.value)}
    else if(ctx.type==='attribute'||ctx.type==='sub'){
        var res1 = $get_ids(ctx.value)
        for(var i=0;i<res1.length;i++){
            if(res.indexOf(res1[i])===-1){res.push(res1[i])}
        }
    }else if(ctx.type==='call'){
        var res1 = $get_ids(ctx.func)
        for(var i=0;i<res1.length;i++){
            if(res.indexOf(res1[i])===-1){res.push(res1[i])}
        }
    }
    if(ctx.tree!==undefined){
        for(var i=0;i<ctx.tree.length;i++){
            var res1 = $get_ids(ctx.tree[i])
            for(var j=0;j<res1.length;j++){
                if(res.indexOf(res1[j])===-1){
                    res.push(res1[j])
                }
            }
        }
    }
    return res
}

function $ws(n){
    var res = ''
    for(var i=0;i<n;i++){res += ' '}
    return res
}

function $to_js(tree,sep){
    if(sep===undefined){sep=','}
    var res = ''
    for(var i=0;i<tree.length;i++){
        if(tree[i].to_js!==undefined){
            res += tree[i].to_js()
        }else{
            throw Error('no to_js() for '+tree[i])
        }
        if(i<tree.length-1){res+=sep}
    }
    return res
}

// expression starters
var $expr_starters = ['id','int','float','str','bytes','[','(','{','not','lambda']

function $arbo(ctx){
    while(ctx.parent!=undefined){ctx=ctx.parent}
    return ctx
}
function $transition(context,token){
    //console.log('arbo '+$arbo(context))
    // console.log('context '+context+' token '+token+' '+arguments[2])
    //console.log('')

    if(context.type==='abstract_expr'){
    
        if($expr_starters.indexOf(token)>-1){
            context.parent.tree.pop() // remove abstract expression
            var commas = context.with_commas
            context = context.parent
        }
        if(token==='id'){return new $IdCtx(new $ExprCtx(context,'id',commas),arguments[2])}
        else if(token==='str'){return new $StringCtx(new $ExprCtx(context,'str',commas),arguments[2])}
        else if(token==='bytes'){
            console.log('bytes '+arguments[2])
            return new $StringCtx(new $ExprCtx(context,'bytes',commas),arguments[2])
            }
        else if(token==='int'){return new $IntCtx(new $ExprCtx(context,'int',commas),arguments[2])}
        else if(token==='float'){return new $FloatCtx(new $ExprCtx(context,'float',commas),arguments[2])}
        else if(token==='('){return new $ListOrTupleCtx(new $ExprCtx(context,'tuple',commas),'tuple')}
        else if(token==='['){return new $ListOrTupleCtx(new $ExprCtx(context,'list',commas),'list')}
        else if(token==='{'){return new $DictOrSetCtx(new $ExprCtx(context,'dict_or_set',commas))}
        else if(token==='not'){
            if(context.type==='op'&&context.op==='is'){ // "is not"
                context.op = 'is_not'
                return context
            }else{
                return new $NotCtx(new $ExprCtx(context,'not',commas))
            }
        }else if(token==='lambda'){return new $LambdaCtx(new $ExprCtx(context,'lambda',commas))}
        else if(token==='op'){
            if('+-~'.search(arguments[2])>-1){ // unary + or -, bitwise ~
                return new $UnaryCtx(new $ExprCtx(context,'unary',false),arguments[2])
            }else{$_SyntaxError(context,'token '+token+' after '+context)}
        }else if(token=='='){
            $_SyntaxError(context,token)
        }else if([')',','].indexOf(token)>-1 && 
            ['list_or_tuple','call_arg'].indexOf(context.parent.type)==-1){
            console.log('err token '+token+' type '+context.parent.type)
            $_SyntaxError(context,token)
        }else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='assert'){
    
        if(token==='eol'){
            return $transition(context.parent,token)
        }else{$_SyntaxError(context,token)}
        
    }else if(context.type==='assign'){
    
        if(token==='eol'){return $transition(context.parent,'eol')}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='attribute'){ 

        if(token==='id'){
            var name = arguments[2]
            //if(name.substr(0,2)=='$$'){name=name.substr(2)}
            context.name=name
            return context.parent
        }else{$_SyntaxError(context,token)}

    }else if(context.type==='break'){
    
        if(token==='eol'){return $transition(context.parent,'eol')}
        else{$_SyntaxError(context,token)}

    }else if(context.type==='call'){ 
        if(token===','){return context}
        else if($expr_starters.indexOf(token)>-1){
            if(context.has_dstar){$_SyntaxError(context,token)}
            var expr = new $CallArgCtx(context)
            return $transition(expr,token,arguments[2])
        }else if(token===')'){context.end=$pos;return context.parent}
        else if(token==='op'){
            var op=arguments[2]
            if(op==='-'||op==='~'){return new $UnaryCtx(new $ExprCtx(context,'unary',false),op)}
            else if(op==='+'){return context}
            else if(op==='*'){context.has_star = true;return new $StarArgCtx(context)}
            else if(op==='**'){context_has_dstar = true;return new $DoubleStarArgCtx(context)}
            else{throw Error('SyntaxError')}
        }else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='call_arg'){

        if($expr_starters.indexOf(token)>-1 && context.expect==='id'){
            context.expect=','
            var expr = new $AbstractExprCtx(context,false)
            return $transition(expr,token,arguments[2])
        }else if(token==='=' && context.expect===','){
            return new $ExprCtx(new $KwArgCtx(context),'kw_value',false)
        }else if(token==='for'){
            // comprehension
            $clear_ns(context) // if inside function
            var lst = new $ListOrTupleCtx(context,'gen_expr')
            lst.vars = context.vars // copy variables
            lst.locals = context.locals
            lst.intervals = [context.start]
            context.tree.pop()
            lst.expression = context.tree
            context.tree = [lst]
            lst.tree = []
            var comp = new $ComprehensionCtx(lst)
            return new $TargetListCtx(new $CompForCtx(comp))
        }else if(token==='op' && context.expect==='id'){
            var op = arguments[2]
            context.expect = ','
            if(op==='+'||op==='-'){
                return $transition(new $AbstractExprCtx(context,false),token,op)
            }else if(op==='*'){context.expect=',';return new $StarArgCtx(context)}
            else if(op==='**'){context.expect=',';return new $DoubleStarArgCtx(context)}
            else{$_SyntaxError(context,'token '+token+' after '+context)}
        }else if(token===')'){
            if(context.tree.length>0){
                var son = context.tree[context.tree.length-1]
                if(son.type==='list_or_tuple'&&son.real==='gen_expr'){
                    son.intervals.push($pos)
                }
            }
            return $transition(context.parent,token)
        }else if(token===':' && context.expect===',' && context.parent.parent.type==='lambda'){
            return $transition(context.parent.parent,token)
        }else if(token===','&& context.expect===','){
            return new $CallArgCtx(context.parent)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='class'){
    
        if(token==='id' && context.expect==='id'){
            context.name = arguments[2]
            context.expect = '(:'
            return context
        }else if(token==='('){return new $CallCtx(context)}
        else if(token===':'){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

        //}
        //else if(token==='(' && context.expect==='(:'){
        //    return $transition(new $AbstractExprCtx(context,true),'(')
        //}else if(token===':' && context.expect==='(:'){return $BodyCtx(context)}
        //else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='comp_if'){

        return $transition(context.parent,token,arguments[2])

    }else if(context.type==='comp_for'){

        if(token==='in' && context.expect==='in'){
            context.expect = null
            return new $AbstractExprCtx(new $CompIterableCtx(context),true)
        }else if(context.expect===null){
            // ids in context.tree[0] are local to the comprehension
            return $transition(context.parent,token,arguments[2])
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='comp_iterable'){

        return $transition(context.parent,token,arguments[2])

    }else if(context.type==='comprehension'){
        if(token==='if'){return new $AbstractExprCtx(new $CompIfCtx(context),false)}
        else if(token==='for'){return new $TargetListCtx(new $CompForCtx(context))}
        else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='condition'){

        if(token===':'){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='decorator'){
    
        if(token==='id' && context.tree.length===0){
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])
        }else if(token==='eol'){return $transition(context.parent,token)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='def'){
    
        if(token==='id'){
            if(context.name){
                $_SyntaxError(context,'token '+token+' after '+context)
            }else{
                context.set_name(arguments[2])
                return context
            }
        }else if(token==='('){context.has_args=true;return new $FuncArgs(context)}
        else if(token===':' && context.has_args){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='del'){

        if(token==='eol'){return $transition(context.parent,token)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='dict_or_set'){ 

        if(context.closed){
            if(token==='['){return new $SubCtx(context.parent)}
            else if(token==='('){return new $CallArgCtx(new $CallCtx(context))}
            //else if(token==='.'){return new $AttrCtx(context)}
            else if(token==='op'){
                return new $AbstractExprCtx(new $OpCtx(context,arguments[2]),false)
            }else{return $transition(context.parent,token,arguments[2])}
        }else{
            if(context.expect===','){
                if(token==='}'){
                    if(context.real==='dict_or_set'&&context.tree.length===1){
                        // set with single element
                        context.real = 'set'
                    }
                    if(['set','set_comp','dict_comp'].indexOf(context.real)>-1||
                        (context.real==='dict'&&context.tree.length%2===0)){
                        context.items = context.tree
                        context.tree = []
                        context.closed = true
                        return context
                    }else{$_SyntaxError(context,'token '+token+' after '+context)}
                }else if(token===','){
                    if(context.real==='dict_or_set'){context.real='set'}
                    if(context.real==='dict' && context.tree.length%2){
                        $_SyntaxError(context,'token '+token+' after '+context)
                    }
                    context.expect = 'id'
                    return context
                }else if(token===':'){
                    if(context.real==='dict_or_set'){context.real='dict'}
                    if(context.real==='dict'){
                        context.expect=','
                        return new $AbstractExprCtx(context,false)
                    }else{$_SyntaxError(context,'token '+token+' after '+context)}
                }else if(token==='for'){
                    // comprehension
                    $clear_ns(context) // if defined inside a function
                    if(context.real==='dict_or_set'){context.real = 'set_comp'}
                    else{context.real='dict_comp'}
                    var lst = new $ListOrTupleCtx(context,'dict_or_set_comp')
                    lst.intervals = [context.start+1]
                    lst.vars = context.vars
                    context.tree.pop()
                    lst.expression = context.tree
                    context.tree = [lst]
                    lst.tree = []
                    var comp = new $ComprehensionCtx(lst)
                    return new $TargetListCtx(new $CompForCtx(comp))

                }else{$_SyntaxError(context,'token '+token+' after '+context)}   
            }else if(context.expect==='id'){
                if(token==='}'){
                    if(context.tree.length==0){ // empty dict
                        context.items = []
                        context.real = 'dict'
                    }else{ // trailing comma, eg {'a':1,'b':2,}
                        context.items = context.tree
                    }              
                    context.tree = []
                    context.closed = true
                    return context
                }else if($expr_starters.indexOf(token)>-1){
                    context.expect = ','
                    var expr = new $AbstractExprCtx(context,false)
                    return $transition(expr,token,arguments[2])
                }else{$_SyntaxError(context,'token '+token+' after '+context)}
            }else{return $transition(context.parent,token,arguments[2])}
        }

    }else if(context.type==='double_star_arg'){
    
        if($expr_starters.indexOf(token)>-1){
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])
        }else if(token===','){return context.parent}
        else if(token===')'){return $transition(context.parent,token)}
        else if(token===':' && context.parent.parent.type==='lambda'){
            return $transition(context.parent.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='except'){ 

        if($expr_starters.indexOf(token)>-1 && context.expect==='id'){
            context.expect = 'as'
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])

        //if(token==='id' && context.expect==='id'){
        //    new $TargetCtx(context,arguments[2])
        //    context.expect='as'
        //    return context
        }else if(token==='as' && context.expect==='as'
            && context.has_alias===undefined) {  // only one alias allowed
            context.expect = 'alias'
            context.has_alias = true
            return context
        }else if(token==='id' && context.expect==='alias'){
            context.expect=':'
            context.tree[0].alias = arguments[2]
            return context
        }else if(token===':' && ['id','as',':'].indexOf(context.expect)>-1){
            return $BodyCtx(context)
        }else if(token==='(' && context.expect==='id' && context.tree.length===0){
            context.parenth = true
            return context
        }else if(token===')' && [',','as'].indexOf(context.expect)>-1){
            context.expect = 'as'
            return context
        }else if(token===',' && context.parenth!==undefined &&
            context.has_alias === undefined &&
            ['as',','].indexOf(context.expect)>-1){
                context.expect='id'
                return context
        }else{$_SyntaxError(context,'token '+token+' after '+context.expect)}
    
    }else if(context.type==='expr'){

        if($expr_starters.indexOf(token)>-1 && context.expect==='expr'){
            context.expect = ','
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])
        }else if(token==='not'&&context.expect===','){
            return new $ExprNot(context)
        }else if(token==='in'&&context.expect===','){
            return $transition(context,'op','in')
        }else if(token===',' && context.expect===','){
            if(context.with_commas){
                // implicit tuple
                context.parent.tree.pop()
                var tuple = new $ListOrTupleCtx(context.parent,'tuple')
                tuple.tree = [context]
                return tuple
            }else{return $transition(context.parent,token)}
        }else if(token==='.'){return new $AttrCtx(context)}
        else if(token==='['){return new $AbstractExprCtx(new $SubCtx(context),false)}
        else if(token==='('){return new $CallCtx(context)}
        else if(token==='op'){
            // handle operator precedence
            var op_parent=context.parent,op=arguments[2]
            var op1 = context.parent,repl=null
            while(true){
                if(op1.type==='expr'){op1=op1.parent}
                else if(op1.type==='op'&&$op_weight[op1.op]>=$op_weight[op]){repl=op1;op1=op1.parent}
                else{break}
            }
            if(repl===null){
                if(['and','or'].indexOf(op)>-1){
                    while(context.parent.type==='not'||
                        (context.parent.type==='expr'&&context.parent.parent.type==='not')){
                        // 'and' and 'or' have higher precedence than 'not'
                        context = context.parent
                        op_parent = context.parent
                    }
                }else{
                    while(true){
                        if(context.parent!==op1){
                            context = context.parent
                            op_parent = context.parent
                        }else{
                            break
                        }
                    }
                }
                context.parent.tree.pop()
                var expr = new $ExprCtx(op_parent,'operand',context.with_commas)
                expr.expect = ','
                context.parent = expr
                var new_op = new $OpCtx(context,op)
                return new $AbstractExprCtx(new_op,false)
            }
            if(repl.type==='op'
                && ['<','<=','==','!=','is','>=','>'].indexOf(repl.op)>-1
                && ['<','<=','==','!=','is','>=','>'].indexOf(op)>-1){
                    // chained comparisons such as 1 <= 3 < 5
                    // replace by (c1 op1 c2) and (c2 op ...)
                    repl.parent.tree.pop()
                    var and_expr = new $OpCtx(repl,'and')
                    var c2 = repl.tree[1] // right operand of op1
                    // clone c2
                    var c2_clone = new Object()
                    for(var attr in c2){c2_clone[attr]=c2[attr]}
                    c2_clone.parent = and_expr
                    // add fake element to and_expr : it will be removed
                    // when new_op is created at the next line
                    and_expr.tree.push('xxx')
                    var new_op = new $OpCtx(c2_clone,op)
                    return new $AbstractExprCtx(new_op,false)
            }
            repl.parent.tree.pop()
            var expr = new $ExprCtx(repl.parent,'operand',false)
            expr.tree = [op1]
            repl.parent = expr
            var new_op = new $OpCtx(repl,op) // replace old operation
            //var res = new $AbstractExprCtx(new_op,false)
            return new $AbstractExprCtx(new_op,false)

        }else if(token==='augm_assign' && context.expect===','){
            return $augmented_assign(context,arguments[2])
        }else if(token==='=' && context.expect===','){
            if(context.parent.type==="call_arg"){
                return new $AbstractExprCtx(new $KwArgCtx(context),true)
            }else{
                while(context.parent!==undefined){context=context.parent}
                context = context.tree[0]
                return new $AbstractExprCtx(new $AssignCtx(context),true)
            }
        }else if(token==='if' && context.parent.type!=='comp_iterable'){ 
            // ternary operator : expr1 if cond else expr2
            return new $AbstractExprCtx(new $TernaryCtx(context),false)
        }else{return $transition(context.parent,token)}

    }else if(context.type==='expr_not'){
    
        if(token==='in'){ // expr not in : operator
            context.parent.tree.pop()
            return new $AbstractExprCtx(new $OpCtx(context.parent,'not_in'),false)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}
        
    }else if(context.type==='for'){
    
        if(token==='in'){return new $AbstractExprCtx(context,true)}
        else if(token===':'){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='from'){

        if((token==='id'||token==='.') && context.expect==='module'){
            if(token==='id'){context.module += arguments[2]}
            else{context.module += '.'}
            return context
        }else if(token==='import' && context.expect==='module'){
            context.expect = 'id'
            return context
        }else if(token==='id' && context.expect==='id'){
            context.names.push(arguments[2])
            context.expect = ','
            return context
        }else if(token==='op' && arguments[2]==='*' 
            && context.expect==='id'
            && context.names.length ===0){
            context.names.push('*')
            context.expect = 'eol'
            return context
        }else if(token===',' && context.expect===','){
            context.expect = 'id'
            return context
        }else if(token==='eol' && 
            (context.expect ===',' || context.expect==='eol')){
            return $transition(context.parent,token)
        }else if (token==='as' &&
            (context.expect ===',' || context.expect==='eol')){
            context.expect='alias'
            return context
        }else if(token==='id' && context.expect==='alias'){
            context.aliases[context.names[context.names.length-1]]= arguments[2]
            context.expect=','
            return context
        }else if (token==='(' && context.expect === 'id') {
            context.expect='id'
            return context
        }else if (token===')' && context.expect === ',') {
            context.expect='eol'
            return context
        }else{$_SyntaxError(context,'token '+token+' after '+context)}
            

    }else if(context.type==='func_arg_id'){
        if(token==='=' && context.expect==='='){
            context.parent.has_default = true
            return new $AbstractExprCtx(context,false)
        }else if(token===',' || token===')'){
            if(context.parent.has_default && context.tree.length==0){
                $pos -= context.name.length
                $_SyntaxError(context,['non-default argument follows default argument'])
            }else{
                return $transition(context.parent,token)
            }
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='func_args'){
    
        if(token==='id' && context.expect==='id'){
            context.expect = ','
            if(context.names.indexOf(arguments[2])>-1){
                $_SyntaxError(context,['duplicate argument '+arguments[2]+' in function definition'])
            }
            return new $FuncArgIdCtx(context,arguments[2])
        }else if(token===','){
            if(context.has_kw_arg){$_SyntaxError(context,'duplicate kw arg')}
            else if(context.expect===','){
                context.expect = 'id'
                return context
            }else{$_SyntaxError(context,'token '+token+' after '+context)}
        }else if(token===')'){
            if(context.expect===','){return context.parent}
            else if(context.tree.length==0){return context.parent} // no argument
            else{$_SyntaxError(context,'token '+token+' after '+context)}
        }else if(token==='op'){
            var op = arguments[2]
            context.expect = ','
            if(op=='*'){
                if(context.has_star_arg){$_SyntaxError(context,'duplicate star arg')}
                return new $FuncStarArgCtx(context,'*')
            }else if(op=='**'){
                return new $FuncStarArgCtx(context,'**')
            }else{$_SyntaxError(context,'token '+op+' after '+context)}
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='func_star_arg'){
    
        if(token==='id' && context.name===undefined){
            if(context.parent.names.indexOf(arguments[2])>-1){
                $_SyntaxError(context,['duplicate argument '+arguments[2]+' in function definition'])
            }
            context.set_name(arguments[2])
            context.parent.names.push(arguments[2])
            return context.parent
        }else if(token==',' && context.name===undefined){
            // anonymous star arg - found in configparser
            context.set_name('$dummy')
            context.parent.names.push('$dummy')
            return $transition(context.parent,token)
        }else if(token==')'){
            // anonymous star arg - found in configparser
            context.set_name('$dummy')
            context.parent.names.push('$dummy')
            return $transition(context.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='global'){

        if(token==='id' && context.expect==='id'){
            new $IdCtx(context,arguments[2])
            context.expect=','
            return context
        }else if(token===',' && context.expect===','){
            context.expect='id'
            return context
        }else if(token==='eol' && context.expect===','){
            return $transition(context.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}
        

    }else if(context.type==='id'){

        if(token==='='){
            if(context.parent.type==='expr' &&
                context.parent.parent !== undefined &&
                context.parent.parent.type ==='call_arg'){
                    return new $AbstractExprCtx(new $KwArgCtx(context.parent),false)
            }else{return $transition(context.parent,token,arguments[2])}             
        }else if(token==='op'){
            return $transition(context.parent,token,arguments[2])
        }else if(['id','str','int','float'].indexOf(token)>-1){
            $_SyntaxError(context,'token '+token+' after '+context)
        }else{
            return $transition(context.parent,token,arguments[2])
        }

    }else if(context.type==='import'){
    
        if(token==='id' && context.expect==='id'){
            new $ImportedModuleCtx(context,arguments[2])
            context.expect=','
            return context
        }else if(token==='.' && context.expect===','){
            context.expect = 'qual'
            return context
        }else if(token==='id' && context.expect==='qual'){
            context.expect = ','
            context.tree[context.tree.length-1].name += '.'+arguments[2]
            context.tree[context.tree.length-1].alias += '.'+arguments[2]
            return context
        }else if(token===',' && context.expect===','){
            context.expect = 'id'
            return context
        }else if(token==='as' && context.expect===','){
            context.expect = 'alias'
            return context
        }else if(token==='id' && context.expect==='alias'){
            context.expect = ','
            context.tree[context.tree.length-1].alias = arguments[2]
            var mod_name=context.tree[context.tree.length-1].name;
            __BRYTHON__.$py_module_alias[mod_name]=arguments[2]
            return context
        }else if(token==='eol' && context.expect===','){
            return $transition(context.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='int'||context.type==='float'){
    
        if($expr_starters.indexOf(token)>-1){
            $_SyntaxError(context,'token '+token+' after '+context)
        }else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='kwarg'){

        if(token===','){return new $CallArgCtx(context.parent)}
        else{return $transition(context.parent,token)}

    }else if(context.type==="lambda"){
    
        if(token===':' && context.args===undefined){
            context.args = context.tree
            context.tree = []
            context.body_start = $pos
            return new $AbstractExprCtx(context,false)
        }else if(context.args!==undefined){ // returning from expression
            context.body_end = $pos
            return $transition(context.parent,token)
        }else if(context.args===undefined){
            return $transition(new $CallCtx(context),token,arguments[2])
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='list_or_tuple'){ 

        if(context.closed){
            if(token==='['){return new $SubCtx(context.parent)}
            else if(token==='('){return new $CallCtx(context)}
            else if(token==='op'){
                return new $AbstractExprCtx(new $OpCtx(context,arguments[2]),false)
            }
            else{return $transition(context.parent,token,arguments[2])}
        }else{
            if(context.expect===','){
                if((context.real==='tuple'||context.real==='gen_expr')
                    && token===')'){
                    context.closed = true
                    if(context.real==='gen_expr'){context.intervals.push($pos)}
                    return context.parent
                }else if((context.real==='list'||context.real==='list_comp')
                    && token===']'){
                    context.closed = true
                    if(context.real==='list_comp'){context.intervals.push($pos)}
                    return context
                }else if(context.real==='dict_or_set_comp' && token==='}'){
                    context.intervals.push($pos)
                    return $transition(context.parent,token)
                }else if(token===','){
                    if(context.real==='tuple'){context.has_comma=true}
                    context.expect = 'id'
                    return context
                }else if(token==='for'){
                    // comprehension
                    if(context.real==='list'){context.real = 'list_comp'}
                    else{context.real='gen_expr'}
                    // remove names already referenced in list from the function
                    // references
                    $clear_ns(context)
                    context.intervals = [context.start+1]
                    context.expression = context.tree
                    context.tree = [] // reset tree
                    var comp = new $ComprehensionCtx(context)
                    return new $TargetListCtx(new $CompForCtx(comp))
                }else{return $transition(context.parent,token,arguments[2])}   
            }else if(context.expect==='id'){
                if(context.real==='tuple' && token===')'){
                    context.closed = true
                    return context.parent
                }else if(context.real==='gen_expr' && token===')'){
                    context.closed = true
                    return $transition(context.parent,token)
                }else if(context.real==='list'&& token===']'){
                    context.closed = true
                    return context
                }else if(token !==')'&&token!==']'&&token!==','){
                    context.expect = ','
                    var expr = new $AbstractExprCtx(context,false)
                    return $transition(expr,token,arguments[2])
                }else if(token==','){
                    $_SyntaxError(context,'unexpected comma inside list')
                }
            }else{return $transition(context.parent,token,arguments[2])}
        }

    }else if(context.type==='list_comp'){ 

        if(token===']'){return context.parent}
        else if(token==='in'){return new $ExprCtx(context,'iterable',true)}
        else if(token==='if'){return new $ExprCtx(context,'condition',true)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='node'){
    
        if($expr_starters.indexOf(token)>-1){
            var expr = new $AbstractExprCtx(context,true)
            return $transition(expr,token,arguments[2])
        }else if(token==="op" && '+-~'.search(arguments[2])>-1){
            var expr = new $AbstractExprCtx(context,true)
            return $transition(expr,token,arguments[2])
        }else if(token==='class'){return new $ClassCtx(context)}
        else if(token==='break'){return new $BreakCtx(context)}
        else if(token==='def'){return new $DefCtx(context)}
        else if(token==='for'){return new $TargetListCtx(new $ForExpr(context))}
        else if(['if','elif','while'].indexOf(token)>-1){
            return new $AbstractExprCtx(new $ConditionCtx(context,token),false)
        }else if(['else','finally'].indexOf(token)>-1){
            return new $SingleKwCtx(context,token)
        }else if(token==='try'){return new $TryCtx(context)}
        else if(token==='except'){return new $ExceptCtx(context)}
        else if(token==='assert'){return new $AbstractExprCtx(new $AssertCtx(context),'assert',true)}
        else if(token==='from'){return new $FromCtx(context)}
        else if(token==='import'){return new $ImportCtx(context)}
        else if(token==='global'){return new $GlobalCtx(context)}
        else if(token==='nonlocal'){return new $NonlocalCtx(context)}
        else if(token==='lambda'){return new $LambdaCtx(context)}
        else if(token==='pass'){return new $PassCtx(context)}
        else if(token==='raise'){return new $RaiseCtx(context)}
        else if(token==='return'){
            var ret = new $ReturnCtx(context)
            return new $AbstractExprCtx(ret,true)
        }else if(token==="with"){return new $AbstractExprCtx(new $WithCtx(context),false)}
        else if(token==='yield'){
            var yield = new $YieldCtx(context)
            return new $AbstractExprCtx(yield,true)
        }else if(token==='del'){return new $AbstractExprCtx(new $DelCtx(context),true)}
        else if(token==='@'){return new $DecoratorCtx(context)}
        else if(token==='eol'){
            if(context.tree.length===0){ // might be the case after a :
                context.node.parent.children.pop()
                return context.node.parent.context
            }
            return context
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='not'){
        if(token==='in'){ // operator not_in
            // not is always in an expression : remove it
            context.parent.parent.tree.pop() // remove 'not'
            return new $ExprCtx(new $OpCtx(context.parent,'not_in'),'op',false)
        }else if($expr_starters.indexOf(token)>-1){
            var expr = new $AbstractExprCtx(context,false)
            return $transition(expr,token,arguments[2])
        }else{return $transition(context.parent,token)}

    }else if(context.type==='op'){ 
    
        if($expr_starters.indexOf(token)>-1){
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])
        }else if(token==='op' && '+-~'.search(arguments[2])>-1){
            return new $UnaryCtx(context,arguments[2])
        }else{return $transition(context.parent,token)}

    }else if(context.type==='pass'){ 

        if(token==='eol'){return context.parent}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='raise'){ 

        if(token==='id' && context.tree.length===0){
            return new $IdCtx(new $ExprCtx(context,'exc',false),arguments[2])
        }else if(token=='from' && context.tree.length>0){
            return new $AbstractExprCtx(context,false)
        }else if(token==='eol'){
            return $transition(context.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='return'){

        return $transition(context.parent,token)

    }else if(context.type==='single_kw'){

        if(token===':'){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='star_arg'){

        if($expr_starters.indexOf(token)>-1){
            return $transition(new $AbstractExprCtx(context,false),token,arguments[2])
        }else if(token===','){return $transition(context.parent,token)}
        else if(token===')'){return $transition(context.parent,token)}
        else if(token===':' && context.parent.parent.type==='lambda'){
            return $transition(context.parent.parent,token)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='str'){

        if(token==='['){return new $AbstractExprCtx(new $SubCtx(context.parent),false)}
        else if(token==='('){return new $CallCtx(context)}
        else if(token=='str'){
            context.tree.push(arguments[2])
            return context
        }else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='sub'){ 
    
        // subscription x[a] or slicing x[a:b:c]
        if($expr_starters.indexOf(token)>-1){
            var expr = new $AbstractExprCtx(context,false)
            return $transition(expr,token,arguments[2])
        }else if(token===']'){return context.parent}
        else if(token===':'){
            return new $AbstractExprCtx(context,false)
        }else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='target_list'){
    
        if(token==='id' && context.expect==='id'){
            context.expect = ','
            new $IdCtx(context,arguments[2])
            return context
        }else if((token==='('||token==='[')&&context.expect==='id'){
            context.expect = ','
            return new $TargetListCtx(context)
        }else if((token===')'||token===']')&&context.expect===','){
            return context.parent
        }else if(token===',' && context.expect==','){
            context.expect='id'
            return context
        }else if(context.expect===','){return $transition(context.parent,token,arguments[2])}
        else{$_SyntaxError(context,'token '+token+' after '+context)}

    }else if(context.type==='ternary'){
    
        if(token==='else'){return new $AbstractExprCtx(context,false)}
        else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='try'){ 

        if(token===':'){return $BodyCtx(context)}
        else{$_SyntaxError(context,'token '+token+' after '+context)}
    
    }else if(context.type==='unary'){

        if(['int','float'].indexOf(token)>-1){
            // replace by real value of integer or float
            // parent of context is a $ExprCtx
            // grand-parent is a $AbstractExprCtx
            // we remove the $ExprCtx and trigger a transition 
            // from the $AbstractExpCtx with an integer or float
            // of the correct value
            context.parent.parent.tree.pop()
            var value = arguments[2]
            if(context.op==='-'){value=-value}
            if(context.op==='~'){value=~value}
            return $transition(context.parent.parent,token,value)
        }else if(token==='id'){
            // replace by x.__neg__(), x.__invert__ or x
            context.parent.parent.tree.pop()
            var expr = new $ExprCtx(context.parent.parent,'call',false)
            var expr1 = new $ExprCtx(expr,'id',false)
            new $IdCtx(expr1,arguments[2]) // create id
            if(context.op !== '+'){
                var repl = new $AttrCtx(expr)
                if(context.op==='-'){repl.name='__neg__'}
                else{repl.name='__invert__'}
                // method is called with no argument
                var call = new $CallCtx(expr)
                // new context is the expression above the id
                return expr1
            }
            return context.parent
        }else if(token==="op" && '+-'.search(arguments[2])>-1){
            var op = arguments[2]
            if(context.op===op){context.op='+'}else{context.op='-'}
            return context
        }else{return $transition(context.parent,token,arguments[2])}

    }else if(context.type==='with'){ 

        if(token==='id' && context.expect==='id'){
            new $TargetCtx(context,arguments[2])
            context.expect='as'
            return context
        }else if(token==='as' && context.expect==='as'
            && context.has_alias===undefined  // only one alias allowed
            && context.tree.length===1){ // if aliased, must be the only exception
            context.expect = 'alias'
            context.has_alias = true
            return context
        }else if(token==='id' && context.expect==='alias'){
            if(context.parenth!==undefined){context.expect = ','}
            else{context.expect=':'}
            context.tree[context.tree.length-1].alias = arguments[2]
            return context
        }else if(token===':' && ['id','as',':'].indexOf(context.expect)>-1){
            return $BodyCtx(context)
        }else if(token==='(' && context.expect==='id' && context.tree.length===0){
            context.parenth = true
            return context
        }else if(token===')' && [',','as'].indexOf(context.expect)>-1){
            context.expect = ':'
            return context
        }else if(token===',' && context.parenth!==undefined &&
            context.has_alias === undefined &&
            ['as',','].indexOf(context.expect)>-1){
                context.expect='id'
                return context
        }else{$_SyntaxError(context,'token '+token+' after '+context.expect)}

    }else if(context.type==='yield'){

        if(token=='from'){ // form "yield from <expr>"
            return new $AbstractExprCtx(context,true)
        }
        return $transition(context.parent,token)

    }
}

__BRYTHON__.forbidden = ['alert','case','catch','constructor','Date','delete',
    'default','document','Error','history','function','location','Math','new','Number','RegExp',
    'this','throw','var','super','window']

function $tokenize(src,module,parent){
    var delimiters = [["#","\n","comment"],['"""','"""',"triple_string"],
        ["'","'","string"],['"','"',"string"],
        ["r'","'","raw_string"],['r"','"',"raw_string"]]
    var br_open = {"(":0,"[":0,"{":0}
    var br_close = {")":"(","]":"[","}":"{"}
    var br_stack = ""
    var br_pos = new Array()
    var kwdict = ["class","return","break",
        "for","lambda","try","finally","raise","def","from",
        "nonlocal","while","del","global","with",
        "as","elif","else","if","yield","assert","import",
        "except","raise","in","not","pass","with"
        //"False","None","True","continue",
        // "and',"or","is"
        ]
    var unsupported = []
    var $indented = ['class','def','for','condition','single_kw','try','except','with']
    // from https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Reserved_Words

    var punctuation = {',':0,':':0} //,';':0}
    var int_pattern = new RegExp("^\\d+")
    var float_pattern1 = new RegExp("^\\d+\\.\\d*([eE][+-]?\\d+)?")
    var float_pattern2 = new RegExp("^\\d+([eE][+-]?\\d+)")
    var hex_pattern = new RegExp("^0[xX]([0-9a-fA-F]+)")
    var octal_pattern = new RegExp("^0[oO]([0-7]+)")
    var binary_pattern = new RegExp("^0[bB]([01]+)")
    var id_pattern = new RegExp("[\\$_a-zA-Z]\\w*")
    var qesc = new RegExp('"',"g") // escape double quotes
    var sqesc = new RegExp("'","g") // escape single quotes    

    var context = null
    var root = new $Node('module')
    root.module = module
    root.parent = parent
    root.indent = -1
    var new_node = new $Node('expression')
    var current = root
    var name = ""
    var _type = null
    var pos = 0
    indent = null

    var lnum = 1
    while(pos<src.length){
        var flag = false
        var car = src.charAt(pos)
        // build tree structure from indentation
        if(indent===null){
            var indent = 0
            while(pos<src.length){
                if(src.charAt(pos)==" "){indent++;pos++}
                else if(src.charAt(pos)=="\t"){ 
                    // tab : fill until indent is multiple of 8
                    indent++;pos++
                    while(indent%8>0){indent++}
                }else{break}
            }
            // ignore empty lines
            if(src.charAt(pos)=='\n'){pos++;lnum++;indent=null;continue}
            else if(src.charAt(pos)==='#'){ // comment
                var offset = src.substr(pos).search(/\n/)
                if(offset===-1){break}
                pos+=offset+1;lnum++;indent=null;continue
            }
            new_node.indent = indent
            new_node.line_num = lnum
            new_node.module = module
            // attach new node to node with indentation immediately smaller
            if(indent>current.indent){
                // control that parent ended with ':'
                if(context!==null){
                    if($indented.indexOf(context.tree[0].type)==-1){
                        $pos = pos
                        $_SyntaxError(context,'unexpected indent1',pos)
                    }
                }
                // add a child to current node
                current.add(new_node)
            }else if(indent<=current.indent &&
                $indented.indexOf(context.tree[0].type)>-1 &&
                context.tree.length<2){
                    $pos = pos
                    $_SyntaxError(context,'expected an indented block',pos)
            }else{ // same or lower level
                while(indent!==current.indent){
                    current = current.parent
                    if(current===undefined || indent>current.indent){
                        $pos = pos
                        $_SyntaxError(context,'unexpected indent2',pos)
                    }
                }
                current.parent.add(new_node)
            }
            current = new_node
            context = new $NodeCtx(new_node)
            continue
        }
        // comment
        if(car=="#"){
            var end = src.substr(pos+1).search('\n')
            if(end==-1){end=src.length-1}
            pos += end+1;continue
        }
        // string
        if(car=='"' || car=="'"){
            var raw = false
            var bytes = false
            var end = null
            if(name.length>0){
                if(name.toLowerCase()=="r"){ // raw string
                    raw = true;name=''
                }else if(name.toLowerCase()=='u'){
                    // in string literals, '\U' and '\u' escapes in raw strings 
                    // are not treated specially.
                    name = ''
                }else if(name.toLowerCase()=='b'){
                    bytes = true;name=''
                }else if(['rb','br'].indexOf(name.toLowerCase())>-1){
                    bytes=true;raw=true;name=''
                }
            }
            if(src.substr(pos,3)==car+car+car){_type="triple_string";end=pos+3}
            else{_type="string";end=pos+1}
            var escaped = false
            var zone = car
            var found = false
            while(end<src.length){
                if(escaped){
                    zone+=src.charAt(end)
                    if(raw && src.charAt(end)=='\\'){zone+='\\'}
                    escaped=false;end+=1
                }else if(src.charAt(end)=="\\"){
                    if(raw){
                        if(end<src.length-1 && src.charAt(end+1)==car){
                            zone += '\\\\'+car
                            end += 2
                        }else{
                            zone += '\\\\'
                            end++
                        }
                        escaped = true
                    } else {
                        if(src.charAt(end+1)=='\n'){
                            // explicit line joining inside strings
                            end += 2
                            lnum++
                        } else {
                            zone+='\\' //src.charAt(end);
                            escaped=true;end+=1
                        }
                    }
                } else if(src.charAt(end)==car){
                    if(_type=="triple_string" && src.substr(end,3)!=car+car+car){
                        zone += src.charAt(end)
                        end++
                    } else {
                        found = true
                        // end of string
                        $pos = pos
                        // Escape quotes inside string, except if they are already escaped
                        // In raw mode, always escape
                        var $string = zone.substr(1),string=''
                        for(var i=0;i<$string.length;i++){
                            var $car = $string.charAt(i)
                            if($car==car &&
                                (raw || (i==0 || $string.charAt(i-1)!=='\\'))){
                                    string += '\\'
                            }
                            string += $car
                        }
                        if(bytes){
                            context = $transition(context,'str','b'+car+string+car)
                        }else{
                            context = $transition(context,'str',car+string+car)
                        }
                        pos = end+1
                        if(_type=="triple_string"){pos = end+3}
                        break
                    }
                } else { 
                    zone += src.charAt(end)
                    if(src.charAt(end)=='\n'){lnum++}
                    end++
                }
            }
            if(!found){
                if(_type==="triple_string"){
                    $_SyntaxError(context,"Triple string end not found")
                }else{
                    $_SyntaxError(context,"String end not found")
                }
            }
            continue
        }
        // identifier ?
        if(name==""){
            if(car.search(/[a-zA-Z_]/)!=-1){
                name=car // identifier start
                pos++;continue
            }
        } else {
            if(car.search(/\w/)!=-1){
                name+=car
                pos++;continue
            } else{
                if(kwdict.indexOf(name)>-1){
                    $pos = pos-name.length
                    if(unsupported.indexOf(name)>-1){
                        $_SyntaxError(context,"Unsupported Python keyword '"+name+"'")                    
                    }
                    context = $transition(context,name)
                } else if($oplist.indexOf(name)>-1) { // and, or
                    $pos = pos-name.length
                    context = $transition(context,'op',name)
                } else {
                    if(__BRYTHON__.forbidden.indexOf(name)>-1){name='$$'+name}
                    $pos = pos-name.length
                    context = $transition(context,'id',name)
                }
                name=""
                continue
            }
        }
        // point, ellipsis (...)
        if(car=="."){
            if(pos<src.length-1 && '0123456789'.indexOf(src.charAt(pos+1))>-1){
                // number starting with . : add a 0 before the point
                src = src.substr(0,pos)+'0'+src.substr(pos)
                continue
            } 
            $pos = pos
            context = $transition(context,'.')
            pos++;continue
        }
        // octal, hexadecimal, binary
        if(car==="0"){
            var res = hex_pattern.exec(src.substr(pos))
            if(res){
                context=$transition(context,'int',parseInt(res[1],16))
                pos += res[0].length
                continue
            }
            var res = octal_pattern.exec(src.substr(pos))
            if(res){
                context=$transition(context,'int',parseInt(res[1],8))
                pos += res[0].length
                continue
            }
            var res = binary_pattern.exec(src.substr(pos))
            if(res){
                context=$transition(context,'int',parseInt(res[1],2))
                pos += res[0].length
                continue
            }
        }
        // number
        if(car.search(/\d/)>-1){
            // digit
            var res = float_pattern1.exec(src.substr(pos))
            if(res){
                if(res[0].search(/[eE]/)>-1){
                    $pos = pos
                    context = $transition(context,'float',res[0])
                }else{
                    $pos = pos
                    context = $transition(context,'float',eval(res[0]))
                }
            }else{
                res = float_pattern2.exec(src.substr(pos))
                if(res){
                    $pos =pos
                    context = $transition(context,'float',res[0])
                }else{
                    res = int_pattern.exec(src.substr(pos))
                    $pos = pos
                    context = $transition(context,'int',eval(res[0]))
                }
            }
            pos += res[0].length
            continue
        }
        // line end
        if(car=="\n"){
            lnum++
            if(br_stack.length>0){
                // implicit line joining inside brackets
                pos++;continue
            } else {
                if(current.context.tree.length>0){
                    $pos = pos
                    context = $transition(context,'eol')
                    indent=null
                    new_node = new $Node()
                }else{
                    new_node.line_num = lnum
                }
                pos++;continue
            }
        }
        if(car in br_open){
            br_stack += car
            br_pos[br_stack.length-1] = [context,pos]
            $pos = pos
            context = $transition(context,car)
            pos++;continue
        }
        if(car in br_close){
            if(br_stack==""){
                $_SyntaxError(context,"Unexpected closing bracket")
            } else if(br_close[car]!=br_stack.charAt(br_stack.length-1)){
                $_SyntaxError(context,"Unbalanced bracket")
            } else {
                br_stack = br_stack.substr(0,br_stack.length-1)
                $pos = pos
                context = $transition(context,car)
                pos++;continue
            }
        }
        if(car=="="){
            if(src.charAt(pos+1)!="="){
                $pos = pos
                context = $transition(context,'=')
                pos++;continue
            } else {
                $pos = pos
                context = $transition(context,'op','==')
                pos+=2;continue
            }
        }
        if(car in punctuation){
            $pos = pos
            context = $transition(context,car)
            pos++;continue
        }
        if(car===";"){ // next instruction
            $transition(context,'eol') // close previous instruction
            // create a new node, at the same level as current's parent
            if(current.context.tree.length===0){
                // consecutive ; are not allowed
                $pos=pos
                $_SyntaxError(context,'invalid syntax')
            }
            // if ; ends the line, ignore it
            var pos1 = pos+1
            var ends_line = false
            while(pos1<src.length){
                if(src.charAt(pos1)=='\n' || src.charAt(pos1)=='#'){
                    ends_line=true;break
                }
                else if(src.charAt(pos1)==' '){pos1++}
                else{break}
            }
            if(ends_line){pos++;continue}
            new_node = new $Node()
            new_node.indent = current.indent
            new_node.line_num = lnum
            new_node.module = module
            current.parent.add(new_node)
            current = new_node
            context = new $NodeCtx(new_node)
            pos++;continue
        }
        // operators
        if($first_op_letter.indexOf(car)>-1){
            // find longest match
            var op_match = ""
            for(op_sign in $operators){
                if(op_sign==src.substr(pos,op_sign.length) 
                    && op_sign.length>op_match.length){
                    op_match=op_sign
                }
            }
            $pos = pos
            if(op_match.length>0){
                if(op_match in $augmented_assigns){
                    context = $transition(context,'augm_assign',op_match)
                }else{
                    context = $transition(context,'op',op_match)
                }
                pos += op_match.length
                continue
            }
        }
        if(car=='\\' && src.charAt(pos+1)=='\n'){
            lnum++;pos+=2;continue
        }
        if(car=='@'){
            $pos = pos
            context = $transition(context,car)
            pos++;continue
        }
        if(car!=' '&&car!=='\t'){$pos=pos;$_SyntaxError(context,'unknown token ['+car+']')}
        pos += 1
    }

    if(br_stack.length!=0){
        var br_err = br_pos[0]
        $pos = br_err[1]
        $_SyntaxError(br_err[0],["Unbalanced bracket "+br_stack.charAt(br_stack.length-1)])
    }
    if(context!==null && $indented.indexOf(context.tree[0].type)>-1){
        $pos = pos-1
        $_SyntaxError(context,'expected an indented block',pos)    
    }
    
    return root

}

__BRYTHON__.py2js = function(src,module,parent){
    // src = Python source (string)
    // module = module name (string)
    // parent = the name of the "calling" module, eg for a list comprehension (string)
    var src = src.replace(/\r\n/gm,'\n')
    while (src.length>0 && (src.charAt(0)=="\n" || src.charAt(0)=="\r")){
        src = src.substr(1)
    }
    if(src.charAt(src.length-1)!="\n"){src+='\n'}
    if(module===undefined){module='__main__'}
    // Python built-in variable __name__
    var __name__ = module
    if(__BRYTHON__.scope[module]===undefined){
        __BRYTHON__.scope[module] = {}
        __BRYTHON__.scope[module].__dict__ = {}
    }
    document.$py_src[module]=src
    var root = $tokenize(src,module,parent)
    root.transform()
    // add variable $globals
    var js = 'var $globals = __BRYTHON__.scope["'+module+'"].__dict__\nvar $locals = $globals\n'
    js += 'var __builtins__ = __BRYTHON__.builtins;\n'
    js += 'for(var $py_builtin in __builtins__)'
    js += '{eval("var "+$py_builtin+"=__builtins__[$py_builtin]")}\n'
    js += 'var JSObject = __BRYTHON__.JSObject\n'
    js += 'var JSConstructor = __BRYTHON__.JSConstructor\n'
    var new_node = new $Node('expression')
    new $NodeJSCtx(new_node,js)
    root.insert(0,new_node)
    // module doc string
    var ds_node = new $Node('expression')
    new $NodeJSCtx(ds_node,'var __doc__=$globals["__doc__"]='+root.doc_string)
    root.insert(1,ds_node)
    // name
    var name_node = new $Node('expression')
    var lib_module = module
    if(module.substr(0,9)=='__main__,'){lib_module='__main__'}
    new $NodeJSCtx(name_node,'var __name__=$globals["__name__"]="'+lib_module+'"')
    root.insert(2,name_node)
    // file
    var file_node = new $Node('expression')
    new $NodeJSCtx(file_node,'var __file__=$globals["__file__"]="'+__BRYTHON__.$py_module_path[module]+'"')
    root.insert(3,file_node)
        
    if(__BRYTHON__.debug>0){$add_line_num(root,null,module)}
    __BRYTHON__.modules[module] = root
    return root
}

function brython(options){
    document.$py_src = {}
    __BRYTHON__.$py_module_path = {}
    __BRYTHON__.$py_module_alias = {}
    __BRYTHON__.path_hooks = []
    //__BRYTHON__.$py_modules = {}
    __BRYTHON__.modules = {}
    __BRYTHON__.imported = {}
    __BRYTHON__.$py_next_hash = -Math.pow(2,53)

    // debug level
    if(options===undefined){options={'debug':0}}
    if(typeof options==='number'){options={'debug':options}}
    __BRYTHON__.debug = options.debug

    if (options.open !== undefined) {__BRYTHON__.builtins.$open = options.open}
    __BRYTHON__.builtins.$CORS=false        // Cross-origin resource sharing
    if (options.CORS !== undefined) {__BRYTHON__.builtins.$CORS = options.CORS}
    __BRYTHON__.$options=options
    __BRYTHON__.exception_stack = []
    __BRYTHON__.call_stack = []
    __BRYTHON__.scope = {}
    __BRYTHON__.events = __BRYTHON__.builtins.dict() // maps $brython_id of DOM elements to events
    var $elts = document.getElementsByTagName("script")
    var $href = window.location.href
    var $href_elts = $href.split('/')
    $href_elts.pop()
    var $script_path = $href_elts.join('/')

    __BRYTHON__.path = []
    if (options.pythonpath!==undefined) {
       __BRYTHON__.path = options.pythonpath
    }
    if (!(__BRYTHON__.path.indexOf($script_path) > -1)) {
       __BRYTHON__.path.push($script_path)
    }

    // get path of brython.js or py2js to determine brython_path
    // it will be used for imports

    for(var $i=0;$i<$elts.length;$i++){
        var $elt = $elts[$i]
        var $br_scripts = ['brython.js','py2js.js','brython_full.js']
        for(var $j=0;$j<$br_scripts.length;$j++){
            var $bs = $br_scripts[$j]
            if($elt.src.substr($elt.src.length-$bs.length)==$bs){
                if($elt.src.length===$bs.length ||
                    $elt.src.charAt($elt.src.length-$bs.length-1)=='/'){
                        var $path = $elt.src.substr(0,$elt.src.length-$bs.length)
                        __BRYTHON__.brython_path = $path
                        if (!(__BRYTHON__.path.indexOf($path+'Lib')> -1)) {
                           __BRYTHON__.path.push($path+'Lib')
                        }
                        break
                }
            }
        }
    }

    // get all scripts with type = text/python and run them
    
    for(var $i=0;$i<$elts.length;$i++){
        var $elt = $elts[$i]
        if($elt.type=="text/python"||$elt.type==="text/python3"){
            var $src = null
            if($elt.src!==''){ 
                // format <script type="text/python" src="python_script.py">
                // get source code by an Ajax call
                if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
                    var $xmlhttp=new XMLHttpRequest();
                }else{// code for IE6, IE5
                    var $xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
                }
                $xmlhttp.onreadystatechange = function(){
                    var state = this.readyState
                    if(state===4){
                        $src = $xmlhttp.responseText
                    }
                }
                $xmlhttp.open('GET',$elt.src,false)
                $xmlhttp.send()
                __BRYTHON__.$py_module_path['__main__']=$elt.src 
                var $src_elts = $elt.src.split('/')
                $src_elts.pop()
                var $src_path = $src_elts.join('/')
                if (__BRYTHON__.path.indexOf($src_path) == -1) {
                    // insert in first position : folder /Lib with built-in modules
                    // should be the last used when importing scripts
                    __BRYTHON__.path.splice(0,0,$src_path)
                }
            }else{
                var $src = ($elt.innerHTML || $elt.textContent)
                __BRYTHON__.$py_module_path['__main__'] = $href
            }

            try{
                var $root = __BRYTHON__.py2js($src,'__main__')
                var $js = $root.to_js()
                if(__BRYTHON__.debug>1){console.log($js)}
                eval($js)
                var _mod = $globals
                for(var $attr in $globals){
                    //console.log('var '+$attr)
                }
                _mod.__class__ = __BRYTHON__.$ModuleDict
                _mod.__name__ = '__main__'
                _mod.__file__ = __BRYTHON__.$py_module_path['__main__']
                __BRYTHON__.imported['__main__'] = _mod
            }catch($err){
                console.log('PY2JS '+$err)
                for(var attr in $err){
                    console.log(attr+' : '+$err[attr])
                }
                console.log('line info '+__BRYTHON__.line_info)
                if($err.py_error===undefined){$err = __BRYTHON__.builtins.RuntimeError($err+'')}
                var $trace = $err.__name__+': '+$err.message
                //if($err.__name__=='SyntaxError'||$err.__name__==='IndentationError'){
                    $trace += '\n'+$err.info
                //}
                __BRYTHON__.stderr.__getattr__('write')($trace)
                //$err.message += '\n'+$err.info
                throw $err
            }
        }
    }
}
__BRYTHON__.$operators = $operators
__BRYTHON__.$Node = $Node
__BRYTHON__.$NodeJSCtx = $NodeJSCtx

// in case the name 'brython' is used in a Javascript library,
// we can use __BRYTHON__.brython

__BRYTHON__.brython = brython 
                              
})()
var brython = __BRYTHON__.brython

