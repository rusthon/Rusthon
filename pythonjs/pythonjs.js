__NULL_OBJECT__ = Object.create(null);
__WEBWORKER__ = false;
__NODEJS__ = false;
__BROWSER__ = false;
if (typeof(process)!=="undefined")
{
	__NODEJS__ = true;
}
if (typeof(window)!=="undefined")
{
	__BROWSER__ = true;
}
if (typeof(importScripts)==="function")
{
	__WEBWORKER__ = true;
}
if (! (__NODEJS__) && ! (__WEBWORKER__))
{
	if (typeof(HTMLDocument)==="undefined")
	{
		HTMLDocument = Document;
	}
}
IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";
KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";
ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";
AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";
RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";
var hasattr = function(ob, attr)
{
	
	return Object.hasOwnProperty.call(ob, attr);
}

var len = function(ob)
{
	
	if (ob instanceof Array)
	{
		return ob.length;
	}
	else
	{
		if (__is_typed_array(ob))
		{
			return ob.length;
		}
		else
		{
			if (ob.__len__)
			{
				return ob.__len__();
			}
			else
			{
				return Object.keys(ob).length;
			}
		}
	}
}

var func = function(a)
{
	
	if (this.indexOf(a)===-1)
	{
		return false;
	}
	else
	{
		return true;
	}
}

