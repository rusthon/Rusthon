// PythonScript Runtime - regenerated on: Tue Nov 26 02:12:03 2013
__NULL_OBJECT__ = Object.create(null);
if (( "window" )  in  this && ( "document" )  in  this) {
  __NODEJS__ = false;
  pythonjs = {  };
} else {
  __NODEJS__ = true;
  console.log(process.title);
  console.log(process.version);
}
jsrange = function(num) {
  "Emulates Python's range function";
  var i, r;
  i = 0;
  r = [];
  while(( i ) < num) {
    r.push(i);
    i = i + 1;
  }
  return r;
}

__create_array__ = function() {
  "Used to fix a bug/feature of Javascript where new Array(number)\n	created a array with number of undefined elements which is not\n	what we want";
  var array;
  array = [];
    var iter = jsrange(arguments.length);

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var i=0; i < iter.length; i++) {
    var backup = i; i = iter[i];
    array.push(arguments[i]);
    i = backup;
  }
  return array;
}

adapt_arguments = function(handler) {
  "Useful to transform Javascript arguments to Python arguments";
    var func = function() {
    handler(Array.prototype.slice.call(arguments));
  }

  return func;
}

__get__ = function(object, attribute) {
  "Retrieve an attribute, method, property, or wrapper function.\n\n	method are actually functions which are converted to methods by\n	prepending their arguments with the current object. Properties are\n	not functions!\n\n	DOM support:\n		http://stackoverflow.com/questions/14202699/document-createelement-not-working\n		https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof\n\n	Direct JavaScript Calls:\n		if an external javascript function is found, and it was not a wrapper that was generated here,\n		check the function for a 'cached_wrapper' attribute, if none is found then generate a new\n		wrapper, cache it on the function, and return the wrapper.\n	";
  if (( attribute ) == "__call__") {
    if (object.pythonscript_function || object.is_wrapper) {
      return object;
    } else {
      if (object.cached_wrapper) {
        return object.cached_wrapper;
      } else {
        if ({}.toString.call(object) === '[object Function]') {
                    var wrapper = function(args, kwargs) {
            return object.apply(undefined, args);
          }

          wrapper.is_wrapper = true;
          object.cached_wrapper = wrapper;
          return wrapper;
        }
      }
    }
  }
  if (Object.hasOwnProperty.call(object, "__getattribute__")) {
    return object.__getattribute__(attribute);
  }
  var attr;
  attr = object[attribute];
  if (( __NODEJS__ ) === false) {
    if (object instanceof HTMLDocument) {
      if (typeof(attr) === 'function') {
                var wrapper = function(args, kwargs) {
          return attr.apply(object, args);
        }

        wrapper.is_wrapper = true;
        return wrapper;
      } else {
        return attr;
      }
    } else {
      if (object instanceof HTMLElement) {
        if (typeof(attr) === 'function') {
                    var wrapper = function(args, kwargs) {
            return attr.apply(object, args);
          }

          wrapper.is_wrapper = true;
          return wrapper;
        } else {
          return attr;
        }
      }
    }
  }
  if (( attr ) !== undefined) {
    if (typeof(attr) === 'function' && attr.pythonscript_function === undefined && attr.is_wrapper === undefined) {
            var wrapper = function(args, kwargs) {
        return attr.apply(object, args);
      }

      wrapper.is_wrapper = true;
      return wrapper;
    } else {
      return attr;
    }
  }
  var __class__, bases;
  attr = object[attribute];
  if (( attr ) != undefined) {
    return attr;
  }
  __class__ = object.__class__;
  if (__class__) {
    if (( attribute )  in  __class__.__properties__) {
      return __class__.__properties__[attribute]["get"]([object], Object());
    }
    if (( attribute )  in  __class__.__unbound_methods__) {
      attr = __class__.__unbound_methods__[attribute];
      if (attr.fastdef) {
                var method = function(args, kwargs) {
          if (arguments && arguments[0]) {
            arguments[0].splice(0, 0, object);
            return attr.apply(this, arguments);
          } else {
            return attr([object], {  });
          }
        }

      } else {
                var method = function() {
          var args;
          args = Array.prototype.slice.call(arguments);
          if (args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && ( args.length ) == 2) {
            /*pass*/
          } else {
            args = [args, Object()];
          }
          args[0].splice(0, 0, object);
          return attr.apply(this, args);
        }

      }
      method.is_wrapper = true;
      object[attribute] = method;
      return method;
    }
    attr = __class__[attribute];
    if (( attribute )  in  __class__) {
      if ({}.toString.call(attr) === '[object Function]') {
        if (attr.fastdef) {
                    var method = function(args, kwargs) {
            if (arguments && arguments[0]) {
              arguments[0].splice(0, 0, object);
              return attr.apply(this, arguments);
            } else {
              return attr([object], {  });
            }
          }

        } else {
                    var method = function() {
            var args;
            args = Array.prototype.slice.call(arguments);
            if (args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && ( args.length ) == 2) {
              /*pass*/
            } else {
              args = [args, Object()];
            }
            args[0].splice(0, 0, object);
            return attr.apply(this, args);
          }

        }
        method.is_wrapper = true;
        object[attribute] = method;
        return method;
      } else {
        return attr;
      }
    }
    bases = __class__.__bases__;
        var iter = bases;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var base=0; base < iter.length; base++) {
      var backup = base; base = iter[base];
      attr = _get_upstream_attribute(base, attribute);
      if (attr) {
        if ({}.toString.call(attr) === '[object Function]') {
          if (attr.fastdef) {
                        var method = function(args, kwargs) {
              if (arguments && arguments[0]) {
                arguments[0].splice(0, 0, object);
                return attr.apply(this, arguments);
              } else {
                return attr([object], {  });
              }
            }

          } else {
                        var method = function() {
              var args;
              args = Array.prototype.slice.call(arguments);
              if (args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && ( args.length ) == 2) {
                /*pass*/
              } else {
                args = [args, Object()];
              }
              args[0].splice(0, 0, object);
              return attr.apply(this, args);
            }

          }
          method.is_wrapper = true;
          object[attribute] = method;
          return method;
        } else {
          return attr;
        }
      }
      base = backup;
    }
        var iter = bases;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var base=0; base < iter.length; base++) {
      var backup = base; base = iter[base];
      var prop;
      prop = _get_upstream_property(base, attribute);
      if (prop) {
        return prop["get"]([object], Object());
      }
      base = backup;
    }
    if (( "__getattr__" )  in  __class__) {
      return __class__["__getattr__"]([object, attribute], Object());
    }
        var iter = bases;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var base=0; base < iter.length; base++) {
      var backup = base; base = iter[base];
      var f;
      f = _get_upstream_attribute(base, "__getattr__");
      if (f) {
        return f([object, attribute], Object());
      }
      base = backup;
    }
  }
  if (object instanceof Array) {
    if (( attribute ) == "__getitem__") {
            var wrapper = function(args, kwargs) {
        return object[args[0]];
      }

      wrapper.is_wrapper = true;
      return wrapper;
    } else {
      if (( attribute ) == "__setitem__") {
                var wrapper = function(args, kwargs) {
          object[args[0]] = args[1];
        }

        wrapper.is_wrapper = true;
        return wrapper;
      }
    }
  } else {
    if (( attribute ) == "__getitem__") {
            var wrapper = function(args, kwargs) {
        return object[args[0]];
      }

      wrapper.is_wrapper = true;
      return wrapper;
    } else {
      if (( attribute ) == "__setitem__") {
                var wrapper = function(args, kwargs) {
          object[args[0]] = args[1];
        }

        wrapper.is_wrapper = true;
        return wrapper;
      }
    }
  }
  return undefined;
}

_get_upstream_attribute = function(base, attr) {
  if (( attr )  in  base) {
    return base[attr];
  }
    var iter = base.__bases__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var parent=0; parent < iter.length; parent++) {
    var backup = parent; parent = iter[parent];
    return _get_upstream_attribute(parent, attr);
    parent = backup;
  }
}

_get_upstream_property = function(base, attr) {
  if (( attr )  in  base.__properties__) {
    return base.__properties__[attr];
  }
    var iter = base.__bases__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var parent=0; parent < iter.length; parent++) {
    var backup = parent; parent = iter[parent];
    return _get_upstream_property(parent, attr);
    parent = backup;
  }
}

__set__ = function(object, attribute, value) {
  "\n	__setattr__ is always called when an attribute is set,\n	unlike __getattr__ that only triggers when an attribute is not found,\n	this asymmetry is in fact part of the Python spec.\n	note there is no __setattribute__\n\n	In normal Python a property setter is not called before __setattr__,\n	this is bad language design because the user has been more explicit\n	in having the property setter.\n\n	In PythonJS, property setters are called instead of __setattr__.\n	";
  if (( "__class__" )  in  object && ( object.__class__.__setters__.indexOf(attribute) ) != -1) {
    object[attribute] = value;
  } else {
    if (( "__setattr__" )  in  object) {
      object.__setattr__(attribute, value);
    } else {
      object[attribute] = value;
    }
  }
}

