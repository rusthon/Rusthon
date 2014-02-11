/**
   @license Copyright 2011 Maximilian Herkender

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

var lua_print = function () {
  try {
    console.log.apply(console, arguments);
  } catch (e) {
    // do nothing
  }
  return [];
};

function lua_load(chunk, chunkname) {
  if (!lua_parser) {
    throw new Error("Lua parser not available, perhaps you're not using the lua+parser.js version of the library?");
  }

  var fn;
  eval(
    "fn = function " + (chunkname || "load") + "() {\n" +
    "return (function () {\n" +
    lua_parser.parse(chunk) + "\n" +
    "})()[0];\n" +
    "};");
  return fn;
}

/*
   Copyright 2011 Maximilian Herkender

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

// slice that works in as3 and js on arguments
function slice(arr, start) {
  if (arr.slice) {
    return arr.slice(start);
  } else {
    return Array.prototype.slice.call(arr, start);
  }
}

// not supported call
function not_supported() {
  throw new Error("Not supported");
}

function ensure_arraymode(table) {
  if (!table.arraymode) {
    var newuints = [];
    for (var i in table.uints) {
      if (table.uints[i] != null) {
        newuints[i - 1] = table.uints[i];
      }
    }
    table.uints = newuints;
    table.arraymode = true;
  }
}
function ensure_notarraymode(table) {
  if (table.arraymode) {
    var newuints = {};
    for (var i in table.uints) {
      if (table.uints[i] != null) {
        newuints[i - -1] = table.uints[i];
      }
    }
    table.uints = newuints;
    delete table.arraymode;
  }
}

/** @constructor */
function ReturnValues(vars) {
  this.vars = vars || [];
}

// methods used by generated lua code
function lua_true(op) {
  return op != null && op !== false;
}
function lua_not(op) {
  return op == null || op === false;
}
function lua_and(op1, op2) {
  return op1 == null || op1 === false ? op1 : op2();
}
function lua_or(op1, op2) {
  return op1 != null && op1 !== false ? op1 : op2();
}
function lua_assertfloat(n) {
  var result = parseFloat(n);
  if (isNaN(result)) {
    throw new Error("Invalid number: " + n);
  }
  return result;
}
function lua_newtable(autoIndexList) {
  var result = {str: {}, uints: {}, floats: {}, bool: {}, objs: []};
  for (var i = 1; i < arguments.length - 1; i += 2) {
    var value = arguments[i + 1];
    if (value == null) {
      continue;
    }
    var key = arguments[i];
    switch (typeof key) {
      case "string":
        result.str[key] = value;
        break;
      case "number":
        if (key != key) {
          throw new Error("Table index is NaN");
        }
        if (key > 0 && (key | 0) == key) {
          result.uints[key] = value;
        } else {
          result.floats[key] = value;
        }
        break;
      case "boolean":
        result.bool[key] = value;
        break;
      case "object":
        if (key == null) {
          throw new Error("Table index is nil");
        }
        var bFound = false;
        for (var i in result.objs) {
          if (result.objs[i][0] === key) {
            if (value == null) {
              result.objs.splice(i, 1); // remove element [i]
            } else {
              bFound = true;
              // modify/overwrite existing entry
              // (could happen that same key is used twice in autoIndexList)
              result.objs[i][1] = value; 
            }
            break;
          }
        }
        if (!bFound) {
          result.objs.push([key,value]); // add new entry
        }
        break;
      default:
        throw new Error("Unsupported type for table: " + (typeof key));
    }
  }
  if (autoIndexList) {
    ensure_arraymode(result);
    if (result.uints.length == 0) {
      result.uints = autoIndexList;
    } else {
      i = autoIndexList.length;
      while (i-- > 0) {
        result.uints[i] = autoIndexList[i];
      }
    }
  }
  return result;
}
function lua_newtable2(str) {
  var str_copy = {};
  for (var i in str) {
    str_copy[i] = str[i];
  }
  return {str: str_copy, uints: {}, floats: {}, bool: {}, objs: {}};
}
function lua_len(op) {
  if (typeof op == "string") {
    return op.length;
  } else if (typeof op == "object" && op != null) {
    if (op.length == null) {
      var index = 0;
      if (op.arraymode) {
        while (op.uints[index++] != null) {};
        return op.length = index - 1;
      } else {
        while (op.uints[++index] != null) {};
        return op.length = index - 1;
      }
    } else {
      return op.length;
    }
  } else {
    var h = op.metatable && op.metatable.str["__len"];
    if (h) {
      return lua_rawcall(h, [op])[0];
    } else {
      throw new Error("Length of <" + op + "> not supported");
    }
  }
}
function lua_rawcall(func, args) {
  try {
    return func.apply(null, args);
  } catch (e) {
    if (e.constructor == ReturnValues) {
      return e.vars;
    }
    // This breaks the stack on Chrome
    // <http://code.google.com/p/chromium/issues/detail?id=60240>
    throw e;
  }
}