Object.defineProperty(String.prototype, "__contains__", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(start, stop, step)
{
	
	if (( start ) === undefined && ( stop ) === undefined && (step===-1))
	{
		return this.split("").reverse().join("");
	}
	else
	{
		if (( stop ) < 0)
		{
			stop = (this.length + stop);
		}
		return this.substring(start, stop);
	}
}

Object.defineProperty(String.prototype, "__getslice__", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function()
{
	
	return this.split("\n");
}

Object.defineProperty(String.prototype, "splitlines", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function()
{
	
	return this.trim();
}

Object.defineProperty(String.prototype, "strip", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(a)
{
	
	if (this.substring(0, a.length)===a)
	{
		return true;
	}
	else
	{
		return false;
	}
}

Object.defineProperty(String.prototype, "startswith", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(a)
{
	
	if (this.substring((this.length - a.length), this.length)===a)
	{
		return true;
	}
	else
	{
		return false;
	}
}

Object.defineProperty(String.prototype, "endswith", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(a)
{
	var i,arr,out;
	out = "";
	if (a instanceof Array)
	{
		arr = a;
	}
	else
	{
		arr = a["$wrapped"];
	}
	i = 0;
		var __iter1 = arr;
	if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
	for (var __i1=0; __i1 < __iter1.length; __i1++) {
		var value = __iter1[ __i1 ];
		out += value;
		i += 1;
		if (( i ) < arr.length)
		{
			out += this;
		}
	}
	return out;
}

Object.defineProperty(String.prototype, "join", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function()
{
	
	return this.toUpperCase();
}

Object.defineProperty(String.prototype, "upper", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function()
{
	
	return this.toLowerCase();
}

Object.defineProperty(String.prototype, "lower", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(a)
{
	var i;
	i = this.indexOf(a);
	if (i===-1)
	{
		throw new ValueError((a + " - not in string"));
	}
	return i;
}

Object.defineProperty(String.prototype, "index", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(a)
{
	
	if (this.indexOf(a)===-1)
	{
		return false;
	}
	else
	{
		return true;
	}
}

Object.defineProperty(Array.prototype, "__contains__", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(start, stop, step)
{
	var i,arr,n;
	arr = [];
	start = (start | 0);
	if (( stop ) === undefined)
	{
		stop = this.length;
	}
	if (( start ) < 0)
	{
		start = (this.length + start);
	}
	if (( stop ) < 0)
	{
		stop = (this.length + stop);
	}
	if (typeof(step)==="number")
	{
		if (( step ) < 0)
		{
			i = start;
			while (( i ) >= 0)
			{
				arr.push(this[i]);
				i += step;
			}
			return arr;
		}
		else
		{
			i = start;
			n = stop;
			while (( i ) < n)
			{
				arr.push(this[i]);
				i += step;
			}
			return arr;
		}
	}
	else
	{
		i = start;
		n = stop;
		while (( i ) < n)
		{
			arr.push(this[i]);
			i += 1;
		}
		return arr;
	}
}

Object.defineProperty(Array.prototype, "__getslice__", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(start, stop, step, items)
{
	var arr;
	if (( start ) === undefined)
	{
		start = 0;
	}
	if (( stop ) === undefined)
	{
		stop = this.length;
	}
	arr = [start, (stop - start)];
		var __iter2 = items;
	if (! (__iter2 instanceof Array || typeof __iter2 == "string" || __is_typed_array(__iter2) || __is_some_array(__iter2) )) { __iter2 = __object_keys__(__iter2) }
	for (var __i2=0; __i2 < __iter2.length; __i2++) {
		var item = __iter2[ __i2 ];
		arr.push(item);
	}
	this.splice.apply(this, arr);
}

Object.defineProperty(Array.prototype, "__setslice__", { enumerable:false, value:func, writeable:true, configurable:true });
var func = function(item)
{
	
	this.push(item);
	return this;
}

Object.defineProperty(Array.prototype, "append", { enumerable:false, value:func, writeable:true, configurable:true });
var extend = function(other)
{
	
		var __iter3 = other;
	if (! (__iter3 instanceof Array || typeof __iter3 == "string" || __is_typed_array(__iter3) || __is_some_array(__iter3) )) { __iter3 = __object_keys__(__iter3) }
	for (var __i3=0; __i3 < __iter3.length; __i3++) {
		var obj = __iter3[ __i3 ];
		this.push(obj);
	}
	return this;
}

Object.defineProperty(Array.prototype, "extend", { enumerable:false, value:extend, writeable:true, configurable:true });
var func = function(item)
{
	var index;
	index = this.indexOf(item);
	this.splice(index, 1);
}

Object.defineProperty(Array.prototype, "remove", { enumerable:false, value:func, writeable:true, configurable:true });
var insert = function(index, obj)
{
	
	if (( index ) < 0)
	{
		index = (this.length + index);
	}
	this.splice(index, 0, obj);
}

Object.defineProperty(Array.prototype, "insert", { enumerable:false, value:insert, writeable:true, configurable:true });
var index = function(obj)
{
	
	return this.indexOf(obj);
}

Object.defineProperty(Array.prototype, "index", { enumerable:false, value:index, writeable:true, configurable:true });
var count = function(obj)
{
	var a;
	a = 0;
		var __iter4 = this;
	if (! (__iter4 instanceof Array || typeof __iter4 == "string" || __is_typed_array(__iter4) || __is_some_array(__iter4) )) { __iter4 = __object_keys__(__iter4) }
	for (var __i4=0; __i4 < __iter4.length; __i4++) {
		var item = __iter4[ __i4 ];
		if (( item ) === obj)
		{
			a += 1;
		}
	}
	return a;
}

Object.defineProperty(Array.prototype, "count", { enumerable:false, value:count, writeable:true, configurable:true });
var __contains__ = function(ob, a)
{
	var t;
	t = typeof(ob);
	if (t==="string")
	{
		if (ob.indexOf(a)===-1)
		{
			return false;
		}
		else
		{
			return true;
		}
	}
	else
	{
		if (t==="number")
		{
			throw new TypeError;
		}
		else
		{
			if (__is_typed_array(ob))
			{
								var __iter5 = ob;
				if (! (__iter5 instanceof Array || typeof __iter5 == "string" || __is_typed_array(__iter5) || __is_some_array(__iter5) )) { __iter5 = __object_keys__(__iter5) }
				for (var __i5=0; __i5 < __iter5.length; __i5++) {
					var x = __iter5[ __i5 ];
					if (x===a)
					{
						return true;
					}
				}
				return false;
			}
			else
			{
				if (ob && ob.__contains__)
				{
					return ob.__contains__(a);
				}
				else
				{
					if (ob instanceof Object && Object.hasOwnProperty.call(ob, a))
					{
						return true;
					}
					else
					{
						return false;
					}
				}
			}
		}
	}
}

__dom_array_types__ = [];
if (typeof(NodeList)==="function")
{
	__dom_array_types__ = [NodeList, FileList, DOMStringList, HTMLCollection, SVGNumberList, SVGTransformList];
	if (typeof(DataTransferItemList)==="function")
	{
		__dom_array_types__.push(DataTransferItemList);
	}
	if (typeof(HTMLAllCollection)==="function")
	{
		__dom_array_types__.push(HTMLAllCollection);
	}
	if (typeof(SVGElementInstanceList)==="function")
	{
		__dom_array_types__.push(SVGElementInstanceList);
	}
	if (typeof(ClientRectList)==="function")
	{
		__dom_array_types__.push(ClientRectList);
	}
}
var __is_some_array = function(ob)
{
	
	if (( __dom_array_types__.length ) > 0)
	{
				var __iter6 = __dom_array_types__;
		if (! (__iter6 instanceof Array || typeof __iter6 == "string" || __is_typed_array(__iter6) || __is_some_array(__iter6) )) { __iter6 = __object_keys__(__iter6) }
		for (var __i6=0; __i6 < __iter6.length; __i6++) {
			var t = __iter6[ __i6 ];
			if (ob instanceof t)
			{
				return true;
			}
		}
	}
	return false;
}

var __is_typed_array = function(ob)
{
	
	if (ob instanceof Int16Array || ob instanceof Uint16Array)
	{
		return true;
	}
	else
	{
		if (ob instanceof Int32Array || ob instanceof Uint32Array)
		{
			return true;
		}
		else
		{
			if (ob instanceof Float32Array || ob instanceof Float64Array)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
	}
}

var __js_typed_array = function(t, a)
{
	var arr;
	if (t==="i")
	{
		arr =  new Int32Array(a.length);
	}
	arr.set(a);
	return arr;
}

/* notes:
			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`
			. this is different from Object.keys because it traverses the prototype chain. */
var __object_keys__ = function(ob)
{
	var arr;
	arr = [];
	for (var key in ob) { arr.push(key) };
	return arr;
}

var __sprintf = function(fmt, args)
{
	var chunks,item,arr;
	if (args instanceof Array)
	{
		chunks = fmt.split("%s");
		arr = [];
		var i;
		i = 0;
				var __iter7 = chunks;
		if (! (__iter7 instanceof Array || typeof __iter7 == "string" || __is_typed_array(__iter7) || __is_some_array(__iter7) )) { __iter7 = __object_keys__(__iter7) }
		for (var __i7=0; __i7 < __iter7.length; __i7++) {
			var txt = __iter7[ __i7 ];
			arr.append(txt);
			if (( i ) >= args.length)
			{
				break;
			}
			item = args[i];
			if (typeof(item)==="string")
			{
				arr.append(item);
			}
			else
			{
				if (typeof(item)==="number")
				{
					arr.append(("" + item));
				}
				else
				{
					arr.append(Object.prototype.toString.call(item));
				}
			}
			i += 1;
		}
		return "".join(arr);
	}
	else
	{
		return fmt.replace('%s', args);
	}
}

var __jsdict = function(items)
{
	var d,key;
	d = {};
		var __iter8 = items;
	if (! (__iter8 instanceof Array || typeof __iter8 == "string" || __is_typed_array(__iter8) || __is_some_array(__iter8) )) { __iter8 = __object_keys__(__iter8) }
	for (var __i8=0; __i8 < __iter8.length; __i8++) {
		var item = __iter8[ __i8 ];
		key = item[0];
		if (key instanceof Array)
		{
			key = JSON.stringify(key);
		}
		else
		{
			if (key.__uid__)
			{
				key = key.__uid__;
			}
		}
		d[key] = item[1];
	}
	return d;
}

var __jsdict_get = function(ob, key, default_value)
{
	
	if (ob instanceof Object)
	{
		if (key instanceof Array)
		{
			key = JSON.stringify(key);
		}
		if (key in ob)
		{
			return ob[key];
		}
		return default_value;
	}
	else
	{
		if (( default_value ) !== undefined)
		{
			return ob.get(key, default_value);
		}
		else
		{
			return ob.get(key);
		}
	}
}

var __jsdict_set = function(ob, key, value)
{
	
	if (ob instanceof Object)
	{
		if (key instanceof Array)
		{
			key = JSON.stringify(key);
		}
		ob[key] = value;
	}
	else
	{
		ob.set(key,value);
	}
}

var __jsdict_keys = function(ob)
{
	
	if (ob instanceof Object)
	{
		return Object.keys( ob );
	}
	else
	{
		return ob.keys();
	}
}

var __jsdict_values = function(ob)
{
	var arr,value;
	if (ob instanceof Object)
	{
		arr = [];
				var __iter9 = ob;
		if (! (__iter9 instanceof Array || typeof __iter9 == "string" || __is_typed_array(__iter9) || __is_some_array(__iter9) )) { __iter9 = __object_keys__(__iter9) }
		for (var __i9=0; __i9 < __iter9.length; __i9++) {
			var key = __iter9[ __i9 ];
			if (ob.hasOwnProperty(key))
			{
				value = ob[key];
				arr.push(value);
			}
		}
		return arr;
	}
	else
	{
		return ob.values();
	}
}

var __jsdict_items = function(ob)
{
	var arr,value;
	if (ob instanceof Object || ( ob.items ) === undefined)
	{
		arr = [];
				var __iter10 = ob;
		if (! (__iter10 instanceof Array || typeof __iter10 == "string" || __is_typed_array(__iter10) || __is_some_array(__iter10) )) { __iter10 = __object_keys__(__iter10) }
		for (var __i10=0; __i10 < __iter10.length; __i10++) {
			var key = __iter10[ __i10 ];
			if (Object.hasOwnProperty.call(ob, key))
			{
				value = ob[key];
				arr.push([key, value]);
			}
		}
		return arr;
	}
	else
	{
		return ob.items();
	}
}

var __jsdict_pop = function(ob, key, _kwargs_)
{
	var v;
	var _default = (_kwargs_ === undefined || _kwargs_._default === undefined)?	null : _kwargs_._default;
	if (ob instanceof Array)
	{
		if (ob.length)
		{
			if (( key ) === undefined)
			{
				return ob.pop();
			}
			else
			{
				return ob.splice(key, 1)[0];
			}
		}
		else
		{
			throw new IndexError(key);
		}
	}
	else
	{
		if (ob instanceof Object)
		{
			if (key in ob)
			{
				v = ob[key];
				delete ob[key];
				return v;
			}
			else
			{
				if (( _default ) === undefined)
				{
					throw new KeyError(key);
				}
				else
				{
					return _default;
				}
			}
		}
		else
		{
			return ob.pop(key, _default);
		}
	}
}

var __jsdict_update = function(ob, other)
{
	
	if (typeof(ob["update"])==="function")
	{
		return ob.update(other);
	}
	else
	{
				var __iter11 = __object_keys__(other);
		if (! (__iter11 instanceof Array || typeof __iter11 == "string" || __is_typed_array(__iter11) || __is_some_array(__iter11) )) { __iter11 = __object_keys__(__iter11) }
		for (var __i11=0; __i11 < __iter11.length; __i11++) {
			var key = __iter11[ __i11 ];
			ob[key] = other[key];
		}
	}
}

_PythonJS_UID = 0;
var __getfast__ = function(ob, attr)
{
	var v;
	v = ob[attr];
	if (( v ) === undefined)
	{
		if (ob.__class__)
		{
			v = ob.__class__[attr];
			if (( v ) !== undefined)
			{
				return v;
			}
		}
		throw new AttributeError(attr);
	}
	else
	{
		return v;
	}
}

var __wrap_function__ = function(f)
{
	
	f.is_wrapper = true;
	return f;
}

var __getattr__ = function(ob, a)
{
	
	if (ob.__getattr__)
	{
		return ob.__getattr__(a);
	}
}

var __test_if_true__ = function(ob)
{
	
	if (( ob ) === true)
	{
		return true;
	}
	else
	{
		if (( ob ) === false)
		{
			return false;
		}
		else
		{
			if (typeof(ob)==="string")
			{
				return (ob.length!==0);
			}
			else
			{
				if (! (ob))
				{
					return false;
				}
				else
				{
					if (ob instanceof Array)
					{
						return (ob.length!==0);
					}
					else
					{
						if (typeof(ob)==="function")
						{
							return true;
						}
						else
						{
							if (ob.__class__ && ( ob.__class__ ) === dict)
							{
								return (Object.keys(ob["$wrapped"]).length!==0);
							}
							else
							{
								if (ob instanceof Object)
								{
									return (Object.keys(ob).length!==0);
								}
								else
								{
									return true;
								}
							}
						}
					}
				}
			}
		}
	}
}

var __replace_method = function(ob, a, b)
{
	
	if (typeof(ob)==="string")
	{
		return ob.split(a).join(b);
	}
	else
	{
		return ob.replace(a, b);
	}
}

var __split_method = function(ob, delim)
{
	
	if (typeof(ob)==="string")
	{
		if (( delim ) === undefined)
		{
			return ob.split(" ");
		}
		else
		{
			return ob.split(delim);
		}
	}
	else
	{
		if (( delim ) === undefined)
		{
			return ob.split();
		}
		else
		{
			return ob.split(delim);
		}
	}
}

var __add_op = function(a, b)
{
	var c,t;
	t = typeof(a);
	if ((t==="string") || (t==="number"))
	{
		return a+b;
	}
	else
	{
		if (a instanceof Array)
		{
			c = [];
			c.extend(a);
			c.extend(b);
			return c;
		}
		else
		{
			if (a.__add__)
			{
				return a.__add__(b);
			}
			else
			{
				throw new TypeError("invalid objects for addition");
			}
		}
	}
}

var __mul_op = function(a, b)
{
	var c,arr,t;
	t = typeof(a);
	if (t==="number")
	{
		return a * b;
	}
	else
	{
		if (t==="string")
		{
			arr = [];
			var i,i__end__;
			i = 0;
			i__end__ = b;
			while (( i ) < i__end__)
			{
				arr.append(a);
				i += 1;
			}
			return "".join(arr);
		}
		else
		{
			if (a instanceof Array)
			{
				c = [];
				
				i = 0;
				i__end__ = b;
				while (( i ) < i__end__)
				{
					c.extend(a);
					i += 1;
				}
				return c;
			}
			else
			{
				if (a.__mul__)
				{
					return a.__mul__(b);
				}
				else
				{
					throw new TypeError("invalid objects for multiplication");
				}
			}
		}
	}
}

var dir = function(ob)
{
	
	if (ob instanceof Object)
	{
		return Object.keys( ob );
	}
	else
	{
		return __object_keys__(ob);
	}
}

var __bind_property_descriptors__ = function(o, klass)
{
	var prop,desc;
		var __iter12 = klass.__properties__;
	if (! (__iter12 instanceof Array || typeof __iter12 == "string" || __is_typed_array(__iter12) || __is_some_array(__iter12) )) { __iter12 = __object_keys__(__iter12) }
	for (var __i12=0; __i12 < __iter12.length; __i12++) {
		var name = __iter12[ __i12 ];
		desc = { "enumerable":true };
		prop = klass.__properties__[name];
		if (prop["get"])
		{
			desc["get"] = __generate_getter__(klass, o, name);
		}
		if (prop["set"])
		{
			desc["set"] = __generate_setter__(klass, o, name);
		}
		Object.defineProperty(o, name, desc);
	}
		var __iter13 = klass.__bases__;
	if (! (__iter13 instanceof Array || typeof __iter13 == "string" || __is_typed_array(__iter13) || __is_some_array(__iter13) )) { __iter13 = __object_keys__(__iter13) }
	for (var __i13=0; __i13 < __iter13.length; __i13++) {
		var base = __iter13[ __i13 ];
		__bind_property_descriptors__(o, base);
	}
}

var __generate_getter__ = function(klass, o, n)
{
	
		var __lambda__ = function()
	{
		
		return klass.__properties__[n]["get"]([o], {  });
	}

	return __lambda__;
}

var __generate_setter__ = function(klass, o, n)
{
	
		var __lambda__ = function(v)
	{
		
		return klass.__properties__[n]["set"]([o, v], {  });
	}

	return __lambda__;
}

/* Create a PythonScript class */
var __create_class__ = function(class_name, parents, attrs, props)
{
	var f,klass,prop;
	klass = Object.create(null);
	klass.__bases__ = parents;
	klass.__name__ = class_name;
	klass.__unbound_methods__ = Object.create(null);
	klass.__all_method_names__ = [];
	klass.__properties__ = props;
	klass.__attributes__ = attrs;
		var __iter14 = attrs;
	if (! (__iter14 instanceof Array || typeof __iter14 == "string" || __is_typed_array(__iter14) || __is_some_array(__iter14) )) { __iter14 = __object_keys__(__iter14) }
	for (var __i14=0; __i14 < __iter14.length; __i14++) {
		var key = __iter14[ __i14 ];
		if (typeof(attrs[key])==="function")
		{
			klass.__all_method_names__.push(key);
			f = attrs[key];
			if (hasattr(f, "is_classmethod") && f.is_classmethod)
			{
				/*pass*/
			}
			else
			{
				if (hasattr(f, "is_staticmethod") && f.is_staticmethod)
				{
					/*pass*/
				}
				else
				{
					klass.__unbound_methods__[key] = attrs[key];
				}
			}
		}
		if (key==="__getattribute__")
		{
			continue
		}
		klass[key] = attrs[key];
	}
	klass.__setters__ = [];
	klass.__getters__ = [];
		var __iter15 = klass.__properties__;
	if (! (__iter15 instanceof Array || typeof __iter15 == "string" || __is_typed_array(__iter15) || __is_some_array(__iter15) )) { __iter15 = __object_keys__(__iter15) }
	for (var __i15=0; __i15 < __iter15.length; __i15++) {
		var name = __iter15[ __i15 ];
		prop = klass.__properties__[name];
		klass.__getters__.push(name);
		if (prop["set"])
		{
			klass.__setters__.push(name);
		}
	}
		var __iter16 = klass.__bases__;
	if (! (__iter16 instanceof Array || typeof __iter16 == "string" || __is_typed_array(__iter16) || __is_some_array(__iter16) )) { __iter16 = __object_keys__(__iter16) }
	for (var __i16=0; __i16 < __iter16.length; __i16++) {
		var base = __iter16[ __i16 ];
		Array.prototype.push.apply(klass.__getters__, base.__getters__);
		Array.prototype.push.apply(klass.__setters__, base.__setters__);
		Array.prototype.push.apply(klass.__all_method_names__, base.__all_method_names__);
	}
		/* Create a PythonJS object */
var __call__ = function()
	{
		var has_getattr,wrapper,object,has_getattribute;
		object = Object.create(null);
		object.__class__ = klass;
		object.__dict__ = object;
		has_getattribute = false;
		has_getattr = false;
				var __iter17 = klass.__all_method_names__;
		if (! (__iter17 instanceof Array || typeof __iter17 == "string" || __is_typed_array(__iter17) || __is_some_array(__iter17) )) { __iter17 = __object_keys__(__iter17) }
		for (var __i17=0; __i17 < __iter17.length; __i17++) {
			var name = __iter17[ __i17 ];
			if (name==="__getattribute__")
			{
				has_getattribute = true;
			}
			else
			{
				if (name==="__getattr__")
				{
					has_getattr = true;
				}
				else
				{
					wrapper = __get__(object, name);
					if (! (wrapper.is_wrapper))
					{
						console.log(["RUNTIME ERROR: failed to get wrapper for:", name]);
					}
				}
			}
		}
		if (has_getattr)
		{
			__get__(object, "__getattr__");
		}
		if (has_getattribute)
		{
			__get__(object, "__getattribute__");
		}
		__bind_property_descriptors__(object, klass);
		if (object.__init__)
		{
			object.__init__.apply(this, arguments);
		}
		return object;
	}

	__call__.is_wrapper = true;
	klass.__call__ = __call__;
	return klass;
}

/* type(object) -> the object's type
	type(name, bases, dict) -> a __new__>>type  ## broken? - TODO test */
var type = function(ob_or_class_name, _kwargs_)
{
	
	var bases      = (_kwargs_ === undefined || _kwargs_.bases === undefined)     ?	null : _kwargs_.bases;
	var class_dict = (_kwargs_ === undefined || _kwargs_.class_dict === undefined)?	null : _kwargs_.class_dict;
	if (( bases ) === null && ( class_dict ) === null)
	{
		return ob_or_class_name.__class__;
	}
	else
	{
		return create_class(ob_or_class_name, bases, class_dict);
	}
}

var getattr = function(ob, attr)
{
	
	return __getfast__(ob, attr);
}

var setattr = function(ob, attr, value)
{
	
	ob[attr] = value;
}

var issubclass = function(C, B)
{
	var i,bases;
	if (( C ) === B)
	{
		return true;
	}
	bases = C.__bases__;
	i = 0;
	while (( i ) < bases.length)
	{
		if (issubclass(bases[i], B))
		{
			return true;
		}
		i += 1;
	}
	return false;
}

var isinstance = function(ob, klass)
{
	var ob_class;
	if (( ob ) === undefined || ( ob ) === null)
	{
		return false;
	}
	else
	{
		if (ob instanceof Array && ( klass ) === list)
		{
			return true;
		}
		else
		{
			if (! (Object.hasOwnProperty.call(ob, "__class__")))
			{
				return false;
			}
		}
	}
	ob_class = ob.__class__;
	if (( ob_class ) === undefined)
	{
		return false;
	}
	else
	{
		return issubclass(ob_class, klass);
	}
}

var int = function(a)
{
	
	a = Math.round(a);
	if (isNaN(a))
	{
		throw new ValueError("not a number");
	}
	return a;
}

var float = function(a)
{
	var b;
	if (typeof(a)==="string")
	{
		if (a.lower()==="nan")
		{
			return NaN;
		}
		else
		{
			if (a.lower()==="inf")
			{
				return Infinity;
			}
		}
	}
	b = Number(a);
	if (isNaN(b))
	{
		throw new ValueError(("can not convert to float: " + a));
	}
	return b;
}

var round = function(a, _kwargs_)
{
	var p,b;
	var places = (_kwargs_ === undefined || _kwargs_.places === undefined)?	0 : _kwargs_.places;
	b = ("" + a);
	if (b.indexOf(".")===-1)
	{
		return a;
	}
	else
	{
		p = Math.pow(10, places);
		return (Math.round((a * p)) / p);
	}
}

var str = function(s)
{
	
	return ("" + s);
}

/* Extend JavaScript String.prototype with methods that implement the Python str API.
	The decorator @String.prototype.[name] assigns the function to the prototype,
	and ensures that the special 'this' variable will work. */
var _setup_str_prototype = function()
{
	
		var func = function(index)
	{
		
		if (( index ) < 0)
		{
			return this[(this.length + index)];
		}
		else
		{
			return this[index];
		}
	}

	Object.defineProperty(String.prototype, "get", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(self)
	{
		
		return Iterator(this, 0);
	}

	Object.defineProperty(String.prototype, "__iter__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(idx)
	{
		
		if (( idx ) < 0)
		{
			return this[(this.length + idx)];
		}
		else
		{
			return this[idx];
		}
	}

	Object.defineProperty(String.prototype, "__getitem__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		
		return this.length;
	}

	Object.defineProperty(String.prototype, "__len__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(a)
	{
		
		return this.indexOf(a);
	}

	Object.defineProperty(String.prototype, "find", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		var digits;
		digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
				var __iter18 = this;
		if (! (__iter18 instanceof Array || typeof __iter18 == "string" || __is_typed_array(__iter18) || __is_some_array(__iter18) )) { __iter18 = __object_keys__(__iter18) }
		for (var __i18=0; __i18 < __iter18.length; __i18++) {
			var char = __iter18[ __i18 ];
			if (__contains__(digits, char))
			{
				/*pass*/
			}
			else
			{
				return false;
			}
		}
		return true;
	}

	Object.defineProperty(String.prototype, "isdigit", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		var digits;
		digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."];
				var __iter19 = this;
		if (! (__iter19 instanceof Array || typeof __iter19 == "string" || __is_typed_array(__iter19) || __is_some_array(__iter19) )) { __iter19 = __object_keys__(__iter19) }
		for (var __i19=0; __i19 < __iter19.length; __i19++) {
			var char = __iter19[ __i19 ];
			if (__contains__(digits, char))
			{
				/*pass*/
			}
			else
			{
				return false;
			}
		}
		return true;
	}

	Object.defineProperty(String.prototype, "isnumber", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(encoding)
	{
		
		return this;
	}

	Object.defineProperty(String.prototype, "decode", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(encoding)
	{
		
		return this;
	}

	Object.defineProperty(String.prototype, "encode", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(fmt)
	{
		var keys,r;
		r = this;
		keys = Object.keys(fmt);
				var __iter20 = keys;
		if (! (__iter20 instanceof Array || typeof __iter20 == "string" || __is_typed_array(__iter20) || __is_some_array(__iter20) )) { __iter20 = __object_keys__(__iter20) }
		for (var __i20=0; __i20 < __iter20.length; __i20++) {
			var key = __iter20[ __i20 ];
			r = r.split(key).join(fmt[key]);
		}
		r = r.split("{").join("").split("}").join("");
		return r;
	}

	Object.defineProperty(String.prototype, "format", { enumerable:false, value:func, writeable:true, configurable:true });
}

_setup_str_prototype();
var __sort_method = function(ob)
{
	
	if (ob instanceof Array)
	{
				var f = function(a, b)
		{
			
			if (( a ) < b)
			{
				return -1;
			}
			else
			{
				if (( a ) > b)
				{
					return 1;
				}
				else
				{
					return 0;
				}
			}
		}

		return ob.sort( f );
	}
	else
	{
		return ob.sort();
	}
}

var _setup_array_prototype = function()
{
	
		var func = function()
	{
		var i,item;
		i = 0;
		while (( i ) < this.length)
		{
			item = this[i];
			if (typeof(item)==="object")
			{
				if (item.jsify)
				{
					this[i] = item.jsify();
				}
			}
			i += 1;
		}
		return this;
	}

	Object.defineProperty(Array.prototype, "jsify", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		
		return this.length;
	}

	Object.defineProperty(Array.prototype, "__len__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(index)
	{
		
		return this[index];
	}

	Object.defineProperty(Array.prototype, "get", { enumerable:false, value:func, writeable:true, configurable:true });
		var __getitem__ = function(index)
	{
		
		if (( index ) < 0)
		{
			index = (this.length + index);
		}
		return this[index];
	}

	Object.defineProperty(Array.prototype, "__getitem__", { enumerable:false, value:__getitem__, writeable:true, configurable:true });
		var __setitem__ = function(index, value)
	{
		
		if (( index ) < 0)
		{
			index = (this.length + index);
		}
		this[index] = value;
	}

	Object.defineProperty(Array.prototype, "__setitem__", { enumerable:false, value:__setitem__, writeable:true, configurable:true });
		var func = function()
	{
		
		return Iterator(this, 0);
	}

	Object.defineProperty(Array.prototype, "__iter__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(x, low, high)
	{
		var a,mid;
		if (( low ) === undefined)
		{
			low = 0;
		}
		if (( high ) === undefined)
		{
			high = this.length;
		}
		while (( low ) < high)
		{
			a = (low + high);
			mid = Math.floor((a / 2));
			if (( x ) < this[mid])
			{
				high = mid;
			}
			else
			{
				low = (mid + 1);
			}
		}
		return low;
	}

	Object.defineProperty(Array.prototype, "bisect", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(other)
	{
		var f;
				var __lambda__ = function(i)
		{
			
			return (other.indexOf(i)===-1);
		}

		f = __lambda__;
		return this.filter(f);
	}

	Object.defineProperty(Array.prototype, "difference", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(other)
	{
		var f;
				var __lambda__ = function(i)
		{
			
			return (other.indexOf(i)!==-1);
		}

		f = __lambda__;
		return this.filter(f);
	}

	Object.defineProperty(Array.prototype, "intersection", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(other)
	{
		
				var __iter21 = this;
		if (! (__iter21 instanceof Array || typeof __iter21 == "string" || __is_typed_array(__iter21) || __is_some_array(__iter21) )) { __iter21 = __object_keys__(__iter21) }
		for (var __i21=0; __i21 < __iter21.length; __i21++) {
			var item = __iter21[ __i21 ];
			if (other.indexOf(item)===-1)
			{
				return false;
			}
		}
		return true;
	}

	Object.defineProperty(Array.prototype, "issubset", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		var i,arr;
		arr = [];
		i = 0;
		while (( i ) < this.length)
		{
			arr.push(this[i]);
			i += 1;
		}
		return arr;
	}

	Object.defineProperty(Array.prototype, "copy", { enumerable:false, value:func, writeable:true, configurable:true });
}

_setup_array_prototype();
var _setup_nodelist_prototype = function()
{
	
		var func = function(a)
	{
		
		if (this.indexOf(a)===-1)
		{
			return false;
		}
		else
		{
			return true;
		}
	}

	Object.defineProperty(NodeList.prototype, "__contains__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function()
	{
		
		return this.length;
	}

	Object.defineProperty(NodeList.prototype, "__len__", { enumerable:false, value:func, writeable:true, configurable:true });
		var func = function(index)
	{
		
		return this[index];
	}

	Object.defineProperty(NodeList.prototype, "get", { enumerable:false, value:func, writeable:true, configurable:true });
		var __getitem__ = function(index)
	{
		
		if (( index ) < 0)
		{
			index = (this.length + index);
		}
		return this[index];
	}

	Object.defineProperty(NodeList.prototype, "__getitem__", { enumerable:false, value:__getitem__, writeable:true, configurable:true });
		var __setitem__ = function(index, value)
	{
		
		if (( index ) < 0)
		{
			index = (this.length + index);
		}
		this[index] = value;
	}

	Object.defineProperty(NodeList.prototype, "__setitem__", { enumerable:false, value:__setitem__, writeable:true, configurable:true });
		var func = function()
	{
		
		return Iterator(this, 0);
	}

	Object.defineProperty(NodeList.prototype, "__iter__", { enumerable:false, value:func, writeable:true, configurable:true });
		var index = function(obj)
	{
		
		return this.indexOf(obj);
	}

	Object.defineProperty(NodeList.prototype, "index", { enumerable:false, value:index, writeable:true, configurable:true });
}

if ((__NODEJS__===false) && (__WEBWORKER__===false))
{
	_setup_nodelist_prototype();
}
var bisect = function(a, x, _kwargs_)
{
	
	var low  = (_kwargs_ === undefined || _kwargs_.low === undefined) ?	null : _kwargs_.low;
	var high = (_kwargs_ === undefined || _kwargs_.high === undefined)?	null : _kwargs_.high;
	return a.bisect(x, low, high);
}

/* Emulates Python's range function */
var range = function(num, stop, step)
{
	var i,arr;
	if (( stop ) !== undefined)
	{
		i = num;
		num = stop;
	}
	else
	{
		i = 0;
	}
	if (( step ) === undefined)
	{
		step = 1;
	}
	arr = [];
	while (( i ) < num)
	{
		arr.push(i);
		i += step;
	}
	return arr;
}

var xrange = function(num, stop, step)
{
	
	return range(num, stop, step);
}

var sum = function(arr)
{
	var a;
	a = 0;
		var __iter22 = arr;
	if (! (__iter22 instanceof Array || typeof __iter22 == "string" || __is_typed_array(__iter22) || __is_some_array(__iter22) )) { __iter22 = __object_keys__(__iter22) }
	for (var __i22=0; __i22 < __iter22.length; __i22++) {
		var b = __iter22[ __i22 ];
		a += b;
	}
	return a;
}

var StopIteration = function()
{
	/*pass*/
}

var next = function(obj)
{
	
	return obj.next();
}

var map = function(func, objs)
{
	var arr,v;
	arr = [];
		var __iter23 = objs;
	if (! (__iter23 instanceof Array || typeof __iter23 == "string" || __is_typed_array(__iter23) || __is_some_array(__iter23) )) { __iter23 = __object_keys__(__iter23) }
	for (var __i23=0; __i23 < __iter23.length; __i23++) {
		var ob = __iter23[ __i23 ];
		v = func(ob);
		arr.push(v);
	}
	return arr;
}

var filter = function(func, objs)
{
	var arr;
	arr = [];
		var __iter24 = objs;
	if (! (__iter24 instanceof Array || typeof __iter24 == "string" || __is_typed_array(__iter24) || __is_some_array(__iter24) )) { __iter24 = __object_keys__(__iter24) }
	for (var __i24=0; __i24 < __iter24.length; __i24++) {
		var ob = __iter24[ __i24 ];
		if (func(ob))
		{
			arr.push(ob);
		}
	}
	return arr;
}

var min = function(lst)
{
	var a;
	a = null;
		var __iter25 = lst;
	if (! (__iter25 instanceof Array || typeof __iter25 == "string" || __is_typed_array(__iter25) || __is_some_array(__iter25) )) { __iter25 = __object_keys__(__iter25) }
	for (var __i25=0; __i25 < __iter25.length; __i25++) {
		var value = __iter25[ __i25 ];
		if (( a ) === null)
		{
			a = value;
		}
		else
		{
			if (( value ) < a)
			{
				a = value;
			}
		}
	}
	return a;
}

var max = function(lst)
{
	var a;
	a = null;
		var __iter26 = lst;
	if (! (__iter26 instanceof Array || typeof __iter26 == "string" || __is_typed_array(__iter26) || __is_some_array(__iter26) )) { __iter26 = __object_keys__(__iter26) }
	for (var __i26=0; __i26 < __iter26.length; __i26++) {
		var value = __iter26[ __i26 ];
		if (( a ) === null)
		{
			a = value;
		}
		else
		{
			if (( value ) > a)
			{
				a = value;
			}
		}
	}
	return a;
}

var abs = function(num)
{
	
	return Math.abs(num);
}

var ord = function(char)
{
	
	return char.charCodeAt(0);
}

var chr = function(num)
{
	
	return String.fromCharCode(num);
}

var __ArrayIterator = function(arr, index)
{
	this.__init__(arr, index);
}

__ArrayIterator.prototype.__init__ = function(arr, index)
{
	
	this.arr = arr;
	this.index = index;
	this.length = arr.length;
}

__ArrayIterator.prototype.next = function()
{
	var index,arr;
	index = this.index;
	this.index += 1;
	arr = this.arr;
	return arr[index];
}

var Iterator = function(obj, index)
{
	this.__init__(obj, index);
}

Iterator.prototype.__init__ = function(obj, index)
{
	
	this.obj = obj;
	this.index = index;
	this.length = len(obj);
	this.obj_get = obj.get;
}

Iterator.prototype.next = function()
{
	var index;
	index = this.index;
	this.index += 1;
	return this.obj_get([index], {  });
}

var tuple = function(a)
{
	
	if (Object.keys(arguments).length===0)
	{
		return [];
	}
	else
	{
		if (a instanceof Array)
		{
			return a.slice();
		}
		else
		{
			if (typeof(a)==="string")
			{
				return a.split("");
			}
			else
			{
				console.log(a);
				console.log(arguments);
				throw new TypeError;
			}
		}
	}
}

var list = function(a)
{
	
	if (Object.keys(arguments).length===0)
	{
		return [];
	}
	else
	{
		if (a instanceof Array)
		{
			return a.slice();
		}
		else
		{
			if (typeof(a)==="string")
			{
				return a.split("");
			}
			else
			{
				console.log(a);
				console.log(arguments);
				throw new TypeError;
			}
		}
	}
}

var __tuple_key__ = function(arr)
{
	var i,item,r,t;
	r = [];
	i = 0;
	while (( i ) < arr.length)
	{
		item = arr[i];
		t = typeof(item);
		if (t==="string")
		{
			r.append((("'" + item) + "'"));
		}
		else
		{
			if (item instanceof Array)
			{
				r.append(__tuple_key__(item));
			}
			else
			{
				if (t==="object")
				{
					if (( item.__uid__ ) === undefined)
					{
						throw new KeyError(item);
					}
					r.append(item.__uid__);
				}
				else
				{
					r.append(item);
				}
			}
		}
		i += 1;
	}
	return r.join(",");
}

/* This returns an array that is a minimal implementation of set.
	Often sets are used simply to remove duplicate entries from a list, 
	and then it get converted back to a list, it is safe to use fastset for this.
	The array prototype is overloaded with basic set functions:
		difference
		intersection
		issubset
	Note: sets in Python are not subscriptable, but can be iterated over.
	Python docs say that set are unordered, some programs may rely on this disorder
	for randomness, for sets of integers we emulate the unorder only uppon initalization 
	of the set, by masking the value by bits-1. Python implements sets starting with an 
	array of length 8, and mask of 7, if set length grows to 6 (3/4th), then it allocates 
	a __new__>>array of length 32 and mask of 31.  This is only emulated for arrays of 
	integers up to an array length of 1536. */
var set = function(a)
{
	var keys,mask,s,hashtable,key,fallback;
	hashtable = null;
	if (( a.length ) <= 1536)
	{
		hashtable = {  };
		keys = [];
		if (( a.length ) < 6)
		{
			mask = 7;
		}
		else
		{
			if (( a.length ) < 22)
			{
				mask = 31;
			}
			else
			{
				if (( a.length ) < 86)
				{
					mask = 127;
				}
				else
				{
					if (( a.length ) < 342)
					{
						mask = 511;
					}
					else
					{
						mask = 2047;
					}
				}
			}
		}
	}
	fallback = false;
	if (hashtable)
	{
				var __iter27 = a;
		if (! (__iter27 instanceof Array || typeof __iter27 == "string" || __is_typed_array(__iter27) || __is_some_array(__iter27) )) { __iter27 = __object_keys__(__iter27) }
		for (var __i27=0; __i27 < __iter27.length; __i27++) {
			var b = __iter27[ __i27 ];
			if ((typeof(b)==="number") && ( b ) === ( (b | 0) ))
			{
				key = (b & mask);
				hashtable[key] = b;
				keys.push(key);
			}
			else
			{
				fallback = true;
				break;
			}
		}
	}
	else
	{
		fallback = true;
	}
	s = [];
	if (fallback)
	{
				var __iter28 = a;
		if (! (__iter28 instanceof Array || typeof __iter28 == "string" || __is_typed_array(__iter28) || __is_some_array(__iter28) )) { __iter28 = __object_keys__(__iter28) }
		for (var __i28=0; __i28 < __iter28.length; __i28++) {
			var item = __iter28[ __i28 ];
			if (s.indexOf(item)===-1)
			{
				s.push(item);
			}
		}
	}
	else
	{
		__sort_method(keys);
				var __iter29 = keys;
		if (! (__iter29 instanceof Array || typeof __iter29 == "string" || __is_typed_array(__iter29) || __is_some_array(__iter29) )) { __iter29 = __object_keys__(__iter29) }
		for (var __i29=0; __i29 < __iter29.length; __i29++) {
			var key = __iter29[ __i29 ];
			s.push(hashtable[key]);
		}
	}
	return s;
}

var frozenset = function(a)
{
	
	return set(a);
}

var array = function(typecode, initializer, little_endian)
{
	this.__init__(typecode, initializer, little_endian);
}

array.prototype.__init__ = function(typecode, _kwargs_)
{
	var size,buff;
	var initializer   = (_kwargs_ === undefined || _kwargs_.initializer === undefined)  ?	null  : _kwargs_.initializer;
	var little_endian = (_kwargs_ === undefined || _kwargs_.little_endian === undefined)?	false : _kwargs_.little_endian;
	this.typecode = typecode;
	this.itemsize = this.typecodes[typecode];
	this.little_endian = little_endian;
	if (initializer)
	{
		this.length = len(initializer);
		this.bytes = (this.length * this.itemsize);
		if (this.typecode==="float8")
		{
			this._scale = max([Math.abs(min(initializer)), max(initializer)]);
			this._norm_get = (this._scale / 127);
			this._norm_set = (1.0 / this._norm_get);
		}
		else
		{
			if (this.typecode==="float16")
			{
				this._scale = max([Math.abs(min(initializer)), max(initializer)]);
				this._norm_get = (this._scale / 32767);
				this._norm_set = (1.0 / this._norm_get);
			}
		}
	}
	else
	{
		this.length = 0;
		this.bytes = 0;
	}
	size = this.bytes;
	buff = new ArrayBuffer(size);
	this.dataview = new DataView(buff);
	this.buffer = buff;
	this.fromlist(initializer);
}

array.prototype.__len__ = function()
{
	
	return this.length;
}

array.prototype.__contains__ = function(value)
{
	var arr;
	arr = this.to_array();
	if (arr.indexOf(value)===-1)
	{
		return false;
	}
	else
	{
		return true;
	}
}

array.prototype.__getitem__ = function(index)
{
	var func_name,dataview,value,step,func,offset;
	step = this.itemsize;
	offset = (step * index);
	dataview = this.dataview;
	func_name = ("get" + this.typecode_names[this.typecode]);
	func = dataview[func_name].bind(dataview);
	if (( offset ) < this.bytes)
	{
		value = func(offset);
		if (this.typecode==="float8")
		{
			value = (value * this._norm_get);
		}
		else
		{
			if (this.typecode==="float16")
			{
				value = (value * this._norm_get);
			}
		}
		return value;
	}
	else
	{
		throw new IndexError(index);
	}
}

array.prototype.__setitem__ = function(index, value)
{
	var func_name,dataview,step,func,offset;
	step = this.itemsize;
	if (( index ) < 0)
	{
		index = ((this.length + index) - 1);
	}
	offset = (step * index);
	dataview = this.dataview;
	func_name = ("set" + this.typecode_names[this.typecode]);
	func = dataview[func_name].bind(dataview);
	if (( offset ) < this.bytes)
	{
		if (this.typecode==="float8")
		{
			value = (value * this._norm_set);
		}
		else
		{
			if (this.typecode==="float16")
			{
				value = (value * this._norm_set);
			}
		}
		func(offset, value);
	}
	else
	{
		throw new IndexError(index);
	}
}

array.prototype.__iter__ = function()
{
	
	return  new Iterator(this, 0);
}

array.prototype.get = function(index)
{
	
	return this[index];
}

array.prototype.fromlist = function(lst)
{
	var typecode,i,func_name,dataview,length,item,step,func,offset,size;
	length = len(lst);
	step = this.itemsize;
	typecode = this.typecode;
	size = (length * step);
	dataview = this.dataview;
	func_name = ("set" + this.typecode_names[typecode]);
	func = dataview[func_name].bind(dataview);
	if (( size ) <= this.bytes)
	{
		i = 0;
		offset = 0;
		while (( i ) < length)
		{
			item = lst[i];
			if (typecode==="float8")
			{
				item *= this._norm_set;
			}
			else
			{
				if (typecode==="float16")
				{
					item *= this._norm_set;
				}
			}
			func(offset,item);
			offset += step;
			i += 1;
		}
	}
	else
	{
		throw new TypeError;
	}
}

array.prototype.resize = function(length)
{
	var source,new_buff,target,new_size,buff;
	buff = this.buffer;
	source = new Uint8Array(buff);
	new_size = (length * this.itemsize);
	new_buff = new ArrayBuffer(new_size);
	target = new Uint8Array(new_buff);
	target.set(source);
	this.length = length;
	this.bytes = new_size;
	this.buffer = new_buff;
	this.dataview = new DataView(new_buff);
}

array.prototype.append = function(value)
{
	var length;
	length = this.length;
	this.resize((this.length + 1));
	this[length] = value;
}

array.prototype.extend = function(lst)
{
	
		var __iter30 = lst;
	if (! (__iter30 instanceof Array || typeof __iter30 == "string" || __is_typed_array(__iter30) || __is_some_array(__iter30) )) { __iter30 = __object_keys__(__iter30) }
	for (var __i30=0; __i30 < __iter30.length; __i30++) {
		var value = __iter30[ __i30 ];
		this.append(value);
	}
}

array.prototype.to_array = function()
{
	var i,item,arr;
	arr = [];
	i = 0;
	while (( i ) < this.length)
	{
		item = this[i];
		arr.push( item );
		i += 1;
	}
	return arr;
}

array.prototype.to_list = function()
{
	
	return this.to_array();
}

array.prototype.to_ascii = function()
{
	var i,length,s,arr;
	s = "";
	arr = this.to_array();
	i = 0;
	length = arr.length;
	while (( i ) < length)
	{
		var char = String.fromCharCode(arr[i]);
		s += char;
		i += 1;
	}
	return s;
}

var file = function(path, flags)
{
	this.__init__(path, flags);
}

file.prototype.__init__ = function(path, flags)
{
	
	this.path = path;
	if (flags==="rb")
	{
		this.flags = "r";
		this.binary = true;
	}
	else
	{
		if (flags==="wb")
		{
			this.flags = "w";
			this.binary = true;
		}
		else
		{
			this.flags = flags;
			this.binary = false;
		}
	}
	this.flags = flags;
}

file.prototype.read = function(_kwargs_)
{
	var _fs,path;
	var binary = (_kwargs_ === undefined || _kwargs_.binary === undefined)?	false : _kwargs_.binary;
	_fs = require("fs");
	path = this.path;
	if (binary || this.binary)
	{
		return _fs.readFileSync(path, { encoding:null });
	}
	else
	{
		return _fs.readFileSync(path, { "encoding":"utf8" });
	}
}

file.prototype.write = function(data, _kwargs_)
{
	var path,buff,_fs;
	var binary = (_kwargs_ === undefined || _kwargs_.binary === undefined)?	false : _kwargs_.binary;
	_fs = require("fs");
	path = this.path;
	if (binary || this.binary)
	{
		binary = (binary || this.binary);
		if (binary==="base64")
		{
			buff =  new Buffer(data, "base64");
			_fs.writeFileSync(path, buff, { "encoding":null });
		}
		else
		{
			_fs.writeFileSync(path, data, { "encoding":null });
		}
	}
	else
	{
		_fs.writeFileSync(path, data, { "encoding":"utf8" });
	}
}

file.prototype.close = function()
{
	
	/*pass*/
}

var __open__ = function(path, _kwargs_)
{
	
	var mode = (_kwargs_ === undefined || _kwargs_.mode === undefined)?	null : _kwargs_.mode;
	return  new file(path, mode);
}

json = { "loads":(function (s) {return JSON.parse(s);}), "dumps":(function (o) {return JSON.stringify(o);}) };
var __get_other_workers_with_shared_arg = function(worker, ob)
{
	var a,other,args;
	a = [];
		var __iter31 = threading.workers;
	if (! (__iter31 instanceof Array || typeof __iter31 == "string" || __is_typed_array(__iter31) || __is_some_array(__iter31) )) { __iter31 = __object_keys__(__iter31) }
	for (var __i31=0; __i31 < __iter31.length; __i31++) {
		var b = __iter31[ __i31 ];
		other = b["worker"];
		args = b["args"];
		if (( other ) !== worker)
		{
						var __iter32 = args;
			if (! (__iter32 instanceof Array || typeof __iter32 == "string" || __is_typed_array(__iter32) || __is_some_array(__iter32) )) { __iter32 = __object_keys__(__iter32) }
			for (var __i32=0; __i32 < __iter32.length; __i32++) {
				var arg = __iter32[ __i32 ];
				if (( arg ) === ob)
				{
					if (! (__contains__(a, other)))
					{
						a.append(other);
					}
				}
			}
		}
	}
	return a;
}

threading = { "workers":[], "_blocking_callback":null };
var __start_new_thread = function(f, args)
{
	var jsargs,worker;
	worker =  new Worker(f);
	worker.__uid__ = len(threading.workers);
	threading.workers.append({ "worker":worker, "args":args });
		var func = function(event)
	{
		var a,res,value;
		if (event.data.type==="terminate")
		{
			worker.terminate();
		}
		else
		{
			if (event.data.type==="call")
			{
				res = __module__[event.data.function].apply(null, event.data.args);
				if (( res ) !== null && ( res ) !== undefined)
				{
					worker.postMessage({ "type":"return_to_blocking_callback", "result":res });
				}
			}
			else
			{
				if (event.data.type==="append")
				{
					a = args[event.data.argindex];
					a.push(event.data.value);
										var __iter33 = __get_other_workers_with_shared_arg(worker, a);
					if (! (__iter33 instanceof Array || typeof __iter33 == "string" || __is_typed_array(__iter33) || __is_some_array(__iter33) )) { __iter33 = __object_keys__(__iter33) }
					for (var __i33=0; __i33 < __iter33.length; __i33++) {
						var other = __iter33[ __i33 ];
						other.postMessage({ "type":"append", "argindex":event.data.argindex, "value":event.data.value });
					}
				}
				else
				{
					if (event.data.type==="__setitem__")
					{
						a = args[event.data.argindex];
						value = event.data.value;
						if (a.__setitem__)
						{
							a.__setitem__(event.data.index, value);
						}
						else
						{
							a[event.data.index] = value;
						}
												var __iter34 = __get_other_workers_with_shared_arg(worker, a);
						if (! (__iter34 instanceof Array || typeof __iter34 == "string" || __is_typed_array(__iter34) || __is_some_array(__iter34) )) { __iter34 = __object_keys__(__iter34) }
						for (var __i34=0; __i34 < __iter34.length; __i34++) {
							var other = __iter34[ __i34 ];
							other.postMessage({ "type":"__setitem__", "argindex":event.data.argindex, "key":event.data.index, "value":event.data.value });
						}
					}
					else
					{
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
		var __iter35 = args;
	if (! (__iter35 instanceof Array || typeof __iter35 == "string" || __is_typed_array(__iter35) || __is_some_array(__iter35) )) { __iter35 = __object_keys__(__iter35) }
	for (var __i35=0; __i35 < __iter35.length; __i35++) {
		var arg = __iter35[ __i35 ];
		if (arg.jsify)
		{
			jsargs.append(arg.jsify());
		}
		else
		{
			jsargs.append(arg);
		}
		if (arg instanceof Array)
		{
			__gen_worker_append(worker, arg, i);
		}
		i += 1;
	}
	worker.postMessage({ "type":"execute", "args":jsargs });
	return worker;
}

var __gen_worker_append = function(worker, ob, index)
{
	
		var append = function(item)
	{
		
		worker.postMessage({ "type":"append", "argindex":index, "value":item });
		ob.push(item);
	}

	Object.defineProperty(ob, "append", { "enumerable":false, "value":append, "writeable":true, "configurable":true });
}

var __webworker_wrap = function(ob, argindex)
{
	
	if (ob instanceof Array)
	{
				var func = function(index, item)
		{
			
			postMessage({ "type":"__setitem__", "index":index, "value":item, "argindex":argindex });
			Array.prototype.__setitem__.call(ob, index, item);
		}

		Object.defineProperty(ob, "__setitem__", { "enumerable":false, "value":func, "writeable":true, "configurable":true });
				var func = function(item)
		{
			
			postMessage({ "type":"append", "value":item, "argindex":argindex });
			Array.prototype.push.call(ob, item);
		}

		Object.defineProperty(ob, "append", { "enumerable":false, "value":func, "writeable":true, "configurable":true });
	}
	else
	{
		if (typeof(ob)==="object")
		{
						var func = function(key, item)
			{
				
				postMessage({ "type":"__setitem__", "index":key, "value":item, "argindex":argindex });
				ob[key] = item;
			}

			Object.defineProperty(ob, "__setitem__", { "enumerable":false, "value":func, "writeable":true, "configurable":true });
		}
	}
	return ob;
}

var __rpc__ = function(url, func, args)
{
	var req;
	req =  new XMLHttpRequest();
	req.open("POST", url, false);
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify({ "call":func, "args":args }));
	return JSON.parse(req.responseText);
}

var __rpc_iter__ = function(url, attr)
{
	var req;
	req =  new XMLHttpRequest();
	req.open("POST", url, false);
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify({ "iter":attr }));
	return JSON.parse(req.responseText);
}

var __rpc_set__ = function(url, attr, value)
{
	var req;
	req =  new XMLHttpRequest();
	req.open("POST", url, false);
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify({ "set":attr, "value":value }));
}

var __rpc_get__ = function(url, attr)
{
	var req;
	req =  new XMLHttpRequest();
	req.open("POST", url, false);
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify({ "get":attr }));
	return JSON.parse(req.responseText);
}