get_arguments = function(signature, args, kwargs) {
  "Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve\n	the actual parameters.\n\n	This will set default keyword arguments and retrieve positional arguments\n	in kwargs if their called as such";
  if (( args ) === undefined) {
    args = [];
  }
  if (( kwargs ) === undefined) {
    kwargs = Object();
  }
  out = Object();
  if (( args.length ) > signature.args.length) {
    if (signature.vararg) {
      /*pass*/
    } else {
      console.log("ERROR args:", args, "kwargs:", kwargs, "sig:", signature);
      throw TypeError("Supplemental positional arguments provided but signature doesn't accept them");
    }
  }
  j = 0;
  while(( j ) < signature.args.length) {
    name = signature.args[j];
    if (( name )  in  kwargs) {
      out[name] = kwargs[name];
    } else {
      if (( j ) < args.length) {
        out[name] = args[j];
      } else {
        if (( name )  in  signature.kwargs) {
          out[name] = signature.kwargs[name];
        }
      }
    }
    j += 1
  }
  args = args.slice(j);
  if (signature.vararg) {
    out[signature.vararg] = args;
  }
  if (signature.varkwarg) {
    out[signature.varkwarg] = kwargs;
  }
  return out;
}
_PythonJS_UID = 0;
__object_keys__ = function(ob) {
  var arr;
  "\n		notes:\n			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`\n			. this is different from Object.keys because it traverses the prototype chain.\n		";
  arr = [];
  for (key in ob) { arr.push(key) };
  return arr;
}

__object_keys__.NAME = "__object_keys__";
__object_keys__.args_signature = ["ob"];
__object_keys__.kwargs_signature = {};
__object_keys__.types_signature = {};
__bind_property_descriptors__ = function(o, klass) {
  var prop, desc;
    var iter = klass.__properties__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var name=0; name < iter.length; name++) {
    var backup = name; name = iter[name];
    desc = { enumerable:true };
    prop = klass.__properties__[ name ];
    if (prop["get"]) {
      desc[ "get" ] = __generate_getter__(klass,o,name);
    }
    if (prop["set"]) {
      desc[ "set" ] = __generate_setter__(klass,o,name);
    }
    Object.defineProperty(o,name,desc);
    name = backup;
  }
    var iter = klass.__bases__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var base=0; base < iter.length; base++) {
    var backup = base; base = iter[base];
    __bind_property_descriptors__(o,base);
    base = backup;
  }
}

__bind_property_descriptors__.NAME = "__bind_property_descriptors__";
__bind_property_descriptors__.args_signature = ["o","klass"];
__bind_property_descriptors__.kwargs_signature = {};
__bind_property_descriptors__.types_signature = {};
__generate_getter__ = function(klass, o, n) {
  return (function () {return klass.__properties__[ n ][ "get" ]([o],{  })});
}

__generate_getter__.NAME = "__generate_getter__";
__generate_getter__.args_signature = ["klass","o","n"];
__generate_getter__.kwargs_signature = {};
__generate_getter__.types_signature = {};
__generate_setter__ = function(klass, o, n) {
  return (function (v) {return klass.__properties__[ n ][ "set" ]([o, v],{  })});
}

__generate_setter__.NAME = "__generate_setter__";
__generate_setter__.args_signature = ["klass","o","n"];
__generate_setter__.kwargs_signature = {};
__generate_setter__.types_signature = {};
__sprintf = function(fmt, args) {
  var i;
  i = 0;
  return fmt.replace(/%((%)|s)/g, function (m) { return m[2] || args[i++] });
}

__sprintf.NAME = "__sprintf";
__sprintf.args_signature = ["fmt","args"];
__sprintf.kwargs_signature = {};
__sprintf.types_signature = {};
create_class = function(class_name, parents, attrs, props) {
  var metaclass, klass, prop;
  "Create a PythonScript class";
  if (attrs.__metaclass__) {
    metaclass = attrs.__metaclass__;
    attrs.__metaclass__=undefined;
    return metaclass([class_name, parents, attrs]);
  }
  klass = Object.create(null);
  klass.__bases__=parents;
  klass.__name__=class_name;
  klass.__unbound_methods__=Object.create(null);
  klass.__all_method_names__=[];
  klass.__properties__=props;
  klass.__attributes__=attrs;
    var iter = attrs;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var key=0; key < iter.length; key++) {
    var backup = key; key = iter[key];
    if (( typeof(attrs[key]) ) == "function") {
      klass.__unbound_methods__[ key ] = attrs[ key ];
      klass.__all_method_names__.push(key);
    }
    if (( key ) == "__getattribute__") {
      continue;
    }
    klass[ key ] = attrs[ key ];
    key = backup;
  }
  klass.__setters__=[];
  klass.__getters__=[];
    var iter = klass.__properties__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var name=0; name < iter.length; name++) {
    var backup = name; name = iter[name];
    prop = klass.__properties__[ name ];
    klass.__getters__.push(name);
    if (prop["set"]) {
      klass.__setters__.push(name);
    }
    name = backup;
  }
    var iter = klass.__bases__;

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var base=0; base < iter.length; base++) {
    var backup = base; base = iter[base];
    Array.prototype.push.apply(klass.__getters__,base.__getters__);
    Array.prototype.push.apply(klass.__setters__,base.__setters__);
    Array.prototype.push.apply(klass.__all_method_names__,base.__all_method_names__);
    base = backup;
  }
    var __call__ = function() {
    var has_getattr, wrapper, object, has_getattribute;
    "Create a PythonJS object";
    object = Object.create(null);
    object.__class__=klass;
    Object.defineProperty(object,"__dict__",{ enumerable:false,value:object,writeable:false,configurable:false });
    has_getattribute = false;
    has_getattr = false;
        var iter = klass.__all_method_names__;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var name=0; name < iter.length; name++) {
      var backup = name; name = iter[name];
      if (( name ) == "__getattribute__") {
        has_getattribute = true;
      } else {
        if (( name ) == "__getattr__") {
          has_getattr = true;
        } else {
          wrapper = __get__(object,name);
          if (!wrapper.is_wrapper) {
            console.log("RUNTIME ERROR: failed to get wrapper for:", name);
          }
        }
      }
      name = backup;
    }
    if (has_getattr) {
      __get__(object,"__getattr__");
    }
    if (has_getattribute) {
      __get__(object,"__getattribute__");
    }
    __bind_property_descriptors__(object,klass);
    if (object.__init__) {
      object.__init__.apply(this,arguments);
    }
    return object;
  }

  __call__.NAME = "__call__";
  __call__.args_signature = [];
  __call__.kwargs_signature = {};
  __call__.types_signature = {};
  __call__.pythonscript_function=true;
  klass.__call__=__call__;
  return klass;
}

create_class.NAME = "create_class";
create_class.args_signature = ["class_name","parents","attrs","props"];
create_class.kwargs_signature = {};
create_class.types_signature = {};
type = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"bases": undefined, "class_dict": undefined}, "args": __create_array__("ob_or_class_name", "bases", "class_dict")};
  arguments = get_arguments(signature, args, kwargs);
  var ob_or_class_name = arguments['ob_or_class_name'];
  var bases = arguments['bases'];
  var class_dict = arguments['class_dict'];
  "\n	type(object) -> the object's type\n	type(name, bases, dict) -> a new type  ## broken? - TODO test\n	";
  if (( bases ) === undefined && ( class_dict ) === undefined) {
    return ob_or_class_name.__class__;
  } else {
    return create_class(ob_or_class_name,bases,class_dict);
  }
}

type.NAME = "type";
type.args_signature = ["ob_or_class_name", "bases", "class_dict"];
type.kwargs_signature = { bases:undefined,class_dict:undefined };
type.types_signature = { bases:"None",class_dict:"None" };
type.pythonscript_function = true;
hasattr = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"method": false}, "args": __create_array__("ob", "attr", "method")};
  arguments = get_arguments(signature, args, kwargs);
  var ob = arguments['ob'];
  var attr = arguments['attr'];
  var method = arguments['method'];
  return Object.hasOwnProperty.call(ob,attr);
}

hasattr.NAME = "hasattr";
hasattr.args_signature = ["ob", "attr", "method"];
hasattr.kwargs_signature = { method:false };
hasattr.types_signature = { method:"False" };
hasattr.pythonscript_function = true;
getattr = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"property": false}, "args": __create_array__("ob", "attr", "property")};
  arguments = get_arguments(signature, args, kwargs);
  var ob = arguments['ob'];
  var attr = arguments['attr'];
  var property = arguments['property'];
  if (property) {
    prop = _get_upstream_property(ob.__class__,attr);
    if (prop && prop["get"]) {
      return prop[ "get" ]([ob],{  });
    } else {
      console.log("ERROR: getattr property error", prop);
    }
  } else {
    return __get__(ob,attr);
  }
}

