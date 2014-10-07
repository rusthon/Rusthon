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
			if (ob instanceof ArrayBuffer)
			{
				return ob.byteLength;
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
				if (ob.__contains__)
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
	
	if (ob instanceof Int8Array || ob instanceof Uint8Array)
	{
		return true;
	}
	else
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
