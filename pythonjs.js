// PythonJS Runtime - regenerated on: Fri Feb 21 00:54:29 2014
__NULL_OBJECT__ = Object.create(null);
if (( "window" )  in  this && ( "document" )  in  this) {
  __WEBWORKER__ = false;
  __NODEJS__ = false;
  pythonjs = {  };
} else {
  if (( "process" )  in  this) {
    __WEBWORKER__ = false;
    __NODEJS__ = true;
  } else {
    __NODEJS__ = false;
    __WEBWORKER__ = true;
  }
}
jsrange = function(num) {
  "Emulates Python's range function";
  var i, r;
  i = 0;
  r = [];
  while (( i ) < num) {
    r.push(i);
    i = (i + 1);
  }
  return r;
}

__create_array__ = function() {
  "Used to fix a bug/feature of Javascript where new Array(number)\n	created a array with number of undefined elements which is not\n	what we want";
  var array;
  array = [];
    var __iter1 = jsrange(arguments.length);
  if (! (__iter1 instanceof Array || typeof __iter1 == "string") ) { __iter1 = __object_keys__(__iter1) }
  for (var __idx1=0; __idx1 < __iter1.length; __idx1++) {
    var i = __iter1[ __idx1 ];
    array.push(arguments[i]);
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
  if (( object ) == undefined) {
    return undefined;
  }
  if (( attribute ) == "__call__") {
    if (object.pythonscript_function || object.is_wrapper) {
      return object;
    } else {
      if (object.cached_wrapper) {
        return object.cached_wrapper;
      } else {
        if ({}.toString.call(object) === '[object Function]') {
                    var wrapper = function(args, kwargs) {
            var i, arg, keys;
            if (( args ) != undefined) {
              i = 0;
              while (( i ) < args.length) {
                arg = args[i];
                if (arg && ( typeof(arg) ) == "object") {
                  if (arg.jsify) {
                    args[i] = arg.jsify();
                  }
                }
                i += 1;
              }
            }
            if (( kwargs ) != undefined) {
              keys = __object_keys__(kwargs);
              if (( keys.length ) != 0) {
                args.push(kwargs);
                i = 0;
                while (( i ) < keys.length) {
                  arg = kwargs[keys[i]];
                  if (arg && ( typeof(arg) ) == "object") {
                    if (arg.jsify) {
                      kwargs[keys[i]] = arg.jsify();
                    }
                  }
                  i += 1;
                }
              }
            }
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
  if (( __NODEJS__ ) === false && ( __WEBWORKER__ ) === false) {
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
    if (typeof(attr) === 'function') {
      if (attr.pythonscript_function === undefined && attr.is_wrapper === undefined) {
                var wrapper = function(args, kwargs) {
          var i, arg, keys;
          if (( args ) != undefined) {
            i = 0;
            while (( i ) < args.length) {
              arg = args[i];
              if (arg && ( typeof(arg) ) == "object") {
                if (arg.jsify) {
                  args[i] = arg.jsify();
                }
              }
              i += 1;
            }
          }
          if (( kwargs ) != undefined) {
            keys = __object_keys__(kwargs);
            if (( keys.length ) != 0) {
              args.push(kwargs);
              i = 0;
              while (( i ) < keys.length) {
                arg = kwargs[keys[i]];
                if (arg && ( typeof(arg) ) == "object") {
                  if (arg.jsify) {
                    kwargs[keys[i]] = arg.jsify();
                  }
                }
                i += 1;
              }
            }
          }
          return attr.apply(object, args);
        }

        wrapper.is_wrapper = true;
        return wrapper;
      } else {
        if (attr.is_classmethod) {
                    var method = function() {
            var args;
            args = Array.prototype.slice.call(arguments);
            if (args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && ( args.length ) == 2) {
              /*pass*/
            } else {
              args = [args, Object()];
            }
            if (object.__class__) {
              args[0].splice(0, 0, object.__class__);
            } else {
              args[0].splice(0, 0, object);
            }
            return attr.apply(this, args);
          }

          method.is_wrapper = true;
          object[attribute] = method;
          return method;
        } else {
          return attr;
        }
      }
    } else {
      return attr;
    }
  }
  var __class__, bases;
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
        if (attr.is_wrapper) {
          return attr;
        } else {
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
        }
        method.is_wrapper = true;
        object[attribute] = method;
        return method;
      } else {
        return attr;
      }
    }
    bases = __class__.__bases__;
        var __iter2 = bases;
    if (! (__iter2 instanceof Array || typeof __iter2 == "string") ) { __iter2 = __object_keys__(__iter2) }
    for (var __idx2=0; __idx2 < __iter2.length; __idx2++) {
      var base = __iter2[ __idx2 ];
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
    }
        var __iter3 = bases;
    if (! (__iter3 instanceof Array || typeof __iter3 == "string") ) { __iter3 = __object_keys__(__iter3) }
    for (var __idx3=0; __idx3 < __iter3.length; __idx3++) {
      var base = __iter3[ __idx3 ];
      var prop;
      prop = _get_upstream_property(base, attribute);
      if (prop) {
        return prop["get"]([object], Object());
      }
    }
    if (( "__getattr__" )  in  __class__) {
      return __class__["__getattr__"]([object, attribute], Object());
    }
        var __iter4 = bases;
    if (! (__iter4 instanceof Array || typeof __iter4 == "string") ) { __iter4 = __object_keys__(__iter4) }
    for (var __idx4=0; __idx4 < __iter4.length; __idx4++) {
      var base = __iter4[ __idx4 ];
      var f;
      f = _get_upstream_attribute(base, "__getattr__");
      if (f) {
        return f([object, attribute], Object());
      }
    }
  }
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
  return undefined;
}

_get_upstream_attribute = function(base, attr) {
  if (( attr )  in  base) {
    return base[attr];
  }
    var __iter5 = base.__bases__;
  if (! (__iter5 instanceof Array || typeof __iter5 == "string") ) { __iter5 = __object_keys__(__iter5) }
  for (var __idx5=0; __idx5 < __iter5.length; __idx5++) {
    var parent = __iter5[ __idx5 ];
    return _get_upstream_attribute(parent, attr);
  }
}

_get_upstream_property = function(base, attr) {
  if (( attr )  in  base.__properties__) {
    return base.__properties__[attr];
  }
    var __iter6 = base.__bases__;
  if (! (__iter6 instanceof Array || typeof __iter6 == "string") ) { __iter6 = __object_keys__(__iter6) }
  for (var __idx6=0; __idx6 < __iter6.length; __idx6++) {
    var parent = __iter6[ __idx6 ];
    return _get_upstream_property(parent, attr);
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
  while (( j ) < signature.args.length) {
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
    j += 1;
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
var IndexError = new RangeError();
var KeyError = new RangeError();
var ValueError = new RangeError();
__contains__ = function(ob, a) {
  var t;
  t = typeof(ob);
  if (( t ) == "string") {
    if (( ob.indexOf(a) ) == -1) {
      return false;
    } else {
      return true;
    }
  } else {
    if (( t ) == "number") {
      throw TypeError;
    } else {
      if (ob.__contains__) {
        return ob.__contains__(a);
      } else {
        if (( typeof(a) ) == "string" && Object.hasOwnProperty.call(ob, a)) {
          return true;
        }
      }
    }
  }
}

__contains__.NAME = "__contains__";
__contains__.args_signature = ["ob", "a"];
__contains__.kwargs_signature = {  };
__contains__.types_signature = {  };
__split_method = function(ob) {
  if (( typeof(ob) ) == "string") {
    return ob.split(" ");
  } else {
    return __split_method(ob);
  }
}

__split_method.NAME = "__split_method";
__split_method.args_signature = ["ob"];
__split_method.kwargs_signature = {  };
__split_method.types_signature = {  };
__test_if_true__ = function(ob) {
  if (! (ob)) {
    return false;
  } else {
    if (ob instanceof Array) {
      return ( ob.length ) != 0;
    } else {
      if (isinstance(ob, dict)) {
        return ( Object.keys(ob["$wrapped"]).length ) != 0;
      } else {
        if (ob instanceof Object) {
          return ( Object.keys(ob).length ) != 0;
        } else {
          return true;
        }
      }
    }
  }
}

__test_if_true__.NAME = "__test_if_true__";
__test_if_true__.args_signature = ["ob"];
__test_if_true__.kwargs_signature = {  };
__test_if_true__.types_signature = {  };
__add_op = function(a, b) {
  var c, t;
  t = typeof(a);
  if (( t ) == "number" || ( t ) == "string") {
    return a+b;
  } else {
    if (a instanceof Array) {
      c = [];
      c.extend(a);
      c.extend(b);
      return c;
    } else {
      if (a.__add__) {
        return a.__add__(b);
      } else {
        throw TypeError;
      }
    }
  }
}

__add_op.NAME = "__add_op";
__add_op.args_signature = ["a", "b"];
__add_op.kwargs_signature = {  };
__add_op.types_signature = {  };
__jsdict = function(items) {
  var d, key;
  d = {};
    var __iter1 = items;
  if (! (__iter1 instanceof Array || typeof __iter1 == "string") ) { __iter1 = __object_keys__(__iter1) }
  for (var __idx1=0; __idx1 < __iter1.length; __idx1++) {
    var item = __iter1[ __idx1 ];
    key = item[0];
    if (key.__uid__) {
      key = key.__uid__;
    }
    d[ (key.__uid__) ? key.__uid__ : key] = item[1];
  }
  return d;
}

__jsdict.NAME = "__jsdict";
__jsdict.args_signature = ["items"];
__jsdict.kwargs_signature = {  };
__jsdict.types_signature = {  };
__jsdict_get = function(ob, key, default_value) {
  if (default_value == undefined) default_value = undefined;
  if (ob instanceof Object) {
    if (key in ob) {
      return ob[ (key.__uid__) ? key.__uid__ : key];
    }
    return default_value;
  } else {
    return ob.get(key, default_value);
  }
}

__jsdict_get.NAME = "__jsdict_get";
__jsdict_get.args_signature = ["ob", "key", "default_value"];
__jsdict_get.kwargs_signature = { default_value:undefined };
__jsdict_get.types_signature = { default_value:"None" };
__jsdict_set = function(ob, key, value) {
  if (ob instanceof Object) {
    ob[ (key.__uid__) ? key.__uid__ : key] = value;
  } else {
    ob.set(key,value);
  }
}

__jsdict_set.NAME = "__jsdict_set";
__jsdict_set.args_signature = ["ob", "key", "value"];
__jsdict_set.kwargs_signature = {  };
__jsdict_set.types_signature = {  };
__jsdict_keys = function(ob) {
  if (ob instanceof Object) {
    return Object.keys( ob );
  } else {
    return ob.keys();
  }
}

__jsdict_keys.NAME = "__jsdict_keys";
__jsdict_keys.args_signature = ["ob"];
__jsdict_keys.kwargs_signature = {  };
__jsdict_keys.types_signature = {  };
__jsdict_values = function(ob) {
  var arr, value;
  if (ob instanceof Object) {
    arr = [];
        var __iter2 = ob;
    if (! (__iter2 instanceof Array || typeof __iter2 == "string") ) { __iter2 = __object_keys__(__iter2) }
    for (var __idx2=0; __idx2 < __iter2.length; __idx2++) {
      var key = __iter2[ __idx2 ];
      if (ob.hasOwnProperty(key)) {
        value = ob[ (key.__uid__) ? key.__uid__ : key];
        arr.push(value);
      }
    }
    return arr;
  } else {
    return ob.values();
  }
}

__jsdict_values.NAME = "__jsdict_values";
__jsdict_values.args_signature = ["ob"];
__jsdict_values.kwargs_signature = {  };
__jsdict_values.types_signature = {  };
__jsdict_items = function(ob) {
  var arr, value;
  if (ob instanceof Object || ( ob.items ) === undefined) {
    arr = [];
        var __iter3 = ob;
    if (! (__iter3 instanceof Array || typeof __iter3 == "string") ) { __iter3 = __object_keys__(__iter3) }
    for (var __idx3=0; __idx3 < __iter3.length; __idx3++) {
      var key = __iter3[ __idx3 ];
      if (Object.hasOwnProperty.call(ob, key)) {
        value = ob[ (key.__uid__) ? key.__uid__ : key];
        arr.push([key, value]);
      }
    }
    return arr;
  } else {
    return ob.items();
  }
}

__jsdict_items.NAME = "__jsdict_items";
__jsdict_items.args_signature = ["ob"];
__jsdict_items.kwargs_signature = {  };
__jsdict_items.types_signature = {  };
__jsdict_pop = function(ob, key, _default) {
  var v;
  if (_default == undefined) _default = undefined;
  if (ob instanceof Array) {
    if (ob.length) {
      return ob.pop(key);
    } else {
      throw IndexError;
    }
  } else {
    if (ob instanceof Object) {
      if (key in ob) {
        v = ob[ (key.__uid__) ? key.__uid__ : key];
        delete ob[key];
        return v;
      } else {
        if (( _default ) === undefined) {
          throw KeyError;
        } else {
          return _default;
        }
      }
    } else {
      return ob.pop(key, _default);
    }
  }
}

__jsdict_pop.NAME = "__jsdict_pop";
__jsdict_pop.args_signature = ["ob", "key", "_default"];
__jsdict_pop.kwargs_signature = { _default:undefined };
__jsdict_pop.types_signature = { _default:"None" };
__object_keys__ = function(ob) {
  var arr;
  "\n		notes:\n			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`\n			. this is different from Object.keys because it traverses the prototype chain.\n		";
  arr = [];
  for (key in ob) { arr.push(key) };
  return arr;
}

__object_keys__.NAME = "__object_keys__";
__object_keys__.args_signature = ["ob"];
__object_keys__.kwargs_signature = {  };
__object_keys__.types_signature = {  };
__bind_property_descriptors__ = function(o, klass) {
  var prop, desc;
    var __iter4 = klass.__properties__;
  if (! (__iter4 instanceof Array || typeof __iter4 == "string") ) { __iter4 = __object_keys__(__iter4) }
  for (var __idx4=0; __idx4 < __iter4.length; __idx4++) {
    var name = __iter4[ __idx4 ];
    desc = __jsdict([["enumerable", true]]);
    prop = klass.__properties__[ (name.__uid__) ? name.__uid__ : name];
    if (prop[ ("get".__uid__) ? "get".__uid__ : "get"]) {
      desc[ ("get".__uid__) ? "get".__uid__ : "get"] = __generate_getter__(klass, o, name);
    }
    if (prop[ ("set".__uid__) ? "set".__uid__ : "set"]) {
      desc[ ("set".__uid__) ? "set".__uid__ : "set"] = __generate_setter__(klass, o, name);
    }
    Object.defineProperty(o, name, desc);
  }
    var __iter5 = klass.__bases__;
  if (! (__iter5 instanceof Array || typeof __iter5 == "string") ) { __iter5 = __object_keys__(__iter5) }
  for (var __idx5=0; __idx5 < __iter5.length; __idx5++) {
    var base = __iter5[ __idx5 ];
    __bind_property_descriptors__(o, base);
  }
}

__bind_property_descriptors__.NAME = "__bind_property_descriptors__";
__bind_property_descriptors__.args_signature = ["o", "klass"];
__bind_property_descriptors__.kwargs_signature = {  };
__bind_property_descriptors__.types_signature = {  };
__generate_getter__ = function(klass, o, n) {
  return (function () {return klass.__properties__[ (n.__uid__) ? n.__uid__ : n][ ("get".__uid__) ? "get".__uid__ : "get"]([o], __jsdict([]))});
}

__generate_getter__.NAME = "__generate_getter__";
__generate_getter__.args_signature = ["klass", "o", "n"];
__generate_getter__.kwargs_signature = {  };
__generate_getter__.types_signature = {  };
__generate_setter__ = function(klass, o, n) {
  return (function (v) {return klass.__properties__[ (n.__uid__) ? n.__uid__ : n][ ("set".__uid__) ? "set".__uid__ : "set"]([o, v], __jsdict([]))});
}

__generate_setter__.NAME = "__generate_setter__";
__generate_setter__.args_signature = ["klass", "o", "n"];
__generate_setter__.kwargs_signature = {  };
__generate_setter__.types_signature = {  };
__sprintf = function(fmt, args) {
  var chunks, item, arr;
  if (args instanceof Array) {
    chunks = fmt.split("%s");
    arr = [];
    var i;
    i = 0;
        var __iter6 = chunks;
    if (! (__iter6 instanceof Array || typeof __iter6 == "string") ) { __iter6 = __object_keys__(__iter6) }
    for (var __idx6=0; __idx6 < __iter6.length; __idx6++) {
      var txt = __iter6[ __idx6 ];
      arr.append(txt);
      if (( i ) >= args.length) {
        break;
      }
      item = args[ (i.__uid__) ? i.__uid__ : i];
      if (( typeof(item) ) == "string") {
        arr.append(item);
      } else {
        if (( typeof(item) ) == "number") {
          arr.append(__add_op("", item));
        } else {
          arr.append(Object.prototype.toString.call(item));
        }
      }
      i += 1;
    }
    return "".join(arr);
  } else {
    return fmt.replace("%s", args);
  }
}

__sprintf.NAME = "__sprintf";
__sprintf.args_signature = ["fmt", "args"];
__sprintf.kwargs_signature = {  };
__sprintf.types_signature = {  };
__create_class__ = function(class_name, parents, attrs, props) {
  var metaclass, klass, prop;
  "Create a PythonScript class";
  if (attrs.__metaclass__) {
    metaclass = attrs.__metaclass__;
    attrs.__metaclass__ = undefined;
    return metaclass([class_name, parents, attrs]);
  }
  klass = Object.create(null);
  klass.__bases__ = parents;
  klass.__name__ = class_name;
  klass.__unbound_methods__ = Object.create(null);
  klass.__all_method_names__ = [];
  klass.__properties__ = props;
  klass.__attributes__ = attrs;
    var __iter7 = attrs;
  if (! (__iter7 instanceof Array || typeof __iter7 == "string") ) { __iter7 = __object_keys__(__iter7) }
  for (var __idx7=0; __idx7 < __iter7.length; __idx7++) {
    var key = __iter7[ __idx7 ];
    if (( typeof(attrs[ (key.__uid__) ? key.__uid__ : key]) ) == "function") {
      klass.__all_method_names__.push(key);
      if (attrs[ (key.__uid__) ? key.__uid__ : key].is_classmethod || attrs[ (key.__uid__) ? key.__uid__ : key].is_staticmethod) {
        /*pass*/
      } else {
        klass.__unbound_methods__[ (key.__uid__) ? key.__uid__ : key] = attrs[ (key.__uid__) ? key.__uid__ : key];
      }
    }
    if (( key ) == "__getattribute__") {
      continue
    }
    klass[ (key.__uid__) ? key.__uid__ : key] = attrs[ (key.__uid__) ? key.__uid__ : key];
  }
  klass.__setters__ = [];
  klass.__getters__ = [];
    var __iter8 = klass.__properties__;
  if (! (__iter8 instanceof Array || typeof __iter8 == "string") ) { __iter8 = __object_keys__(__iter8) }
  for (var __idx8=0; __idx8 < __iter8.length; __idx8++) {
    var name = __iter8[ __idx8 ];
    prop = klass.__properties__[ (name.__uid__) ? name.__uid__ : name];
    klass.__getters__.push(name);
    if (prop[ ("set".__uid__) ? "set".__uid__ : "set"]) {
      klass.__setters__.push(name);
    }
  }
    var __iter9 = klass.__bases__;
  if (! (__iter9 instanceof Array || typeof __iter9 == "string") ) { __iter9 = __object_keys__(__iter9) }
  for (var __idx9=0; __idx9 < __iter9.length; __idx9++) {
    var base = __iter9[ __idx9 ];
    Array.prototype.push.apply(klass.__getters__, base.__getters__);
    Array.prototype.push.apply(klass.__setters__, base.__setters__);
    Array.prototype.push.apply(klass.__all_method_names__, base.__all_method_names__);
  }
    var __call__ = function() {
    var has_getattr, wrapper, object, has_getattribute;
    "Create a PythonJS object";
    object = Object.create(null);
    object.__class__ = klass;
    object.__dict__ = object;
    has_getattribute = false;
    has_getattr = false;
        var __iter10 = klass.__all_method_names__;
    if (! (__iter10 instanceof Array || typeof __iter10 == "string") ) { __iter10 = __object_keys__(__iter10) }
    for (var __idx10=0; __idx10 < __iter10.length; __idx10++) {
      var name = __iter10[ __idx10 ];
      if (( name ) == "__getattribute__") {
        has_getattribute = true;
      } else {
        if (( name ) == "__getattr__") {
          has_getattr = true;
        } else {
          wrapper = __get__(object, name);
          if (! (wrapper.is_wrapper)) {
            console.log("RUNTIME ERROR: failed to get wrapper for:", name);
          }
        }
      }
    }
    if (__test_if_true__(has_getattr)) {
      __get__(object, "__getattr__");
    }
    if (__test_if_true__(has_getattribute)) {
      __get__(object, "__getattribute__");
    }
    __bind_property_descriptors__(object, klass);
    if (object.__init__) {
      object.__init__.apply(this, arguments);
    }
    return object;
  }

  __call__.NAME = "__call__";
  __call__.args_signature = [];
  __call__.kwargs_signature = {  };
  __call__.types_signature = {  };
  __call__.pythonscript_function = true;
  klass.__call__ = __call__;
  return klass;
}

__create_class__.NAME = "__create_class__";
__create_class__.args_signature = ["class_name", "parents", "attrs", "props"];
__create_class__.kwargs_signature = {  };
__create_class__.types_signature = {  };
type = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"bases": undefined, "class_dict": undefined},args:__create_array__("ob_or_class_name", "bases", "class_dict") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob_or_class_name = __args__['ob_or_class_name'];
  var bases = __args__['bases'];
  var class_dict = __args__['class_dict'];
  "\n	type(object) -> the object's type\n	type(name, bases, dict) -> a new type  ## broken? - TODO test\n	";
  if (( bases ) === undefined && ( class_dict ) === undefined) {
    return ob_or_class_name.__class__;
  } else {
    return create_class(ob_or_class_name, bases, class_dict);
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
  var __sig__, __args__;
  __sig__ = { kwargs:{"method": false},args:__create_array__("ob", "attr", "method") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  var method = __args__['method'];
  return Object.hasOwnProperty.call(ob, attr);
}

hasattr.NAME = "hasattr";
hasattr.args_signature = ["ob", "attr", "method"];
hasattr.kwargs_signature = { method:false };
hasattr.types_signature = { method:"False" };
hasattr.pythonscript_function = true;
getattr = function(args, kwargs) {
  var prop;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"property": false},args:__create_array__("ob", "attr", "property") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  var property = __args__['property'];
  if (__test_if_true__(property)) {
    prop = _get_upstream_property(ob.__class__, attr);
    if (prop && prop[ ("get".__uid__) ? "get".__uid__ : "get"]) {
      return prop[ ("get".__uid__) ? "get".__uid__ : "get"]([ob], __jsdict([]));
    } else {
      console.log("ERROR: getattr property error", prop);
    }
  } else {
    return __get__(ob, attr);
  }
}

getattr.NAME = "getattr";
getattr.args_signature = ["ob", "attr", "property"];
getattr.kwargs_signature = { property:false };
getattr.types_signature = { property:"False" };
getattr.pythonscript_function = true;
setattr = function(args, kwargs) {
  var prop;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"property": false},args:__create_array__("ob", "attr", "value", "property") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  var value = __args__['value'];
  var property = __args__['property'];
  if (__test_if_true__(property)) {
    prop = _get_upstream_property(ob.__class__, attr);
    if (prop && prop[ ("set".__uid__) ? "set".__uid__ : "set"]) {
      prop[ ("set".__uid__) ? "set".__uid__ : "set"]([ob, value], __jsdict([]));
    } else {
      console.log("ERROR: setattr property error", prop);
    }
  } else {
    __set__(ob, attr, value);
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("C", "B") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var C = __args__['C'];
  var B = __args__['B'];
  if (( C ) === B) {
    return true;
  }
  bases = C.__bases__;
  i = 0;
  while (( i ) < __get__(bases, "length")) {
    if (issubclass([__get__(bases, "__getitem__")([i], Object()), B], __NULL_OBJECT__)) {
      return true;
    }
    i += 1;
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("ob", "klass") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob = __args__['ob'];
  var klass = __args__['klass'];
  if (( ob ) === undefined || ( ob ) === null) {
    return false;
  } else {
    if (ob instanceof Array && ( klass ) === list) {
      return true;
    } else {
      if (( klass ) === dict && ob instanceof Object) {
        if (ob instanceof Array) {
          return false;
        } else {
          if (ob.__class__) {
            return false;
          } else {
            return true;
          }
        }
      } else {
        if (! (Object.hasOwnProperty.call(ob, "__class__"))) {
          return false;
        }
      }
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
  ;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  a = Math.round(a);
  if (isNaN(a)) {
    throw ValueError;
  }
  return a;
}

int.NAME = "int";
int.args_signature = ["a"];
int.kwargs_signature = {  };
int.types_signature = {  };
int.pythonscript_function = true;
float = function(args, kwargs) {
  ;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  a = Number(a);
  if (isNaN(a)) {
    throw ValueError;
  }
  return a;
}

float.NAME = "float";
float.args_signature = ["a"];
float.kwargs_signature = {  };
float.types_signature = {  };
float.pythonscript_function = true;
round = function(args, kwargs) {
  var y, x, c, b;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a", "places") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  var places = __args__['places'];
  b = __add_op("", a);
  if (( b.indexOf(".") ) == -1) {
    return a;
  } else {
    c = b.split(".");
    x = c[0];
    y = c[1].substring(0, places);
    return parseFloat(__add_op(__add_op(x, "."), y));
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("s") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var s = __args__['s'];
  return __add_op("", s);
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
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.__contains__ = func;
    var func = function(index) {
    return this[ (index.__uid__) ? index.__uid__ : index];
  }

  func.NAME = "func";
  func.args_signature = ["index"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.get = func;
    var func = function(self) {
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  func.NAME = "func";
  func.args_signature = ["self"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.__iter__ = func;
    var func = function(idx) {
    return this[ (idx.__uid__) ? idx.__uid__ : idx];
  }

  func.NAME = "func";
  func.args_signature = ["idx"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.__getitem__ = func;
    var func = function() {
    return this.length;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.__len__ = func;
    var func = function(start, stop, step) {
    ;
    if (( start ) === undefined && ( stop ) === undefined && ( step ) == -1) {
      return this.split("").reverse().join("");
    } else {
      if (( stop ) < 0) {
        stop = __add_op(this.length, stop);
      }
      return this.substring(start, stop);
    }
  }

  func.NAME = "func";
  func.args_signature = ["start", "stop", "step"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.__getslice__ = func;
    var func = function() {
    return this.split("\n");
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.splitlines = func;
    var func = function() {
    return this.trim();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.strip = func;
    var func = function(a) {
    if (( this.substring(0, a.length) ) == a) {
      return true;
    } else {
      return false;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.startswith = func;
    var func = function(a) {
    if (( this.substring((this.length - a.length), this.length) ) == a) {
      return true;
    } else {
      return false;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.endswith = func;
    var func = function(a) {
    var i, arr, out;
    out = "";
    if (a instanceof Array) {
      arr = a;
    } else {
      arr = a["$wrapped"];
    }
    i = 0;
        var __iter11 = arr;
    if (! (__iter11 instanceof Array || typeof __iter11 == "string") ) { __iter11 = __object_keys__(__iter11) }
    for (var __idx11=0; __idx11 < __iter11.length; __idx11++) {
      var value = __iter11[ __idx11 ];
      out += value;
      i += 1;
      if (( i ) < arr.length) {
        out += this;
      }
    }
    return out;
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.join = func;
    var func = function() {
    return this.toUpperCase();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.upper = func;
    var func = function() {
    return this.toLowerCase();
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.lower = func;
    var func = function(a) {
    ;
    a = this.indexOf(a);
    if (( a ) == -1) {
      throw ValueError;
    }
    return a;
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.index = func;
    var func = function(a) {
    return this.indexOf(a);
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.find = func;
    var func = function() {
    var digits;
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
        var __iter12 = this;
    if (! (__iter12 instanceof Array || typeof __iter12 == "string") ) { __iter12 = __object_keys__(__iter12) }
    for (var __idx12=0; __idx12 < __iter12.length; __idx12++) {
      var char = __iter12[ __idx12 ];
      if (__contains__(digits, char)) {
        /*pass*/
      } else {
        return false;
      }
    }
    return true;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.isdigit = func;
    var func = function(encoding) {
    return this;
  }

  func.NAME = "func";
  func.args_signature = ["encoding"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.decode = func;
    var func = function(encoding) {
    return this;
  }

  func.NAME = "func";
  func.args_signature = ["encoding"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  String.prototype.encode = func;
}

_setup_str_prototype.NAME = "_setup_str_prototype";
_setup_str_prototype.args_signature = [];
_setup_str_prototype.kwargs_signature = {  };
_setup_str_prototype.types_signature = {  };
_setup_str_prototype.pythonscript_function = true;
_setup_str_prototype();
_setup_array_prototype = function(args, kwargs) {
    var func = function() {
    var i, item;
    i = 0;
    while (( i ) < this.length) {
      item = this[ (i.__uid__) ? i.__uid__ : i];
      if (( typeof(item) ) == "object") {
        if (item.jsify) {
          this[ (i.__uid__) ? i.__uid__ : i] = item.jsify();
        }
      }
      i += 1;
    }
    return this;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.jsify = func;
    var func = function(a) {
    if (( this.indexOf(a) ) == -1) {
      return false;
    } else {
      return true;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.__contains__ = func;
    var func = function() {
    return this.length;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.__len__ = func;
    var func = function(index) {
    return this[ (index.__uid__) ? index.__uid__ : index];
  }

  func.NAME = "func";
  func.args_signature = ["index"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.get = func;
    var __getitem__ = function(index) {
    ;
    if (( index ) < 0) {
      index = __add_op(this.length, index);
    }
    return this[ (index.__uid__) ? index.__uid__ : index];
  }

  __getitem__.NAME = "__getitem__";
  __getitem__.args_signature = ["index"];
  __getitem__.kwargs_signature = {  };
  __getitem__.types_signature = {  };
  Array.prototype.__getitem__ = __getitem__;
    var __setitem__ = function(index, value) {
    ;
    if (( index ) < 0) {
      index = __add_op(this.length, index);
    }
    this[ (index.__uid__) ? index.__uid__ : index] = value;
  }

  __setitem__.NAME = "__setitem__";
  __setitem__.args_signature = ["index", "value"];
  __setitem__.kwargs_signature = {  };
  __setitem__.types_signature = {  };
  Array.prototype.__setitem__ = __setitem__;
    var func = function() {
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.__iter__ = func;
    var func = function(start, stop, step) {
    ;
    if (( stop ) < 0) {
      stop = __add_op(this.length, stop);
    }
    return this.slice(start, stop);
  }

  func.NAME = "func";
  func.args_signature = ["start", "stop", "step"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.__getslice__ = func;
    var func = function(item) {
    this.push(item);
  }

  func.NAME = "func";
  func.args_signature = ["item"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.append = func;
    var extend = function(other) {
        var __iter13 = other;
    if (! (__iter13 instanceof Array || typeof __iter13 == "string") ) { __iter13 = __object_keys__(__iter13) }
    for (var __idx13=0; __idx13 < __iter13.length; __idx13++) {
      var obj = __iter13[ __idx13 ];
      this.push(obj);
    }
  }

  extend.NAME = "extend";
  extend.args_signature = ["other"];
  extend.kwargs_signature = {  };
  extend.types_signature = {  };
  Array.prototype.extend = extend;
    var func = function(item) {
    var index;
    index = this.indexOf(item);
    this.splice(index, 1);
  }

  func.NAME = "func";
  func.args_signature = ["item"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.remove = func;
    var insert = function(index, obj) {
    ;
    if (( index ) < 0) {
      index = __add_op(this.length, index);
    }
    this.splice(index, 0, obj);
  }

  insert.NAME = "insert";
  insert.args_signature = ["index", "obj"];
  insert.kwargs_signature = {  };
  insert.types_signature = {  };
  Array.prototype.insert = insert;
    var remove = function(obj) {
    var index;
    index = this.indexOf(obj);
    this.splice(index, 1);
  }

  remove.NAME = "remove";
  remove.args_signature = ["obj"];
  remove.kwargs_signature = {  };
  remove.types_signature = {  };
  Array.prototype.remove = remove;
    var index = function(obj) {
    return this.indexOf(obj);
  }

  index.NAME = "index";
  index.args_signature = ["obj"];
  index.kwargs_signature = {  };
  index.types_signature = {  };
  Array.prototype.index = index;
    var count = function(obj) {
    var a;
    a = 0;
        var __iter14 = this;
    if (! (__iter14 instanceof Array || typeof __iter14 == "string") ) { __iter14 = __object_keys__(__iter14) }
    for (var __idx14=0; __idx14 < __iter14.length; __idx14++) {
      var item = __iter14[ __idx14 ];
      if (( item ) === obj) {
        a += 1;
      }
    }
    return a;
  }

  count.NAME = "count";
  count.args_signature = ["obj"];
  count.kwargs_signature = {  };
  count.types_signature = {  };
  Array.prototype.count = count;
    var func = function(x, low, high) {
    var a, mid;
    if (( low ) === undefined) {
      low = 0;
    }
    if (( high ) === undefined) {
      high = this.length;
    }
    while (( low ) < high) {
      a = __add_op(low, high);
      mid = Math.floor((a / 2));
      if (( x ) < this[ (mid.__uid__) ? mid.__uid__ : mid]) {
        high = mid;
      } else {
        low = __add_op(mid, 1);
      }
    }
    return low;
  }

  func.NAME = "func";
  func.args_signature = ["x", "low", "high"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.bisect = func;
    var func = function(other) {
    return this.filter((function (i) {return ( other.indexOf(i) ) == -1}));
  }

  func.NAME = "func";
  func.args_signature = ["other"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.difference = func;
    var func = function(other) {
    return this.filter((function (i) {return ( other.indexOf(i) ) != -1}));
  }

  func.NAME = "func";
  func.args_signature = ["other"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.intersection = func;
    var func = function(other) {
        var __iter15 = this;
    if (! (__iter15 instanceof Array || typeof __iter15 == "string") ) { __iter15 = __object_keys__(__iter15) }
    for (var __idx15=0; __idx15 < __iter15.length; __idx15++) {
      var item = __iter15[ __idx15 ];
      if (( other.indexOf(item) ) == -1) {
        return false;
      }
    }
    return true;
  }

  func.NAME = "func";
  func.args_signature = ["other"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  Array.prototype.issubset = func;
}

_setup_array_prototype.NAME = "_setup_array_prototype";
_setup_array_prototype.args_signature = [];
_setup_array_prototype.kwargs_signature = {  };
_setup_array_prototype.types_signature = {  };
_setup_array_prototype.pythonscript_function = true;
_setup_array_prototype();
_setup_nodelist_prototype = function(args, kwargs) {
    var func = function(a) {
    if (( this.indexOf(a) ) == -1) {
      return false;
    } else {
      return true;
    }
  }

  func.NAME = "func";
  func.args_signature = ["a"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  NodeList.prototype.__contains__ = func;
    var func = function() {
    return this.length;
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  NodeList.prototype.__len__ = func;
    var func = function(index) {
    return this[ (index.__uid__) ? index.__uid__ : index];
  }

  func.NAME = "func";
  func.args_signature = ["index"];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  NodeList.prototype.get = func;
    var __getitem__ = function(index) {
    ;
    if (( index ) < 0) {
      index = __add_op(this.length, index);
    }
    return this[ (index.__uid__) ? index.__uid__ : index];
  }

  __getitem__.NAME = "__getitem__";
  __getitem__.args_signature = ["index"];
  __getitem__.kwargs_signature = {  };
  __getitem__.types_signature = {  };
  NodeList.prototype.__getitem__ = __getitem__;
    var __setitem__ = function(index, value) {
    ;
    if (( index ) < 0) {
      index = __add_op(this.length, index);
    }
    this[ (index.__uid__) ? index.__uid__ : index] = value;
  }

  __setitem__.NAME = "__setitem__";
  __setitem__.args_signature = ["index", "value"];
  __setitem__.kwargs_signature = {  };
  __setitem__.types_signature = {  };
  NodeList.prototype.__setitem__ = __setitem__;
    var func = function() {
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  func.NAME = "func";
  func.args_signature = [];
  func.kwargs_signature = {  };
  func.types_signature = {  };
  NodeList.prototype.__iter__ = func;
    var index = function(obj) {
    return this.indexOf(obj);
  }

  index.NAME = "index";
  index.args_signature = ["obj"];
  index.kwargs_signature = {  };
  index.types_signature = {  };
  NodeList.prototype.index = index;
}

_setup_nodelist_prototype.NAME = "_setup_nodelist_prototype";
_setup_nodelist_prototype.args_signature = [];
_setup_nodelist_prototype.kwargs_signature = {  };
_setup_nodelist_prototype.types_signature = {  };
_setup_nodelist_prototype.pythonscript_function = true;
if (( __NODEJS__ ) == false && ( __WEBWORKER__ ) == false) {
  _setup_nodelist_prototype();
}
bisect = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"low": undefined, "high": undefined},args:__create_array__("a", "x", "low", "high") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  var x = __args__['x'];
  var low = __args__['low'];
  var high = __args__['high'];
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
  var i, arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("num", "stop") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var num = __args__['num'];
  var stop = __args__['stop'];
  "Emulates Python's range function";
  if (( stop ) !== undefined) {
    i = num;
    num = stop;
  } else {
    i = 0;
  }
  arr = [];
  while (( i ) < num) {
    arr.push(i);
    i += 1;
  }
  return arr;
}

range.NAME = "range";
range.args_signature = ["num", "stop"];
range.kwargs_signature = {  };
range.types_signature = {  };
range.pythonscript_function = true;
xrange = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("num", "stop") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var num = __args__['num'];
  var stop = __args__['stop'];
  return range([num, stop], __NULL_OBJECT__);
}

xrange.NAME = "xrange";
xrange.args_signature = ["num", "stop"];
xrange.kwargs_signature = {  };
xrange.types_signature = {  };
xrange.pythonscript_function = true;
var StopIteration, __StopIteration_attrs, __StopIteration_parents;
__StopIteration_attrs = Object();
__StopIteration_parents = [];
__StopIteration_properties = Object();
StopIteration = __create_class__("StopIteration", __StopIteration_parents, __StopIteration_attrs, __StopIteration_properties);
len = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("ob") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var ob = __args__['ob'];
  if (ob instanceof Array) {
    return ob.length;
  } else {
    if (ob instanceof Object) {
      return Object.keys(ob).length;
    } else {
      return __get__(__get__(ob, "__len__"), "__call__")();
    }
  }
}

len.NAME = "len";
len.args_signature = ["ob"];
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var obj = __args__['obj'];
  return __get__(__get__(obj, "next"), "__call__")();
}

next.NAME = "next";
next.args_signature = ["obj"];
next.kwargs_signature = {  };
next.types_signature = {  };
next.pythonscript_function = true;
map = function(args, kwargs) {
  var arr, v;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("func", "objs") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var func = __args__['func'];
  var objs = __args__['objs'];
  arr = [];
  var ob, __iterator__;
  __iterator__ = __get__(__get__(objs, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    ob = __next__();
    v = __get__(func, "__call__")([ob], __NULL_OBJECT__);
    arr.push(v);
  }
  return arr;
}

map.NAME = "map";
map.args_signature = ["func", "objs"];
map.kwargs_signature = {  };
map.types_signature = {  };
map.pythonscript_function = true;
filter = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("func", "objs") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var func = __args__['func'];
  var objs = __args__['objs'];
  arr = [];
  var ob, __iterator__;
  __iterator__ = __get__(__get__(objs, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    ob = __next__();
    if (__get__(func, "__call__")([ob], __NULL_OBJECT__)) {
      arr.push(ob);
    }
  }
  return arr;
}

filter.NAME = "filter";
filter.args_signature = ["func", "objs"];
filter.kwargs_signature = {  };
filter.types_signature = {  };
filter.pythonscript_function = true;
min = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("lst") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var lst = __args__['lst'];
  a = undefined;
  var value, __iterator__;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("lst") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var lst = __args__['lst'];
  a = undefined;
  var value, __iterator__;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("num") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var num = __args__['num'];
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("char") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var char = __args__['char'];
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("num") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var num = __args__['num'];
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  var index = __args__['index'];
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
__Iterator_attrs.__init__ = __Iterator___init__;
__Iterator_next = function(args, kwargs) {
  var index, length, item;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  index = self.index;
  length = len([self.obj], __NULL_OBJECT__);
  if (( index ) == length) {
    throw StopIteration;
  }
  item = __jsdict_get(self.obj, self.index);
  self.index = __add_op(self.index, 1);
  return item;
}

__Iterator_next.NAME = "__Iterator_next";
__Iterator_next.args_signature = ["self"];
__Iterator_next.kwargs_signature = {  };
__Iterator_next.types_signature = {  };
__Iterator_next.pythonscript_function = true;
__Iterator_attrs.next = __Iterator_next;
__Iterator_next_fast = function(args, kwargs) {
  var index;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  index = self.index;
  self.index += 1;
  return self.obj_get([index], __jsdict([]));
}

__Iterator_next_fast.NAME = "__Iterator_next_fast";
__Iterator_next_fast.args_signature = ["self"];
__Iterator_next_fast.kwargs_signature = {  };
__Iterator_next_fast.types_signature = {  };
__Iterator_next_fast.pythonscript_function = true;
__Iterator_attrs.next_fast = __Iterator_next_fast;
Iterator = __create_class__("Iterator", __Iterator_parents, __Iterator_attrs, __Iterator_properties);
tuple = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  if (( Object.keys(arguments).length ) == 0) {
    return [];
  } else {
    if (a instanceof Array) {
      return a.slice();
    } else {
      if (( typeof(a) ) == "string") {
        return a.split("");
      } else {
        console.log(a);
        console.log(arguments);
        throw TypeError;
      }
    }
  }
}

tuple.NAME = "tuple";
tuple.args_signature = ["a"];
tuple.kwargs_signature = {  };
tuple.types_signature = {  };
tuple.pythonscript_function = true;
var pytuple, __pytuple_attrs, __pytuple_parents;
__pytuple_attrs = Object();
__pytuple_parents = [];
__pytuple_properties = Object();
__pytuple___init__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"js_object": undefined, "pointer": undefined},args:__create_array__("self", "js_object", "pointer") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var js_object = __args__['js_object'];
  var pointer = __args__['pointer'];
  if (__test_if_true__(pointer)) {
    self["$wrapped"] = pointer;
  } else {
    arr = [];
    self["$wrapped"] = arr;
  }
  if (js_object instanceof Array) {
    var item, __iterator__;
    __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while (( __iterator__.index ) < __iterator__.length) {
      item = __next__();
      __get__(__get__(arr, "push"), "__call__")([item], __NULL_OBJECT__);
    }
  } else {
    if (__test_if_true__(js_object)) {
      if (isinstance([js_object, array], __NULL_OBJECT__) || isinstance([js_object, tuple], __NULL_OBJECT__) || isinstance([js_object, list], __NULL_OBJECT__)) {
        var v;
        __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
        ;
        __next__ = __get__(__iterator__, "next_fast");
        while (( __iterator__.index ) < __iterator__.length) {
          v = __next__();
          __get__(__get__(arr, "push"), "__call__")([v], __NULL_OBJECT__);
        }
      } else {
        throw TypeError;
      }
    }
  }
}

__pytuple___init__.NAME = "__pytuple___init__";
__pytuple___init__.args_signature = ["self", "js_object", "pointer"];
__pytuple___init__.kwargs_signature = { js_object:undefined,pointer:undefined };
__pytuple___init__.types_signature = { js_object:"None",pointer:"None" };
__pytuple___init__.pythonscript_function = true;
__pytuple_attrs.__init__ = __pytuple___init__;
__pytuple___getitem__ = function(args, kwargs) {
  ;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  if (( index ) < 0) {
    index = __add_op(__get__(self["$wrapped"], "length"), index);
  }
  return self["$wrapped"][ (index.__uid__) ? index.__uid__ : index];
}

__pytuple___getitem__.NAME = "__pytuple___getitem__";
__pytuple___getitem__.args_signature = ["self", "index"];
__pytuple___getitem__.kwargs_signature = {  };
__pytuple___getitem__.types_signature = {  };
__pytuple___getitem__.pythonscript_function = true;
__pytuple_attrs.__getitem__ = __pytuple___getitem__;
__pytuple___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__pytuple___iter__.NAME = "__pytuple___iter__";
__pytuple___iter__.args_signature = ["self"];
__pytuple___iter__.kwargs_signature = {  };
__pytuple___iter__.types_signature = {  };
__pytuple___iter__.return_type = "Iterator";
__pytuple___iter__.pythonscript_function = true;
__pytuple_attrs.__iter__ = __pytuple___iter__;
__pytuple___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"].length;
}

__pytuple___len__.NAME = "__pytuple___len__";
__pytuple___len__.args_signature = ["self"];
__pytuple___len__.kwargs_signature = {  };
__pytuple___len__.types_signature = {  };
__pytuple___len__.pythonscript_function = true;
__pytuple_attrs.__len__ = __pytuple___len__;
__pytuple_length__getprop__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"].length;
}

__pytuple_length__getprop__.NAME = "__pytuple_length__getprop__";
__pytuple_length__getprop__.args_signature = ["self"];
__pytuple_length__getprop__.kwargs_signature = {  };
__pytuple_length__getprop__.types_signature = {  };
__pytuple_length__getprop__.pythonscript_function = true;
__pytuple_index = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  return self["$wrapped"].indexOf(obj);
}

__pytuple_index.NAME = "__pytuple_index";
__pytuple_index.args_signature = ["self", "obj"];
__pytuple_index.kwargs_signature = {  };
__pytuple_index.types_signature = {  };
__pytuple_index.pythonscript_function = true;
__pytuple_attrs.index = __pytuple_index;
__pytuple_count = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  a = 0;
    var __iter16 = self["$wrapped"];
  if (! (__iter16 instanceof Array || typeof __iter16 == "string") ) { __iter16 = __object_keys__(__iter16) }
  for (var __idx16=0; __idx16 < __iter16.length; __idx16++) {
    var item = __iter16[ __idx16 ];
    if (( item ) == obj) {
      a += 1;
    }
  }
  return a;
}

__pytuple_count.NAME = "__pytuple_count";
__pytuple_count.args_signature = ["self", "obj"];
__pytuple_count.kwargs_signature = {  };
__pytuple_count.types_signature = {  };
__pytuple_count.pythonscript_function = true;
__pytuple_attrs.count = __pytuple_count;
__pytuple_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  return self["$wrapped"][ (index.__uid__) ? index.__uid__ : index];
}

__pytuple_get.NAME = "__pytuple_get";
__pytuple_get.args_signature = ["self", "index"];
__pytuple_get.kwargs_signature = {  };
__pytuple_get.types_signature = {  };
__pytuple_get.pythonscript_function = true;
__pytuple_attrs.get = __pytuple_get;
__pytuple___contains__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
  if (( self["$wrapped"].indexOf(value) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__pytuple___contains__.NAME = "__pytuple___contains__";
__pytuple___contains__.args_signature = ["self", "value"];
__pytuple___contains__.kwargs_signature = {  };
__pytuple___contains__.types_signature = {  };
__pytuple___contains__.pythonscript_function = true;
__pytuple_attrs.__contains__ = __pytuple___contains__;
__pytuple_properties["length"] = Object();
__pytuple_properties["length"]["get"] = __pytuple_length__getprop__;
pytuple = __create_class__("pytuple", __pytuple_parents, __pytuple_attrs, __pytuple_properties);
list = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  if (( Object.keys(arguments).length ) == 0) {
    return [];
  } else {
    if (a instanceof Array) {
      return a.slice();
    } else {
      if (( typeof(a) ) == "string") {
        return a.split("");
      } else {
        console.log(a);
        console.log(arguments);
        throw TypeError;
      }
    }
  }
}

list.NAME = "list";
list.args_signature = ["a"];
list.kwargs_signature = {  };
list.types_signature = {  };
list.pythonscript_function = true;
var pylist, __pylist_attrs, __pylist_parents;
__pylist_attrs = Object();
__pylist_parents = [];
__pylist_properties = Object();
__pylist___init__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"js_object": undefined, "pointer": undefined},args:__create_array__("self", "js_object", "pointer") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var js_object = __args__['js_object'];
  var pointer = __args__['pointer'];
  if (__test_if_true__(pointer)) {
    self["$wrapped"] = pointer;
  } else {
    arr = [];
    self["$wrapped"] = arr;
    if (js_object instanceof Array) {
      var item, __iterator__;
      __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
      var __next__;
      __next__ = __get__(__iterator__, "next_fast");
      while (( __iterator__.index ) < __iterator__.length) {
        item = __next__();
        __get__(__get__(arr, "push"), "__call__")([item], __NULL_OBJECT__);
      }
    } else {
      if (__test_if_true__(js_object)) {
        if (isinstance([js_object, array], __NULL_OBJECT__) || isinstance([js_object, tuple], __NULL_OBJECT__) || isinstance([js_object, list], __NULL_OBJECT__)) {
          var v;
          __iterator__ = __get__(__get__(js_object, "__iter__"), "__call__")([], Object());
          ;
          __next__ = __get__(__iterator__, "next_fast");
          while (( __iterator__.index ) < __iterator__.length) {
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

__pylist___init__.NAME = "__pylist___init__";
__pylist___init__.args_signature = ["self", "js_object", "pointer"];
__pylist___init__.kwargs_signature = { js_object:undefined,pointer:undefined };
__pylist___init__.types_signature = { js_object:"None",pointer:"None" };
__pylist___init__.pythonscript_function = true;
__pylist_attrs.__init__ = __pylist___init__;
__pylist___getitem__ = function(args, kwargs) {
  ;
  var self = args[ 0 ];
  var index = args[ 1 ];
  if (( index ) < 0) {
    index = __add_op(__get__(self["$wrapped"], "length"), index);
  }
  return self["$wrapped"][ (index.__uid__) ? index.__uid__ : index];
}

__pylist___getitem__.NAME = "__pylist___getitem__";
__pylist___getitem__.args_signature = ["self", "index"];
__pylist___getitem__.kwargs_signature = {  };
__pylist___getitem__.fastdef = true;
__pylist___getitem__.types_signature = {  };
__pylist___getitem__.pythonscript_function = true;
__pylist_attrs.__getitem__ = __pylist___getitem__;
__pylist___setitem__ = function(args, kwargs) {
  var self = args[ 0 ];
  var index = args[ 1 ];
  var value = args[ 2 ];
  self["$wrapped"][ (index.__uid__) ? index.__uid__ : index] = value;
}

__pylist___setitem__.NAME = "__pylist___setitem__";
__pylist___setitem__.args_signature = ["self", "index", "value"];
__pylist___setitem__.kwargs_signature = {  };
__pylist___setitem__.fastdef = true;
__pylist___setitem__.types_signature = {  };
__pylist___setitem__.pythonscript_function = true;
__pylist_attrs.__setitem__ = __pylist___setitem__;
__pylist___getslice__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"step": undefined},args:__create_array__("self", "start", "stop", "step") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var start = __args__['start'];
  var stop = __args__['stop'];
  var step = __args__['step'];
  arr = self["$wrapped"].__getslice__(start, stop);
  var __args_0, __kwargs_0;
  __args_0 = [];
  __kwargs_0 = {"pointer": arr};
  return __get__(list, "__call__")(__args_0, __kwargs_0);
}

__pylist___getslice__.NAME = "__pylist___getslice__";
__pylist___getslice__.args_signature = ["self", "start", "stop", "step"];
__pylist___getslice__.kwargs_signature = { step:undefined };
__pylist___getslice__.types_signature = { step:"None" };
__pylist___getslice__.return_type = "list";
__pylist___getslice__.pythonscript_function = true;
__pylist_attrs.__getslice__ = __pylist___getslice__;
__pylist_append = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  self["$wrapped"].push(obj);
}

__pylist_append.NAME = "__pylist_append";
__pylist_append.args_signature = ["self", "obj"];
__pylist_append.kwargs_signature = {  };
__pylist_append.types_signature = {  };
__pylist_append.pythonscript_function = true;
__pylist_attrs.append = __pylist_append;
__pylist_extend = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "other") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var other = __args__['other'];
  var obj, __iterator__;
  __iterator__ = __get__(__get__(other, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    obj = __next__();
    __get__(__get__(self, "append"), "__call__")([obj], __NULL_OBJECT__);
  }
}

__pylist_extend.NAME = "__pylist_extend";
__pylist_extend.args_signature = ["self", "other"];
__pylist_extend.kwargs_signature = {  };
__pylist_extend.types_signature = {  };
__pylist_extend.pythonscript_function = true;
__pylist_attrs.extend = __pylist_extend;
__pylist_insert = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  var obj = __args__['obj'];
  self["$wrapped"].splice(index, 0, obj);
}

__pylist_insert.NAME = "__pylist_insert";
__pylist_insert.args_signature = ["self", "index", "obj"];
__pylist_insert.kwargs_signature = {  };
__pylist_insert.types_signature = {  };
__pylist_insert.pythonscript_function = true;
__pylist_attrs.insert = __pylist_insert;
__pylist_remove = function(args, kwargs) {
  var index;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  index = __get__(__get__(self, "index"), "__call__")([obj], __NULL_OBJECT__);
  self["$wrapped"].splice(index, 1);
}

__pylist_remove.NAME = "__pylist_remove";
__pylist_remove.args_signature = ["self", "obj"];
__pylist_remove.kwargs_signature = {  };
__pylist_remove.types_signature = {  };
__pylist_remove.pythonscript_function = true;
__pylist_attrs.remove = __pylist_remove;
__pylist_pop = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __jsdict_pop(self["$wrapped"]);
}

__pylist_pop.NAME = "__pylist_pop";
__pylist_pop.args_signature = ["self"];
__pylist_pop.kwargs_signature = {  };
__pylist_pop.types_signature = {  };
__pylist_pop.pythonscript_function = true;
__pylist_attrs.pop = __pylist_pop;
__pylist_index = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  return self["$wrapped"].indexOf(obj);
}

__pylist_index.NAME = "__pylist_index";
__pylist_index.args_signature = ["self", "obj"];
__pylist_index.kwargs_signature = {  };
__pylist_index.types_signature = {  };
__pylist_index.pythonscript_function = true;
__pylist_attrs.index = __pylist_index;
__pylist_count = function(args, kwargs) {
  var a;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "obj") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  a = 0;
    var __iter17 = self["$wrapped"];
  if (! (__iter17 instanceof Array || typeof __iter17 == "string") ) { __iter17 = __object_keys__(__iter17) }
  for (var __idx17=0; __idx17 < __iter17.length; __idx17++) {
    var item = __iter17[ __idx17 ];
    if (( item ) == obj) {
      a += 1;
    }
  }
  return a;
}

__pylist_count.NAME = "__pylist_count";
__pylist_count.args_signature = ["self", "obj"];
__pylist_count.kwargs_signature = {  };
__pylist_count.types_signature = {  };
__pylist_count.pythonscript_function = true;
__pylist_attrs.count = __pylist_count;
__pylist_reverse = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  self["$wrapped"] = self["$wrapped"].reverse();
}

__pylist_reverse.NAME = "__pylist_reverse";
__pylist_reverse.args_signature = ["self"];
__pylist_reverse.kwargs_signature = {  };
__pylist_reverse.types_signature = {  };
__pylist_reverse.pythonscript_function = true;
__pylist_attrs.reverse = __pylist_reverse;
__pylist_shift = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"].shift();
}

__pylist_shift.NAME = "__pylist_shift";
__pylist_shift.args_signature = ["self"];
__pylist_shift.kwargs_signature = {  };
__pylist_shift.types_signature = {  };
__pylist_shift.pythonscript_function = true;
__pylist_attrs.shift = __pylist_shift;
__pylist_slice = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "start", "end") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var start = __args__['start'];
  var end = __args__['end'];
  return self["$wrapped"].slice(start, end);
}

__pylist_slice.NAME = "__pylist_slice";
__pylist_slice.args_signature = ["self", "start", "end"];
__pylist_slice.kwargs_signature = {  };
__pylist_slice.types_signature = {  };
__pylist_slice.pythonscript_function = true;
__pylist_attrs.slice = __pylist_slice;
__pylist___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__pylist___iter__.NAME = "__pylist___iter__";
__pylist___iter__.args_signature = ["self"];
__pylist___iter__.kwargs_signature = {  };
__pylist___iter__.types_signature = {  };
__pylist___iter__.return_type = "Iterator";
__pylist___iter__.pythonscript_function = true;
__pylist_attrs.__iter__ = __pylist___iter__;
__pylist_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  return self["$wrapped"][ (index.__uid__) ? index.__uid__ : index];
}

__pylist_get.NAME = "__pylist_get";
__pylist_get.args_signature = ["self", "index"];
__pylist_get.kwargs_signature = {  };
__pylist_get.types_signature = {  };
__pylist_get.pythonscript_function = true;
__pylist_attrs.get = __pylist_get;
__pylist_set = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  var value = __args__['value'];
  self["$wrapped"][ (index.__uid__) ? index.__uid__ : index] = value;
}

__pylist_set.NAME = "__pylist_set";
__pylist_set.args_signature = ["self", "index", "value"];
__pylist_set.kwargs_signature = {  };
__pylist_set.types_signature = {  };
__pylist_set.pythonscript_function = true;
__pylist_attrs.set = __pylist_set;
__pylist___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"].length;
}

__pylist___len__.NAME = "__pylist___len__";
__pylist___len__.args_signature = ["self"];
__pylist___len__.kwargs_signature = {  };
__pylist___len__.types_signature = {  };
__pylist___len__.pythonscript_function = true;
__pylist_attrs.__len__ = __pylist___len__;
__pylist_length__getprop__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"].length;
}

__pylist_length__getprop__.NAME = "__pylist_length__getprop__";
__pylist_length__getprop__.args_signature = ["self"];
__pylist_length__getprop__.kwargs_signature = {  };
__pylist_length__getprop__.types_signature = {  };
__pylist_length__getprop__.pythonscript_function = true;
__pylist___contains__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
  if (( self["$wrapped"].indexOf(value) ) == -1) {
    return false;
  } else {
    return true;
  }
}

__pylist___contains__.NAME = "__pylist___contains__";
__pylist___contains__.args_signature = ["self", "value"];
__pylist___contains__.kwargs_signature = {  };
__pylist___contains__.types_signature = {  };
__pylist___contains__.pythonscript_function = true;
__pylist_attrs.__contains__ = __pylist___contains__;
__pylist_properties["length"] = Object();
__pylist_properties["length"]["get"] = __pylist_length__getprop__;
pylist = __create_class__("pylist", __pylist_parents, __pylist_attrs, __pylist_properties);
var jsifyable, __jsifyable_attrs, __jsifyable_parents;
__jsifyable_attrs = Object();
__jsifyable_parents = [];
__jsifyable_properties = Object();
__jsifyable_jsify = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self["$wrapped"];
}

__jsifyable_jsify.NAME = "__jsifyable_jsify";
__jsifyable_jsify.args_signature = ["self"];
__jsifyable_jsify.kwargs_signature = {  };
__jsifyable_jsify.types_signature = {  };
__jsifyable_jsify.pythonscript_function = true;
__jsifyable_attrs.jsify = __jsifyable_jsify;
jsifyable = __create_class__("jsifyable", __jsifyable_parents, __jsifyable_attrs, __jsifyable_properties);
var dict, __dict_attrs, __dict_parents;
__dict_attrs = Object();
__dict_parents = [];
__dict_properties = Object();
__dict___init__ = function(args, kwargs) {
  var ob, value;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"js_object": undefined, "pointer": undefined},args:__create_array__("self", "js_object", "pointer") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var js_object = __args__['js_object'];
  var pointer = __args__['pointer'];
  self["$wrapped"] = __jsdict([]);
  if (( pointer ) !== undefined) {
    self["$wrapped"] = pointer;
  } else {
    if (__test_if_true__(js_object)) {
      ob = js_object;
      if (ob instanceof Array) {
        var o, __iterator__;
        __iterator__ = __get__(__get__(ob, "__iter__"), "__call__")([], Object());
        var __next__;
        __next__ = __get__(__iterator__, "next_fast");
        while (( __iterator__.index ) < __iterator__.length) {
          o = __next__();
          if (o instanceof Array) {
            __get__(__get__(self, "__setitem__"), "__call__")([__get__(o, "__getitem__")([0], Object()), __get__(o, "__getitem__")([1], Object())], __NULL_OBJECT__);
          } else {
            __get__(__get__(self, "__setitem__"), "__call__")([__get__(o, "__getitem__")(["key"], Object()), __get__(o, "__getitem__")(["value"], Object())], __NULL_OBJECT__);
          }
        }
      } else {
        if (isinstance([ob, dict], __NULL_OBJECT__)) {
          var key;
          __iterator__ = __get__(__get__(__jsdict_keys(ob), "__iter__"), "__call__")([], Object());
          ;
          __next__ = __get__(__iterator__, "next_fast");
          while (( __iterator__.index ) < __iterator__.length) {
            key = __next__();
            value = __get__(ob, "__getitem__")([key], Object());
            __get__(__get__(self, "__setitem__"), "__call__")([key, value], __NULL_OBJECT__);
          }
        } else {
          console.log("ERROR init dict from:", js_object);
          throw TypeError;
        }
      }
    }
  }
}

__dict___init__.NAME = "__dict___init__";
__dict___init__.args_signature = ["self", "js_object", "pointer"];
__dict___init__.kwargs_signature = { js_object:undefined,pointer:undefined };
__dict___init__.types_signature = { js_object:"None",pointer:"None" };
__dict___init__.pythonscript_function = true;
__dict_attrs.__init__ = __dict___init__;
__dict_jsify = function(args, kwargs) {
  var keys, value;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  keys = __object_keys__([self["$wrapped"]], __NULL_OBJECT__);
  var key, __iterator__;
  __iterator__ = __get__(__get__(keys, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    key = __next__();
    value = __get__(self["$wrapped"], "__getitem__")([key], Object());
    if (( typeof(value) ) == "object") {
      if (__get__(value, "jsify")) {
        __get__(__get__(self["$wrapped"], "__setitem__"), "__call__")([key, __get__(__get__(value, "jsify"), "__call__")()], Object());
      }
    }
  }
  return self["$wrapped"];
}

__dict_jsify.NAME = "__dict_jsify";
__dict_jsify.args_signature = ["self"];
__dict_jsify.kwargs_signature = {  };
__dict_jsify.types_signature = {  };
__dict_jsify.pythonscript_function = true;
__dict_attrs.jsify = __dict_jsify;
__dict_copy = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(dict, "__call__")([self], __NULL_OBJECT__);
}

__dict_copy.NAME = "__dict_copy";
__dict_copy.args_signature = ["self"];
__dict_copy.kwargs_signature = {  };
__dict_copy.types_signature = {  };
__dict_copy.return_type = "dict";
__dict_copy.pythonscript_function = true;
__dict_attrs.copy = __dict_copy;
__dict_clear = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  self["$wrapped"] = __jsdict([]);
}

__dict_clear.NAME = "__dict_clear";
__dict_clear.args_signature = ["self"];
__dict_clear.kwargs_signature = {  };
__dict_clear.types_signature = {  };
__dict_clear.pythonscript_function = true;
__dict_attrs.clear = __dict_clear;
__dict_has_key = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "key") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object' || typeof(key) === 'function') {
    key = __get__(key, "__uid__");
  }
  if (key in __dict) {
    return true;
  } else {
    return false;
  }
}

__dict_has_key.NAME = "__dict_has_key";
__dict_has_key.args_signature = ["self", "key"];
__dict_has_key.kwargs_signature = {  };
__dict_has_key.types_signature = {  };
__dict_has_key.pythonscript_function = true;
__dict_attrs.has_key = __dict_has_key;
__dict_update = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "other") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var other = __args__['other'];
  var key, __iterator__;
  __iterator__ = __get__(__get__(other, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    key = __next__();
    __get__(__get__(self, "__setitem__"), "__call__")([key, __get__(other, "__getitem__")([key], Object())], __NULL_OBJECT__);
  }
}

__dict_update.NAME = "__dict_update";
__dict_update.args_signature = ["self", "other"];
__dict_update.kwargs_signature = {  };
__dict_update.types_signature = {  };
__dict_update.pythonscript_function = true;
__dict_attrs.update = __dict_update;
__dict_items = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  arr = [];
  var key, __iterator__;
  __iterator__ = __get__(__get__(__jsdict_keys(self), "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    key = __next__();
    __get__(__get__(arr, "append"), "__call__")([[key, __get__(self, "__getitem__")([key], Object())]], __NULL_OBJECT__);
  }
  return arr;
}

__dict_items.NAME = "__dict_items";
__dict_items.args_signature = ["self"];
__dict_items.kwargs_signature = {  };
__dict_items.types_signature = {  };
__dict_items.pythonscript_function = true;
__dict_attrs.items = __dict_items;
__dict_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"_default": undefined},args:__create_array__("self", "key", "_default") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var _default = __args__['_default'];
    try {
return __get__(self, "__getitem__")([key], Object());
  } catch(__exception__) {
return _default;

}
}

__dict_get.NAME = "__dict_get";
__dict_get.args_signature = ["self", "key", "_default"];
__dict_get.kwargs_signature = { _default:undefined };
__dict_get.types_signature = { _default:"None" };
__dict_get.pythonscript_function = true;
__dict_attrs.get = __dict_get;
__dict_set = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "key", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var value = __args__['value'];
  __get__(__get__(self, "__setitem__"), "__call__")([key, value], __NULL_OBJECT__);
}

__dict_set.NAME = "__dict_set";
__dict_set.args_signature = ["self", "key", "value"];
__dict_set.kwargs_signature = {  };
__dict_set.types_signature = {  };
__dict_set.pythonscript_function = true;
__dict_attrs.set = __dict_set;
__dict___len__ = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  __dict = self["$wrapped"];
  return Object.keys(__dict).length;
}

__dict___len__.NAME = "__dict___len__";
__dict___len__.args_signature = ["self"];
__dict___len__.kwargs_signature = {  };
__dict___len__.types_signature = {  };
__dict___len__.pythonscript_function = true;
__dict_attrs.__len__ = __dict___len__;
__dict___getitem__ = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "key") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  "\n		notes:\n			. '4' and 4 are the same key\n			. it is possible that the translator mistakes a javascript-object for a dict and inlines this function,\n			  that is why below we return the key in self if __dict is undefined.\n		";
  __dict = self["$wrapped"];
  if (typeof(key) === 'object' || typeof(key) === 'function') {
    if (key.__uid__ && key.__uid__ in __dict) {
      return __dict[key.__uid__];
    }
    throw KeyError;
  }
  if (__dict && key in __dict) {
    return __dict[key];
  } else {
    if (( __dict ) === undefined && key in self) {
      return self[key];
    }
  }
  throw KeyError;
}

__dict___getitem__.NAME = "__dict___getitem__";
__dict___getitem__.args_signature = ["self", "key"];
__dict___getitem__.kwargs_signature = {  };
__dict___getitem__.types_signature = {  };
__dict___getitem__.pythonscript_function = true;
__dict_attrs.__getitem__ = __dict___getitem__;
__dict___setitem__ = function(args, kwargs) {
  var __dict;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "key", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var value = __args__['value'];
  __dict = self["$wrapped"];
  if (typeof(key) === 'object' || typeof(key) === 'function') {
    if (key.__uid__ === undefined) {
      key.__uid__ = '￼' + _PythonJS_UID++;
    }
    __dict[key.__uid__] = value;
  } else {
    __dict[key] = value;
  }
}

__dict___setitem__.NAME = "__dict___setitem__";
__dict___setitem__.args_signature = ["self", "key", "value"];
__dict___setitem__.kwargs_signature = {  };
__dict___setitem__.types_signature = {  };
__dict___setitem__.pythonscript_function = true;
__dict_attrs.__setitem__ = __dict___setitem__;
__dict_keys = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return Object.keys(self["$wrapped"]);
}

__dict_keys.NAME = "__dict_keys";
__dict_keys.args_signature = ["self"];
__dict_keys.kwargs_signature = {  };
__dict_keys.types_signature = {  };
__dict_keys.pythonscript_function = true;
__dict_attrs.keys = __dict_keys;
__dict_pop = function(args, kwargs) {
  var js_object, v;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"d": undefined},args:__create_array__("self", "key", "d") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var d = __args__['d'];
  v = __jsdict_get(self, key, undefined);
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
__dict_attrs.pop = __dict_pop;
__dict_values = function(args, kwargs) {
  var keys, out;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  keys = Object.keys(self["$wrapped"]);
  out = [];
    var __iter18 = keys;
  if (! (__iter18 instanceof Array || typeof __iter18 == "string") ) { __iter18 = __object_keys__(__iter18) }
  for (var __idx18=0; __idx18 < __iter18.length; __idx18++) {
    var key = __iter18[ __idx18 ];
    out.push(self["$wrapped"][ (key.__uid__) ? key.__uid__ : key]);
  }
  return out;
}

__dict_values.NAME = "__dict_values";
__dict_values.args_signature = ["self"];
__dict_values.kwargs_signature = {  };
__dict_values.types_signature = {  };
__dict_values.pythonscript_function = true;
__dict_attrs.values = __dict_values;
__dict___contains__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
    try {
__dict___getitem__([self, value], Object());
return true;
  } catch(__exception__) {
return false;

}
}

__dict___contains__.NAME = "__dict___contains__";
__dict___contains__.args_signature = ["self", "value"];
__dict___contains__.kwargs_signature = {  };
__dict___contains__.types_signature = {  };
__dict___contains__.pythonscript_function = true;
__dict_attrs.__contains__ = __dict___contains__;
__dict___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([__jsdict_keys(self), 0], __NULL_OBJECT__);
}

__dict___iter__.NAME = "__dict___iter__";
__dict___iter__.args_signature = ["self"];
__dict___iter__.kwargs_signature = {  };
__dict___iter__.types_signature = {  };
__dict___iter__.return_type = "Iterator";
__dict___iter__.pythonscript_function = true;
__dict_attrs.__iter__ = __dict___iter__;
dict = __create_class__("dict", __dict_parents, __dict_attrs, __dict_properties);
set = function(args, kwargs) {
  var keys, mask, s, hashtable, key, fallback;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  "\n	This returns an array that is a minimal implementation of set.\n	Often sets are used simply to remove duplicate entries from a list, \n	and then it get converted back to a list, it is safe to use fastset for this.\n\n	The array prototype is overloaded with basic set functions:\n		difference\n		intersection\n		issubset\n\n	Note: sets in Python are not subscriptable, but can be iterated over.\n\n	Python docs say that set are unordered, some programs may rely on this disorder\n	for randomness, for sets of integers we emulate the unorder only uppon initalization \n	of the set, by masking the value by bits-1. Python implements sets starting with an \n	array of length 8, and mask of 7, if set length grows to 6 (3/4th), then it allocates \n	a new array of length 32 and mask of 31.  This is only emulated for arrays of \n	integers up to an array length of 1536.\n\n	";
  if (isinstance(a, list)) {
    a = a["$wrapped"];
  }
  hashtable = null;
  if (( a.length ) <= 1536) {
    hashtable = __jsdict([]);
    keys = [];
    if (( a.length ) < 6) {
      mask = 7;
    } else {
      if (( a.length ) < 22) {
        mask = 31;
      } else {
        if (( a.length ) < 86) {
          mask = 127;
        } else {
          if (( a.length ) < 342) {
            mask = 511;
          } else {
            mask = 2047;
          }
        }
      }
    }
  }
  fallback = false;
  if (__test_if_true__(hashtable)) {
        var __iter19 = a;
    if (! (__iter19 instanceof Array || typeof __iter19 == "string") ) { __iter19 = __object_keys__(__iter19) }
    for (var __idx19=0; __idx19 < __iter19.length; __idx19++) {
      var b = __iter19[ __idx19 ];
      if (typeof(b, "number") && ( b ) === ( (b | 0) )) {
        key = (b & mask);
        hashtable[ (key.__uid__) ? key.__uid__ : key] = b;
        keys.push(key);
      } else {
        fallback = true;
        break;
      }
    }
  } else {
    fallback = true;
  }
  s = [];
  if (__test_if_true__(fallback)) {
        var __iter20 = a;
    if (! (__iter20 instanceof Array || typeof __iter20 == "string") ) { __iter20 = __object_keys__(__iter20) }
    for (var __idx20=0; __idx20 < __iter20.length; __idx20++) {
      var item = __iter20[ __idx20 ];
      if (( s.indexOf(item) ) == -1) {
        s.push(item);
      }
    }
  } else {
    keys.sort();
        var __iter21 = keys;
    if (! (__iter21 instanceof Array || typeof __iter21 == "string") ) { __iter21 = __object_keys__(__iter21) }
    for (var __idx21=0; __idx21 < __iter21.length; __idx21++) {
      var key = __iter21[ __idx21 ];
      s.push(hashtable[ (key.__uid__) ? key.__uid__ : key]);
    }
  }
  return s;
}

set.NAME = "set";
set.args_signature = ["a"];
set.kwargs_signature = {  };
set.types_signature = {  };
set.pythonscript_function = true;
frozenset = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("a") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var a = __args__['a'];
  return set([a], __NULL_OBJECT__);
}

frozenset.NAME = "frozenset";
frozenset.args_signature = ["a"];
frozenset.kwargs_signature = {  };
frozenset.types_signature = {  };
frozenset.pythonscript_function = true;
var array, __array_attrs, __array_parents;
__array_attrs = Object();
__array_parents = [];
__array_properties = Object();
__array_typecodes = __jsdict([["c", 1], ["b", 1], ["B", 1], ["u", 2], ["h", 2], ["H", 2], ["i", 4], ["I", 4], ["l", 4], ["L", 4], ["f", 4], ["d", 8], ["float32", 4], ["float16", 2], ["float8", 1], ["int32", 4], ["uint32", 4], ["int16", 2], ["uint16", 2], ["int8", 1], ["uint8", 1]]);
__array_attrs.typecodes = __array_typecodes;
__array_typecode_names = __jsdict([["c", "Int8"], ["b", "Int8"], ["B", "Uint8"], ["u", "Uint16"], ["h", "Int16"], ["H", "Uint16"], ["i", "Int32"], ["I", "Uint32"], ["f", "Float32"], ["d", "Float64"], ["float32", "Float32"], ["float16", "Int16"], ["float8", "Int8"], ["int32", "Int32"], ["uint32", "Uint32"], ["int16", "Int16"], ["uint16", "Uint16"], ["int8", "Int8"], ["uint8", "Uint8"]]);
__array_attrs.typecode_names = __array_typecode_names;
__array___init__ = function(args, kwargs) {
  var size, buff;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:{"initializer": undefined, "little_endian": false},args:__create_array__("self", "typecode", "initializer", "little_endian") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var typecode = __args__['typecode'];
  var initializer = __args__['initializer'];
  var little_endian = __args__['little_endian'];
  self.typecode = typecode;
  self.itemsize = __get__(__get__(self, "typecodes"), "__getitem__")([typecode], Object());
  self.little_endian = little_endian;
  if (__test_if_true__(initializer)) {
    self.length = len([initializer], __NULL_OBJECT__);
    self.bytes = (self.length * self.itemsize);
    if (( self.typecode ) == "float8") {
      self._scale = max([[abs([min([initializer], __NULL_OBJECT__)], __NULL_OBJECT__), max([initializer], __NULL_OBJECT__)]], __NULL_OBJECT__);
      self._norm_get = (self._scale / 127);
      self._norm_set = (1.0 / self._norm_get);
    } else {
      if (( self.typecode ) == "float16") {
        self._scale = max([[abs([min([initializer], __NULL_OBJECT__)], __NULL_OBJECT__), max([initializer], __NULL_OBJECT__)]], __NULL_OBJECT__);
        self._norm_get = (self._scale / 32767);
        self._norm_set = (1.0 / self._norm_get);
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
__array_attrs.__init__ = __array___init__;
__array___len__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return self.length;
}

__array___len__.NAME = "__array___len__";
__array___len__.args_signature = ["self"];
__array___len__.kwargs_signature = {  };
__array___len__.types_signature = {  };
__array___len__.pythonscript_function = true;
__array_attrs.__len__ = __array___len__;
__array___contains__ = function(args, kwargs) {
  var arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
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
__array_attrs.__contains__ = __array___contains__;
__array___getitem__ = function(args, kwargs) {
  var func_name, dataview, value, step, func, offset;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  step = self.itemsize;
  offset = (step * index);
  dataview = self.dataview;
  func_name = __add_op("get", __get__(__get__(self, "typecode_names"), "__getitem__")([self.typecode], Object()));
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    value = func(offset);
    if (( self.typecode ) == "float8") {
      value = (value * self._norm_get);
    } else {
      if (( self.typecode ) == "float16") {
        value = (value * self._norm_get);
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
__array_attrs.__getitem__ = __array___getitem__;
__array___setitem__ = function(args, kwargs) {
  var func_name, dataview, step, func, offset;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  var value = __args__['value'];
  step = self.itemsize;
  if (( index ) < 0) {
    index = (__add_op(self.length, index) - 1);
  }
  offset = (step * index);
  dataview = self.dataview;
  func_name = __add_op("set", __get__(__get__(self, "typecode_names"), "__getitem__")([self.typecode], Object()));
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    if (( self.typecode ) == "float8") {
      value = (value * self._norm_set);
    } else {
      if (( self.typecode ) == "float16") {
        value = (value * self._norm_set);
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
__array_attrs.__setitem__ = __array___setitem__;
__array___iter__ = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
}

__array___iter__.NAME = "__array___iter__";
__array___iter__.args_signature = ["self"];
__array___iter__.kwargs_signature = {  };
__array___iter__.types_signature = {  };
__array___iter__.return_type = "Iterator";
__array___iter__.pythonscript_function = true;
__array_attrs.__iter__ = __array___iter__;
__array_get = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "index") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  return __array___getitem__([self, index], Object());
}

__array_get.NAME = "__array_get";
__array_get.args_signature = ["self", "index"];
__array_get.kwargs_signature = {  };
__array_get.types_signature = {  };
__array_get.pythonscript_function = true;
__array_attrs.get = __array_get;
__array_fromlist = function(args, kwargs) {
  var typecode, i, func_name, dataview, length, item, step, func, offset, size;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "lst") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var lst = __args__['lst'];
  length = len([lst], __NULL_OBJECT__);
  step = self.itemsize;
  typecode = self.typecode;
  size = (length * step);
  dataview = self.dataview;
  func_name = __add_op("set", __get__(__get__(self, "typecode_names"), "__getitem__")([typecode], Object()));
  func = dataview[func_name].bind(dataview);
  if (( size ) <= self.bytes) {
    i = 0;
    offset = 0;
    while (( i ) < length) {
      item = __get__(lst, "__getitem__")([i], Object());
      if (( typecode ) == "float8") {
        item *= self._norm_set;
      } else {
        if (( typecode ) == "float16") {
          item *= self._norm_set;
        }
      }
      func(offset,item);
      offset += step;
      i += 1;
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
__array_attrs.fromlist = __array_fromlist;
__array_resize = function(args, kwargs) {
  var source, new_buff, target, new_size, buff;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "length") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var length = __args__['length'];
  buff = self.buffer;
  source = new Uint8Array(buff);
  new_size = (length * self.itemsize);
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
__array_attrs.resize = __array_resize;
__array_append = function(args, kwargs) {
  var length;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "value") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
  length = self.length;
  __get__(__get__(self, "resize"), "__call__")([__add_op(self.length, 1)], __NULL_OBJECT__);
  __get__(__get__(self, "__setitem__"), "__call__")([length, value], Object());
}

__array_append.NAME = "__array_append";
__array_append.args_signature = ["self", "value"];
__array_append.kwargs_signature = {  };
__array_append.types_signature = {  };
__array_append.pythonscript_function = true;
__array_attrs.append = __array_append;
__array_extend = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self", "lst") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  var lst = __args__['lst'];
  var value, __iterator__;
  __iterator__ = __get__(__get__(lst, "__iter__"), "__call__")([], Object());
  var __next__;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    value = __next__();
    __get__(__get__(self, "append"), "__call__")([value], __NULL_OBJECT__);
  }
}

__array_extend.NAME = "__array_extend";
__array_extend.args_signature = ["self", "lst"];
__array_extend.kwargs_signature = {  };
__array_extend.types_signature = {  };
__array_extend.pythonscript_function = true;
__array_attrs.extend = __array_extend;
__array_to_array = function(args, kwargs) {
  var i, item, arr;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  arr = [];
  i = 0;
  while (( i ) < self.length) {
    item = __array___getitem__([self, i], Object());
    arr.push( item );
    i += 1;
  }
  return arr;
}

__array_to_array.NAME = "__array_to_array";
__array_to_array.args_signature = ["self"];
__array_to_array.kwargs_signature = {  };
__array_to_array.types_signature = {  };
__array_to_array.pythonscript_function = true;
__array_attrs.to_array = __array_to_array;
__array_to_list = function(args, kwargs) {
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(__get__(self, "to_array"), "__call__")();
}

__array_to_list.NAME = "__array_to_list";
__array_to_list.args_signature = ["self"];
__array_to_list.kwargs_signature = {  };
__array_to_list.types_signature = {  };
__array_to_list.pythonscript_function = true;
__array_attrs.to_list = __array_to_list;
__array_to_ascii = function(args, kwargs) {
  var i, length, arr, string;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("self") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var self = __args__['self'];
  string = "";
  arr = __get__(__get__(self, "to_array"), "__call__")();
  i = 0;
  length = __get__(arr, "length");
  while (( i ) < length) {
    var num = arr[i];
    var char = String.fromCharCode(num);
    string += char;
    i += 1;
  }
  return string;
}

__array_to_ascii.NAME = "__array_to_ascii";
__array_to_ascii.args_signature = ["self"];
__array_to_ascii.kwargs_signature = {  };
__array_to_ascii.types_signature = {  };
__array_to_ascii.pythonscript_function = true;
__array_attrs.to_ascii = __array_to_ascii;
array = __create_class__("array", __array_parents, __array_attrs, __array_properties);
json = __jsdict([["loads", (function (s) {return JSON.parse(s)})], ["dumps", (function (o) {return JSON.stringify(o)})]]);
_to_pythonjs = function(args, kwargs) {
  var set, keys, raw, jstype, output, append;
  if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && ( arguments.length ) == 2) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments);
    kwargs = Object();
  }
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("json") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var json = __args__['json'];
  var item;
  jstype = typeof json;
  if (( jstype ) == "number") {
    return json;
  }
  if (( jstype ) == "string") {
    return json;
  }
  if (Object.prototype.toString.call(json) === '[object Array]') {
    output = __get__(list, "__call__")();
    var __args_1, __kwargs_1;
    __args_1 = [];
    __kwargs_1 = {"js_object": json};
    raw = __get__(list, "__call__")(__args_1, __kwargs_1);
    ;
    append = __get__(output, "append");
    var __iterator__;
    __iterator__ = __get__(__get__(raw, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while (( __iterator__.index ) < __iterator__.length) {
      item = __next__();
      __get__(append, "__call__")([_to_pythonjs([item], __NULL_OBJECT__)], __NULL_OBJECT__);
    }
    return output;
  }
  output = __get__(dict, "__call__")();
  ;
  set = __get__(output, "set");
  var __args_2, __kwargs_2;
  __args_2 = [];
  __kwargs_2 = {"js_object": Object.keys(json)};
  keys = __get__(list, "__call__")(__args_2, __kwargs_2);
  var key;
  __iterator__ = __get__(__get__(keys, "__iter__"), "__call__")([], Object());
  ;
  __next__ = __get__(__iterator__, "next_fast");
  while (( __iterator__.index ) < __iterator__.length) {
    key = __next__();
    set([key, _to_pythonjs([json[key]], __NULL_OBJECT__)], __NULL_OBJECT__);
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("json") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var json = __args__['json'];
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("pythonjs") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var pythonjs = __args__['pythonjs'];
  if (isinstance([pythonjs, list], __NULL_OBJECT__)) {
    r = [];
    var i, __iterator__;
    __iterator__ = __get__(__get__(pythonjs, "__iter__"), "__call__")([], Object());
    var __next__;
    __next__ = __get__(__iterator__, "next_fast");
    while (( __iterator__.index ) < __iterator__.length) {
      i = __next__();
      __get__(__get__(r, "push"), "__call__")([_to_json([i], __NULL_OBJECT__)], __NULL_OBJECT__);
    }
  } else {
    if (isinstance([pythonjs, dict], __NULL_OBJECT__)) {
      ;
      r = Object();
      ;
      __iterator__ = __get__(__get__(__jsdict_keys(pythonjs), "__iter__"), "__call__")([], Object());
      ;
      __next__ = __get__(__iterator__, "next_fast");
      while (( __iterator__.index ) < __iterator__.length) {
        key = __next__();
        value = _to_json([__jsdict_get(pythonjs, key)], __NULL_OBJECT__);
        key = _to_json([key], __NULL_OBJECT__);
        r[ (key.__uid__) ? key.__uid__ : key] = value;
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
  var __sig__, __args__;
  __sig__ = { kwargs:Object(),args:__create_array__("pythonjs") };
  __args__ = get_arguments(__sig__, args, kwargs);
  var pythonjs = __args__['pythonjs'];
  return __get__(__get__(JSON, "stringify"), "__call__")([_to_json([pythonjs], __NULL_OBJECT__)], __NULL_OBJECT__);
}

pythonjs_to_json.NAME = "pythonjs_to_json";
pythonjs_to_json.args_signature = ["pythonjs"];
pythonjs_to_json.kwargs_signature = {  };
pythonjs_to_json.types_signature = {  };
pythonjs_to_json.pythonscript_function = true;