getattr.NAME = "getattr";
getattr.args_signature = ["ob", "attr", "property"];
getattr.kwargs_signature = { property:false };
getattr.types_signature = { property:"False" };
getattr.pythonscript_function = true;
setattr = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"property": false}, "args": __create_array__("ob", "attr", "value", "property")};
  arguments = get_arguments(signature, args, kwargs);
  var ob = arguments['ob'];
  var attr = arguments['attr'];
  var value = arguments['value'];
  var property = arguments['property'];
  if (property) {
    prop = _get_upstream_property(ob.__class__,attr);
    if (prop && prop["set"]) {
      prop[ "set" ]([ob, value],{  });
    } else {
      console.log("ERROR: setattr property error", prop);
    }
  } else {
    set_attribute(ob,attr,value);
  }
}

setattr.NAME = "setattr";
setattr.args_signature = ["ob", "attr", "value", "property"];
setattr.kwargs_signature = { property:false };
setattr.types_signature = { property:"False" };
setattr.pythonscript_function = true;
issubclass = function(args, kwargs) {
  var i, bases;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("C", "B")};
  arguments = get_arguments(signature, args, kwargs);
  var C = arguments['C'];
  var B = arguments['B'];
  if (( C ) === B) {
    return true;
  }
  bases = C.__bases__;
  i = 0;
  while(( i ) < __get__(bases, "length")) {
    if (issubclass([__get__(bases, "__getitem__")([i], Object()), B], __NULL_OBJECT__)) {
      return true;
    }
    i += 1
  }
  return false;
}

issubclass.NAME = "issubclass";
issubclass.args_signature = ["C", "B"];
issubclass.kwargs_signature = {  };
issubclass.types_signature = {  };
issubclass.pythonscript_function = true;
isinstance = function(args, kwargs) {
  var ob_class;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("ob", "klass")};
  arguments = get_arguments(signature, args, kwargs);
  var ob = arguments['ob'];
  var klass = arguments['klass'];
  if (( ob ) === undefined || ( ob ) === null) {
    return false;
  } else {
    if (!Object.hasOwnProperty.call(ob, "__class__")) {
      return false;
    }
  }
  ob_class = ob.__class__;
  if (( ob_class ) === undefined) {
    return false;
  } else {
    return issubclass([ob_class, klass], __NULL_OBJECT__);
  }
}

isinstance.NAME = "isinstance";
isinstance.args_signature = ["ob", "klass"];
isinstance.kwargs_signature = {  };
isinstance.types_signature = {  };
isinstance.pythonscript_function = true;
int = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("a")};
  arguments = get_arguments(signature, args, kwargs);
  var a = arguments['a'];
  if (a instanceof String) {
    return window.parseInt(a);
  } else {
    return Math.round(a);
  }
}

int.NAME = "int";
int.args_signature = ["a"];
int.kwargs_signature = {  };
int.types_signature = {  };
int.pythonscript_function = true;
float = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("a")};
  arguments = get_arguments(signature, args, kwargs);
  var a = arguments['a'];
  if (a instanceof String) {
    return window.parseFloat(a);
  } else {
    return a;
  }
}

float.NAME = "float";
float.args_signature = ["a"];
float.kwargs_signature = {  };
float.types_signature = {  };
float.pythonscript_function = true;
round = function(args, kwargs) {
  var b;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("a", "places")};
  arguments = get_arguments(signature, args, kwargs);
  var a = arguments['a'];
  var places = arguments['places'];
  b = "" + a;
  if (( b.indexOf(".") ) == -1) {
    return a;
  } else {
    c = b.split(".");
    x = c[ 0 ];
    y = c[ 1 ].substring(0,places);
    return parseFloat(x + "." + y);
  }
}

round.NAME = "round";
round.args_signature = ["a", "places"];
round.kwargs_signature = {  };
round.types_signature = {  };
round.pythonscript_function = true;
str = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("s")};
  arguments = get_arguments(signature, args, kwargs);
  var s = arguments['s'];
  return "" + s;
}

