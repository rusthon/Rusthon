__NULL_OBJECT__ = Object.create(null);
__WEBWORKER__ = false;
__NODEJS__ = false;
__BROWSER__ = false;
if ((!(typeof(process) instanceof Array ? JSON.stringify(typeof(process))==JSON.stringify("undefined") : typeof(process)==="undefined"))) {
  __NODEJS__ = true;
}
if ((!(typeof(window) instanceof Array ? JSON.stringify(typeof(window))==JSON.stringify("undefined") : typeof(window)==="undefined"))) {
  __BROWSER__ = true;
}
if ((typeof(importScripts) instanceof Array ? JSON.stringify(typeof(importScripts))==JSON.stringify("function") : typeof(importScripts)==="function")) {
  __WEBWORKER__ = true;
}
var __create_array__ = function() {
  "Used to fix a bug/feature of Javascript where new Array(number)\n	created a array with number of undefined elements which is not\n	what we want";
  var i,array;
  array = [];
  i = 0;
  while (( i ) < arguments.length) {
    array.push(arguments[i]);
    i += 1;
  }
  return array;
}

var __get__ = function(object, attribute, error_message) {
  "Retrieve an attribute, method, property, or wrapper function.\n\n	method are actually functions which are converted to methods by\n	prepending their arguments with the current object. Properties are\n	not functions!\n\n	DOM support:\n		http://stackoverflow.com/questions/14202699/document-createelement-not-working\n		https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof\n\n	Direct JavaScript Calls:\n		if an external javascript function is found, and it was not a wrapper that was generated here,\n		check the function for a 'cached_wrapper' attribute, if none is found then generate a new\n		wrapper, cache it on the function, and return the wrapper.\n	";
  if (( object ) === null) {
    if (error_message) {
      throw new AttributeError(("(`null` has no attributes) " + error_message));
    } else {
      throw new AttributeError(("null object (None) has no attribute: " + attribute));
    }
  } else {
    if (( object ) === undefined) {
      if (error_message) {
        throw new AttributeError(("(`undefined` has no attributes) " + error_message));
      } else {
        throw new AttributeError(("undefined has no attribute: " + attribute));
      }
    }
  }
  if ((attribute instanceof Array ? JSON.stringify(attribute)==JSON.stringify("__call__") : attribute==="__call__")) {
    if ((object.pythonscript_function || object.is_wrapper)) {
      return object;
    } else {
      if (object.cached_wrapper) {
        return object.cached_wrapper;
      } else {
        if ({}.toString.call(object) === '[object Function]') {
                              var wrapper = function(args, kwargs) {
            var i,arg,keys;
            if ((!(args instanceof Array ? JSON.stringify(args)==JSON.stringify(null) : args===null))) {
              i = 0;
              while (( i ) < args.length) {
                arg = args[i];
                if ((arg && (typeof(arg) instanceof Array ? JSON.stringify(typeof(arg))==JSON.stringify("object") : typeof(arg)==="object"))) {
                  if (arg.jsify) {
                    args[i] = arg.jsify();
                  }
                }
                i += 1;
              }
            }
            if ((!(kwargs instanceof Array ? JSON.stringify(kwargs)==JSON.stringify(null) : kwargs===null))) {
              keys = __object_keys__(kwargs);
              if ((!(keys.length instanceof Array ? JSON.stringify(keys.length)==JSON.stringify(0) : keys.length===0))) {
                args.push(kwargs);
                i = 0;
                while (( i ) < keys.length) {
                  arg = kwargs[keys[i]];
                  if ((arg && (typeof(arg) instanceof Array ? JSON.stringify(typeof(arg))==JSON.stringify("object") : typeof(arg)==="object"))) {
                    if (arg.jsify) {
                      kwargs[keys[i]] = arg.jsify();
                    }
                  }
                  i += 1;
                }
              }
            }
            return object.apply(null, args);
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
  if ((( __NODEJS__ ) === false && ( __WEBWORKER__ ) === false)) {
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
    if ((typeof(attr) instanceof Array ? JSON.stringify(typeof(attr))==JSON.stringify("function") : typeof(attr)==="function")) {
      if (attr.pythonscript_function === undefined && attr.is_wrapper === undefined) {
        if ((attr.prototype instanceof Object && ( Object.keys(attr.prototype).length ) > 0)) {
          return attr;
        }
                        var wrapper = function(args, kwargs) {
          var i,arg,keys;
          if ((!(args instanceof Array ? JSON.stringify(args)==JSON.stringify(null) : args===null))) {
            i = 0;
            while (( i ) < args.length) {
              arg = args[i];
              if ((arg && (typeof(arg) instanceof Array ? JSON.stringify(typeof(arg))==JSON.stringify("object") : typeof(arg)==="object"))) {
                if (arg.jsify) {
                  args[i] = arg.jsify();
                }
              }
              i += 1;
            }
          }
          if ((!(kwargs instanceof Array ? JSON.stringify(kwargs)==JSON.stringify(null) : kwargs===null))) {
            keys = __object_keys__(kwargs);
            if ((!(keys.length instanceof Array ? JSON.stringify(keys.length)==JSON.stringify(0) : keys.length===0))) {
              args.push(kwargs);
              i = 0;
              while (( i ) < keys.length) {
                arg = kwargs[keys[i]];
                if ((arg && (typeof(arg) instanceof Array ? JSON.stringify(typeof(arg))==JSON.stringify("object") : typeof(arg)==="object"))) {
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
        wrapper.wrapped = attr;
        return wrapper;
      } else {
        if (attr.is_classmethod) {
                              var method = function() {
            var args;
            args = Array.prototype.slice.call(arguments);
            if ((args[0] instanceof Array && {}.toString.call(args[1]) === '[object Object]' && (args.length instanceof Array ? JSON.stringify(args.length)==JSON.stringify(2) : args.length===2))) {
              /*pass*/
            } else {
              args = [args, {}];
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
  var __class__,bases;
  __class__ = object.__class__;
  if (__class__) {
    if (( attribute )  in  __class__.__properties__) {
      return __class__.__properties__[attribute]["get"]([object], {});
    }
    if (( attribute )  in  __class__.__unbound_methods__) {
      attr = __class__.__unbound_methods__[attribute];
      if (attr.fastdef) {
                        var method = function(args, kwargs) {
          if ((arguments && arguments[0])) {
            arguments[0].splice(0, 0, object);
            return attr.apply(this, arguments);
          } else {
            return attr([object], {  });
          }
        }

      } else {
                        var method = function(args, kwargs) {
          if ((arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(0) : arguments.length===0)) {
            return attr([object], __NULL_OBJECT__);
          } else {
            if ((args instanceof Array && ( typeof(kwargs) ) === "object" && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
              args.splice(0, 0, object);
              if (( kwargs ) === undefined) {
                return attr(args, __NULL_OBJECT__);
              } else {
                return attr(args, kwargs);
              }
            } else {
              args = Array.prototype.slice.call(arguments);
              args.splice(0, 0, object);
              args = [args, __NULL_OBJECT__];
              return attr.apply(this, args);
            }
          }
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
              if ((arguments && arguments[0])) {
                arguments[0].splice(0, 0, object);
                return attr.apply(this, arguments);
              } else {
                return attr([object], {  });
              }
            }

          } else {
                                    var method = function(args, kwargs) {
              if ((arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(0) : arguments.length===0)) {
                return attr([object], __NULL_OBJECT__);
              } else {
                if ((args instanceof Array && ( typeof(kwargs) ) === "object" && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
                  args.splice(0, 0, object);
                  if (( kwargs ) === undefined) {
                    return attr(args, __NULL_OBJECT__);
                  } else {
                    return attr(args, kwargs);
                  }
                } else {
                  args = Array.prototype.slice.call(arguments);
                  args.splice(0, 0, object);
                  args = [args, __NULL_OBJECT__];
                  return attr.apply(this, args);
                }
              }
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
        var __iter1 = bases;
    if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
    for (var __idx1=0; __idx1 < __iter1.length; __idx1++) {
      var base = __iter1[ __idx1 ];
      attr = _get_upstream_attribute(base, attribute);
      if (( attr ) !== undefined) {
        if ({}.toString.call(attr) === '[object Function]') {
          if (attr.fastdef) {
                                    var method = function(args, kwargs) {
              if ((arguments && arguments[0])) {
                arguments[0].splice(0, 0, object);
                return attr.apply(this, arguments);
              } else {
                return attr([object], {  });
              }
            }

          } else {
                                    var method = function(args, kwargs) {
              if ((arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(0) : arguments.length===0)) {
                return attr([object], __NULL_OBJECT__);
              } else {
                if ((args instanceof Array && ( typeof(kwargs) ) === "object" && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
                  args.splice(0, 0, object);
                  if (( kwargs ) === undefined) {
                    return attr(args, __NULL_OBJECT__);
                  } else {
                    return attr(args, kwargs);
                  }
                } else {
                  args = Array.prototype.slice.call(arguments);
                  args.splice(0, 0, object);
                  args = [args, __NULL_OBJECT__];
                  return attr.apply(this, args);
                }
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
    }
        var __iter2 = bases;
    if (! (__iter2 instanceof Array || typeof __iter2 == "string" || __is_typed_array(__iter2) || __is_some_array(__iter2) )) { __iter2 = __object_keys__(__iter2) }
    for (var __idx2=0; __idx2 < __iter2.length; __idx2++) {
      var base = __iter2[ __idx2 ];
      var prop;
      prop = _get_upstream_property(base, attribute);
      if (( prop ) !== undefined) {
        return prop["get"]([object], {});
      }
    }
    if (( "__getattr__" )  in  __class__) {
      return __class__["__getattr__"]([object, attribute], {});
    }
        var __iter3 = bases;
    if (! (__iter3 instanceof Array || typeof __iter3 == "string" || __is_typed_array(__iter3) || __is_some_array(__iter3) )) { __iter3 = __object_keys__(__iter3) }
    for (var __idx3=0; __idx3 < __iter3.length; __idx3++) {
      var base = __iter3[ __idx3 ];
      var f;
      f = _get_upstream_attribute(base, "__getattr__");
      if (( f ) !== undefined) {
        return f([object, attribute], {});
      }
    }
  }
  if ((attribute instanceof Array ? JSON.stringify(attribute)==JSON.stringify("__getitem__") : attribute==="__getitem__")) {
            var wrapper = function(args, kwargs) {
      v = object[args[0]];
      if (( v ) === undefined) {
        throw new KeyError(args[0]);
      }
    }

    wrapper.is_wrapper = true;
    return wrapper;
  } else {
    if ((attribute instanceof Array ? JSON.stringify(attribute)==JSON.stringify("__setitem__") : attribute==="__setitem__")) {
                  var wrapper = function(args, kwargs) {
        object[args[0]] = args[1];
      }

      wrapper.is_wrapper = true;
      return wrapper;
    }
  }
  if ((typeof(object, "function") && object.is_wrapper)) {
    return object.wrapped[attribute];
  }
  if (((attribute instanceof Array ? JSON.stringify(attribute)==JSON.stringify("__iter__") : attribute==="__iter__") && object instanceof Object)) {
            var wrapper = function(args, kwargs) {
      return  new __ArrayIterator(Object.keys(object), 0);
    }

    wrapper.is_wrapper = true;
    return wrapper;
  }
  if (((attribute instanceof Array ? JSON.stringify(attribute)==JSON.stringify("__contains__") : attribute==="__contains__") && object instanceof Object)) {
            var wrapper = function(args, kwargs) {
      return (!(Object.keys(object).indexOf(args[0]) instanceof Array ? JSON.stringify(Object.keys(object).indexOf(args[0]))==JSON.stringify(-1) : Object.keys(object).indexOf(args[0])===-1));
    }

    wrapper.is_wrapper = true;
    return wrapper;
  }
  if (( attr ) === undefined) {
    if (error_message) {
      throw new AttributeError(error_message);
    } else {
      throw new AttributeError(attribute);
    }
  } else {
    return attr;
  }
}

var _get_upstream_attribute = function(base, attr) {
  if (( attr )  in  base) {
    return base[attr];
  }
    var __iter4 = base.__bases__;
  if (! (__iter4 instanceof Array || typeof __iter4 == "string" || __is_typed_array(__iter4) || __is_some_array(__iter4) )) { __iter4 = __object_keys__(__iter4) }
  for (var __idx4=0; __idx4 < __iter4.length; __idx4++) {
    var parent = __iter4[ __idx4 ];
    return _get_upstream_attribute(parent, attr);
  }
}

var _get_upstream_property = function(base, attr) {
  if (( attr )  in  base.__properties__) {
    return base.__properties__[attr];
  }
    var __iter5 = base.__bases__;
  if (! (__iter5 instanceof Array || typeof __iter5 == "string" || __is_typed_array(__iter5) || __is_some_array(__iter5) )) { __iter5 = __object_keys__(__iter5) }
  for (var __idx5=0; __idx5 < __iter5.length; __idx5++) {
    var parent = __iter5[ __idx5 ];
    return _get_upstream_property(parent, attr);
  }
}

var __set__ = function(object, attribute, value) {
  "\n	__setattr__ is always called when an attribute is set,\n	unlike __getattr__ that only triggers when an attribute is not found,\n	this asymmetry is in fact part of the Python spec.\n	note there is no __setattribute__\n\n	In normal Python a property setter is not called before __setattr__,\n	this is bad language design because the user has been more explicit\n	in having the property setter.\n\n	In PythonJS, property setters are called instead of __setattr__.\n	";
  if ((( "__class__" )  in  object && (!(object.__class__.__setters__.indexOf(attribute) instanceof Array ? JSON.stringify(object.__class__.__setters__.indexOf(attribute))==JSON.stringify(-1) : object.__class__.__setters__.indexOf(attribute)===-1)))) {
    object[attribute] = value;
  } else {
    if (( "__setattr__" )  in  object) {
      object.__setattr__(attribute, value);
    } else {
      object[attribute] = value;
    }
  }
}

var __getargs__ = function(func_name, signature, args, kwargs) {
  "Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve\n	the actual parameters.\n\n	This will set default keyword arguments and retrieve positional arguments\n	in kwargs if their called as such";
  if (( args ) === null) {
    args = [];
  }
  if (( kwargs ) === null) {
    kwargs = {  };
  }
  out = {  };
  if (( args.length ) > signature.args.length) {
    if (signature.vararg) {
      /*pass*/
    } else {
      console.log(("Error in function->" + func_name));
      console.log("args:", args, "kwargs:", kwargs, "sig:", signature);
      throw new TypeError("Supplemental positional arguments provided but signature doesn't accept them");
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
IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";
KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";
ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";
AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";
RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";
var __getfast__ = function(ob, attr) {
  var v;
  v = ob[attr];
  if (( v ) === undefined) {
    throw new AttributeError(attr);
  } else {
    return v;
  }
}

var __wrap_function__ = function(f) {
  
  f.is_wrapper = true;
  return f;
}

var __gpu_object = function(cls, struct_name, data_name) {
  
  cls.prototype.__struct_name__ = struct_name;
  cls.prototype.__struct_data__ = data_name;
}

gpu = { "object":__gpu_object };
var glsljit_runtime = function(header) {
  
  return  new GLSLJITRuntime(header);
}

var GLSLJITRuntime = function(header) {
  GLSLJITRuntime.__init__(this, header);
  this.__class__ = GLSLJITRuntime;
  this.__uid__ = ("￼" + _PythonJS_UID);
  _PythonJS_UID += 1;
}

GLSLJITRuntime.__uid__ = ("￼" + _PythonJS_UID);
_PythonJS_UID += 1;
GLSLJITRuntime.prototype.__init__ = function(header) {
  
  this.header = header;
  this.shader = [];
  this.object_packagers = [];
  this.struct_types = __jsdict([]);
  this.glsltypes = ["vec2", "vec3", "vec4", "mat4"];
  this.matrices = [];
}

GLSLJITRuntime.__init__ = function () { return GLSLJITRuntime.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.compile_header = function() {
  var a,b;
  a = [];
    var __iter1 = this.struct_types;
  if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
  for (var __idx1=0; __idx1 < __iter1.length; __idx1++) {
    var sname = __iter1[ __idx1 ];
    if (__contains__(this.glsltypes, sname)) {
      /*pass*/
    } else {
      a.push(this.struct_types[sname]["code"]);
    }
  }
  a.push(__sprintf("int matrix_index() { return int(get_global_id().y*%s.0); }", this.matrices.length));
  a.push("int matrix_row() { return int(get_global_id().x*4.0); }");
  a = "\n".join(a);
  b = "\n".join(this.header);
  return "\n".join([a, b]);
}

GLSLJITRuntime.compile_header = function () { return GLSLJITRuntime.prototype.compile_header.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.compile_main = function() {
  
  return "\n".join(this.shader);
}

GLSLJITRuntime.compile_main = function () { return GLSLJITRuntime.prototype.compile_main.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.push = function(s) {
  
  this.shader.push(s);
}

GLSLJITRuntime.push = function () { return GLSLJITRuntime.prototype.push.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.define_structure = function(ob) {
  var integers,arr,code,struct_name,struct_type,member_list,subtype,t,members,arrays,structs,floats;
  struct_name = null;
  if (__test_if_true__(ob.__struct_name__)) {
    struct_name = ob.__struct_name__;
    if (__contains__(this.struct_types, struct_name)) {
      return struct_name;
    }
  }
  arrays = [];
  floats = [];
  integers = [];
  structs = [];
  struct_type = [];
  if (__test_if_true__((struct_name && __contains__(this.glsltypes, struct_name)))) {
    return struct_name;
  }
    var __iter2 = dir(ob);
  if (! (__iter2 instanceof Array || typeof __iter2 == "string" || __is_typed_array(__iter2) || __is_some_array(__iter2) )) { __iter2 = __object_keys__(__iter2) }
  for (var __idx2=0; __idx2 < __iter2.length; __idx2++) {
    var key = __iter2[ __idx2 ];
    if (__test_if_true__(((key.length instanceof Array ? JSON.stringify(key.length)==JSON.stringify(1) : key.length===1) && __contains__("0123456789", key)))) {
      throw new RuntimeError(key);
    }
    t = typeof(ob[key]);
    if (__test_if_true__(((t instanceof Array ? JSON.stringify(t)==JSON.stringify("object") : t==="object") && ob[key] instanceof Array && ob[key].length && (typeof(ob[key][0]) instanceof Array ? JSON.stringify(typeof(ob[key][0]))==JSON.stringify("number") : typeof(ob[key][0])==="number")))) {
      struct_type.push(("ARY_" + key));
      arrays.push(key);
    } else {
      if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("number") : t==="number")) {
        struct_type.push(("NUM_" + key));
        floats.push(key);
      } else {
        if (__test_if_true__(ob[key] instanceof Int16Array)) {
          struct_type.push(("INT_" + key));
          if ((ob[key].length instanceof Array ? JSON.stringify(ob[key].length)==JSON.stringify(1) : ob[key].length===1)) {
            integers.push(key);
          } else {
            /*pass*/
          }
        } else {
          if (__test_if_true__(((t instanceof Array ? JSON.stringify(t)==JSON.stringify("object") : t==="object") && ob[key].__struct_name__))) {
            struct_type.push(("S_" + key));
            structs.push(key);
            if (! (__contains__(this.struct_types, ob[key].__struct_name__))) {
              if (__contains__(this.glsltypes, ob[key].__struct_name__)) {
                /*pass*/
              } else {
                this.define_structure(ob[key]);
              }
            }
          }
        }
      }
    }
  }
  if (( struct_name ) === null) {
    struct_name = "".join(struct_type);
    ob.__struct_name__ = struct_name;
  }
  if (! (__contains__(this.struct_types, struct_name))) {
    member_list = [];
        var __iter3 = integers;
    if (! (__iter3 instanceof Array || typeof __iter3 == "string" || __is_typed_array(__iter3) || __is_some_array(__iter3) )) { __iter3 = __object_keys__(__iter3) }
    for (var __idx3=0; __idx3 < __iter3.length; __idx3++) {
      var key = __iter3[ __idx3 ];
      member_list.append((("int " + key) + ";"));
    }
        var __iter4 = floats;
    if (! (__iter4 instanceof Array || typeof __iter4 == "string" || __is_typed_array(__iter4) || __is_some_array(__iter4) )) { __iter4 = __object_keys__(__iter4) }
    for (var __idx4=0; __idx4 < __iter4.length; __idx4++) {
      var key = __iter4[ __idx4 ];
      member_list.append((("float " + key) + ";"));
    }
        var __iter5 = arrays;
    if (! (__iter5 instanceof Array || typeof __iter5 == "string" || __is_typed_array(__iter5) || __is_some_array(__iter5) )) { __iter5 = __object_keys__(__iter5) }
    for (var __idx5=0; __idx5 < __iter5.length; __idx5++) {
      var key = __iter5[ __idx5 ];
      arr = ob[key];
      member_list.append((((("float " + key) + "[") + arr.length) + "];"));
    }
        var __iter6 = structs;
    if (! (__iter6 instanceof Array || typeof __iter6 == "string" || __is_typed_array(__iter6) || __is_some_array(__iter6) )) { __iter6 = __object_keys__(__iter6) }
    for (var __idx6=0; __idx6 < __iter6.length; __idx6++) {
      var key = __iter6[ __idx6 ];
      subtype = ob[key].__struct_name__;
      member_list.append((((subtype + " ") + key) + ";"));
    }
    if ((len(member_list) instanceof Array ? JSON.stringify(len(member_list))==JSON.stringify(0) : len(member_list)===0)) {
      throw new RuntimeError(struct_name);
    }
    members = "".join(member_list);
    code = (((("struct " + struct_name) + " {") + members) + "};");
    this.struct_types[struct_name] = __jsdict([["arrays", arrays], ["floats", floats], ["integers", integers], ["structs", structs], ["code", code]]);
  }
  return struct_name;
}

GLSLJITRuntime.define_structure = function () { return GLSLJITRuntime.prototype.define_structure.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.structure = function(ob, name) {
  var sname,stype,args,value,has_arrays,o,aname,wrapper;
  wrapper = null;
  if (__test_if_true__(ob instanceof Object)) {
    /*pass*/
  } else {
    if (( ob.__class__ ) === dict) {
      wrapper = ob;
      ob = ob["$wrapped"];
    }
  }
  sname = this.define_structure(ob);
  if (__test_if_true__(wrapper)) {
    wrapper.__struct_name__ = sname;
  }
  args = [];
  stype = this.struct_types[sname];
  if (! (__contains__(this.struct_types, sname))) {
    if (__contains__(this.glsltypes, sname)) {
      if ((sname instanceof Array ? JSON.stringify(sname)==JSON.stringify("mat4") : sname==="mat4")) {
        if (__test_if_true__(ob.__struct_data__)) {
          o = ob[ob.__struct_data__];
        } else {
          o = ob;
        }
        var i,i__end__;
        i = 0;
        i__end__ = o.length;
        while (( i ) < i__end__) {
          value = (o[i] + "");
          if (! (__contains__(value, "."))) {
            value += ".0";
          }
          args.push(value);
          i += 1;
        }
      }
    } else {
      throw new RuntimeError(("no method to pack structure: " + sname));
    }
  }
  has_arrays = false;
  if (__test_if_true__(stype)) {
    if (( stype["arrays"].length ) > 0) {
      has_arrays = true;
    }
        var __iter7 = stype["integers"];
    if (! (__iter7 instanceof Array || typeof __iter7 == "string" || __is_typed_array(__iter7) || __is_some_array(__iter7) )) { __iter7 = __object_keys__(__iter7) }
    for (var __idx7=0; __idx7 < __iter7.length; __idx7++) {
      var key = __iter7[ __idx7 ];
      args.push((ob[key][0] + ""));
    }
        var __iter8 = stype["floats"];
    if (! (__iter8 instanceof Array || typeof __iter8 == "string" || __is_typed_array(__iter8) || __is_some_array(__iter8) )) { __iter8 = __object_keys__(__iter8) }
    for (var __idx8=0; __idx8 < __iter8.length; __idx8++) {
      var key = __iter8[ __idx8 ];
      value = (ob[key] + "");
      if (! (__contains__(value, "."))) {
        value += ".0";
      }
      args.push(value);
    }
        var __iter9 = stype["arrays"];
    if (! (__iter9 instanceof Array || typeof __iter9 == "string" || __is_typed_array(__iter9) || __is_some_array(__iter9) )) { __iter9 = __object_keys__(__iter9) }
    for (var __idx9=0; __idx9 < __iter9.length; __idx9++) {
      var key = __iter9[ __idx9 ];
      aname = (("_" + key) + name);
      this.array(ob[key], aname);
      args.push(aname);
    }
        var __iter10 = stype["structs"];
    if (! (__iter10 instanceof Array || typeof __iter10 == "string" || __is_typed_array(__iter10) || __is_some_array(__iter10) )) { __iter10 = __object_keys__(__iter10) }
    for (var __idx10=0; __idx10 < __iter10.length; __idx10++) {
      var key = __iter10[ __idx10 ];
      aname = (("_" + key) + name);
      this.structure(ob[key], aname);
      args.push(aname);
    }
  }
  args = ",".join(args);
  if (__test_if_true__(has_arrays)) {
    this.shader.push((((((((sname + " ") + name) + "=") + sname) + "(") + args) + ");"));
  } else {
    this.header.push((((((((("const " + sname) + " ") + name) + "=") + sname) + "(") + args) + ");"));
  }
  return stype;
}

GLSLJITRuntime.structure = function () { return GLSLJITRuntime.prototype.structure.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.int16array = function(ob, name) {
  var a,i;
  a = [(((("int " + name) + "[") + ob.length) + "]")];
  i = 0;
  while (( i ) < ob.length) {
    a.push((((((";" + name) + "[") + i) + "]=") + ob[i]));
    i += 1;
  }
  this.shader.push("".join(a));
}

GLSLJITRuntime.int16array = function () { return GLSLJITRuntime.prototype.int16array.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.array = function(ob, name) {
  var a,i,j,subname,subarr,v;
  if (__test_if_true__(ob[0] instanceof Array)) {
    a = [];
    i = 0;
    while (( i ) < ob.length) {
      subarr = ob[i];
      subname = __sprintf("%s_%s", [name, i]);
      if ((a.length instanceof Array ? JSON.stringify(a.length)==JSON.stringify(0) : a.length===0)) {
        a.append((((("float " + subname) + "[") + subarr.length) + "]"));
      } else {
        a.append(((((";float " + subname) + "[") + subarr.length) + "]"));
      }
      j = 0;
      while (( j ) < subarr.length) {
        v = (subarr[j] + "");
        if (! (__contains__(v, "."))) {
          v += ".0";
        }
        a.push((((((";" + subname) + "[") + j) + "]=") + v));
        j += 1;
      }
      i += 1;
    }
    this.shader.push("".join(a));
  } else {
    if (__test_if_true__((ob[0] instanceof Object || ( ob[0].__class__ ) === dict))) {
      i = 0;
      while (( i ) < ob.length) {
        this.structure(ob[i], ((name + "_") + i));
        i += 1;
      }
    } else {
      a = [(((("float " + name) + "[") + ob.length) + "];")];
      i = 0;
      while (( i ) < ob.length) {
        a.push((((((name + "[") + i) + "]=") + ob[i]) + ";"));
        i += 1;
      }
      this.shader.push("".join(a));
    }
  }
}

GLSLJITRuntime.array = function () { return GLSLJITRuntime.prototype.array.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.object = function(ob, name) {
  var func,cls;
    var __iter11 = this.object_packagers;
  if (! (__iter11 instanceof Array || typeof __iter11 == "string" || __is_typed_array(__iter11) || __is_some_array(__iter11) )) { __iter11 = __object_keys__(__iter11) }
  for (var __idx11=0; __idx11 < __iter11.length; __idx11++) {
    var p = __iter11[ __idx11 ];
    var __r_0;
    __r_0 = p;
    cls = __r_0[0];
    func = __r_0[1];
    if (__test_if_true__(ob instanceof cls)) {
      return func(ob);
    }
  }
}

GLSLJITRuntime.object = function () { return GLSLJITRuntime.prototype.object.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.unpack_array2d = function(arr, dims) {
  var h,rows,w,row;
  if ((typeof(dims) instanceof Array ? JSON.stringify(typeof(dims))==JSON.stringify("number") : typeof(dims)==="number")) {
    return arr;
  }
  var __r_1;
  __r_1 = dims;
  w = __r_1[0];
  h = __r_1[1];
  row = [];
  rows = [row];
    var __iter12 = arr;
  if (! (__iter12 instanceof Array || typeof __iter12 == "string" || __is_typed_array(__iter12) || __is_some_array(__iter12) )) { __iter12 = __object_keys__(__iter12) }
  for (var __idx12=0; __idx12 < __iter12.length; __idx12++) {
    var value = __iter12[ __idx12 ];
    row.append(value);
    if (( row.length ) >= w) {
      row = [];
      rows.append(row);
    }
  }
  __jsdict_pop(rows);
  if ((!(rows.length instanceof Array ? JSON.stringify(rows.length)==JSON.stringify(h) : rows.length===h))) {
    console.log("ERROR: __unpack_array2d, invalid height.");
  }
  return rows;
}

GLSLJITRuntime.unpack_array2d = function () { return GLSLJITRuntime.prototype.unpack_array2d.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.unpack_vec4 = function(arr, dims) {
  var rows,i,h,vec,w,row;
  if ((typeof(dims) instanceof Array ? JSON.stringify(typeof(dims))==JSON.stringify("number") : typeof(dims)==="number")) {
    w = dims;
    h = 1;
  } else {
    var __r_2;
    __r_2 = dims;
    w = __r_2[0];
    h = __r_2[1];
  }
  rows = [];
  i = 0;
  var y,y__end__;
  y = 0;
  y__end__ = h;
  while (( y ) < y__end__) {
    row = [];
    rows.append(row);
    var x,x__end__;
    x = 0;
    x__end__ = w;
    while (( x ) < x__end__) {
      vec = [];
      var j,j__end__;
      j = 0;
      j__end__ = 4;
      while (( j ) < j__end__) {
        vec.append(arr[i]);
        i += 1;
        j += 1;
      }
      row.append(vec);
      x += 1;
    }
    y += 1;
  }
  if ((!(rows.length instanceof Array ? JSON.stringify(rows.length)==JSON.stringify(h) : rows.length===h))) {
    console.log("ERROR: __unpack_vec4, invalid height.");
  }
  return rows;
}

GLSLJITRuntime.unpack_vec4 = function () { return GLSLJITRuntime.prototype.unpack_vec4.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.unpack_mat4 = function(arr) {
  var i;
  i = 0;
    var __iter13 = this.matrices;
  if (! (__iter13 instanceof Array || typeof __iter13 == "string" || __is_typed_array(__iter13) || __is_some_array(__iter13) )) { __iter13 = __object_keys__(__iter13) }
  for (var __idx13=0; __idx13 < __iter13.length; __idx13++) {
    var mat = __iter13[ __idx13 ];
    var j,j__end__;
    j = 0;
    j__end__ = 16;
    while (( j ) < j__end__) {
      mat[j] = arr[i];
      i += 1;
      j += 1;
    }
  }
  return this.matrices;
}

GLSLJITRuntime.unpack_mat4 = function () { return GLSLJITRuntime.prototype.unpack_mat4.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
GLSLJITRuntime.prototype.__properties__ = {  };
GLSLJITRuntime.prototype.__unbound_methods__ = {  };
var __getattr__ = function(ob, a) {
  
  if (ob.__getattr__) {
    return ob.__getattr__(a);
  }
};__getattr__.is_wrapper = true;
var __test_if_true__ = function(ob) {
  
  if (( ob ) === true) {
    return true;
  } else {
    if (( ob ) === false) {
      return false;
    } else {
      if ((typeof(ob) instanceof Array ? JSON.stringify(typeof(ob))==JSON.stringify("string") : typeof(ob)==="string")) {
        return (!(ob.length instanceof Array ? JSON.stringify(ob.length)==JSON.stringify(0) : ob.length===0));
      } else {
        if (! (ob)) {
          return false;
        } else {
          if (ob instanceof Array) {
            return (!(ob.length instanceof Array ? JSON.stringify(ob.length)==JSON.stringify(0) : ob.length===0));
          } else {
            if ((typeof(ob) instanceof Array ? JSON.stringify(typeof(ob))==JSON.stringify("function") : typeof(ob)==="function")) {
              return true;
            } else {
              if ((ob.__class__ && ( ob.__class__ ) === dict)) {
                return (!(Object.keys(ob["$wrapped"]).length instanceof Array ? JSON.stringify(Object.keys(ob["$wrapped"]).length)==JSON.stringify(0) : Object.keys(ob["$wrapped"]).length===0));
              } else {
                if (ob instanceof Object) {
                  return (!(Object.keys(ob).length instanceof Array ? JSON.stringify(Object.keys(ob).length)==JSON.stringify(0) : Object.keys(ob).length===0));
                } else {
                  return true;
                }
              }
            }
          }
        }
      }
    }
  }
};__test_if_true__.is_wrapper = true;
var __replace_method = function(ob, a, b) {
  
  if ((typeof(ob) instanceof Array ? JSON.stringify(typeof(ob))==JSON.stringify("string") : typeof(ob)==="string")) {
    return ob.split(a).join(b);
  } else {
    return ob.replace(a, b);
  }
};__replace_method.is_wrapper = true;
var __split_method = function(ob, delim) {
  
  if ((typeof(ob) instanceof Array ? JSON.stringify(typeof(ob))==JSON.stringify("string") : typeof(ob)==="string")) {
    if (( delim ) === undefined) {
      return ob.split(" ");
    } else {
      return ob.split(delim);
    }
  } else {
    if (( delim ) === undefined) {
      return ob.split();
    } else {
      return ob.split(delim);
    }
  }
};__split_method.is_wrapper = true;
__dom_array_types__ = [];
if ((typeof(NodeList) instanceof Array ? JSON.stringify(typeof(NodeList))==JSON.stringify("function") : typeof(NodeList)==="function")) {
  __dom_array_types__ = [NodeList, FileList, DOMStringList, HTMLCollection, SVGNumberList, SVGTransformList];
  if ((typeof(DataTransferItemList) instanceof Array ? JSON.stringify(typeof(DataTransferItemList))==JSON.stringify("function") : typeof(DataTransferItemList)==="function")) {
    __dom_array_types__.push(DataTransferItemList);
  }
  if ((typeof(HTMLAllCollection) instanceof Array ? JSON.stringify(typeof(HTMLAllCollection))==JSON.stringify("function") : typeof(HTMLAllCollection)==="function")) {
    __dom_array_types__.push(HTMLAllCollection);
  }
  if ((typeof(SVGElementInstanceList) instanceof Array ? JSON.stringify(typeof(SVGElementInstanceList))==JSON.stringify("function") : typeof(SVGElementInstanceList)==="function")) {
    __dom_array_types__.push(SVGElementInstanceList);
  }
  if ((typeof(ClientRectList) instanceof Array ? JSON.stringify(typeof(ClientRectList))==JSON.stringify("function") : typeof(ClientRectList)==="function")) {
    __dom_array_types__.push(ClientRectList);
  }
}
var __is_some_array = function(ob) {
  
  if (( __dom_array_types__.length ) > 0) {
        var __iter14 = __dom_array_types__;
    if (! (__iter14 instanceof Array || typeof __iter14 == "string" || __is_typed_array(__iter14) || __is_some_array(__iter14) )) { __iter14 = __object_keys__(__iter14) }
    for (var __idx14=0; __idx14 < __iter14.length; __idx14++) {
      var t = __iter14[ __idx14 ];
      if (__test_if_true__(ob instanceof t)) {
        return true;
      }
    }
  }
  return false;
}

var __is_typed_array = function(ob) {
  
  if (__test_if_true__((ob instanceof Int8Array || ob instanceof Uint8Array))) {
    return true;
  } else {
    if (__test_if_true__((ob instanceof Int16Array || ob instanceof Uint16Array))) {
      return true;
    } else {
      if (__test_if_true__((ob instanceof Int32Array || ob instanceof Uint32Array))) {
        return true;
      } else {
        if (__test_if_true__((ob instanceof Float32Array || ob instanceof Float64Array))) {
          return true;
        } else {
          return false;
        }
      }
    }
  }
}

var __js_typed_array = function(t, a) {
  var arr;
  if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("i") : t==="i")) {
    arr =  new Int32Array(a.length);
  }
  arr.set(a);
  return arr;
}

var __contains__ = function(ob, a) {
  var t;
  t = typeof(ob);
  if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("string") : t==="string")) {
    if ((ob.indexOf(a) instanceof Array ? JSON.stringify(ob.indexOf(a))==JSON.stringify(-1) : ob.indexOf(a)===-1)) {
      return false;
    } else {
      return true;
    }
  } else {
    if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("number") : t==="number")) {
      throw new TypeError;
    } else {
      if (__test_if_true__(__is_typed_array(ob))) {
                var __iter15 = ob;
        if (! (__iter15 instanceof Array || typeof __iter15 == "string" || __is_typed_array(__iter15) || __is_some_array(__iter15) )) { __iter15 = __object_keys__(__iter15) }
        for (var __idx15=0; __idx15 < __iter15.length; __idx15++) {
          var x = __iter15[ __idx15 ];
          if ((x instanceof Array ? JSON.stringify(x)==JSON.stringify(a) : x===a)) {
            return true;
          }
        }
        return false;
      } else {
        if (__test_if_true__(ob.__contains__)) {
          return ob.__contains__(a);
        } else {
          if (__test_if_true__((ob instanceof Object && Object.hasOwnProperty.call(ob, a)))) {
            return true;
          } else {
            return false;
          }
        }
      }
    }
  }
}

var __add_op = function(a, b) {
  var c,t;
  t = typeof(a);
  if (__test_if_true__(((t instanceof Array ? JSON.stringify(t)==JSON.stringify("string") : t==="string") || (t instanceof Array ? JSON.stringify(t)==JSON.stringify("number") : t==="number")))) {
    return a+b;
  } else {
    if (__test_if_true__(a instanceof Array)) {
      c = [];
      c.extend(a);
      c.extend(b);
      return c;
    } else {
      if (__test_if_true__(a.__add__)) {
        return a.__add__(b);
      } else {
        throw new TypeError("invalid objects for addition");
      }
    }
  }
}

var __mul_op = function(a, b) {
  var c,arr,t;
  t = typeof(a);
  if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("number") : t==="number")) {
    return a * b;
  } else {
    if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("string") : t==="string")) {
      arr = [];
      var i,i__end__;
      i = 0;
      i__end__ = b;
      while (( i ) < i__end__) {
        arr.append(a);
        i += 1;
      }
      return "".join(arr);
    } else {
      if (__test_if_true__(a instanceof Array)) {
        c = [];
        
        i = 0;
        i__end__ = b;
        while (( i ) < i__end__) {
          c.extend(a);
          i += 1;
        }
        return c;
      } else {
        if (__test_if_true__(a.__mul__)) {
          return a.__mul__(b);
        } else {
          throw new TypeError("invalid objects for multiplication");
        }
      }
    }
  }
}

var __jsdict = function(items) {
  var d,key;
  d = {};
    var __iter16 = items;
  if (! (__iter16 instanceof Array || typeof __iter16 == "string" || __is_typed_array(__iter16) || __is_some_array(__iter16) )) { __iter16 = __object_keys__(__iter16) }
  for (var __idx16=0; __idx16 < __iter16.length; __idx16++) {
    var item = __iter16[ __idx16 ];
    key = item[0];
    if (__test_if_true__(key instanceof Array)) {
      key = JSON.stringify(key);
    } else {
      if (__test_if_true__(key.__uid__)) {
        key = key.__uid__;
      }
    }
    d[key] = item[1];
  }
  return d;
}

var __jsdict_get = function(ob, key, default_value) {
  
  if (__test_if_true__(ob instanceof Object)) {
    if (__test_if_true__(key instanceof Array)) {
      key = JSON.stringify(key);
    }
    if (__test_if_true__(key in ob)) {
      return ob[key];
    }
    return default_value;
  } else {
    if (( default_value ) !== undefined) {
      return ob.get(key, default_value);
    } else {
      return ob.get(key);
    }
  }
}

var __jsdict_set = function(ob, key, value) {
  
  if (__test_if_true__(ob instanceof Object)) {
    if (__test_if_true__(key instanceof Array)) {
      key = JSON.stringify(key);
    }
    ob[key] = value;
  } else {
    ob.set(key,value);
  }
}

var __jsdict_keys = function(ob) {
  
  if (__test_if_true__(ob instanceof Object)) {
    return Object.keys( ob );
  } else {
    return ob.keys();
  }
}

var __jsdict_values = function(ob) {
  var arr,value;
  if (__test_if_true__(ob instanceof Object)) {
    arr = [];
        var __iter17 = ob;
    if (! (__iter17 instanceof Array || typeof __iter17 == "string" || __is_typed_array(__iter17) || __is_some_array(__iter17) )) { __iter17 = __object_keys__(__iter17) }
    for (var __idx17=0; __idx17 < __iter17.length; __idx17++) {
      var key = __iter17[ __idx17 ];
      if (__test_if_true__(ob.hasOwnProperty(key))) {
        value = ob[key];
        arr.push(value);
      }
    }
    return arr;
  } else {
    return ob.values();
  }
}

var __jsdict_items = function(ob) {
  var arr,value;
  if (__test_if_true__((ob instanceof Object || ( ob.items ) === undefined))) {
    arr = [];
        var __iter18 = ob;
    if (! (__iter18 instanceof Array || typeof __iter18 == "string" || __is_typed_array(__iter18) || __is_some_array(__iter18) )) { __iter18 = __object_keys__(__iter18) }
    for (var __idx18=0; __idx18 < __iter18.length; __idx18++) {
      var key = __iter18[ __idx18 ];
      if (__test_if_true__(Object.hasOwnProperty.call(ob, key))) {
        value = ob[key];
        arr.push([key, value]);
      }
    }
    return arr;
  } else {
    return ob.items();
  }
}

var __jsdict_pop = function(ob, key, _kwargs_) {
  var v;
  if (!( _kwargs_ instanceof Object )) {;
  var _kwargs_ = {ob: arguments[0],key: arguments[1],_default: arguments[2]};
  };
  if (_kwargs_ === undefined || _kwargs_._default === undefined) {var _default = null} else {var _default=_kwargs_._default};
  if (__test_if_true__(ob instanceof Array)) {
    if (__test_if_true__(ob.length)) {
      if (( key ) === undefined) {
        return ob.pop();
      } else {
        return ob.splice(key, 1)[0];
      }
    } else {
      throw new IndexError(key);
    }
  } else {
    if (__test_if_true__(ob instanceof Object)) {
      if (__test_if_true__(key in ob)) {
        v = ob[key];
        delete ob[key];
        return v;
      } else {
        if (( _default ) === undefined) {
          throw new KeyError(key);
        } else {
          return _default;
        }
      }
    } else {
      return ob.pop(key, _default);
    }
  }
}

var dir = function(ob) {
  
  if (__test_if_true__(ob instanceof Object)) {
    return Object.keys( ob );
  } else {
    return __object_keys__(ob);
  }
}

var __object_keys__ = function(ob) {
  var arr;
  "\n		notes:\n			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`\n			. this is different from Object.keys because it traverses the prototype chain.\n		";
  arr = [];
  for (var key in ob) { arr.push(key) };
  return arr;
}

var __bind_property_descriptors__ = function(o, klass) {
  var prop,desc;
    var __iter19 = klass.__properties__;
  if (! (__iter19 instanceof Array || typeof __iter19 == "string" || __is_typed_array(__iter19) || __is_some_array(__iter19) )) { __iter19 = __object_keys__(__iter19) }
  for (var __idx19=0; __idx19 < __iter19.length; __idx19++) {
    var name = __iter19[ __idx19 ];
    desc = __jsdict([["enumerable", true]]);
    prop = klass.__properties__[name];
    if (__test_if_true__(prop["get"])) {
      desc["get"] = __generate_getter__(klass, o, name);
    }
    if (__test_if_true__(prop["set"])) {
      desc["set"] = __generate_setter__(klass, o, name);
    }
    Object.defineProperty(o, name, desc);
  }
    var __iter20 = klass.__bases__;
  if (! (__iter20 instanceof Array || typeof __iter20 == "string" || __is_typed_array(__iter20) || __is_some_array(__iter20) )) { __iter20 = __object_keys__(__iter20) }
  for (var __idx20=0; __idx20 < __iter20.length; __idx20++) {
    var base = __iter20[ __idx20 ];
    __bind_property_descriptors__(o, base);
  }
}

var __generate_getter__ = function(klass, o, n) {
  
      var __lambda__ = function() {
    
    return klass.__properties__[n]["get"]([o], __jsdict([]));
  }

  return __lambda__;
}

var __generate_setter__ = function(klass, o, n) {
  
      var __lambda__ = function(v) {
    
    return klass.__properties__[n]["set"]([o, v], __jsdict([]));
  }

  return __lambda__;
}

var __sprintf = function(fmt, args) {
  var chunks,item,arr;
  if (__test_if_true__(args instanceof Array)) {
    chunks = fmt.split("%s");
    arr = [];
    var i;
    i = 0;
        var __iter21 = chunks;
    if (! (__iter21 instanceof Array || typeof __iter21 == "string" || __is_typed_array(__iter21) || __is_some_array(__iter21) )) { __iter21 = __object_keys__(__iter21) }
    for (var __idx21=0; __idx21 < __iter21.length; __idx21++) {
      var txt = __iter21[ __idx21 ];
      arr.append(txt);
      if (( i ) >= args.length) {
        break;
      }
      item = args[i];
      if ((typeof(item) instanceof Array ? JSON.stringify(typeof(item))==JSON.stringify("string") : typeof(item)==="string")) {
        arr.append(item);
      } else {
        if ((typeof(item) instanceof Array ? JSON.stringify(typeof(item))==JSON.stringify("number") : typeof(item)==="number")) {
          arr.append(("" + item));
        } else {
          arr.append(Object.prototype.toString.call(item));
        }
      }
      i += 1;
    }
    return "".join(arr);
  } else {
    return __replace_method(fmt, "%s", args);
  }
}

var __create_class__ = function(class_name, parents, attrs, props) {
  var f,klass,prop;
  "Create a PythonScript class";
  klass = Object.create(null);
  klass.__bases__ = parents;
  klass.__name__ = class_name;
  klass.__unbound_methods__ = Object.create(null);
  klass.__all_method_names__ = [];
  klass.__properties__ = props;
  klass.__attributes__ = attrs;
    var __iter22 = attrs;
  if (! (__iter22 instanceof Array || typeof __iter22 == "string" || __is_typed_array(__iter22) || __is_some_array(__iter22) )) { __iter22 = __object_keys__(__iter22) }
  for (var __idx22=0; __idx22 < __iter22.length; __idx22++) {
    var key = __iter22[ __idx22 ];
    if ((typeof(attrs[key]) instanceof Array ? JSON.stringify(typeof(attrs[key]))==JSON.stringify("function") : typeof(attrs[key])==="function")) {
      klass.__all_method_names__.push(key);
      f = attrs[key];
      if (__test_if_true__((hasattr(f, "is_classmethod") && f.is_classmethod))) {
        /*pass*/
      } else {
        if (__test_if_true__((hasattr(f, "is_staticmethod") && f.is_staticmethod))) {
          /*pass*/
        } else {
          klass.__unbound_methods__[key] = attrs[key];
        }
      }
    }
    if ((key instanceof Array ? JSON.stringify(key)==JSON.stringify("__getattribute__") : key==="__getattribute__")) {
      continue
    }
    klass[key] = attrs[key];
  }
  klass.__setters__ = [];
  klass.__getters__ = [];
    var __iter23 = klass.__properties__;
  if (! (__iter23 instanceof Array || typeof __iter23 == "string" || __is_typed_array(__iter23) || __is_some_array(__iter23) )) { __iter23 = __object_keys__(__iter23) }
  for (var __idx23=0; __idx23 < __iter23.length; __idx23++) {
    var name = __iter23[ __idx23 ];
    prop = klass.__properties__[name];
    klass.__getters__.push(name);
    if (__test_if_true__(prop["set"])) {
      klass.__setters__.push(name);
    }
  }
    var __iter24 = klass.__bases__;
  if (! (__iter24 instanceof Array || typeof __iter24 == "string" || __is_typed_array(__iter24) || __is_some_array(__iter24) )) { __iter24 = __object_keys__(__iter24) }
  for (var __idx24=0; __idx24 < __iter24.length; __idx24++) {
    var base = __iter24[ __idx24 ];
    Array.prototype.push.apply(klass.__getters__, base.__getters__);
    Array.prototype.push.apply(klass.__setters__, base.__setters__);
    Array.prototype.push.apply(klass.__all_method_names__, base.__all_method_names__);
  }
      var __call__ = function() {
    var has_getattr,wrapper,object,has_getattribute;
    "Create a PythonJS object";
    object = Object.create(null);
    object.__class__ = klass;
    object.__dict__ = object;
    has_getattribute = false;
    has_getattr = false;
        var __iter25 = klass.__all_method_names__;
    if (! (__iter25 instanceof Array || typeof __iter25 == "string" || __is_typed_array(__iter25) || __is_some_array(__iter25) )) { __iter25 = __object_keys__(__iter25) }
    for (var __idx25=0; __idx25 < __iter25.length; __idx25++) {
      var name = __iter25[ __idx25 ];
      if ((name instanceof Array ? JSON.stringify(name)==JSON.stringify("__getattribute__") : name==="__getattribute__")) {
        has_getattribute = true;
      } else {
        if ((name instanceof Array ? JSON.stringify(name)==JSON.stringify("__getattr__") : name==="__getattr__")) {
          has_getattr = true;
        } else {
          wrapper = __get__(object, name);
          if (__test_if_true__(! (wrapper.is_wrapper))) {
            console.log(["RUNTIME ERROR: failed to get wrapper for:", name]);
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
    if (__test_if_true__(object.__init__)) {
      object.__init__.apply(this, arguments);
    }
    return object;
  }

  __call__.is_wrapper = true;
  klass.__call__ = __call__;
  return klass;
}

var type = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{"bases": null, "class_dict": null},args:["ob_or_class_name", "bases", "class_dict"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("type", __sig__, args, kwargs);
  var ob_or_class_name = __args__['ob_or_class_name'];
  var bases = __args__['bases'];
  var class_dict = __args__['class_dict'];
  "\n	type(object) -> the object's type\n	type(name, bases, dict) -> a __new__>>type  ## broken? - TODO test\n	";
  if (__test_if_true__((( bases ) === null && ( class_dict ) === null))) {
    return ob_or_class_name.__class__;
  } else {
    return create_class(ob_or_class_name, bases, class_dict);
  }
};type.is_wrapper = true;
var hasattr = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["ob", "attr"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("hasattr", __sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  return Object.hasOwnProperty.call(ob, attr);
};hasattr.is_wrapper = true;
var getattr = function(args, kwargs) {
  var prop;
  var __sig__,__args__;
  __sig__ = { kwargs:{"property": false},args:["ob", "attr", "property"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("getattr", __sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  var property = __args__['property'];
  if (__test_if_true__(property)) {
    prop = _get_upstream_property(ob.__class__, attr);
    if (__test_if_true__((prop && prop["get"]))) {
      return prop["get"]([ob], __jsdict([]));
    } else {
      console.log(["ERROR: getattr property error", prop]);
    }
  } else {
    return __get__(ob, attr);
  }
};getattr.is_wrapper = true;
var setattr = function(args, kwargs) {
  var prop;
  var __sig__,__args__;
  __sig__ = { kwargs:{"property": false},args:["ob", "attr", "value", "property"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("setattr", __sig__, args, kwargs);
  var ob = __args__['ob'];
  var attr = __args__['attr'];
  var value = __args__['value'];
  var property = __args__['property'];
  if (__test_if_true__(property)) {
    prop = _get_upstream_property(ob.__class__, attr);
    if (__test_if_true__((prop && prop["set"]))) {
      prop["set"]([ob, value], __jsdict([]));
    } else {
      console.log(["ERROR: setattr property error", prop]);
    }
  } else {
    __set__(ob, attr, value);
  }
};setattr.is_wrapper = true;
var issubclass = function(args, kwargs) {
  var i,bases;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["C", "B"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("issubclass", __sig__, args, kwargs);
  var C = __args__['C'];
  var B = __args__['B'];
  if (( C ) === B) {
    return true;
  }
  bases = C.__bases__;
  i = 0;
  while (( i ) < __get__(bases, "length", "missing attribute `length` - line 655: while i < bases.length:")) {
    if (__test_if_true__(issubclass([((bases instanceof Array) ? bases[i] : __get__(bases, "__getitem__", "line 656: if issubclass( bases[i], B ):")([i], __NULL_OBJECT__)), B], __NULL_OBJECT__))) {
      return true;
    }
    i += 1;
  }
  return false;
};issubclass.is_wrapper = true;
var isinstance = function(args, kwargs) {
  var ob_class;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["ob", "klass"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("isinstance", __sig__, args, kwargs);
  var ob = __args__['ob'];
  var klass = __args__['klass'];
  if (__test_if_true__((( ob ) === undefined || ( ob ) === null))) {
    return false;
  } else {
    if (__test_if_true__((ob instanceof Array && ( klass ) === list))) {
      return true;
    } else {
      if (__test_if_true__(! (Object.hasOwnProperty.call(ob, "__class__")))) {
        return false;
      }
    }
  }
  ob_class = ob.__class__;
  if (( ob_class ) === undefined) {
    return false;
  } else {
    return issubclass([ob_class, klass], __NULL_OBJECT__);
  }
};isinstance.is_wrapper = true;
var int = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("int", __sig__, args, kwargs);
  var a = __args__['a'];
  a = Math.round(a);
  if (__test_if_true__(isNaN(a))) {
    throw new ValueError("not a number");
  }
  return a;
};int.is_wrapper = true;
var int16 = function(a) {
  var arr;
  arr =  new Int16Array(1);
  arr[0] = a;
  return arr;
}

var float = function(args, kwargs) {
  var b;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("float", __sig__, args, kwargs);
  var a = __args__['a'];
  if ((typeof(a) instanceof Array ? JSON.stringify(typeof(a))==JSON.stringify("string") : typeof(a)==="string")) {
    if ((a.lower() instanceof Array ? JSON.stringify(a.lower())==JSON.stringify("nan") : a.lower()==="nan")) {
      return NaN;
    } else {
      if ((a.lower() instanceof Array ? JSON.stringify(a.lower())==JSON.stringify("inf") : a.lower()==="inf")) {
        return Infinity;
      }
    }
  }
  b = Number(a);
  if (__test_if_true__(isNaN(b))) {
    throw new ValueError(("can not convert to float: " + a));
  }
  return b;
};float.is_wrapper = true;
var round = function(args, kwargs) {
  var p,b;
  var __sig__,__args__;
  __sig__ = { kwargs:{"places": 0},args:["a", "places"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("round", __sig__, args, kwargs);
  var a = __args__['a'];
  var places = __args__['places'];
  b = ("" + a);
  if ((b.indexOf(".") instanceof Array ? JSON.stringify(b.indexOf("."))==JSON.stringify(-1) : b.indexOf(".")===-1)) {
    return a;
  } else {
    p = Math.pow(10, places);
    return (Math.round((a * p)) / p);
  }
};round.is_wrapper = true;
var str = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["s"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("str", __sig__, args, kwargs);
  var s = __args__['s'];
  return ("" + s);
};str.is_wrapper = true;
var _setup_str_prototype = function() {
  
  "\n	Extend JavaScript String.prototype with methods that implement the Python str API.\n	The decorator @String.prototype.[name] assigns the function to the prototype,\n	and ensures that the special 'this' variable will work.\n	";
      var func = function(a) {
    
    if ((this.indexOf(a) instanceof Array ? JSON.stringify(this.indexOf(a))==JSON.stringify(-1) : this.indexOf(a)===-1)) {
      return false;
    } else {
      return true;
    }
  }

  Object.defineProperty(String.prototype, "__contains__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(index) {
    
    if (( index ) < 0) {
      return this[(this.length + index)];
    } else {
      return this[index];
    }
  }

  Object.defineProperty(String.prototype, "get", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(self) {
    
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  Object.defineProperty(String.prototype, "__iter__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(idx) {
    
    if (( idx ) < 0) {
      return this[(this.length + idx)];
    } else {
      return this[idx];
    }
  }

  Object.defineProperty(String.prototype, "__getitem__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.length;
  }

  Object.defineProperty(String.prototype, "__len__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(start, stop, step) {
    
    if (__test_if_true__((( start ) === undefined && ( stop ) === undefined && (step instanceof Array ? JSON.stringify(step)==JSON.stringify(-1) : step===-1)))) {
      return this.split("").reverse().join("");
    } else {
      if (( stop ) < 0) {
        stop = (this.length + stop);
      }
      return this.substring(start, stop);
    }
  }

  Object.defineProperty(String.prototype, "__getslice__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.split("\n");
  }

  Object.defineProperty(String.prototype, "splitlines", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.trim();
  }

  Object.defineProperty(String.prototype, "strip", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    
    if ((this.substring(0, a.length) instanceof Array ? JSON.stringify(this.substring(0, a.length))==JSON.stringify(a) : this.substring(0, a.length)===a)) {
      return true;
    } else {
      return false;
    }
  }

  Object.defineProperty(String.prototype, "startswith", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    
    if ((this.substring((this.length - a.length), this.length) instanceof Array ? JSON.stringify(this.substring((this.length - a.length), this.length))==JSON.stringify(a) : this.substring((this.length - a.length), this.length)===a)) {
      return true;
    } else {
      return false;
    }
  }

  Object.defineProperty(String.prototype, "endswith", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    var i,arr,out;
    out = "";
    if (__test_if_true__(a instanceof Array)) {
      arr = a;
    } else {
      arr = a["$wrapped"];
    }
    i = 0;
        var __iter26 = arr;
    if (! (__iter26 instanceof Array || typeof __iter26 == "string" || __is_typed_array(__iter26) || __is_some_array(__iter26) )) { __iter26 = __object_keys__(__iter26) }
    for (var __idx26=0; __idx26 < __iter26.length; __idx26++) {
      var value = __iter26[ __idx26 ];
      out += value;
      i += 1;
      if (( i ) < arr.length) {
        out += this;
      }
    }
    return out;
  }

  Object.defineProperty(String.prototype, "join", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.toUpperCase();
  }

  Object.defineProperty(String.prototype, "upper", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.toLowerCase();
  }

  Object.defineProperty(String.prototype, "lower", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    var i;
    i = this.indexOf(a);
    if ((i instanceof Array ? JSON.stringify(i)==JSON.stringify(-1) : i===-1)) {
      throw new ValueError((a + " - not in string"));
    }
    return i;
  }

  Object.defineProperty(String.prototype, "index", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    
    return this.indexOf(a);
  }

  Object.defineProperty(String.prototype, "find", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    var digits;
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
        var __iter27 = this;
    if (! (__iter27 instanceof Array || typeof __iter27 == "string" || __is_typed_array(__iter27) || __is_some_array(__iter27) )) { __iter27 = __object_keys__(__iter27) }
    for (var __idx27=0; __idx27 < __iter27.length; __idx27++) {
      var char = __iter27[ __idx27 ];
      if (__contains__(digits, char)) {
        /*pass*/
      } else {
        return false;
      }
    }
    return true;
  }

  Object.defineProperty(String.prototype, "isdigit", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    var digits;
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."];
        var __iter28 = this;
    if (! (__iter28 instanceof Array || typeof __iter28 == "string" || __is_typed_array(__iter28) || __is_some_array(__iter28) )) { __iter28 = __object_keys__(__iter28) }
    for (var __idx28=0; __idx28 < __iter28.length; __idx28++) {
      var char = __iter28[ __idx28 ];
      if (__contains__(digits, char)) {
        /*pass*/
      } else {
        return false;
      }
    }
    return true;
  }

  Object.defineProperty(String.prototype, "isnumber", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(encoding) {
    
    return this;
  }

  Object.defineProperty(String.prototype, "decode", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(encoding) {
    
    return this;
  }

  Object.defineProperty(String.prototype, "encode", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(fmt) {
    var keys,r;
    r = this;
    keys = Object.keys(fmt);
        var __iter29 = keys;
    if (! (__iter29 instanceof Array || typeof __iter29 == "string" || __is_typed_array(__iter29) || __is_some_array(__iter29) )) { __iter29 = __object_keys__(__iter29) }
    for (var __idx29=0; __idx29 < __iter29.length; __idx29++) {
      var key = __iter29[ __idx29 ];
      r = r.split(key).join(fmt[key]);
    }
    r = r.split("{").join("").split("}").join("");
    return r;
  }

  Object.defineProperty(String.prototype, "format", { enumerable:false,value:func,writeable:true,configurable:true });
};_setup_str_prototype.is_wrapper = true;
_setup_str_prototype();
var __sort_method = function(ob) {
  
  if (__test_if_true__(ob instanceof Array)) {
            var f = function(a, b) {
      
      if (( a ) < b) {
        return -1;
      } else {
        if (( a ) > b) {
          return 1;
        } else {
          return 0;
        }
      }
    }

    return ob.sort( f );
  } else {
    return ob.sort();
  }
}

var _setup_array_prototype = function() {
  
      var func = function() {
    var i,item;
    i = 0;
    while (( i ) < this.length) {
      item = this[i];
      if ((typeof(item) instanceof Array ? JSON.stringify(typeof(item))==JSON.stringify("object") : typeof(item)==="object")) {
        if (__test_if_true__(item.jsify)) {
          this[i] = item.jsify();
        }
      }
      i += 1;
    }
    return this;
  }

  Object.defineProperty(Array.prototype, "jsify", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(a) {
    
    if ((this.indexOf(a) instanceof Array ? JSON.stringify(this.indexOf(a))==JSON.stringify(-1) : this.indexOf(a)===-1)) {
      return false;
    } else {
      return true;
    }
  }

  Object.defineProperty(Array.prototype, "__contains__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.length;
  }

  Object.defineProperty(Array.prototype, "__len__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(index) {
    
    return this[index];
  }

  Object.defineProperty(Array.prototype, "get", { enumerable:false,value:func,writeable:true,configurable:true });
      var __getitem__ = function(index) {
    
    if (( index ) < 0) {
      index = (this.length + index);
    }
    return this[index];
  }

  Object.defineProperty(Array.prototype, "__getitem__", { enumerable:false,value:__getitem__,writeable:true,configurable:true });
      var __setitem__ = function(index, value) {
    
    if (( index ) < 0) {
      index = (this.length + index);
    }
    this[index] = value;
  }

  Object.defineProperty(Array.prototype, "__setitem__", { enumerable:false,value:__setitem__,writeable:true,configurable:true });
      var func = function() {
    
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  Object.defineProperty(Array.prototype, "__iter__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(start, stop, step) {
    var i,arr,n;
    arr = [];
    start = (start | 0);
    if (( stop ) === undefined) {
      stop = this.length;
    }
    if (( start ) < 0) {
      start = (this.length + start);
    }
    if (( stop ) < 0) {
      stop = (this.length + stop);
    }
    if ((typeof(step) instanceof Array ? JSON.stringify(typeof(step))==JSON.stringify("number") : typeof(step)==="number")) {
      if (( step ) < 0) {
        i = start;
        while (( i ) >= 0) {
          arr.push(this[i]);
          i += step;
        }
        return arr;
      } else {
        i = start;
        n = stop;
        while (( i ) < n) {
          arr.push(this[i]);
          i += step;
        }
        return arr;
      }
    } else {
      i = start;
      n = stop;
      while (( i ) < n) {
        arr.push(this[i]);
        i += 1;
      }
      return arr;
    }
  }

  Object.defineProperty(Array.prototype, "__getslice__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(start, stop, step, items) {
    var arr;
    if (( start ) === undefined) {
      start = 0;
    }
    if (( stop ) === undefined) {
      stop = this.length;
    }
    arr = [start, (stop - start)];
        var __iter30 = items;
    if (! (__iter30 instanceof Array || typeof __iter30 == "string" || __is_typed_array(__iter30) || __is_some_array(__iter30) )) { __iter30 = __object_keys__(__iter30) }
    for (var __idx30=0; __idx30 < __iter30.length; __idx30++) {
      var item = __iter30[ __idx30 ];
      arr.push(item);
    }
    this.splice.apply(this, arr);
  }

  Object.defineProperty(Array.prototype, "__setslice__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(item) {
    
    this.push(item);
    return this;
  }

  Object.defineProperty(Array.prototype, "append", { enumerable:false,value:func,writeable:true,configurable:true });
      var extend = function(other) {
    
        var __iter31 = other;
    if (! (__iter31 instanceof Array || typeof __iter31 == "string" || __is_typed_array(__iter31) || __is_some_array(__iter31) )) { __iter31 = __object_keys__(__iter31) }
    for (var __idx31=0; __idx31 < __iter31.length; __idx31++) {
      var obj = __iter31[ __idx31 ];
      this.push(obj);
    }
    return this;
  }

  Object.defineProperty(Array.prototype, "extend", { enumerable:false,value:extend,writeable:true,configurable:true });
      var func = function(item) {
    var index;
    index = this.indexOf(item);
    this.splice(index, 1);
  }

  Object.defineProperty(Array.prototype, "remove", { enumerable:false,value:func,writeable:true,configurable:true });
      var insert = function(index, obj) {
    
    if (( index ) < 0) {
      index = (this.length + index);
    }
    this.splice(index, 0, obj);
  }

  Object.defineProperty(Array.prototype, "insert", { enumerable:false,value:insert,writeable:true,configurable:true });
      var index = function(obj) {
    
    return this.indexOf(obj);
  }

  Object.defineProperty(Array.prototype, "index", { enumerable:false,value:index,writeable:true,configurable:true });
      var count = function(obj) {
    var a;
    a = 0;
        var __iter32 = this;
    if (! (__iter32 instanceof Array || typeof __iter32 == "string" || __is_typed_array(__iter32) || __is_some_array(__iter32) )) { __iter32 = __object_keys__(__iter32) }
    for (var __idx32=0; __idx32 < __iter32.length; __idx32++) {
      var item = __iter32[ __idx32 ];
      if (( item ) === obj) {
        a += 1;
      }
    }
    return a;
  }

  Object.defineProperty(Array.prototype, "count", { enumerable:false,value:count,writeable:true,configurable:true });
      var func = function(x, low, high) {
    var a,mid;
    if (( low ) === undefined) {
      low = 0;
    }
    if (( high ) === undefined) {
      high = this.length;
    }
    while (( low ) < high) {
      a = (low + high);
      mid = Math.floor((a / 2));
      if (( x ) < this[mid]) {
        high = mid;
      } else {
        low = (mid + 1);
      }
    }
    return low;
  }

  Object.defineProperty(Array.prototype, "bisect", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(other) {
    var f;
            var __lambda__ = function(i) {
      
      return (other.indexOf(i) instanceof Array ? JSON.stringify(other.indexOf(i))==JSON.stringify(-1) : other.indexOf(i)===-1);
    }

    f = __lambda__;
    return this.filter(f);
  }

  Object.defineProperty(Array.prototype, "difference", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(other) {
    var f;
            var __lambda__ = function(i) {
      
      return (!(other.indexOf(i) instanceof Array ? JSON.stringify(other.indexOf(i))==JSON.stringify(-1) : other.indexOf(i)===-1));
    }

    f = __lambda__;
    return this.filter(f);
  }

  Object.defineProperty(Array.prototype, "intersection", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(other) {
    
        var __iter33 = this;
    if (! (__iter33 instanceof Array || typeof __iter33 == "string" || __is_typed_array(__iter33) || __is_some_array(__iter33) )) { __iter33 = __object_keys__(__iter33) }
    for (var __idx33=0; __idx33 < __iter33.length; __idx33++) {
      var item = __iter33[ __idx33 ];
      if ((other.indexOf(item) instanceof Array ? JSON.stringify(other.indexOf(item))==JSON.stringify(-1) : other.indexOf(item)===-1)) {
        return false;
      }
    }
    return true;
  }

  Object.defineProperty(Array.prototype, "issubset", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    var i,arr;
    arr = [];
    i = 0;
    while (( i ) < this.length) {
      arr.push(this[i]);
      i += 1;
    }
    return arr;
  }

  Object.defineProperty(Array.prototype, "copy", { enumerable:false,value:func,writeable:true,configurable:true });
};_setup_array_prototype.is_wrapper = true;
_setup_array_prototype();
var _setup_nodelist_prototype = function() {
  
      var func = function(a) {
    
    if ((this.indexOf(a) instanceof Array ? JSON.stringify(this.indexOf(a))==JSON.stringify(-1) : this.indexOf(a)===-1)) {
      return false;
    } else {
      return true;
    }
  }

  Object.defineProperty(NodeList.prototype, "__contains__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function() {
    
    return this.length;
  }

  Object.defineProperty(NodeList.prototype, "__len__", { enumerable:false,value:func,writeable:true,configurable:true });
      var func = function(index) {
    
    return this[index];
  }

  Object.defineProperty(NodeList.prototype, "get", { enumerable:false,value:func,writeable:true,configurable:true });
      var __getitem__ = function(index) {
    
    if (( index ) < 0) {
      index = (this.length + index);
    }
    return this[index];
  }

  Object.defineProperty(NodeList.prototype, "__getitem__", { enumerable:false,value:__getitem__,writeable:true,configurable:true });
      var __setitem__ = function(index, value) {
    
    if (( index ) < 0) {
      index = (this.length + index);
    }
    this[index] = value;
  }

  Object.defineProperty(NodeList.prototype, "__setitem__", { enumerable:false,value:__setitem__,writeable:true,configurable:true });
      var func = function() {
    
    return __get__(Iterator, "__call__")([this, 0], __NULL_OBJECT__);
  }

  Object.defineProperty(NodeList.prototype, "__iter__", { enumerable:false,value:func,writeable:true,configurable:true });
      var index = function(obj) {
    
    return this.indexOf(obj);
  }

  Object.defineProperty(NodeList.prototype, "index", { enumerable:false,value:index,writeable:true,configurable:true });
};_setup_nodelist_prototype.is_wrapper = true;
if (__test_if_true__(((__NODEJS__ instanceof Array ? JSON.stringify(__NODEJS__)==JSON.stringify(false) : __NODEJS__===false) && (__WEBWORKER__ instanceof Array ? JSON.stringify(__WEBWORKER__)==JSON.stringify(false) : __WEBWORKER__===false)))) {
  _setup_nodelist_prototype();
}
var bisect = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{"low": null, "high": null},args:["a", "x", "low", "high"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("bisect", __sig__, args, kwargs);
  var a = __args__['a'];
  var x = __args__['x'];
  var low = __args__['low'];
  var high = __args__['high'];
  return a.bisect(x, low, high);
};bisect.is_wrapper = true;
var range = function(args, kwargs) {
  var i,arr;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["num", "stop", "step"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("range", __sig__, args, kwargs);
  var num = __args__['num'];
  var stop = __args__['stop'];
  var step = __args__['step'];
  "Emulates Python's range function";
  if (( stop ) !== undefined) {
    i = num;
    num = stop;
  } else {
    i = 0;
  }
  if (( step ) === undefined) {
    step = 1;
  }
  arr = [];
  while (( i ) < num) {
    arr.push(i);
    i += step;
  }
  return arr;
};range.is_wrapper = true;
var xrange = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["num", "stop", "step"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("xrange", __sig__, args, kwargs);
  var num = __args__['num'];
  var stop = __args__['stop'];
  var step = __args__['step'];
  return range([num, stop, step], __NULL_OBJECT__);
};xrange.is_wrapper = true;
var sum = function(args, kwargs) {
  var a;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["arr"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("sum", __sig__, args, kwargs);
  var arr = __args__['arr'];
  a = 0;
  var b,__iterator__40;
  __iterator__40 = __get__(__get__(arr, "__iter__", "no iterator - line 1065: for b in arr:"), "__call__")([], __NULL_OBJECT__);
  var __next__40;
  __next__40 = __get__(__iterator__40, "next");
  while (( __iterator__40.index ) < __iterator__40.length) {
    b = __next__40();
    a += b;
  }
  return a;
};sum.is_wrapper = true;
var StopIteration,__StopIteration_attrs,__StopIteration_parents;
__StopIteration_attrs = {};
__StopIteration_parents = [];
__StopIteration_properties = {};
StopIteration = __create_class__("StopIteration", __StopIteration_parents, __StopIteration_attrs, __StopIteration_properties);
var len = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["ob"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("len", __sig__, args, kwargs);
  var ob = __args__['ob'];
  if (__test_if_true__(ob instanceof Array)) {
    return ob.length;
  } else {
    if (__test_if_true__(__is_typed_array(ob))) {
      return ob.length;
    } else {
      if (__test_if_true__(ob instanceof ArrayBuffer)) {
        return ob.byteLength;
      } else {
        if (__test_if_true__(ob.__len__)) {
          return ob.__len__();
        } else {
          return Object.keys(ob).length;
        }
      }
    }
  }
};len.is_wrapper = true;
var next = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["obj"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("next", __sig__, args, kwargs);
  var obj = __args__['obj'];
  return __get__(__get__(obj, "next", "missing attribute `next` - line 1083: return obj.next()"), "__call__")();
};next.is_wrapper = true;
var map = function(args, kwargs) {
  var arr,v;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["func", "objs"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("map", __sig__, args, kwargs);
  var func = __args__['func'];
  var objs = __args__['objs'];
  arr = [];
  var ob,__iterator__41;
  __iterator__41 = __get__(__get__(objs, "__iter__", "no iterator - line 1086: for ob in objs:"), "__call__")([], __NULL_OBJECT__);
  var __next__41;
  __next__41 = __get__(__iterator__41, "next");
  while (( __iterator__41.index ) < __iterator__41.length) {
    ob = __next__41();
    v = __get__(func, "__call__")([ob], __NULL_OBJECT__);
    arr.push(v);
  }
  return arr;
};map.is_wrapper = true;
var filter = function(args, kwargs) {
  var arr;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["func", "objs"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("filter", __sig__, args, kwargs);
  var func = __args__['func'];
  var objs = __args__['objs'];
  arr = [];
  var ob,__iterator__42;
  __iterator__42 = __get__(__get__(objs, "__iter__", "no iterator - line 1093: for ob in objs:"), "__call__")([], __NULL_OBJECT__);
  var __next__42;
  __next__42 = __get__(__iterator__42, "next");
  while (( __iterator__42.index ) < __iterator__42.length) {
    ob = __next__42();
    if (__test_if_true__(__get__(func, "__call__")([ob], __NULL_OBJECT__))) {
      arr.push(ob);
    }
  }
  return arr;
};filter.is_wrapper = true;
var min = function(args, kwargs) {
  var a;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["lst"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("min", __sig__, args, kwargs);
  var lst = __args__['lst'];
  a = null;
  var value,__iterator__43;
  __iterator__43 = __get__(__get__(lst, "__iter__", "no iterator - line 1100: for value in lst:"), "__call__")([], __NULL_OBJECT__);
  var __next__43;
  __next__43 = __get__(__iterator__43, "next");
  while (( __iterator__43.index ) < __iterator__43.length) {
    value = __next__43();
    if (( a ) === null) {
      a = value;
    } else {
      if (( value ) < a) {
        a = value;
      }
    }
  }
  return a;
};min.is_wrapper = true;
var max = function(args, kwargs) {
  var a;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["lst"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("max", __sig__, args, kwargs);
  var lst = __args__['lst'];
  a = null;
  var value,__iterator__44;
  __iterator__44 = __get__(__get__(lst, "__iter__", "no iterator - line 1106: for value in lst:"), "__call__")([], __NULL_OBJECT__);
  var __next__44;
  __next__44 = __get__(__iterator__44, "next");
  while (( __iterator__44.index ) < __iterator__44.length) {
    value = __next__44();
    if (( a ) === null) {
      a = value;
    } else {
      if (( value ) > a) {
        a = value;
      }
    }
  }
  return a;
};max.is_wrapper = true;
var abs = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["num"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("abs", __sig__, args, kwargs);
  var num = __args__['num'];
  return Math.abs(num);
};abs.is_wrapper = true;
var ord = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["char"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("ord", __sig__, args, kwargs);
  var char = __args__['char'];
  return char.charCodeAt(0);
};ord.is_wrapper = true;
var chr = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["num"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("chr", __sig__, args, kwargs);
  var num = __args__['num'];
  return String.fromCharCode(num);
};chr.is_wrapper = true;
var __ArrayIterator = function(arr, index) {
  __ArrayIterator.__init__(this, arr, index);
  this.__class__ = __ArrayIterator;
  this.__uid__ = ("￼" + _PythonJS_UID);
  _PythonJS_UID += 1;
}

__ArrayIterator.__uid__ = ("￼" + _PythonJS_UID);
_PythonJS_UID += 1;
__ArrayIterator.prototype.__init__ = function(arr, index) {
  
  this.arr = arr;
  this.index = index;
  this.length = arr.length;
}

__ArrayIterator.__init__ = function () { return __ArrayIterator.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
__ArrayIterator.prototype.next = function() {
  var index,arr;
  index = this.index;
  this.index += 1;
  arr = this.arr;
  return arr[index];
}

__ArrayIterator.next = function () { return __ArrayIterator.prototype.next.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
__ArrayIterator.prototype.__properties__ = {  };
__ArrayIterator.prototype.__unbound_methods__ = {  };
var Iterator,__Iterator_attrs,__Iterator_parents;
__Iterator_attrs = {};
__Iterator_parents = [];
__Iterator_properties = {};
var __Iterator___init__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "obj", "index"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__Iterator___init__", __sig__, args, kwargs);
  var self = __args__['self'];
  var obj = __args__['obj'];
  var index = __args__['index'];
  self.obj = obj;
  self.index = index;
  self.length = len([obj], __NULL_OBJECT__);
  self.obj_get = __get__(obj, "get", "missing attribute `get` - line 1134: self.obj_get = obj.get  ## cache this for speed");
};__Iterator___init__.is_wrapper = true;
__Iterator_attrs.__init__ = __Iterator___init__;
var __Iterator_next = function(args, kwargs) {
  var index;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__Iterator_next", __sig__, args, kwargs);
  var self = __args__['self'];
  index = self.index;
  self.index += 1;
  return self.obj_get([index], __jsdict([]));
};__Iterator_next.is_wrapper = true;
__Iterator_attrs.next = __Iterator_next;
Iterator = __create_class__("Iterator", __Iterator_parents, __Iterator_attrs, __Iterator_properties);
var tuple = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("tuple", __sig__, args, kwargs);
  var a = __args__['a'];
  if ((Object.keys(arguments).length instanceof Array ? JSON.stringify(Object.keys(arguments).length)==JSON.stringify(0) : Object.keys(arguments).length===0)) {
    return [];
  } else {
    if (__test_if_true__(a instanceof Array)) {
      return a.slice();
    } else {
      if ((typeof(a) instanceof Array ? JSON.stringify(typeof(a))==JSON.stringify("string") : typeof(a)==="string")) {
        return a.split("");
      } else {
        console.log(a);
        console.log(arguments);
        throw new TypeError;
      }
    }
  }
};tuple.is_wrapper = true;
var list = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("list", __sig__, args, kwargs);
  var a = __args__['a'];
  if ((Object.keys(arguments).length instanceof Array ? JSON.stringify(Object.keys(arguments).length)==JSON.stringify(0) : Object.keys(arguments).length===0)) {
    return [];
  } else {
    if (__test_if_true__(a instanceof Array)) {
      return a.slice();
    } else {
      if ((typeof(a) instanceof Array ? JSON.stringify(typeof(a))==JSON.stringify("string") : typeof(a)==="string")) {
        return a.split("");
      } else {
        console.log(a);
        console.log(arguments);
        throw new TypeError;
      }
    }
  }
};list.is_wrapper = true;
var __tuple_key__ = function(arr) {
  var i,item,r,t;
  r = [];
  i = 0;
  while (( i ) < arr.length) {
    item = arr[i];
    t = typeof(item);
    if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("string") : t==="string")) {
      r.append((("'" + item) + "'"));
    } else {
      if (__test_if_true__(item instanceof Array)) {
        r.append(__tuple_key__(item));
      } else {
        if ((t instanceof Array ? JSON.stringify(t)==JSON.stringify("object") : t==="object")) {
          if (( item.__uid__ ) === undefined) {
            throw new KeyError(item);
          }
          r.append(item.__uid__);
        } else {
          r.append(item);
        }
      }
    }
    i += 1;
  }
  return r.join(",");
}

var dict,__dict_attrs,__dict_parents;
__dict_attrs = {};
__dict_parents = [];
__dict_properties = {};
var __dict___init__ = function(args, kwargs) {
  var k,ob,value,v;
  var __sig__,__args__;
  __sig__ = { kwargs:{"js_object": null, "pointer": null},args:["self", "js_object", "pointer"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___init__", __sig__, args, kwargs);
  var self = __args__['self'];
  var js_object = __args__['js_object'];
  var pointer = __args__['pointer'];
  self["$wrapped"] = __jsdict([]);
  if (( pointer ) !== null) {
    self["$wrapped"] = pointer;
  } else {
    if (__test_if_true__(js_object)) {
      ob = js_object;
      if (__test_if_true__(ob instanceof Array)) {
        var o,__iterator__45;
        __iterator__45 = __get__(__get__(ob, "__iter__", "no iterator - line 1196: for o in ob:"), "__call__")([], __NULL_OBJECT__);
        var __next__45;
        __next__45 = __get__(__iterator__45, "next");
        while (( __iterator__45.index ) < __iterator__45.length) {
          o = __next__45();
          if (o instanceof Array) {
            k = o[0];
            v = o[1];
          } else {
            k = o["key"];
            v = o["value"];
          }
                    try {
__get__(__get__(self, "__setitem__", "missing attribute `__setitem__` - line 1203: self.__setitem__( k,v )"), "__call__")([k, v], __NULL_OBJECT__);
          } catch(__exception__) {
if (__exception__ == KeyError || __exception__ instanceof KeyError) {
throw new KeyError("error in dict init, bad key");
}

}
        }
      } else {
        if (__test_if_true__(isinstance([ob, dict], __NULL_OBJECT__))) {
          var key,__iterator__46;
          __iterator__46 = __get__(__get__(__jsdict_keys(ob), "__iter__", "no iterator - line 1207: for key in ob.keys():"), "__call__")([], __NULL_OBJECT__);
          var __next__46;
          __next__46 = __get__(__iterator__46, "next");
          while (( __iterator__46.index ) < __iterator__46.length) {
            key = __next__46();
            value = ((ob instanceof Array) ? ob[key] : __get__(ob, "__getitem__", "line 1208: value = ob[ key ]")([key], __NULL_OBJECT__));
            __get__(__get__(self, "__setitem__", "missing attribute `__setitem__` - line 1209: self.__setitem__( key, value )"), "__call__")([key, value], __NULL_OBJECT__);
          }
        } else {
          console.log(["ERROR init dict from:", js_object]);
          throw new TypeError;
        }
      }
    }
  }
};__dict___init__.is_wrapper = true;
__dict_attrs.__init__ = __dict___init__;
var __dict_jsify = function(args, kwargs) {
  var keys,value;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_jsify", __sig__, args, kwargs);
  var self = __args__['self'];
  keys = __object_keys__([self["$wrapped"]], __NULL_OBJECT__);
  var key,__iterator__47;
  __iterator__47 = __get__(__get__(keys, "__iter__", "no iterator - line 1216: for key in keys:"), "__call__")([], __NULL_OBJECT__);
  var __next__47;
  __next__47 = __get__(__iterator__47, "next");
  while (( __iterator__47.index ) < __iterator__47.length) {
    key = __next__47();
    value = __get__(self["$wrapped"], "__getitem__", "line 1217: value = self[...][key]")([key], __NULL_OBJECT__);
    if ((typeof(value) instanceof Array ? JSON.stringify(typeof(value))==JSON.stringify("object") : typeof(value)==="object")) {
      if (__test_if_true__(hasattr([value, "jsify"], __NULL_OBJECT__))) {
        __get__(__get__(self["$wrapped"], "__setitem__"), "__call__")([key, __get__(__get__(value, "jsify", "missing attribute `jsify` - line 1220: self[...][key] = value.jsify()"), "__call__")()], {});
      }
    } else {
      if ((typeof(value) instanceof Array ? JSON.stringify(typeof(value))==JSON.stringify("function") : typeof(value)==="function")) {
        throw new RuntimeError("can not jsify function");
      }
    }
  }
  return self["$wrapped"];
};__dict_jsify.is_wrapper = true;
__dict_attrs.jsify = __dict_jsify;
var __dict_copy = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_copy", __sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(dict, "__call__")([self], __NULL_OBJECT__);
};__dict_copy.is_wrapper = true;
__dict_attrs.copy = __dict_copy;
var __dict_clear = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_clear", __sig__, args, kwargs);
  var self = __args__['self'];
  self["$wrapped"] = __jsdict([]);
};__dict_clear.is_wrapper = true;
__dict_attrs.clear = __dict_clear;
var __dict_has_key = function(args, kwargs) {
  var __dict;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "key"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_has_key", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  __dict = self["$wrapped"];
  if (__test_if_true__(typeof(key) === 'object' || typeof(key) === 'function')) {
    key = __get__(key, "__uid__", "missing attribute `__uid__` - line 1233: key = key.__uid__");
  }
  if (__test_if_true__(key in __dict)) {
    return true;
  } else {
    return false;
  }
};__dict_has_key.is_wrapper = true;
__dict_attrs.has_key = __dict_has_key;
var __dict_update = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "other"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_update", __sig__, args, kwargs);
  var self = __args__['self'];
  var other = __args__['other'];
  var key,__iterator__48;
  __iterator__48 = __get__(__get__(other, "__iter__", "no iterator - line 1239: for key in other:"), "__call__")([], __NULL_OBJECT__);
  var __next__48;
  __next__48 = __get__(__iterator__48, "next");
  while (( __iterator__48.index ) < __iterator__48.length) {
    key = __next__48();
    __get__(__get__(self, "__setitem__", "missing attribute `__setitem__` - line 1240: self.__setitem__( key, other[key] )"), "__call__")([key, ((other instanceof Array) ? other[key] : __get__(other, "__getitem__", "line 1240: self.__setitem__( key, other[key] )")([key], __NULL_OBJECT__))], __NULL_OBJECT__);
  }
};__dict_update.is_wrapper = true;
__dict_attrs.update = __dict_update;
var __dict_items = function(args, kwargs) {
  var arr;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_items", __sig__, args, kwargs);
  var self = __args__['self'];
  arr = [];
  var key,__iterator__49;
  __iterator__49 = __get__(__get__(__jsdict_keys(self), "__iter__", "no iterator - line 1243: for key in self.keys():"), "__call__")([], __NULL_OBJECT__);
  var __next__49;
  __next__49 = __get__(__iterator__49, "next");
  while (( __iterator__49.index ) < __iterator__49.length) {
    key = __next__49();
    __get__(__get__(arr, "append", "missing attribute `append` - line 1244: arr.append( [key, self[key]] )"), "__call__")([[key, __get__(self, "__getitem__")([key], __NULL_OBJECT__)]], __NULL_OBJECT__);
  }
  return arr;
};__dict_items.is_wrapper = true;
__dict_attrs.items = __dict_items;
var __dict_get = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{"_default": null},args:["self", "key", "_default"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_get", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var _default = __args__['_default'];
    try {
return __get__(self, "__getitem__")([key], __NULL_OBJECT__);
  } catch(__exception__) {
return _default;

}
};__dict_get.is_wrapper = true;
__dict_attrs.get = __dict_get;
var __dict_set = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "key", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_set", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var value = __args__['value'];
  __get__(__get__(self, "__setitem__", "missing attribute `__setitem__` - line 1252: self.__setitem__(key, value)"), "__call__")([key, value], __NULL_OBJECT__);
};__dict_set.is_wrapper = true;
__dict_attrs.set = __dict_set;
var __dict___len__ = function(args, kwargs) {
  var __dict;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___len__", __sig__, args, kwargs);
  var self = __args__['self'];
  __dict = self["$wrapped"];
  return Object.keys(__dict).length;
};__dict___len__.is_wrapper = true;
__dict_attrs.__len__ = __dict___len__;
var __dict___getitem__ = function(args, kwargs) {
  var __dict,msg,err;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "key"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___getitem__", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  "\n		note: `\"4\"` and `4` are the same key in javascript, is there a sane way to workaround this,\n		that can remain compatible with external javascript?\n		";
  __dict = self["$wrapped"];
  err = false;
  if (__test_if_true__(key instanceof Array)) {
    key = __tuple_key__(key);
  } else {
    if (__test_if_true__(typeof(key) === 'object' || typeof(key) === 'function')) {
      if (__test_if_true__(key.__uid__ && key.__uid__ in __dict)) {
        return __dict[key.__uid__];
      } else {
        err = true;
      }
    }
  }
  if (__test_if_true__((__dict && key in __dict))) {
    return __dict[key];
  } else {
    err = true;
  }
  if (__test_if_true__(err)) {
    msg = __sprintf("missing key: %s -\n", key);
    throw new KeyError(__jsdict_keys(__dict));
  }
};__dict___getitem__.is_wrapper = true;
__dict_attrs.__getitem__ = __dict___getitem__;
var __dict___setitem__ = function(args, kwargs) {
  var __dict;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "key", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___setitem__", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var value = __args__['value'];
  if (( key ) === undefined) {
    throw new KeyError("undefined is invalid key type");
  }
  if (( key ) === null) {
    throw new KeyError("null is invalid key type");
  }
  __dict = self["$wrapped"];
  if (__test_if_true__(key instanceof Array)) {
    key = __tuple_key__(key);
    if (( key ) === undefined) {
      throw new KeyError("undefined is invalid key type (tuple)");
    }
    __dict[key] = value;
  } else {
    if (__test_if_true__(typeof(key) === 'object' || typeof(key) === 'function')) {
      if (__test_if_true__(key.__uid__ === undefined)) {
        key.__uid__ = 'ï¿¼' + _PythonJS_UID++;
      }
      __dict[key.__uid__] = value;
    } else {
      __dict[key] = value;
    }
  }
};__dict___setitem__.is_wrapper = true;
__dict_attrs.__setitem__ = __dict___setitem__;
var __dict_keys = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_keys", __sig__, args, kwargs);
  var self = __args__['self'];
  return Object.keys(self["$wrapped"]);
};__dict_keys.is_wrapper = true;
__dict_attrs.keys = __dict_keys;
var __dict_pop = function(args, kwargs) {
  var js_object,v;
  var __sig__,__args__;
  __sig__ = { kwargs:{"d": null},args:["self", "key", "d"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_pop", __sig__, args, kwargs);
  var self = __args__['self'];
  var key = __args__['key'];
  var d = __args__['d'];
  v = __jsdict_get(self, key, null);
  if (( v ) === null) {
    return d;
  } else {
    js_object = self["$wrapped"];
    delete js_object[key];
    return v;
  }
};__dict_pop.is_wrapper = true;
__dict_attrs.pop = __dict_pop;
var __dict_values = function(args, kwargs) {
  var keys,out;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict_values", __sig__, args, kwargs);
  var self = __args__['self'];
  keys = Object.keys(self["$wrapped"]);
  out = [];
    var __iter34 = keys;
  if (! (__iter34 instanceof Array || typeof __iter34 == "string" || __is_typed_array(__iter34) || __is_some_array(__iter34) )) { __iter34 = __object_keys__(__iter34) }
  for (var __idx34=0; __idx34 < __iter34.length; __idx34++) {
    var key = __iter34[ __idx34 ];
    out.push(self["$wrapped"][key]);
  }
  return out;
};__dict_values.is_wrapper = true;
__dict_attrs.values = __dict_values;
var __dict___contains__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___contains__", __sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
    try {
__dict___getitem__([self, value], {});
return true;
  } catch(__exception__) {
return false;

}
};__dict___contains__.is_wrapper = true;
__dict_attrs.__contains__ = __dict___contains__;
var __dict___iter__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__dict___iter__", __sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([__jsdict_keys(self), 0], __NULL_OBJECT__);
};__dict___iter__.is_wrapper = true;
__dict_attrs.__iter__ = __dict___iter__;
dict = __create_class__("dict", __dict_parents, __dict_attrs, __dict_properties);
var set = function(args, kwargs) {
  var keys,mask,s,hashtable,key,fallback;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("set", __sig__, args, kwargs);
  var a = __args__['a'];
  "\n	This returns an array that is a minimal implementation of set.\n	Often sets are used simply to remove duplicate entries from a list, \n	and then it get converted back to a list, it is safe to use fastset for this.\n	The array prototype is overloaded with basic set functions:\n		difference\n		intersection\n		issubset\n	Note: sets in Python are not subscriptable, but can be iterated over.\n	Python docs say that set are unordered, some programs may rely on this disorder\n	for randomness, for sets of integers we emulate the unorder only uppon initalization \n	of the set, by masking the value by bits-1. Python implements sets starting with an \n	array of length 8, and mask of 7, if set length grows to 6 (3/4th), then it allocates \n	a __new__>>array of length 32 and mask of 31.  This is only emulated for arrays of \n	integers up to an array length of 1536.\n	";
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
        var __iter35 = a;
    if (! (__iter35 instanceof Array || typeof __iter35 == "string" || __is_typed_array(__iter35) || __is_some_array(__iter35) )) { __iter35 = __object_keys__(__iter35) }
    for (var __idx35=0; __idx35 < __iter35.length; __idx35++) {
      var b = __iter35[ __idx35 ];
      if (__test_if_true__(((typeof(b) instanceof Array ? JSON.stringify(typeof(b))==JSON.stringify("number") : typeof(b)==="number") && ( b ) === ( (b | 0) )))) {
        key = (b & mask);
        hashtable[key] = b;
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
        var __iter36 = a;
    if (! (__iter36 instanceof Array || typeof __iter36 == "string" || __is_typed_array(__iter36) || __is_some_array(__iter36) )) { __iter36 = __object_keys__(__iter36) }
    for (var __idx36=0; __idx36 < __iter36.length; __idx36++) {
      var item = __iter36[ __idx36 ];
      if ((s.indexOf(item) instanceof Array ? JSON.stringify(s.indexOf(item))==JSON.stringify(-1) : s.indexOf(item)===-1)) {
        s.push(item);
      }
    }
  } else {
    __sort_method(keys);
        var __iter37 = keys;
    if (! (__iter37 instanceof Array || typeof __iter37 == "string" || __is_typed_array(__iter37) || __is_some_array(__iter37) )) { __iter37 = __object_keys__(__iter37) }
    for (var __idx37=0; __idx37 < __iter37.length; __idx37++) {
      var key = __iter37[ __idx37 ];
      s.push(hashtable[key]);
    }
  }
  return s;
};set.is_wrapper = true;
var frozenset = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["a"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("frozenset", __sig__, args, kwargs);
  var a = __args__['a'];
  return set([a], __NULL_OBJECT__);
};frozenset.is_wrapper = true;
var array,__array_attrs,__array_parents;
__array_attrs = {};
__array_parents = [];
__array_properties = {};
__array_typecodes = __jsdict([["c", 1], ["b", 1], ["B", 1], ["u", 2], ["h", 2], ["H", 2], ["i", 4], ["I", 4], ["l", 4], ["L", 4], ["f", 4], ["d", 8], ["float32", 4], ["float16", 2], ["float8", 1], ["int32", 4], ["uint32", 4], ["int16", 2], ["uint16", 2], ["int8", 1], ["uint8", 1]]);
__array_attrs.typecodes = __array_typecodes;
__array_typecode_names = __jsdict([["c", "Int8"], ["b", "Int8"], ["B", "Uint8"], ["u", "Uint16"], ["h", "Int16"], ["H", "Uint16"], ["i", "Int32"], ["I", "Uint32"], ["f", "Float32"], ["d", "Float64"], ["float32", "Float32"], ["float16", "Int16"], ["float8", "Int8"], ["int32", "Int32"], ["uint32", "Uint32"], ["int16", "Int16"], ["uint16", "Uint16"], ["int8", "Int8"], ["uint8", "Uint8"]]);
__array_attrs.typecode_names = __array_typecode_names;
var __array___init__ = function(args, kwargs) {
  var size,buff;
  var __sig__,__args__;
  __sig__ = { kwargs:{"initializer": null, "little_endian": false},args:["self", "typecode", "initializer", "little_endian"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___init__", __sig__, args, kwargs);
  var self = __args__['self'];
  var typecode = __args__['typecode'];
  var initializer = __args__['initializer'];
  var little_endian = __args__['little_endian'];
  self.typecode = typecode;
  self.itemsize = __get__(__get__(self, "typecodes", "missing attribute `typecodes` - line 1436: self.itemsize = self.typecodes[ typecode ]"), "__getitem__", "line 1436: self.itemsize = self.typecodes[ typecode ]")([typecode], __NULL_OBJECT__);
  self.little_endian = little_endian;
  if (__test_if_true__(initializer)) {
    self.length = len([initializer], __NULL_OBJECT__);
    self.bytes = (self.length * self.itemsize);
    if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float8") : self.typecode==="float8")) {
      self._scale = max([[abs([min([initializer], __NULL_OBJECT__)], __NULL_OBJECT__), max([initializer], __NULL_OBJECT__)]], __NULL_OBJECT__);
      self._norm_get = (self._scale / 127);
      self._norm_set = (1.0 / self._norm_get);
    } else {
      if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float16") : self.typecode==="float16")) {
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
  __get__(__get__(self, "fromlist", "missing attribute `fromlist` - line 1457: self.fromlist( initializer )"), "__call__")([initializer], __NULL_OBJECT__);
};__array___init__.is_wrapper = true;
__array_attrs.__init__ = __array___init__;
var __array___len__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___len__", __sig__, args, kwargs);
  var self = __args__['self'];
  return self.length;
};__array___len__.is_wrapper = true;
__array_attrs.__len__ = __array___len__;
var __array___contains__ = function(args, kwargs) {
  var arr;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___contains__", __sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
  arr = __get__(__get__(self, "to_array", "missing attribute `to_array` - line 1463: arr = self.to_array()"), "__call__")();
  if ((arr.indexOf(value) instanceof Array ? JSON.stringify(arr.indexOf(value))==JSON.stringify(-1) : arr.indexOf(value)===-1)) {
    return false;
  } else {
    return true;
  }
};__array___contains__.is_wrapper = true;
__array_attrs.__contains__ = __array___contains__;
var __array___getitem__ = function(args, kwargs) {
  var func_name,dataview,value,step,func,offset;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "index"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___getitem__", __sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  step = self.itemsize;
  offset = (step * index);
  dataview = self.dataview;
  func_name = ("get" + __get__(__get__(self, "typecode_names", "missing attribute `typecode_names` - line 1471: func_name = 'get'+self.typecode_names[ self.typecode ]"), "__getitem__", "line 1471: func_name = 'get'+self.typecode_names[ self.typecode ]")([self.typecode], __NULL_OBJECT__));
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    value = func(offset);
    if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float8") : self.typecode==="float8")) {
      value = (value * self._norm_get);
    } else {
      if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float16") : self.typecode==="float16")) {
        value = (value * self._norm_get);
      }
    }
    return value;
  } else {
    throw new IndexError(index);
  }
};__array___getitem__.is_wrapper = true;
__array_attrs.__getitem__ = __array___getitem__;
var __array___setitem__ = function(args, kwargs) {
  var func_name,dataview,step,func,offset;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "index", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___setitem__", __sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  var value = __args__['value'];
  step = self.itemsize;
  if (( index ) < 0) {
    index = ((self.length + index) - 1);
  }
  offset = (step * index);
  dataview = self.dataview;
  func_name = ("set" + __get__(__get__(self, "typecode_names", "missing attribute `typecode_names` - line 1487: func_name = 'set'+self.typecode_names[ self.typecode ]"), "__getitem__", "line 1487: func_name = 'set'+self.typecode_names[ self.typecode ]")([self.typecode], __NULL_OBJECT__));
  func = dataview[func_name].bind(dataview);
  if (( offset ) < self.bytes) {
    if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float8") : self.typecode==="float8")) {
      value = (value * self._norm_set);
    } else {
      if ((self.typecode instanceof Array ? JSON.stringify(self.typecode)==JSON.stringify("float16") : self.typecode==="float16")) {
        value = (value * self._norm_set);
      }
    }
    func(offset, value);
  } else {
    throw new IndexError(index);
  }
};__array___setitem__.is_wrapper = true;
__array_attrs.__setitem__ = __array___setitem__;
var __array___iter__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array___iter__", __sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(Iterator, "__call__")([self, 0], __NULL_OBJECT__);
};__array___iter__.is_wrapper = true;
__array_attrs.__iter__ = __array___iter__;
var __array_get = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "index"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_get", __sig__, args, kwargs);
  var self = __args__['self'];
  var index = __args__['index'];
  return __array___getitem__([self, index], {});
};__array_get.is_wrapper = true;
__array_attrs.get = __array_get;
var __array_fromlist = function(args, kwargs) {
  var typecode,i,func_name,dataview,length,item,step,func,offset,size;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "lst"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_fromlist", __sig__, args, kwargs);
  var self = __args__['self'];
  var lst = __args__['lst'];
  length = len([lst], __NULL_OBJECT__);
  step = self.itemsize;
  typecode = self.typecode;
  size = (length * step);
  dataview = self.dataview;
  func_name = ("set" + __get__(__get__(self, "typecode_names", "missing attribute `typecode_names` - line 1507: func_name = 'set'+self.typecode_names[ typecode ]"), "__getitem__", "line 1507: func_name = 'set'+self.typecode_names[ typecode ]")([typecode], __NULL_OBJECT__));
  func = dataview[func_name].bind(dataview);
  if (( size ) <= self.bytes) {
    i = 0;
    offset = 0;
    while (( i ) < length) {
      item = ((lst instanceof Array) ? lst[i] : __get__(lst, "__getitem__", "line 1512: item = lst[i]")([i], __NULL_OBJECT__));
      if ((typecode instanceof Array ? JSON.stringify(typecode)==JSON.stringify("float8") : typecode==="float8")) {
        item *= self._norm_set;
      } else {
        if ((typecode instanceof Array ? JSON.stringify(typecode)==JSON.stringify("float16") : typecode==="float16")) {
          item *= self._norm_set;
        }
      }
      func(offset,item);
      offset += step;
      i += 1;
    }
  } else {
    throw new TypeError;
  }
};__array_fromlist.is_wrapper = true;
__array_attrs.fromlist = __array_fromlist;
var __array_resize = function(args, kwargs) {
  var source,new_buff,target,new_size,buff;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "length"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_resize", __sig__, args, kwargs);
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
};__array_resize.is_wrapper = true;
__array_attrs.resize = __array_resize;
var __array_append = function(args, kwargs) {
  var length;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "value"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_append", __sig__, args, kwargs);
  var self = __args__['self'];
  var value = __args__['value'];
  length = self.length;
  __get__(__get__(self, "resize", "missing attribute `resize` - line 1535: self.resize( self.length + 1 )"), "__call__")([(self.length + 1)], __NULL_OBJECT__);
  __get__(__get__(self, "__setitem__"), "__call__")([length, value], {});
};__array_append.is_wrapper = true;
__array_attrs.append = __array_append;
var __array_extend = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "lst"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_extend", __sig__, args, kwargs);
  var self = __args__['self'];
  var lst = __args__['lst'];
  var value,__iterator__54;
  __iterator__54 = __get__(__get__(lst, "__iter__", "no iterator - line 1538: for value in lst:"), "__call__")([], __NULL_OBJECT__);
  var __next__54;
  __next__54 = __get__(__iterator__54, "next");
  while (( __iterator__54.index ) < __iterator__54.length) {
    value = __next__54();
    __get__(__get__(self, "append", "missing attribute `append` - line 1539: self.append( value )"), "__call__")([value], __NULL_OBJECT__);
  }
};__array_extend.is_wrapper = true;
__array_attrs.extend = __array_extend;
var __array_to_array = function(args, kwargs) {
  var i,item,arr;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_to_array", __sig__, args, kwargs);
  var self = __args__['self'];
  arr = [];
  i = 0;
  while (( i ) < self.length) {
    item = __array___getitem__([self, i], {});
    arr.push( item );
    i += 1;
  }
  return arr;
};__array_to_array.is_wrapper = true;
__array_attrs.to_array = __array_to_array;
var __array_to_list = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_to_list", __sig__, args, kwargs);
  var self = __args__['self'];
  return __get__(__get__(self, "to_array", "missing attribute `to_array` - line 1549: return self.to_array()"), "__call__")();
};__array_to_list.is_wrapper = true;
__array_attrs.to_list = __array_to_list;
var __array_to_ascii = function(args, kwargs) {
  var i,length,arr,string;
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__array_to_ascii", __sig__, args, kwargs);
  var self = __args__['self'];
  string = "";
  arr = __get__(__get__(self, "to_array", "missing attribute `to_array` - line 1552: arr = self.to_array()"), "__call__")();
  i = 0;
  length = __get__(arr, "length", "missing attribute `length` - line 1553: i = 0; length = arr.length");
  while (( i ) < length) {
    var num = arr[i];
    var char = String.fromCharCode(num);
    string += char;
    i += 1;
  }
  return string;
};__array_to_ascii.is_wrapper = true;
__array_attrs.to_ascii = __array_to_ascii;
array = __create_class__("array", __array_parents, __array_attrs, __array_properties);
var file,__file_attrs,__file_parents;
__file_attrs = {};
__file_parents = [];
__file_properties = {};
var __file___init__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self", "path", "flags"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__file___init__", __sig__, args, kwargs);
  var self = __args__['self'];
  var path = __args__['path'];
  var flags = __args__['flags'];
  self.path = path;
  if ((flags instanceof Array ? JSON.stringify(flags)==JSON.stringify("rb") : flags==="rb")) {
    self.flags = "r";
    self.binary = true;
  } else {
    if ((flags instanceof Array ? JSON.stringify(flags)==JSON.stringify("wb") : flags==="wb")) {
      self.flags = "w";
      self.binary = true;
    } else {
      self.flags = flags;
      self.binary = false;
    }
  }
  self.flags = flags;
};__file___init__.is_wrapper = true;
__file_attrs.__init__ = __file___init__;
var __file_read = function(args, kwargs) {
  var _fs,path;
  var __sig__,__args__;
  __sig__ = { kwargs:{"binary": false},args:["self", "binary"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__file_read", __sig__, args, kwargs);
  var self = __args__['self'];
  var binary = __args__['binary'];
  _fs = __get__(require, "__call__")(["fs"], __NULL_OBJECT__);
  path = self.path;
  if (__test_if_true__((binary || self.binary))) {
    return _fs.readFileSync(path, { encoding:null });
  } else {
    return _fs.readFileSync(path, __jsdict([["encoding", "utf8"]]));
  }
};__file_read.is_wrapper = true;
__file_attrs.read = __file_read;
var __file_write = function(args, kwargs) {
  var path,buff,_fs;
  var __sig__,__args__;
  __sig__ = { kwargs:{"binary": false},args:["self", "data", "binary"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__file_write", __sig__, args, kwargs);
  var self = __args__['self'];
  var data = __args__['data'];
  var binary = __args__['binary'];
  _fs = __get__(require, "__call__")(["fs"], __NULL_OBJECT__);
  path = self.path;
  if (__test_if_true__((binary || self.binary))) {
    binary = (binary || self.binary);
    if ((binary instanceof Array ? JSON.stringify(binary)==JSON.stringify("base64") : binary==="base64")) {
      buff =  new Buffer(data, "base64");
      _fs.writeFileSync(path, buff, __jsdict([["encoding", null]]));
    } else {
      _fs.writeFileSync(path, data, __jsdict([["encoding", null]]));
    }
  } else {
    _fs.writeFileSync(path, data, __jsdict([["encoding", "utf8"]]));
  }
};__file_write.is_wrapper = true;
__file_attrs.write = __file_write;
var __file_close = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{},args:["self"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__file_close", __sig__, args, kwargs);
  var self = __args__['self'];
  /*pass*/
};__file_close.is_wrapper = true;
__file_attrs.close = __file_close;
file = __create_class__("file", __file_parents, __file_attrs, __file_properties);
var __open__ = function(args, kwargs) {
  
  var __sig__,__args__;
  __sig__ = { kwargs:{"mode": null},args:["path", "mode"] };
  if ((args instanceof Array && (Object.prototype.toString.call(kwargs) instanceof Array ? JSON.stringify(Object.prototype.toString.call(kwargs))==JSON.stringify("[object Object]") : Object.prototype.toString.call(kwargs)==="[object Object]") && (arguments.length instanceof Array ? JSON.stringify(arguments.length)==JSON.stringify(2) : arguments.length===2))) {
    /*pass*/
  } else {
    args = Array.prototype.slice.call(arguments, 0, __sig__.args.length);
    kwargs = {};
  }
  __args__ = __getargs__("__open__", __sig__, args, kwargs);
  var path = __args__['path'];
  var mode = __args__['mode'];
  return __get__(file, "__call__")([path, mode], __NULL_OBJECT__);
};__open__.is_wrapper = true;
json = __jsdict([["loads", (function (s) {return JSON.parse(s);})], ["dumps", (function (o) {return JSON.stringify(o);})]]);
var __get_other_workers_with_shared_arg = function(worker, ob) {
  var a,other,args;
  a = [];
    var __iter38 = threading.workers;
  if (! (__iter38 instanceof Array || typeof __iter38 == "string" || __is_typed_array(__iter38) || __is_some_array(__iter38) )) { __iter38 = __object_keys__(__iter38) }
  for (var __idx38=0; __idx38 < __iter38.length; __idx38++) {
    var b = __iter38[ __idx38 ];
    other = b["worker"];
    args = b["args"];
    if (( other ) !== worker) {
            var __iter39 = args;
      if (! (__iter39 instanceof Array || typeof __iter39 == "string" || __is_typed_array(__iter39) || __is_some_array(__iter39) )) { __iter39 = __object_keys__(__iter39) }
      for (var __idx39=0; __idx39 < __iter39.length; __idx39++) {
        var arg = __iter39[ __idx39 ];
        if (( arg ) === ob) {
          if (! (__contains__(a, other))) {
            a.append(other);
          }
        }
      }
    }
  }
  return a;
}

threading = __jsdict([["workers", []], ["_blocking_callback", null]]);
var __start_new_thread = function(f, args) {
  var jsargs,worker;
  worker =  new Worker(f);
  worker.__uid__ = len(threading.workers);
  threading.workers.append(__jsdict([["worker", worker], ["args", args]]));
      var func = function(event) {
    var a,res,value;
    if ((event.data.type instanceof Array ? JSON.stringify(event.data.type)==JSON.stringify("terminate") : event.data.type==="terminate")) {
      worker.terminate();
    } else {
      if ((event.data.type instanceof Array ? JSON.stringify(event.data.type)==JSON.stringify("call") : event.data.type==="call")) {
        res = __module__[event.data.function].apply(null, event.data.args);
        if (__test_if_true__((( res ) !== null && ( res ) !== undefined))) {
          worker.postMessage(__jsdict([["type", "return_to_blocking_callback"], ["result", res]]));
        }
      } else {
        if ((event.data.type instanceof Array ? JSON.stringify(event.data.type)==JSON.stringify("append") : event.data.type==="append")) {
          a = args[event.data.argindex];
          a.push(event.data.value);
                    var __iter40 = __get_other_workers_with_shared_arg(worker, a);
          if (! (__iter40 instanceof Array || typeof __iter40 == "string" || __is_typed_array(__iter40) || __is_some_array(__iter40) )) { __iter40 = __object_keys__(__iter40) }
          for (var __idx40=0; __idx40 < __iter40.length; __idx40++) {
            var other = __iter40[ __idx40 ];
            other.postMessage(__jsdict([["type", "append"], ["argindex", event.data.argindex], ["value", event.data.value]]));
          }
        } else {
          if ((event.data.type instanceof Array ? JSON.stringify(event.data.type)==JSON.stringify("__setitem__") : event.data.type==="__setitem__")) {
            a = args[event.data.argindex];
            value = event.data.value;
            if (__test_if_true__(a.__setitem__)) {
              a.__setitem__(event.data.index, value);
            } else {
              a[event.data.index] = value;
            }
                        var __iter41 = __get_other_workers_with_shared_arg(worker, a);
            if (! (__iter41 instanceof Array || typeof __iter41 == "string" || __is_typed_array(__iter41) || __is_some_array(__iter41) )) { __iter41 = __object_keys__(__iter41) }
            for (var __idx41=0; __idx41 < __iter41.length; __idx41++) {
              var other = __iter41[ __idx41 ];
              other.postMessage(__jsdict([["type", "__setitem__"], ["argindex", event.data.argindex], ["key", event.data.index], ["value", event.data.value]]));
            }
          } else {
            throw new RuntimeError("unknown event");
          }
        }
      }
    }
  }

  worker.onmessage = func;
  jsargs = [];
  var i;
  i = 0;
    var __iter42 = args;
  if (! (__iter42 instanceof Array || typeof __iter42 == "string" || __is_typed_array(__iter42) || __is_some_array(__iter42) )) { __iter42 = __object_keys__(__iter42) }
  for (var __idx42=0; __idx42 < __iter42.length; __idx42++) {
    var arg = __iter42[ __idx42 ];
    if (__test_if_true__(arg.jsify)) {
      jsargs.append(arg.jsify());
    } else {
      jsargs.append(arg);
    }
    if (__test_if_true__(arg instanceof Array)) {
      __gen_worker_append(worker, arg, i);
    }
    i += 1;
  }
  worker.postMessage(__jsdict([["type", "execute"], ["args", jsargs]]));
  return worker;
}

var __gen_worker_append = function(worker, ob, index) {
  
      var append = function(item) {
    
    worker.postMessage(__jsdict([["type", "append"], ["argindex", index], ["value", item]]));
    ob.push(item);
  }

  Object.defineProperty(ob, "append", __jsdict([["enumerable", false], ["value", append], ["writeable", true], ["configurable", true]]));
}

var __webworker_wrap = function(ob, argindex) {
  
  if (__test_if_true__(ob instanceof Array)) {
            var func = function(index, item) {
      
      postMessage(__jsdict([["type", "__setitem__"], ["index", index], ["value", item], ["argindex", argindex]]));
      Array.prototype.__setitem__.call(ob, index, item);
    }

    Object.defineProperty(ob, "__setitem__", __jsdict([["enumerable", false], ["value", func], ["writeable", true], ["configurable", true]]));
            var func = function(item) {
      
      postMessage(__jsdict([["type", "append"], ["value", item], ["argindex", argindex]]));
      Array.prototype.push.call(ob, item);
    }

    Object.defineProperty(ob, "append", __jsdict([["enumerable", false], ["value", func], ["writeable", true], ["configurable", true]]));
  } else {
    if ((typeof(ob) instanceof Array ? JSON.stringify(typeof(ob))==JSON.stringify("object") : typeof(ob)==="object")) {
                  var func = function(key, item) {
        
        postMessage(__jsdict([["type", "__setitem__"], ["index", key], ["value", item], ["argindex", argindex]]));
        ob[key] = item;
      }

      Object.defineProperty(ob, "__setitem__", __jsdict([["enumerable", false], ["value", func], ["writeable", true], ["configurable", true]]));
    }
  }
  return ob;
}

var __rpc__ = function(url, func, args) {
  var req;
  req =  new XMLHttpRequest();
  req.open("POST", url, false);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify(__jsdict([["call", func], ["args", args]])));
  return JSON.parse(req.responseText);
}

var __rpc_iter__ = function(url, attr) {
  var req;
  req =  new XMLHttpRequest();
  req.open("POST", url, false);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify(__jsdict([["iter", attr]])));
  return JSON.parse(req.responseText);
}

var __rpc_set__ = function(url, attr, value) {
  var req;
  req =  new XMLHttpRequest();
  req.open("POST", url, false);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify(__jsdict([["set", attr], ["value", value]])));
}

var __rpc_get__ = function(url, attr) {
  var req;
  req =  new XMLHttpRequest();
  req.open("POST", url, false);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify(__jsdict([["get", attr]])));
  return JSON.parse(req.responseText);
}