// could be replaced by lua_call(lua_tableget(table, key), args)
// but this gives better error messages
function lua_tablegetcall(table, key, args) {
  var func = lua_tableget(table, key);
  if (typeof func == "function") {
    return lua_rawcall(func, args);
  } else {
    if (func == null) {
      throw new Error("attempt to call field '" + key + "' (a nil value)");
    }
    var h = func.metatable && func.metatable.str["__call"];
    if (h != null) {
      return lua_rawcall(h, [func].concat(args));
    } else {
      throw new Error("Could not call " + func + " as function");
    }
  }
}
function lua_call(func, args) {
  if (typeof func == "function") {
    return lua_rawcall(func, args);
  } else {
    if (func == null) {
      throw new Error("attempt to call function (a nil value)");
    }
    var h = func.metatable && func.metatable.str["__call"];
    if (h != null) {
      return lua_rawcall(h, [func].concat(args));
    } else {
      throw new Error("Could not call " + func + " as function");
    }
  }
}
function lua_mcall(obj, methodname, args) {
  var func = lua_tableget(obj, methodname);
  if (func == null) {
    throw new Error("attempt to call method '" + methodname + "' (a nil value)");
  }
  return lua_call(func, [obj].concat(args));
}
function lua_eq(op1, op2) {
  if (typeof op1 != typeof op2) {
    if (op1 == null && op2 == null) {
      return true;
    }
    return false;
  }
  if (op1 == op2) {
    return true;
  }
  if (op1 == null || op2 == null) {
    return false;
  }
  var h = op1.metatable && op1.metatable.str["__eq"];
  if (h && h == (op2.metatable && op2.metatable.str["__eq"])) {
    return lua_true(lua_rawcall(h, [op1, op2])[0]);
  } else {
    return false;
  }
}
function lua_lt(op1, op2) {
  if (typeof op1 == "number" && typeof op2 == "number") {
    return op1 < op2;
  } else if (typeof op1 == "string" && typeof op2 == "string") {
    // TODO: not sure how similar lua/javascript string comparison is
    return op1 < op2;
  } else {
    var h = op1.metatable && op1.metatable.str["__lt"];
    if (h && h == (op2.metatable && op2.metatable.str["__lt"])) {
      return lua_true(lua_rawcall(h, [op1, op2])[0]);
    } else {
      throw new Error("Unable to compare " + op1 + " and " + op2);
    }
  }
}
function lua_lte(op1, op2) {
  if (typeof op1 == "number" && typeof op2 == "number") {
    return op1 <= op2;
  } else if (typeof op1 == "string" && typeof op2 == "string") {
    // TODO: not sure how similar lua/javascript string comparison is
    return op1 <= op2;
  } else {
    var h = op1.metatable && op1.metatable.str["__le"];
    if (h && h == (op2.metatable && op2.metatable.str["__le"])) {
      return lua_true(lua_rawcall(h, [op1, op2])[0]);
    } else {
      var h = op1.metatable && op1.metatable.str["__lt"];
      if (h && h == (op2.metatable && op2.metatable.str["__lt"])) {
        return lua_not(lua_rawcall(h, [op2, op1])[0]);
      } else {
        throw new Error("Unable to compare " + op1 + " and " + op2);
      }
    }
  }
}
function lua_unm(op) {
  var o = parseFloat(op);
  if (!isNaN(o)) {
    return -o;
  } else {
    var h = op.metatable && op.metatable.str["__unm"];
    if (h) {
      return lua_rawcall(h, [op])[0];
    } else {
      throw new Error("Inverting <" + op + "> not supported");
    }
  }
}
function lua_add(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__add"]) || (op2.metatable && op2.metatable.str["__add"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Adding <" + op1 + "> and <" + op2 + "> not supported");
    }
  } else {
    return o1 + o2;
  }
}
function lua_subtract(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__sub"]) || (op2.metatable && op2.metatable.str["__sub"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Subtracting <" + op1 + "> and <" + op2 + "> not supported");
    }
  } else {
    return o1 - o2;
  }
}
function lua_divide(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__div"]) || (op2.metatable && op2.metatable.str["__div"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Dividing <" + op1 + "> and <" + op2 + "> not supported");
    }
  } else {
    return o1 / o2;
  }
}
function lua_multiply(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__mul"]) || (op2.metatable && op2.metatable.str["__mul"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Multiplying <" + op1 + "> and <" + op2 + "> not supported");
    }
  } else {
    return o1 * o2;
  }
}
function lua_power(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__pow"]) || (op2.metatable && op2.metatable.str["__pow"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("<" + op1 + "> to the power of <" + op2 + "> not supported");
    }
  } else {
    return Math.pow(o1, o2);
  }
}
function lua_mod(op1, op2) {
  var o1 = parseFloat(op1), o2 = parseFloat(op2);
  if (isNaN(o1) || isNaN(o2)) {
    var h = (op1.metatable && op1.metatable.str["__mod"]) || (op2.metatable && op2.metatable.str["__mod"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Modulo <" + op1 + "> and <" + op2 + "> not supported");
    }
  } else {
    if (o1 >= 0) {
      if (o2 >= 0) {
        return o1 % o2;
      } else {
        return (o2 + (o1 % o2)) % o2;
      }
    } else {
      if (o2 >= 0) {
        return (o2 + (o1 % o2)) % o2;
      } else {
        return o1 % o2;
      }
    }
  }
}
function lua_rawget(table, key) {
  switch (typeof key) {
    case "string":
      return table.str[key];
    case "number":
      if (key != key) {
        throw new Error("Table index is NaN");
      }
      if (key > 0 && (key | 0) == key) {
        if (table.arraymode) {
          return table.uints[key - 1];
        } else {
          return table.uints[key];
        }
      } else {
        return table.floats[key];
      }
    case "boolean":
      return table.bool[key];
    case "object":
      if (key == null) {
        return null;
      }
      for (var i in table.objs) {
        if (table.objs[i][0] == key) {
          return table.objs[i][1];
        }
      }
	break;
    default:
      throw new Error("Unsupported key for table: " + (typeof key));
  }
}
function lua_rawset(table, key, value) {
  delete table.length;
  switch (typeof key) {
    case "string":
      if (value == null) {
        delete table.str[key];
      } else {
        table.str[key] = value;
      }
      break;
    case "number":
      if (key != key) {
        throw new Error("Table index is NaN");
      }
      if (key > 0 && (key | 0) == key) {
        ensure_notarraymode(table);
        if (value == null) {
          delete table.uints[key];
        } else {
          table.uints[key] = value;
        }
      } else {
        if (value == null) {
          delete table.floats[key];
        } else {
          table.floats[key] = value;
        }
      }
      break;
    case "boolean":
      if (value == null) {
        delete table.bool[key];
      } else {
        table.bool[key] = value;
      }
      break;
    case "object":
      if (key == null) {
        throw new Error("Table index is nil");
      }
      var bFound = false;
      for (var i in table.objs) {
        if (table.objs[i][0] == key) {
          if (value == null) {
            table.objs.splice(i,1); // remove element [i]
          } else {
            bFound = true;
            table.objs[i][1] = value; // modifiy/overwrite existing entry
          }
          break;
        }
      }
      if (!bFound) {
        table.objs.push([key,value]); // add new entry
      }
      break;
    default:
      throw new Error("Unsupported key for table: " + (typeof key));
  }
}
function lua_tableget(table, key) {
  if (table == null) {
    throw new Error("attempt to index field '" + key + "' in a nil value");
  }
  if (typeof table == "object") {
    var v = lua_rawget(table, key);
    if (v != null) {
      return v;
    }
    var h = table.metatable && table.metatable.str["__index"];
    if (h == null) {
      return null;
    }
  } else {
    var h = table.metatable && table.metatable.str["__index"];
    if (h == null) {
      throw new Error("Unable to index key " + key + " from " + table);
    }
  }
  if (typeof h == "function") {
    return lua_rawcall(h, [table, key])[0];
  } else {
    return lua_tableget(h, key);
  }
}
function lua_tableset(table, key, value) {
  if (table == null) {
    throw new Error("attempt to set field '" + key + "' in a nil value");
  }
  if (typeof table == "object") {
    var v = lua_rawget(table, key);
    if (v != null) {
      lua_rawset(table, key, value);
      return;
    }
    var h = table.metatable && table.metatable.str["__newindex"];
    if (h == null) {
      lua_rawset(table, key, value);
      return;
    }
  } else {
    var h = table.metatable && table.metatable.str["__newindex"];
    if (h == null) {
      throw new Error("Unable to set key " + key + " in table " + table);
    }
  }
  if (typeof h == "function") {
    lua_rawcall(h, [table, key, value]);
  } else {
    lua_tableset(h, key, value);
  }
}
function lua_concat(op1, op2) {
  if (typeof op1 == "number" && typeof op2 == "number") {
    throw new Error("number concat not supported yet");
  } else if ((typeof op1 == "string" || typeof op1 == "number") && (typeof op2 == "string" || typeof op2 == "number")) {
    return op1 + op2;
  } else {
    var h = (op1.metatable && op1.metatable.str["__concat"]) || (op2.metatable && op2.metatable.str["__concat"]);
    if (h) {
      return lua_rawcall(h, [op1, op2])[0];
    } else {
      throw new Error("Unable to concat " + op1 + " and " + op2);
    }
  }
}

// core lua functions
function _ipairs_next(table, index) {
  var entry;
  if (table.arraymode) {
    entry = table.uints[index];
  } else {
    entry = table.uints[index + 1];
  }
  if (entry == null) {
    return [null, null];
  }
  return [index + 1, entry];
}
var lua_libs = {};
var lua_core = {
  "assert": function (value, message) {
    if (arguments.length < 1) {
      message = "assertion failed!";
    }
    if (value != null && value !== false) {
      return [value];
    } else {
      throw new Error(message);
    }
  },
  "collectgarbage": function () {},// no-op
  "dofile": function () {
    not_supported();
  },
  "error": function (message, level) {
    // TODO: "level" is currently ignored
    throw new Error(message);
  },
  "getfenv": function (func, table) {
    not_supported();
  },
  "getmetatable": function (op) {
    return [op.metatable && (op.metatable.str["__metatable"] || op.metatable)];
  },
  "ipairs": function (table) {
    return [_ipairs_next, table, 0];
  },
  "load": function (func, chunkname) {
    var script = "", chunk;
    while ((chunk = func()) != null && chunk != "") {
      script += chunk;
    }
    try {
      return [lua_load(script, chunkname)];
    } catch (e) {
      return [null, e.message];
    }
  },
  "loadfile": function () {
    not_supported();
  },
  "loadstring": function (string, chunkname) {
    try {
      return [lua_load(string, chunkname)];
    } catch (e) {
      return [null, e.message];
    }
  },
  "next": function () {
    not_supported();
  },
  "pairs": function (table) {
    var props = [], i;
    for (i in table.str) {
      props.push(i);
    }
    if (table.arraymode) {
      var j = table.uints.length;
      while (j-- > 0) {
        if (table.uints[j] != null) {
          props.push(j + 1);
        }
      }
    } else {
      for (i in table.uints) {
        props.push(parseFloat(i));
      }
    }
    for (i in table.floats) {
      props.push(parseFloat(i));
    }
    for (i in table.bool) {
      props.push(i === "true" ? true : false);
    }
    for (i in table.objs) {
      props.push(table.objs[i][0]);
    }

    // okay, so I'm faking it here
    // regardless of what key is given, this function will return the next value
    // not sure how to do it the "right way" right now
    i = 0;
    return [function (table, key) {
      var entry;
      do {
        if (i >= props.length) {
          return [null, null];
        }
        key = props[i++];
        entry = lua_rawget(table, key);
      } while (entry == null);
      return [key, entry];
    }, table, null];
  },
  "pcall": function (func) {
    try {
      return [true].concat(func.apply(null, slice(arguments, 1)));
    } catch (e) {
      return [false, e.message];
    }
  },
  "print": lua_print,
  "rawequal": function (op1, op2) {
    return [(op1 == op2) || (op1 == null && op2 == null)];
  },
  "rawget": function (table, key) {
    if (typeof table == "object" && table != null) {
      return [lua_rawget(table, key)];
    }
    throw new Error("Unable to index key " + key + " from " + table);
  },
  "rawset": function (table, key, value) {
    if (typeof table == "object" && table != null && key != null) {
      lua_rawset(table, key, value);
      return [table];
    }
    throw new Error("Unable set key " + key + " in " + table);
  },
  "select": function (n) {
    if (n === "#") {
      return [arguments.length - 1];
    } else {
      n = lua_assertfloat(n);
      if (n >= 1) {
        return slice(arguments, lua_assertfloat(n));
      } else {
        throw new Error("Index out of range");
      }
    }
  },
  "setfenv": function (func, table) {
    not_supported();
  },
  "setmetatable": function (table, metatable) {
    if (typeof table != "object" || table == null) {
      throw new Error("table expected, got " + table);
    }
    if (metatable == null) {
      delete table.metatable;
    } else if (typeof metatable === "object") {
      table.metatable = metatable;
    } else {
      throw new Error("table or nil expected, got " + metatable);
    }
    return [table]
  },
  "tonumber": function (e, base) {
    if (typeof e == "number") {
      return [e];
    }
    if (base === 10 || base == null) {
      return [parseFloat(e)];
    } else {
      return [parseInt(e, base)];
    }
  },
  "tostring": function (e) {
    if (e == null) {
      return ["nil"];
    }
    var h = e.metatable && e.metatable.str["__tostring"];
    if (h) {
      return lua_rawcall(h, [e]);
    } else {
      switch (typeof(e)) {
        case "number":
        case "boolean":
          return [e.toString()];
        case "string":
          return [e];
        case "object":
          return ["table"];
        case "function":
          return ["function"];
        default:
          return ["nil"];
      }
    }
  },
  "type": function (v) {
    switch (typeof v) {
      case "number":
        return ["number"];
      case "string":
        return ["string"];
      case "boolean":
        return ["boolean"];
      case "function":
        return ["function"];
      case "object":
        return [v === null ? "nil" : "table"];
      case "undefined":
        return ["nil"];
      default:
        throw new Error("Unepected value of type " + typeof v);
    }
  },
  "unpack": function (list, i, j) {
    ensure_arraymode(list);
    if (list.length != null) {
      j = list.length;
    } else {
      j = 0;
      while (list.uints[j++] != null) {};
      list.length = --j;
    }

    if (i == null || i < 1) {
      i = 1;
    }
    if (j == null) {
      j = list.length;
    }
    throw new ReturnValues(list.uints.slice(i - 1, j));
  },
  "_VERSION": "Lua 5.1",
  "xpcall": function () {
    not_supported();
  }
};

// coroutine
var _lua_coroutine = lua_libs["coroutine"] = {};
_lua_coroutine["resume"] = _lua_coroutine["running"] = _lua_coroutine["status"] = _lua_coroutine["wrap"] = _lua_coroutine["yield"] = _lua_coroutine["create"] = function () {
  not_supported();
};

// debug
var _lua_debug = lua_libs["debug"] = {
  "getmetatable": function (obj) {
    return [obj.metatable];
  }
};
_lua_debug["traceback"] = _lua_debug["getfenv"] = _lua_debug["gethook"] = _lua_debug["getinfo"] = _lua_debug["getlocal"] = _lua_debug["getregistry"] = _lua_debug["getupvalue"] = _lua_debug["setfenv"] = _lua_debug["sethook"] = _lua_debug["setlocal"] = _lua_debug["setupvalue"] = _lua_debug["debug"] = function () {
  not_supported();
};

// io
var _lua_write_buffer = "";
var _lua_io = lua_libs["io"] = {
  "write": function () {
    _lua_write_buffer += Array.prototype.join.call(arguments, "");
    var lines = _lua_write_buffer.split("\n");
    while (lines.length > 1) {
      _lua_print(lines.shift());
    }
    _lua_write_buffer = lines[0];
    return [];
  },
  "flush": function () {},// no-op
  "stderr": null,
  "stdin": null,
  "stdout": null
};
_lua_io["close"] = _lua_io["input"] = _lua_io["lines"] = _lua_io["output"] = _lua_io["popen"] = _lua_io["read"] = _lua_io["tmpfile"] = _lua_io["type"] = _lua_io["open"] = function () {
  not_supported();
};

// math
var _lua_randmax = 0x100000000;
var _lua_randseed = (Math.random() * _lua_randmax) & (_lua_randmax - 1);
lua_libs["math"] = {
  "abs": function (x) {
    return [Math.abs(x)];
  },
  "acos": function (x) {
    return [Math.acos(x)];
  },
  "asin": function (x) {
    return [Math.asin(x)];
  },
  "atan": function (x) {
    return [Math.atan(x)];
  },
  "atan2": function (y, x) {
    return [Math.atan2(y, x)];
  },
  "ceil": function (x) {
    return [Math.ceil(x)];
  },
  "cos": function (x) {
    return [Math.cos(x)];
  },
  "cosh": function (x) {
    return [(Math.exp(x) + Math.exp(-x)) / 2];
  },
  "deg": function (x) {
    return [x * (180 / Math.PI)];
  },
  "exp": function (x) {
    return [Math.exp(x)];
  },
  "floor": function (x) {
    return [Math.floor(x)];
  },
  "fmod": function (x, y) {
    return [x % y];
  },
  "frexp": function (m, e) {
    not_supported();
  },
  "huge": Infinity,
  "ldexp": function (m, e) {
    return [m * Math.pow(2, e)];
  },
  "log": function (x) {
    return [Math.log(x)];
  },
  "log10": function (x) {
    return [Math.log(x) / Math.LN10];
  },
  "max": function () {
    return [Math.max.apply(null, arguments)];
  },
  "min": function () {
    return [Math.min.apply(null, arguments)];
  },
  "modf": function (x) {
    var frac = x % 1;
    return [x - frac, frac];
  },
  "pi": Math.PI,
  "pow": function (x, y) {
    return [Math.pow(x, y)];
  },
  "rad": function (x) {
    return [x * (Math.PI / 180)];
  },
  "sin": function (x) {
    return [Math.sin(x)];
  },
  "sinh": function (x) {
    return [(Math.exp(x) - Math.exp(-x)) / 2];
  },
  "sqrt": function (x) {
    return [Math.sqrt(x)];
  },
  "tan": function (x) {
    return [Math.tan(x)];
  },
  "tanh": function (x) {
    var a = Math.exp(x);
    var b = Math.exp(-x);
    return [(a - b) / (a + b)];
  },
  "random": function (m, n) {
    // Based on the 32 bit mix function found here:
    // http://www.concentric.net/~Ttwang/tech/inthash.htm
    _lua_randseed = ~_lua_randseed + (_lua_randseed << 15); // _lua_randseed = (_lua_randseed << 15) - _lua_randseed - 1;
    _lua_randseed = _lua_randseed ^ (_lua_randseed >>> 12);
    _lua_randseed = _lua_randseed + (_lua_randseed << 2);
    _lua_randseed = _lua_randseed ^ (_lua_randseed >>> 4);
    _lua_randseed = _lua_randseed * 2057; // _lua_randseed = (_lua_randseed + (_lua_randseed << 3)) + (_lua_randseed << 11);
    _lua_randseed = _lua_randseed ^ (_lua_randseed >>> 16);

    var val;
    if (_lua_randseed < 0) {
      val = ((_lua_randseed + _lua_randmax) / _lua_randmax) % 1;
    } else {
      val = (_lua_randseed / _lua_randmax) % 1;
    }

    if (arguments.length >= 2) {
      m = m | 0;
      n = n | 0;
      if (m >= n) {
        throw new Error("Invalid range");
      }
      return [Math.floor(val * (n - m + 1) + m)];
    } else if (arguments.length == 1) {
      m = m | 0;
      return [Math.floor(val * m + 1)];
    } else {
      return [val];
    }
  },
  "randomseed": function (x) {
    _lua_randseed = x & (_lua_randmax - 1);
  }
};

// os
// TODO: this should be different for each script, I think?
var _lua_clock_start = (new Date()).getTime() / 1000;
lua_libs["os"] = {
  "clock": function () {
    // This function is supposed to return the time the script has been executing
    // not the time since it started, but I don't know of a way to do this.
    return [(((new Date()).getTime()) / 1000) - _lua_clock_script];
  },
  "date": function (format, time) {
    // TODO
    return ["[" + time + "]" + format];
  },
  "difftime": function (t2, t1) {
    return [t2 - t1];
  },
  "execute": function () {
    return 0;// all commands fail
  },
  "exit": function () {
    //window.close();
    not_supported();
  },
  "getenv": function (varname) {
    return [null];
  },
  "remove": function () {
    not_supported();
  },
  "rename": function () {
    not_supported();
  },
  "setlocale": function () {
    not_supported();
  },
  "time": function (table) {
    if (table) {
      not_supported();
    } else {
      return [Math.floor(new Date().getTime() / 1000)];
    }
  }
};

// package
var lua_packages = lua_newtable();
function lua_createmodule(G, name, options) {
  var t = lua_tableget(lua_packages, name) || lua_tableget(G, name) || lua_newtable();
  lua_tableset(G, name, t);
  lua_tableset(lua_packages, name, t);
  lua_tableset(t, "_NAME", name);
  lua_tableset(t, "_M", t);
  lua_tableset(t, "_PACKAGE", name.split(".").slice(0, -1).join("."));

  for (var i = 0; i < options.length; i++) {
    lua_call(options[i], [t]);
  }
  return t;
}
function lua_module(name) {
  var t = lua_tableget(lua_packages, name);
  if (t == null) {
    throw new Error("Module " + name + " not found. Module must be loaded before use.");
  }
  return t;
}
function lua_require(G, name) {
  var t = lua_module(name);
  var pkg = G;
  var names = name.split(".");
  for (var i = 0; i < names.length - 1; i++) {
    if (!lua_tableget(pkg, names[i])) {
      var newPkg = lua_newtable();
      lua_tableset(pkg, names[i], newPkg);
      pkg = newPkg;
    }
  }
  lua_tableset(pkg, names[names.length - 1], t);
  return t;
}
lua_libs["package"] = {
  "path": "",
  "cpath": "",
  "loaded": lua_packages,
  "loaders": lua_newtable(),// not used
  "preload": lua_newtable(),// not used
  "loadlib": function () {
    not_supported();
  }
};

// string
lua_libs["string"] = {
  "byte": function (s, i, j) {
    if (i == null) {
      i = 0;
    }
    if (j == null) {
      j = i;
    }
    var result = [];
    while (i < j && i < s.length) {
      result.push(s.charCodeAt(i));
    }
    return result;
  },
  "char": function () {
    return [String.fromCharCode.apply(null, arguments)];
  },
  "dump": function (func) {
    not_supported();
  },
  "find": function () {
    // TODO
    not_supported();
  },
  "format": function (formatstring) {
    // TODO: Finish implementation
    return ["[" + slice(arguments, 1).join(", ") + "]" + arguments[0]];
  },
  "gmatch": function (s, pattern) {
    // TODO
    not_supported();
  },
  "gsub": function (s, pattern, repl, n) {
    // TODO
    not_supported();
  },
  "len": function (s) {
    if (typeof s == "string") {
      return [s.length];
    } else {
      throw new Error("Input not string");
    }
  },
  "lower": function (s) {
    if (typeof s == "string") {
      return [s.toLowerCase()];
    } else {
      throw new Error("Input not string");
    }
  },
  "match": function (s) {
    // TODO
    not_supported();
  },
  "rep": function (s, n) {
    if (typeof s == "string" && typeof n == "number") {
      var result = [];
      while (n-- > 0) {
        result.push(s);
      }
      return [result.join("")];
    } else {
      throw new Error("Input not string and number");
    }
  },
  "reverse": function (s) {
    if (typeof s == "string") {
      return [s.split("").reverse().join("")];
    } else {
      throw new Error("Input not string");
    }
  },
  "sub": function (s, i, j) {
    // thanks to ghoulsblade for pointing out the bugs in string.sub
    i = i < 0 ? (i + s.length + 1) : (i >= 0 ? i : 0)
    if (j == null) {
      j = -1;
    }
    j = j < 0 ? (j + s.length + 1) : (j >= 0 ? j : 0)
    if (i < 1) {
      i = 1;
    }
    if (j > s.length) {
      j = s.length;
    }
    if (i <= j) {
      return [s.substr(i - 1, j - i + 1)];
    } else {
      return [""];
    }
  },
  "upper": function (s) {
    if (typeof s == "string") {
      return [s.toUpperCase()];
    } else {
      throw new Error("Input not string");
    }
  }
};

// add string functions to every string
String.prototype["metatable"] = lua_newtable(null, "__index", lua_newtable2(lua_libs["string"]));

// table
lua_libs["table"] = {
  "concat": function (table, sep, i, j) {
    ensure_arraymode(table);
    if (sep == null) {
      sep = "";
    }
    if (i != null) {
      if (j == null) {
        j = table.uints.length;
      }
      return [table.uints.slice(i - 1, j).join(sep)];
    } else {
      return [table.uints.join(sep)];
    }
  },
  "insert": function (table, pos, value) {
    ensure_arraymode(table);
    if (arguments.length == 2) {
      value = pos;
      pos = table.uints.length + 1;
    }
    table.uints.splice(pos - 1, 0, value);
    if (table.length != null) {
      table.length++;
    }
    return [];
  },
  "maxn": function (table) {
    if (table.arraymode) {
      return [table.uints.length];
    } else {
      var max = 0;
      for (var i in table.uints) {
        var val = parseFloat(i);
        if (val > max) {
          max = val;
        }
      }
      return [max];
    }
  },
  "remove": function (table, pos) {
    ensure_arraymode(table);
    if (pos == null) {
      pos = table.uints.length;
    } else {
      pos = lua_assertfloat(pos);
    }
    if (table.uints.length) {
      var value = table.uints[pos - 1];
      table.uints.splice(pos - 1, 1);
      if (table.length != null) {
        table.length--;
      }
      return [value];
    } else {
      return [];
    }
  },
  "sort": function (table, comp) {
    ensure_arraymode(table)
    if (comp) {
      table.uints.sort(function (a, b) {
        return comp(a, b)[0] ? -1 : 1;
      });
    } else {
      table.uints.sort(function (a, b) {
        return lua_lt(a, b) ? -1 : 1;
      });
    }
    return [];
  }
};

// bit (based on BitOp <http://bitop.luajit.org/>)
lua_libs["bit"] = {
  "tobit": function (x) {
    return [x << 0]
  },
  "tohex": function (x, n) {
    if (n > 0) {
      var str = x.toString(16).substr(-n);
      while (str.length < n) {
        str = "0" + str;
      }
      return [str];
    } else if (n < 0) {
      var str = x.toString(16).substr(n).toUpperCase();
      while (str.length < -n) {
        str = "0" + str;
      }
      return [str];
    } else {
      return [x.toString(16)]
    }
  },
  "bnot": function (x) {
    return [~x];
  },
  "bor": function (x) {
    x = lua_assertfloat(x);
    for (var i = 1; i < arguments.length; i++) {
      x |= arguments[i];
    }
    return [x];
  },
  "band": function (x) {
    x = lua_assertfloat(x);
    for (var i = 1; i < arguments.length; i++) {
      x &= arguments[i];
    }
    return [x];
  },
  "bxor": function (x) {
    x = lua_assertfloat(x);
    for (var i = 1; i < arguments.length; i++) {
      x ^= arguments[i];
    }
    return [x];
  },
  "lshift": function (x, n) {
    return [x << n];
  },
  "rshift": function (x, n) {
    return [x >>> n];
  },
  "arshift": function (x, n) {
    return [x >> n];
  },
  "rol": function (x, n) {
    n &= 0xf;
    return [(x << n) | (x >>> -n)];
  },
  "ror": function (x, n) {
    n &= 0xf;
    return [(x >>> n) | (x << -n)];
  },
  "bswap": function (x) {
    // from Bit Twiddling hacks <http://graphics.stanford.edu/~seander/bithacks.html>
    x = ((x >> 1) & 0x55555555) | ((x & 0x55555555) << 1);
    x = ((x >> 2) & 0x33333333) | ((x & 0x33333333) << 2);
    x = ((x >> 4) & 0x0F0F0F0F) | ((x & 0x0F0F0F0F) << 4);
    x = ((x >> 8) & 0x00FF00FF) | ((x & 0x00FF00FF) << 8);
    x = (x >> 16) | (x << 16);
    return [x];
  }
};