str.NAME = "str";
str.args_signature = ["s"];
str.kwargs_signature = {  };
str.types_signature = {  };
str.pythonscript_function = true;
_setup_str_prototype = function(args, kwargs) {
  "\n	Extend JavaScript String.prototype with methods that implement the Python str API.\n	The decorator @String.prototype.[name] assigns the function to the prototype,\n	and ensures that the special 'this' variable will work.\n	";
    var func = function(a) {
    if (( this.indexOf(a) ) == -1) {
      return false;
    } else {
      return true;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.__contains__=func;
    var func = function(index) {
    return this[ index ];
  }

  func.NAME = "func";
  func.args_signature = ["index"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.get=func;
    var func = function(self) {
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  func.NAME = "func";
  func.args_signature = ["self"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.__iter__=func;
    var func = function(idx) {
    return this[ idx ];
  }

  func.NAME = "func";
  func.args_signature = ["idx"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.__getitem__=func;
    var func = function() {
    return this.length;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.__len__=func;
    var func = function(start, stop, step) {
    var stop;
    if (( stop ) < 0) {
      stop = this.length + stop;
    }
    return this.substring(start,stop);
  }

  func.NAME = "func";
  func.args_signature = ["start","stop","step"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.__getslice__=func;
    var func = function() {
    return this.split("\n");
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.splitlines=func;
    var func = function() {
    return this.trim();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.strip=func;
    var func = function(a) {
    if (( this.substring(0, a.length) ) == a) {
      return true;
    } else {
      return false;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.startswith=func;
    var func = function(a) {
    if (( this.substring(this.length - a.length, this.length) ) == a) {
      return true;
    } else {
      return false;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.endswith=func;
    var func = function(a) {
    var i, arr, out;
    out = "";
    if (a instanceof Array) {
      arr = a;
    } else {
      arr = a["$wrapped"];
    }
    i = 0;
        var iter = arr;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var value=0; value < iter.length; value++) {
      var backup = value; value = iter[value];
      out += value;
      i += 1;
      if (( i ) < arr.length) {
        out += this;
      }
      value = backup;
    }
    return out;
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.join=func;
    var func = function() {
    return this.toUpperCase();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.upper=func;
    var func = function() {
    return this.toLowerCase();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.lower=func;
    var func = function(a) {
    return this.indexOf(a);
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.index=func;
    var func = function() {
    var digits;
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
        var iter = this;

    if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
    for (var char=0; char < iter.length; char++) {
      var backup = char; char = iter[char];
      if (( char )  in  digits || Object.hasOwnProperty.call(digits, "__contains__") && digits["__contains__"](char)) {
        /*pass*/
      } else {
        return false;
      }
      char = backup;
    }
    return true;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.isdigit=func;
    var func = function(encoding) {
    return this;
  }

  func.NAME = "func";
  func.args_signature = ["encoding"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.decode=func;
    var func = function(encoding) {
    return this;
  }

  func.NAME = "func";
  func.args_signature = ["encoding"];
  func.kwargs_signature = {};
  func.types_signature = {};
  String.prototype.encode=func;
}

_setup_str_prototype.NAME = "_setup_str_prototype";
_setup_str_prototype.args_signature = [];
_setup_str_prototype.kwargs_signature = {  };
_setup_str_prototype.types_signature = {  };
_setup_str_prototype.pythonscript_function = true;
_setup_str_prototype();
_setup_array_prototype = function(args, kwargs) {
    var func = function(a) {
    if (( this.indexOf(a) ) == -1) {
      return false;
    } else {
      return true;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.__contains__=func;
    var func = function() {
    return this.length;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.__len__=func;
    var func = function(index) {
    return this[ index ];
  }

  func.NAME = "func";
  func.args_signature = ["index"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.get=func;
    var func = function(self) {
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  func.NAME = "func";
  func.args_signature = ["self"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.__iter__=func;
    var func = function(start, stop, step) {
    var stop;
    if (( stop ) < 0) {
      stop = this.length + stop;
    }
    return this.slice(start,stop);
  }

  func.NAME = "func";
  func.args_signature = ["start","stop","step"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.__getslice__=func;
    var func = function(item) {
    this.push(item);
  }

  func.NAME = "func";
  func.args_signature = ["item"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.append=func;
    var func = function(x, low, high) {
    var high, a, low, mid;
    if (( low ) === undefined) {
      low = 0;
    }
    if (( high ) === undefined) {
      high = this.length;
    }
    while(( low ) < high) {
      a = low + high;
      mid = Math.floor(a / 2);
      if (( x ) < this[mid]) {
        high = mid;
      } else {
        low = mid + 1;
      }
    }
    return low;
  }

  func.NAME = "func";
  func.args_signature = ["x","low","high"];
  func.kwargs_signature = {};
  func.types_signature = {};
  Array.prototype.bisect=func;
}

_setup_array_prototype.NAME = "_setup_array_prototype";
_setup_array_prototype.args_signature = [];
_setup_array_prototype.kwargs_signature = {  };
_setup_array_prototype.types_signature = {  };
_setup_array_prototype.pythonscript_function = true;
_setup_array_prototype();
bisect = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"low": undefined, "high": undefined}, "args": __create_array__("a", "x", "low", "high")};
  arguments = get_arguments(signature, args, kwargs);
  var a = arguments['a'];
  var x = arguments['x'];
  var low = arguments['low'];
  var high = arguments['high'];
  if (isinstance([a, list], __NULL_OBJECT__)) {
    return __get__(__get__(a["$wrapped"], "bisect"), "__call__")([x, low, high], __NULL_OBJECT__);
  } else {
    return __get__(__get__(a, "bisect"), "__call__")([x, low, high], __NULL_OBJECT__);
  }
}

bisect.NAME = "bisect";
bisect.args_signature = ["a", "x", "low", "high"];
bisect.kwargs_signature = { low:undefined,high:undefined };
bisect.types_signature = { low:"None",high:"None" };
bisect.pythonscript_function = true;
range = function(args, kwargs) {
  var i, arr, num;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("num", "stop")};
  arguments = get_arguments(signature, args, kwargs);
  var num = arguments['num'];
  var stop = arguments['stop'];
  "Emulates Python's range function";
  if (( stop ) !== undefined) {
    i = num;
    num = stop;
  } else {
    i = 0;
  }
  arr = [];
  while(( i ) < num) {
    arr.push(i);
    i += 1;
  }
  var __args_0, __kwargs_0;
  __args_0 = [];
  __kwargs_0 = {"pointer": arr};
  return __get__(list, "__call__")([], __kwargs_0);
}

range.NAME = "range";
range.args_signature = ["num", "stop"];
range.kwargs_signature = {  };
range.types_signature = {  };
range.return_type = "list";
range.pythonscript_function = true;
var StopIteration, __StopIteration_attrs, __StopIteration_parents;
__StopIteration_attrs = Object();
__StopIteration_parents = [];
__StopIteration_properties = Object();
StopIteration = create_class("StopIteration", __StopIteration_parents, __StopIteration_attrs, __StopIteration_properties);
len = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("obj")};
  arguments = get_arguments(signature, args, kwargs);
  var obj = arguments['obj'];
  return __get__(__get__(obj, "__len__"), "__call__")();
}

len.NAME = "len";
len.args_signature = ["obj"];
len.kwargs_signature = {  };
len.types_signature = {  };
len.pythonscript_function = true;
next = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("obj")};
  arguments = get_arguments(signature, args, kwargs);
  var obj = arguments['obj'];
  return __get__(__get__(obj, "next"), "__call__")();
}

next.NAME = "next";
next.args_signature = ["obj"];
next.kwargs_signature = {  };
next.types_signature = {  };
next.pythonscript_function = true;
map = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("func", "objs")};
  arguments = get_arguments(signature, args, kwargs);
  var func = arguments['func'];
  var objs = arguments['objs'];
  var __args_1, __kwargs_1;
  __args_1 = [];
  __kwargs_1 = {"js_object": map([func, objs["$wrapped"]], __NULL_OBJECT__)};
  return __get__(list, "__call__")([], __kwargs_1);
}

map.NAME = "map";
map.args_signature = ["func", "objs"];
map.kwargs_signature = {  };
map.types_signature = {  };
map.return_type = "list";
map.pythonscript_function = true;
min = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("lst")};
  arguments = get_arguments(signature, args, kwargs);
  var lst = arguments['lst'];
  a = undefined;
  var __iterator__, value;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while(( __iterator__.index ) < __iterator__.length) {
    value = __next__();
    if (( a ) === undefined) {
      a = value;
    } else {
      if (( value ) < a) {
        a = value;
      }
    }
  }
  return a;
}

min.NAME = "min";
min.args_signature = ["lst"];
min.kwargs_signature = {  };
min.types_signature = {  };
min.pythonscript_function = true;
max = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("lst")};
  arguments = get_arguments(signature, args, kwargs);
  var lst = arguments['lst'];
  a = undefined;
  var __iterator__, value;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while(( __iterator__.index ) < __iterator__.length) {
    value = __next__();
    if (( a ) === undefined) {
      a = value;
    } else {
      if (( value ) > a) {
        a = value;
      }
    }
  }
  return a;
}

max.NAME = "max";
max.args_signature = ["lst"];
max.kwargs_signature = {  };
max.types_signature = {  };
max.pythonscript_function = true;
abs = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("num")};
  arguments = get_arguments(signature, args, kwargs);
  var num = arguments['num'];
  return Math.abs(num);
}

abs.NAME = "abs";
abs.args_signature = ["num"];
abs.kwargs_signature = {  };
abs.types_signature = {  };
abs.pythonscript_function = true;
ord = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("char")};
  arguments = get_arguments(signature, args, kwargs);
  var char = arguments['char'];
  return char.charCodeAt(0);
}

ord.NAME = "ord";
ord.args_signature = ["char"];
ord.kwargs_signature = {  };
ord.types_signature = {  };
ord.pythonscript_function = true;
chr = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("num")};
  arguments = get_arguments(signature, args, kwargs);
  var num = arguments['num'];
  return String.fromCharCode(num);
}

chr.NAME = "chr";
chr.args_signature = ["num"];
chr.kwargs_signature = {  };
chr.types_signature = {  };
chr.pythonscript_function = true;
var Iterator, __Iterator_attrs, __Iterator_parents;
__Iterator_attrs = Object();
__Iterator_parents = [];
__Iterator_properties = Object();
__Iterator___init__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  var index = arguments['index'];
  self.obj = obj;
  self.index = index;
  self.length = len([obj], __NULL_OBJECT__);
  self.obj_get = __get__(obj, "get");
}

__Iterator___init__.NAME = "__Iterator___init__";
__Iterator___init__.args_signature = ["self", "obj", "index"];
__Iterator___init__.kwargs_signature = {  };
__Iterator___init__.types_signature = {  };
__Iterator___init__.pythonscript_function = true;
__Iterator_attrs["__init__"] = __Iterator___init__;
__Iterator_next = function(args, kwargs) {
  var index, length, item;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  index = self.index;
  length = len([self.obj], __NULL_OBJECT__);
  if (( index ) == length) {
    throw StopIteration;
  }
  item = __get__(__get__(self.obj, "get"), "__call__")([self.index], __NULL_OBJECT__);
  self.index = self.index + 1;
  return item;
}

__Iterator_next.NAME = "__Iterator_next";
__Iterator_next.args_signature = ["self"];
__Iterator_next.kwargs_signature = {  };
__Iterator_next.types_signature = {  };
__Iterator_next.pythonscript_function = true;
__Iterator_attrs["next"] = __Iterator_next;
__Iterator_next_fast = function(args, kwargs) {
  var index;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  index = self.index;
  self.index += 1;
  return self.obj_get([index],{  });
}

__Iterator_next_fast.NAME = "__Iterator_next_fast";
__Iterator_next_fast.args_signature = ["self"];
__Iterator_next_fast.kwargs_signature = {  };
__Iterator_next_fast.types_signature = {  };
__Iterator_next_fast.pythonscript_function = true;
__Iterator_attrs["next_fast"] = __Iterator_next_fast;
Iterator = create_class("Iterator", __Iterator_parents, __Iterator_attrs, __Iterator_properties);
var tuple, __tuple_attrs, __tuple_parents;
__tuple_attrs = Object();
__tuple_parents = [];
__tuple_properties = Object();
__tuple___init__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"js_object": undefined}, "args": __create_array__("self", "js_object")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var js_object = arguments['js_object'];
  arr = [];
  self["$wrapped"] = arr;
  if (js_object instanceof Array) {
    var __iterator__, item;
    __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while(( __iterator__.index ) < __iterator__.length) {
      item = __next__();
      __get__(__get__(arr, "push"), "__call__")([item], __NULL_OBJECT__);
    }
  } else {
    if (js_object) {
      if (isinstance([js_object, array], __NULL_OBJECT__) || isinstance([js_object, tuple], __NULL_OBJECT__) || isinstance([js_object, list], __NULL_OBJECT__)) {
        var __iterator__, v;
        __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
        var __next__;
        __next__ = __get__(__iterator__, "next_fast");
        while(( __iterator__.index ) < __iterator__.length) {
          v = __next__();
          __get__(__get__(arr, "push"), "__call__")([v], __NULL_OBJECT__);
        }
      } else {
        throw TypeError;
      }
    }
  }
}

__tuple___init__.NAME = "__tuple___init__";
__tuple___init__.args_signature = ["self", "js_object"];
__tuple___init__.kwargs_signature = { js_object:undefined };
__tuple___init__.types_signature = { js_object:"None" };
__tuple___init__.pythonscript_function = true;
__tuple_attrs["__init__"] = __tuple___init__;
__tuple___getitem__ = function(args, kwargs) {
  var index;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  if (( index ) < 0) {
    index = __get__(self["$wrapped"], "length") + index;
  }
  return self["$wrapped"][ index ];
}

__tuple___getitem__.NAME = "__tuple___getitem__";
__tuple___getitem__.args_signature = ["self", "index"];
__tuple___getitem__.kwargs_signature = {  };
__tuple___getitem__.types_signature = {  };
__tuple___getitem__.pythonscript_function = true;
__tuple_attrs["__getitem__"] = __tuple___getitem__;
__tuple___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__tuple___iter__.NAME = "__tuple___iter__";
__tuple___iter__.args_signature = ["self"];
__tuple___iter__.kwargs_signature = {  };
__tuple___iter__.types_signature = {  };
__tuple___iter__.return_type = "Iterator";
__tuple___iter__.pythonscript_function = true;
__tuple_attrs["__iter__"] = __tuple___iter__;
__tuple___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return self["$wrapped"].length;
}

__tuple___len__.NAME = "__tuple___len__";
__tuple___len__.args_signature = ["self"];
__tuple___len__.kwargs_signature = {  };
__tuple___len__.types_signature = {  };
__tuple___len__.pythonscript_function = true;
__tuple_attrs["__len__"] = __tuple___len__;
__tuple_index = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  return self["$wrapped"].indexOf(obj);
}

__tuple_index.NAME = "__tuple_index";
__tuple_index.args_signature = ["self", "obj"];
__tuple_index.kwargs_signature = {  };
__tuple_index.types_signature = {  };
__tuple_index.pythonscript_function = true;
__tuple_attrs["index"] = __tuple_index;
__tuple_count = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  a = 0;
    var iter = self["$wrapped"];

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var item=0; item < iter.length; item++) {
    var backup = item; item = iter[item];
    if (( item ) == obj) {
      a += 1;
    }
    item = backup;
  }
  return a;
}

__tuple_count.NAME = "__tuple_count";
__tuple_count.args_signature = ["self", "obj"];
__tuple_count.kwargs_signature = {  };
__tuple_count.types_signature = {  };
__tuple_count.pythonscript_function = true;
__tuple_attrs["count"] = __tuple_count;
__tuple_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  return self["$wrapped"][ index ];
}

__tuple_get.NAME = "__tuple_get";
__tuple_get.args_signature = ["self", "index"];
__tuple_get.kwargs_signature = {  };
__tuple_get.types_signature = {  };
__tuple_get.pythonscript_function = true;
__tuple_attrs["get"] = __tuple_get;
__tuple___contains__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var value = arguments['value'];
  if (( self["$wrapped"].indexOf(value) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__tuple___contains__.NAME = "__tuple___contains__";
__tuple___contains__.args_signature = ["self", "value"];
__tuple___contains__.kwargs_signature = {  };
__tuple___contains__.types_signature = {  };
__tuple___contains__.pythonscript_function = true;
__tuple_attrs["__contains__"] = __tuple___contains__;
tuple = create_class("tuple", __tuple_parents, __tuple_attrs, __tuple_properties);
var list, __list_attrs, __list_parents;
__list_attrs = Object();
__list_parents = [];
__list_properties = Object();
__list___init__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"js_object": undefined, "pointer": undefined}, "args": __create_array__("self", "js_object", "pointer")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var js_object = arguments['js_object'];
  var pointer = arguments['pointer'];
  if (pointer) {
    self["$wrapped"] = pointer;
  } else {
    arr = [];
    self["$wrapped"] = arr;
    if (js_object instanceof Array) {
      var __iterator__, item;
      __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
      var __next__;
      __next__ = __get__(__iterator__, "next_fast");
      while(( __iterator__.index ) < __iterator__.length) {
        item = __next__();
        __get__(__get__(arr, "push"), "__call__")([item], __NULL_OBJECT__);
      }
    } else {
      if (js_object) {
        if (isinstance([js_object, array], __NULL_OBJECT__) || isinstance([js_object, tuple], __NULL_OBJECT__) || isinstance([js_object, list], __NULL_OBJECT__)) {
          var __iterator__, v;
          __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
          var __next__;
          __next__ = __get__(__iterator__, "next_fast");
          while(( __iterator__.index ) < __iterator__.length) {
            v = __next__();
            __get__(__get__(arr, "push"), "__call__")([v], __NULL_OBJECT__);
          }
        } else {
          throw TypeError;
        }
      }
    }
  }
}

__list___init__.NAME = "__list___init__";
__list___init__.args_signature = ["self", "js_object", "pointer"];
__list___init__.kwargs_signature = { js_object:undefined,pointer:undefined };
__list___init__.types_signature = { js_object:"None",pointer:"None" };
__list___init__.pythonscript_function = true;
__list_attrs["__init__"] = __list___init__;
__list___getitem__ = function(args, kwargs) {
  var index;
  var self = args[ 0 ];
  var index = args[ 1 ];
  if (( index ) < 0) {
    index = __get__(self["$wrapped"], "length") + index;
  }
  return self["$wrapped"][ index ];
}

__list___getitem__.NAME = "__list___getitem__";
__list___getitem__.args_signature = ["self", "index"];
__list___getitem__.kwargs_signature = {  };
__list___getitem__.fastdef = true;
__list___getitem__.types_signature = {  };
__list___getitem__.pythonscript_function = true;
__list_attrs["__getitem__"] = __list___getitem__;
__list___setitem__ = function(args, kwargs) {
  var self = args[ 0 ];
  var index = args[ 1 ];
  var value = args[ 2 ];
  self["$wrapped"][ index ] = value;
}

__list___setitem__.NAME = "__list___setitem__";
__list___setitem__.args_signature = ["self", "index", "value"];
__list___setitem__.kwargs_signature = {  };
__list___setitem__.fastdef = true;
__list___setitem__.types_signature = {  };
__list___setitem__.pythonscript_function = true;
__list_attrs["__setitem__"] = __list___setitem__;
__list___getslice__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"step": undefined}, "args": __create_array__("self", "start", "stop", "step")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var start = arguments['start'];
  var stop = arguments['stop'];
  var step = arguments['step'];
  arr = self["$wrapped"].__getslice__(start,stop);
  var __args_2, __kwargs_2;
  __args_2 = [];
  __kwargs_2 = {"pointer": arr};
  return __get__(list, "__call__")([], __kwargs_2);
}

__list___getslice__.NAME = "__list___getslice__";
__list___getslice__.args_signature = ["self", "start", "stop", "step"];
__list___getslice__.kwargs_signature = { step:undefined };
__list___getslice__.types_signature = { step:"None" };
__list___getslice__.return_type = "list";
__list___getslice__.pythonscript_function = true;
__list_attrs["__getslice__"] = __list___getslice__;
__list_append = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  self["$wrapped"].push(obj);
}

__list_append.NAME = "__list_append";
__list_append.args_signature = ["self", "obj"];
__list_append.kwargs_signature = {  };
__list_append.types_signature = {  };
__list_append.pythonscript_function = true;
__list_attrs["append"] = __list_append;
__list_extend = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "other")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var other = arguments['other'];
  var __iterator__, obj;
  __iterator__ = __get__(__get__(other, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while(( __iterator__.index ) < __iterator__.length) {
    obj = __next__();
    __get__(__get__(self, "append"), "__call__")([obj], __NULL_OBJECT__);
  }
}

__list_extend.NAME = "__list_extend";
__list_extend.args_signature = ["self", "other"];
__list_extend.kwargs_signature = {  };
__list_extend.types_signature = {  };
__list_extend.pythonscript_function = true;
__list_attrs["extend"] = __list_extend;
__list_insert = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  var obj = arguments['obj'];
  self["$wrapped"].splice(index,0,obj);
}

__list_insert.NAME = "__list_insert";
__list_insert.args_signature = ["self", "index", "obj"];
__list_insert.kwargs_signature = {  };
__list_insert.types_signature = {  };
__list_insert.pythonscript_function = true;
__list_attrs["insert"] = __list_insert;
__list_remove = function(args, kwargs) {
  var index;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  index = __get__(__get__(self, "index"), "__call__")([obj], __NULL_OBJECT__);
  self["$wrapped"].splice(index,1);
}

__list_remove.NAME = "__list_remove";
__list_remove.args_signature = ["self", "obj"];
__list_remove.kwargs_signature = {  };
__list_remove.types_signature = {  };
__list_remove.pythonscript_function = true;
__list_attrs["remove"] = __list_remove;
__list_pop = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return self["$wrapped"].pop();
}

__list_pop.NAME = "__list_pop";
__list_pop.args_signature = ["self"];
__list_pop.kwargs_signature = {  };
__list_pop.types_signature = {  };
__list_pop.pythonscript_function = true;
__list_attrs["pop"] = __list_pop;
__list_index = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  return self["$wrapped"].indexOf(obj);
}

__list_index.NAME = "__list_index";
__list_index.args_signature = ["self", "obj"];
__list_index.kwargs_signature = {  };
__list_index.types_signature = {  };
__list_index.pythonscript_function = true;
__list_attrs["index"] = __list_index;
__list_count = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "obj")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var obj = arguments['obj'];
  a = 0;
    var iter = self["$wrapped"];

  if (! (iter instanceof Array) ) { iter = __object_keys__(iter) }
  for (var item=0; item < iter.length; item++) {
    var backup = item; item = iter[item];
    if (( item ) == obj) {
      a += 1;
    }
    item = backup;
  }
  return a;
}

__list_count.NAME = "__list_count";
__list_count.args_signature = ["self", "obj"];
__list_count.kwargs_signature = {  };
__list_count.types_signature = {  };
__list_count.pythonscript_function = true;
__list_attrs["count"] = __list_count;
__list_reverse = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  self["$wrapped"] = self["$wrapped"].reverse();
}

__list_reverse.NAME = "__list_reverse";
__list_reverse.args_signature = ["self"];
__list_reverse.kwargs_signature = {  };
__list_reverse.types_signature = {  };
__list_reverse.pythonscript_function = true;
__list_attrs["reverse"] = __list_reverse;
__list_shift = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return self["$wrapped"].shift();
}

__list_shift.NAME = "__list_shift";
__list_shift.args_signature = ["self"];
__list_shift.kwargs_signature = {  };
__list_shift.types_signature = {  };
__list_shift.pythonscript_function = true;
__list_attrs["shift"] = __list_shift;
__list_slice = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "start", "end")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var start = arguments['start'];
  var end = arguments['end'];
  return self["$wrapped"].slice(start,end);
}

__list_slice.NAME = "__list_slice";
__list_slice.args_signature = ["self", "start", "end"];
__list_slice.kwargs_signature = {  };
__list_slice.types_signature = {  };
__list_slice.pythonscript_function = true;
__list_attrs["slice"] = __list_slice;
__list___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__list___iter__.NAME = "__list___iter__";
__list___iter__.args_signature = ["self"];
__list___iter__.kwargs_signature = {  };
__list___iter__.types_signature = {  };
__list___iter__.return_type = "Iterator";
__list___iter__.pythonscript_function = true;
__list_attrs["__iter__"] = __list___iter__;
__list_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  return self["$wrapped"][ index ];
}

__list_get.NAME = "__list_get";
__list_get.args_signature = ["self", "index"];
__list_get.kwargs_signature = {  };
__list_get.types_signature = {  };
__list_get.pythonscript_function = true;
__list_attrs["get"] = __list_get;
__list_set = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  var value = arguments['value'];
  self["$wrapped"][ index ] = value;
}

__list_set.NAME = "__list_set";
__list_set.args_signature = ["self", "index", "value"];
__list_set.kwargs_signature = {  };
__list_set.types_signature = {  };
__list_set.pythonscript_function = true;
__list_attrs["set"] = __list_set;
__list___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return self["$wrapped"].length;
}

__list___len__.NAME = "__list___len__";
__list___len__.args_signature = ["self"];
__list___len__.kwargs_signature = {  };
__list___len__.types_signature = {  };
__list___len__.pythonscript_function = true;
__list_attrs["__len__"] = __list___len__;
__list___contains__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var value = arguments['value'];
  if (( self["$wrapped"].indexOf(value) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__list___contains__.NAME = "__list___contains__";
__list___contains__.args_signature = ["self", "value"];
__list___contains__.kwargs_signature = {  };
__list___contains__.types_signature = {  };
__list___contains__.pythonscript_function = true;
__list_attrs["__contains__"] = __list___contains__;
list = create_class("list", __list_parents, __list_attrs, __list_properties);
var dict, __dict_attrs, __dict_parents;
__dict_attrs = Object();
__dict_parents = [];
__dict_properties = Object();
__dict_UID = 0;
__dict_attrs["UID"] = __dict_UID;
__dict___init__ = function(args, kwargs) {
  var i;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"js_object": undefined}, "args": __create_array__("self", "js_object")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var js_object = arguments['js_object'];
  self["$wrapped"] = {  };
  if (js_object) {
    if (js_object instanceof Array) {
      i = 0;
      while(( i ) < __get__(js_object, "length")) {
        var key = js_object[i]["key"];
        var value = js_object[i]["value"];
        __get__(__get__(self, "set"), "__call__")([key, value], __NULL_OBJECT__);
        i += 1
      }
    } else {
      self["$wrapped"] = js_object;
    }
  }
}

__dict___init__.NAME = "__dict___init__";
__dict___init__.args_signature = ["self", "js_object"];
__dict___init__.kwargs_signature = { js_object:undefined };
__dict___init__.types_signature = { js_object:"None" };
__dict___init__.pythonscript_function = true;
__dict_attrs["__init__"] = __dict___init__;
__dict_get = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"_default": undefined}, "args": __create_array__("self", "key", "_default")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var key = arguments['key'];
  var _default = arguments['_default'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object') {
    var uid = "@"+key.uid;
    if (uid in __dict) {
      return __dict[uid];
    }
  } else {
    if (typeof(key) === 'function') {
      var uid = "@"+key.uid;
      if (uid in __dict) {
        return __dict[uid];
      }
    } else {
      if (key in __dict) {
        return __dict[key];
      }
    }
  }
  return _default;
}

__dict_get.NAME = "__dict_get";
__dict_get.args_signature = ["self", "key", "_default"];
__dict_get.kwargs_signature = { _default:undefined };
__dict_get.types_signature = { _default:"None" };
__dict_get.pythonscript_function = true;
__dict_attrs["get"] = __dict_get;
__dict_set = function(args, kwargs) {
  var __dict, uid;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "key", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var key = arguments['key'];
  var value = arguments['value'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object') {
    if (key.uid === undefined) {
      uid = _PythonJS_UID;
      key.uid = uid;
      _PythonJS_UID += 1
    }
    var uid = key.uid;
    __dict["@"+uid] = value;
  } else {
    if (typeof(key) === 'function') {
      if (key.uid === undefined) {
        uid = _PythonJS_UID;
        key.uid = uid;
        _PythonJS_UID += 1
      }
      var uid = key.uid;
      __dict["@"+uid] = value;
    } else {
      __dict[key] = value;
    }
  }
}

__dict_set.NAME = "__dict_set";
__dict_set.args_signature = ["self", "key", "value"];
__dict_set.kwargs_signature = {  };
__dict_set.types_signature = {  };
__dict_set.pythonscript_function = true;
__dict_attrs["set"] = __dict_set;
__dict___len__ = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  __dict = self["$wrapped"];
  return Object.keys(__dict).length;
}

__dict___len__.NAME = "__dict___len__";
__dict___len__.args_signature = ["self"];
__dict___len__.kwargs_signature = {  };
__dict___len__.types_signature = {  };
__dict___len__.pythonscript_function = true;
__dict_attrs["__len__"] = __dict___len__;
__dict___getitem__ = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "key")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var key = arguments['key'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object') {
    var uid = key.uid;
    return __dict["@"+uid];
  } else {
    if (typeof(key) === 'function') {
      var uid = key.uid;
      return __dict["@"+uid];
    } else {
      return __dict[key];
    }
  }
}

__dict___getitem__.NAME = "__dict___getitem__";
__dict___getitem__.args_signature = ["self", "key"];
__dict___getitem__.kwargs_signature = {  };
__dict___getitem__.types_signature = {  };
__dict___getitem__.pythonscript_function = true;
__dict_attrs["__getitem__"] = __dict___getitem__;
__dict___setitem__ = function(args, kwargs) {
  var __dict, uid;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "key", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var key = arguments['key'];
  var value = arguments['value'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object') {
    if (key.uid === undefined) {
      uid = _PythonJS_UID;
      key.uid = uid;
      _PythonJS_UID += 1
    }
    var uid = key.uid;
    __dict["@"+uid] = value;
  } else {
    if (typeof(key) === 'function') {
      if (key.uid === undefined) {
        uid = _PythonJS_UID;
        key.uid = uid;
        _PythonJS_UID += 1
      }
      var uid = key.uid;
      __dict["@"+uid] = value;
    } else {
      __dict[key] = value;
    }
  }
}

__dict___setitem__.NAME = "__dict___setitem__";
__dict___setitem__.args_signature = ["self", "key", "value"];
__dict___setitem__.kwargs_signature = {  };
__dict___setitem__.types_signature = {  };
__dict___setitem__.pythonscript_function = true;
__dict_attrs["__setitem__"] = __dict___setitem__;
__dict_keys = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  arr = Object.keys(self["$wrapped"]);
  var __args_3, __kwargs_3;
  __args_3 = [];
  __kwargs_3 = {"js_object": arr};
  return __get__(list, "__call__")([], __kwargs_3);
}

__dict_keys.NAME = "__dict_keys";
__dict_keys.args_signature = ["self"];
__dict_keys.kwargs_signature = {  };
__dict_keys.types_signature = {  };
__dict_keys.return_type = "list";
__dict_keys.pythonscript_function = true;
__dict_attrs["keys"] = __dict_keys;
__dict_pop = function(args, kwargs) {
  var js_object, v;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"d": undefined}, "args": __create_array__("self", "key", "d")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var key = arguments['key'];
  var d = arguments['d'];
  v = __get__(__get__(self, "get"), "__call__")([key, undefined], __NULL_OBJECT__);
  if (( v ) === undefined) {
    return d;
  } else {
    js_object = self["$wrapped"];
    delete js_object[key];
    return v;
  }
}

__dict_pop.NAME = "__dict_pop";
__dict_pop.args_signature = ["self", "key", "d"];
__dict_pop.kwargs_signature = { d:undefined };
__dict_pop.types_signature = { d:"None" };
__dict_pop.pythonscript_function = true;
__dict_attrs["pop"] = __dict_pop;
__dict_values = function(args, kwargs) {
  var __dict, __keys, i, out;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  __dict = self["$wrapped"];
  __keys = Object.keys(__dict);
  out = __get__(list, "__call__")();
  i = 0;
  while(( i ) < __get__(__keys, "length")) {
    __get__(__get__(out, "append"), "__call__")([__dict[ __keys[i] ]], __NULL_OBJECT__);
    i += 1
  }
  return out;
}

__dict_values.NAME = "__dict_values";
__dict_values.args_signature = ["self"];
__dict_values.kwargs_signature = {  };
__dict_values.types_signature = {  };
__dict_values.pythonscript_function = true;
__dict_attrs["values"] = __dict_values;
__dict___contains__ = function(args, kwargs) {
  var keys;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var value = arguments['value'];
  keys = Object.keys(self["$wrapped"]);
  if (( typeof(value) ) == "object") {
    key = "@" + value.uid;
  } else {
    key = "" + value;
  }
  if (( keys.indexOf(key) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__dict___contains__.NAME = "__dict___contains__";
__dict___contains__.args_signature = ["self", "value"];
__dict___contains__.kwargs_signature = {  };
__dict___contains__.types_signature = {  };
__dict___contains__.pythonscript_function = true;
__dict_attrs["__contains__"] = __dict___contains__;
__dict___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return __get__(Iterator, "__call__")([__get__(__get__(self, "keys"), "__call__")(), 0], __NULL_OBJECT__);
}

__dict___iter__.NAME = "__dict___iter__";
__dict___iter__.args_signature = ["self"];
__dict___iter__.kwargs_signature = {  };
__dict___iter__.types_signature = {  };
__dict___iter__.return_type = "Iterator";
__dict___iter__.pythonscript_function = true;
__dict_attrs["__iter__"] = __dict___iter__;
dict = create_class("dict", __dict_parents, __dict_attrs, __dict_properties);
var array, __array_attrs, __array_parents;
__array_attrs = Object();
__array_parents = [];
__array_properties = Object();
__array_typecodes = { "c":1,"b":1,"B":1,"u":2,"h":2,"H":2,"i":4,"I":4,"l":4,"L":4,"f":4,"d":8,"float32":4,"float16":2,"float8":1,"int32":4,"uint32":4,"int16":2,"uint16":2,"int8":1,"uint8":1 };
__array_attrs["typecodes"] = __array_typecodes;
__array_typecode_names = { "c":"Int8","b":"Int8","B":"Uint8","u":"Uint16","h":"Int16","H":"Uint16","i":"Int32","I":"Uint32","f":"Float32","d":"Float64","float32":"Float32","float16":"Int16","float8":"Int8","int32":"Int32","uint32":"Uint32","int16":"Int16","uint16":"Uint16","int8":"Int8","uint8":"Uint8" };
__array_attrs["typecode_names"] = __array_typecode_names;
__array___init__ = function(args, kwargs) {
  var size, buff;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": {"initializer": undefined, "little_endian": false}, "args": __create_array__("self", "typecode", "initializer", "little_endian")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var typecode = arguments['typecode'];
  var initializer = arguments['initializer'];
  var little_endian = arguments['little_endian'];
  self.typecode = typecode;
  self.itemsize = __get__(__get__(self, "typecodes"), "__getitem__")([typecode], Object());
  self.little_endian = little_endian;
  if (initializer) {
    self.length = len([initializer], __NULL_OBJECT__);
    self.bytes = self.length * self.itemsize;
    if (( self.typecode ) == "float8") {
      self._scale = max([__get__(list, "__call__")([], {"js_object": [abs([min([initializer], __NULL_OBJECT__)], __NULL_OBJECT__), max([initializer], __NULL_OBJECT__)]})], __NULL_OBJECT__);
      self._norm_get = self._scale / 127;
      self._norm_set = 1.0 / self._norm_get;
    } else {
      if (( self.typecode ) == "float16") {
        self._scale = max([__get__(list, "__call__")([], {"js_object": [abs([min([initializer], __NULL_OBJECT__)], __NULL_OBJECT__), max([initializer], __NULL_OBJECT__)]})], __NULL_OBJECT__);
        self._norm_get = self._scale / 32767;
        self._norm_set = 1.0 / self._norm_get;
      }
    }
  } else {
    self.length = 0;
    self.bytes = 0;
  }
  size = self.bytes;
  buff = new ArrayBuffer(size);
  self.dataview = new DataView(buff);
  self.buffer = buff;
  __get__(__get__(self, "fromlist"), "__call__")([initializer], __NULL_OBJECT__);
}

__array___init__.NAME = "__array___init__";
__array___init__.args_signature = ["self", "typecode", "initializer", "little_endian"];
__array___init__.kwargs_signature = { initializer:undefined,little_endian:false };
__array___init__.types_signature = { initializer:"None",little_endian:"False" };
__array___init__.pythonscript_function = true;
__array_attrs["__init__"] = __array___init__;
__array___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return self.length;
}

__array___len__.NAME = "__array___len__";
__array___len__.args_signature = ["self"];
__array___len__.kwargs_signature = {  };
__array___len__.types_signature = {  };
__array___len__.pythonscript_function = true;
__array_attrs["__len__"] = __array___len__;
__array___contains__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var value = arguments['value'];
  arr = __get__(__get__(self, "to_array"), "__call__")();
  if (( arr.indexOf(value) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__array___contains__.NAME = "__array___contains__";
__array___contains__.args_signature = ["self", "value"];
__array___contains__.kwargs_signature = {  };
__array___contains__.types_signature = {  };
__array___contains__.pythonscript_function = true;
__array_attrs["__contains__"] = __array___contains__;
__array___getitem__ = function(args, kwargs) {
  var func_name, dataview, value, step, func, offset;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  step = self.itemsize;
  offset = step * index;
  dataview = self.dataview;
  func_name = "get" + __get__(__get__(self, "typecode_names"), "__getitem__")([self.typecode], Object());
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    value = func(offset);
    if (( self.typecode ) == "float8") {
      value = value * self._norm_get;
    } else {
      if (( self.typecode ) == "float16") {
        value = value * self._norm_get;
      }
    }
    return value;
  } else {
    throw IndexError;
  }
}

__array___getitem__.NAME = "__array___getitem__";
__array___getitem__.args_signature = ["self", "index"];
__array___getitem__.kwargs_signature = {  };
__array___getitem__.types_signature = {  };
__array___getitem__.pythonscript_function = true;
__array_attrs["__getitem__"] = __array___getitem__;
__array___setitem__ = function(args, kwargs) {
  var index, func_name, dataview, value, step, func, offset;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  var value = arguments['value'];
  step = self.itemsize;
  if (( index ) < 0) {
    index = self.length + index - 1;
  }
  offset = step * index;
  dataview = self.dataview;
  func_name = "set" + __get__(__get__(self, "typecode_names"), "__getitem__")([self.typecode], Object());
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    if (( self.typecode ) == "float8") {
      value = value * self._norm_set;
    } else {
      if (( self.typecode ) == "float16") {
        value = value * self._norm_set;
      }
    }
    func(offset, value);
  } else {
    throw IndexError;
  }
}

__array___setitem__.NAME = "__array___setitem__";
__array___setitem__.args_signature = ["self", "index", "value"];
__array___setitem__.kwargs_signature = {  };
__array___setitem__.types_signature = {  };
__array___setitem__.pythonscript_function = true;
__array_attrs["__setitem__"] = __array___setitem__;
__array___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__array___iter__.NAME = "__array___iter__";
__array___iter__.args_signature = ["self"];
__array___iter__.kwargs_signature = {  };
__array___iter__.types_signature = {  };
__array___iter__.return_type = "Iterator";
__array___iter__.pythonscript_function = true;
__array_attrs["__iter__"] = __array___iter__;
__array_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "index")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var index = arguments['index'];
  return __array___getitem__([self, index], Object());
}

__array_get.NAME = "__array_get";
__array_get.args_signature = ["self", "index"];
__array_get.kwargs_signature = {  };
__array_get.types_signature = {  };
__array_get.pythonscript_function = true;
__array_attrs["get"] = __array_get;
__array_fromlist = function(args, kwargs) {
  var typecode, i, func_name, dataview, length, item, step, func, offset, size;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "lst")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var lst = arguments['lst'];
  length = len([lst], __NULL_OBJECT__);
  step = self.itemsize;
  typecode = self.typecode;
  size = length * step;
  dataview = self.dataview;
  func_name = "set" + __get__(__get__(self, "typecode_names"), "__getitem__")([typecode], Object());
  func = dataview[func_name].bind(dataview);
  if (( size ) <= self.bytes) {
    i = 0;
    offset = 0;
    while(( i ) < length) {
      item = __get__(lst, "__getitem__")([i], Object());
      if (( typecode ) == "float8") {
        item *= self._norm_set
      } else {
        if (( typecode ) == "float16") {
          item *= self._norm_set
        }
      }
      func(offset,item);
      offset += step
      i += 1
    }
  } else {
    throw TypeError;
  }
}

__array_fromlist.NAME = "__array_fromlist";
__array_fromlist.args_signature = ["self", "lst"];
__array_fromlist.kwargs_signature = {  };
__array_fromlist.types_signature = {  };
__array_fromlist.pythonscript_function = true;
__array_attrs["fromlist"] = __array_fromlist;
__array_resize = function(args, kwargs) {
  var source, new_buff, target, new_size, buff;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "length")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var length = arguments['length'];
  buff = self.buffer;
  source = new Uint8Array(buff);
  new_size = length * self.itemsize;
  new_buff = new ArrayBuffer(new_size);
  target = new Uint8Array(new_buff);
  target.set(source);
  self.length = length;
  self.bytes = new_size;
  self.buffer = new_buff;
  self.dataview = new DataView(new_buff);
}

__array_resize.NAME = "__array_resize";
__array_resize.args_signature = ["self", "length"];
__array_resize.kwargs_signature = {  };
__array_resize.types_signature = {  };
__array_resize.pythonscript_function = true;
__array_attrs["resize"] = __array_resize;
__array_append = function(args, kwargs) {
  var length;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "value")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var value = arguments['value'];
  length = self.length;
  __get__(__get__(self, "resize"), "__call__")([self.length + 1], __NULL_OBJECT__);
  __get__(__get__(self, "__setitem__"), "__call__")([length, value], Object());
}

__array_append.NAME = "__array_append";
__array_append.args_signature = ["self", "value"];
__array_append.kwargs_signature = {  };
__array_append.types_signature = {  };
__array_append.pythonscript_function = true;
__array_attrs["append"] = __array_append;
__array_extend = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self", "lst")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var lst = arguments['lst'];
  var __iterator__, value;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while(( __iterator__.index ) < __iterator__.length) {
    value = __next__();
    __get__(__get__(self, "append"), "__call__")([value], __NULL_OBJECT__);
  }
}

__array_extend.NAME = "__array_extend";
__array_extend.args_signature = ["self", "lst"];
__array_extend.kwargs_signature = {  };
__array_extend.types_signature = {  };
__array_extend.pythonscript_function = true;
__array_attrs["extend"] = __array_extend;
__array_to_array = function(args, kwargs) {
  var i, item, arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  arr = [];
  i = 0;
  while(( i ) < self.length) {
    item = __array___getitem__([self, i], Object());
    arr.push( item );
    i += 1
  }
  return arr;
}

__array_to_array.NAME = "__array_to_array";
__array_to_array.args_signature = ["self"];
__array_to_array.kwargs_signature = {  };
__array_to_array.types_signature = {  };
__array_to_array.pythonscript_function = true;
__array_attrs["to_array"] = __array_to_array;
__array_to_list = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  var __args_4, __kwargs_4;
  __args_4 = [];
  __kwargs_4 = {"js_object": __get__(__get__(self, "to_array"), "__call__")()};
  return __get__(list, "__call__")([], __kwargs_4);
}

__array_to_list.NAME = "__array_to_list";
__array_to_list.args_signature = ["self"];
__array_to_list.kwargs_signature = {  };
__array_to_list.types_signature = {  };
__array_to_list.return_type = "list";
__array_to_list.pythonscript_function = true;
__array_attrs["to_list"] = __array_to_list;
__array_to_ascii = function(args, kwargs) {
  var i, length, arr, string;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("self")};
  arguments = get_arguments(signature, args, kwargs);
  var self = arguments['self'];
  string = "";
  arr = __get__(__get__(self, "to_array"), "__call__")();
  i = 0;
  length = __get__(arr, "length");
  while(( i ) < length) {
    var num = arr[i];
    var char = String.fromCharCode(num);
    string += char
    i += 1
  }
  return string;
}

__array_to_ascii.NAME = "__array_to_ascii";
__array_to_ascii.args_signature = ["self"];
__array_to_ascii.kwargs_signature = {  };
__array_to_ascii.types_signature = {  };
__array_to_ascii.pythonscript_function = true;
__array_attrs["to_ascii"] = __array_to_ascii;
array = create_class("array", __array_parents, __array_attrs, __array_properties);
json = { "loads":(function (s) {return JSON.parse(s)}),"dumps":(function (o) {return JSON.stringify(o)}) };
_to_pythonjs = function(args, kwargs) {
  var set, keys, raw, jstype, output, append;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("json")};
  arguments = get_arguments(signature, args, kwargs);
  var json = arguments['json'];
  var jstype, item, output;
  jstype = typeof json;
  if (( jstype ) == "number") {
    return json;
  }
  if (( jstype ) == "string") {
    return json;
  }
  if (Object.prototype.toString.call(json) === '[object Array]') {
    output = __get__(list, "__call__")();
    var __args_5, __kwargs_5;
    __args_5 = [];
    __kwargs_5 = {"js_object": json};
    raw = __get__(list, "__call__")([], __kwargs_5);
    var append;
    append = __get__(output, "append");
    var __iterator__, item;
    __iterator__ = __get__(__get__(raw, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while(( __iterator__.index ) < __iterator__.length) {
      item = __next__();
      __get__(append, "__call__")([_to_pythonjs([item], __NULL_OBJECT__)], __NULL_OBJECT__);
    }
    return output;
  }
  output = __get__(dict, "__call__")();
  var set;
  set = __get__(output, "set");
  var __args_6, __kwargs_6;
  __args_6 = [];
  __kwargs_6 = {"js_object": Object.keys(json)};
  keys = __get__(list, "__call__")([], __kwargs_6);
  var __iterator__, key;
  __iterator__ = __get__(__get__(keys, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while(( __iterator__.index ) < __iterator__.length) {
    key = __next__();
    __get__(set, "__call__")([key, _to_pythonjs([json[key]], __NULL_OBJECT__)], __NULL_OBJECT__);
  }
  return output;
}

_to_pythonjs.NAME = "_to_pythonjs";
_to_pythonjs.args_signature = ["json"];
_to_pythonjs.kwargs_signature = {  };
_to_pythonjs.types_signature = {  };
_to_pythonjs.pythonscript_function = true;
json_to_pythonjs = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("json")};
  arguments = get_arguments(signature, args, kwargs);
  var json = arguments['json'];
  return _to_pythonjs([__get__(__get__(JSON, "parse"), "__call__")([json], __NULL_OBJECT__)], __NULL_OBJECT__);
}

json_to_pythonjs.NAME = "json_to_pythonjs";
json_to_pythonjs.args_signature = ["json"];
json_to_pythonjs.kwargs_signature = {  };
json_to_pythonjs.types_signature = {  };
json_to_pythonjs.pythonscript_function = true;
_to_json = function(args, kwargs) {
  var r, key, value;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("pythonjs")};
  arguments = get_arguments(signature, args, kwargs);
  var pythonjs = arguments['pythonjs'];
  if (isinstance([pythonjs, list], __NULL_OBJECT__)) {
    r = [];
    var __iterator__, i;
    __iterator__ = __get__(__get__(pythonjs, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while(( __iterator__.index ) < __iterator__.length) {
      i = __next__();
      __get__(__get__(r, "push"), "__call__")([_to_json([i], __NULL_OBJECT__)], __NULL_OBJECT__);
    }
  } else {
    if (isinstance([pythonjs, dict], __NULL_OBJECT__)) {
      var r;
      r = Object();
      var __iterator__, key;
      __iterator__ = __get__(__get__(__get__(__get__(pythonjs, "keys"), "__call__")(), "__iter__"), "__call__")([], Object());
      var __next__;
      __next__ = __get__(__iterator__, "next_fast");
      while(( __iterator__.index ) < __iterator__.length) {
        key = __next__();
        value = _to_json([__get__(__get__(pythonjs, "get"), "__call__")([key], __NULL_OBJECT__)], __NULL_OBJECT__);
        key = _to_json([key], __NULL_OBJECT__);
        r[ key ] = value;
      }
    } else {
      r = pythonjs;
    }
  }
  return r;
}

_to_json.NAME = "_to_json";
_to_json.args_signature = ["pythonjs"];
_to_json.kwargs_signature = {  };
_to_json.types_signature = {  };
_to_json.pythonscript_function = true;
pythonjs_to_json = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var signature, arguments;
  signature = {"kwargs": Object(), "args": __create_array__("pythonjs")};
  arguments = get_arguments(signature, args, kwargs);
  var pythonjs = arguments['pythonjs'];
  return __get__(__get__(JSON, "stringify"), "__call__")([_to_json([pythonjs], __NULL_OBJECT__)], __NULL_OBJECT__);
}

pythonjs_to_json.NAME = "pythonjs_to_json";
pythonjs_to_json.args_signature = ["pythonjs"];
pythonjs_to_json.kwargs_signature = {  };
pythonjs_to_json.types_signature = {  };
pythonjs_to_json.pythonscript_function = true;