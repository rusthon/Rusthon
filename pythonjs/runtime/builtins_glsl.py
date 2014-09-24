pythonjs.configure( runtime_exceptions=False )
pythonjs.configure( direct_operator='+' )
pythonjs.configure( direct_operator='*' )
pythonjs.configure( direct_keys=True )


with javascript:
	def int16(a):  ## used by glsljit when packing structs.
		arr = new(Int16Array(1))
		arr[0]=a
		return arr

	def __gpu_object(cls, struct_name, data_name):
		cls.prototype.__struct_name__ = struct_name
		cls.prototype.__struct_data__ = data_name
	with lowlevel:
		gpu = {
			'object' : __gpu_object
		}

	def glsljit_runtime(header):
		return new( GLSLJITRuntime(header) )

	class GLSLJITRuntime:
		def __init__(self, header):
			self.header = header
			self.shader = []
			self.object_packagers = []
			self.struct_types = {}
			self.glsltypes = ['vec2', 'vec3', 'vec4', 'mat4']
			self.matrices = []

		def compile_header(self):
			a = []  ## insert structs at top of header
			for sname in self.struct_types:
				if sname in self.glsltypes:
					pass
				else:
					a.push( self.struct_types[sname]['code'] )

			## calls get_global_id, see WebCLGL API docs. ##
			a.push('int matrix_index() { return int(get_global_id().y*%s.0); }' %self.matrices.length)
			a.push('int matrix_row() { return int(get_global_id().x*4.0); }')  ## returns: 0, 1, 2, 3

			## first class array error, can not return an array, even when the size is known ##
			#a.push('float[3] floatN( float a, float b, float c) { float f[3]; f[0]=a; f[1]=b; f[2]=b; return f; }')

			## these could be generated for each array size to reduce the mess in main,
			## TODO it would be better to upload them as uniforms.
			#a.push('void floatN( float f[3], float a, float b, float c) { f[0]=a; f[1]=b; f[2]=b; }')

			## the array can be declared in the header, but not filled with data here.
			#a.push('float XXX[3];')
			#a.push('floatN( XXX, 1.1, 2.2, 3.3 );')
			#a.push('XXX[0]=1.1;')


			a = '\n'.join(a)
			## code in header could be methods that reference the struct types above.
			b = "\n".join(self.header)
			return '\n'.join([a,b])

		def compile_main(self):
			return '\n'.join(self.shader)

		def push(self, s):
			self.shader.push(s)


		def define_structure(self, ob):
			struct_name = None
			#if Object.hasOwnProperty.call(ob,'__struct_name__'):
			if ob.__struct_name__:
				struct_name = ob.__struct_name__
				if struct_name in self.struct_types:
					return struct_name

			arrays = []
			floats = []
			integers = []
			structs = []
			struct_type = []  ## fallback for javascript objects

			if struct_name and struct_name in self.glsltypes:
				return struct_name

			#for key in ob.keys():
			for key in dir( ob ):
				if key.length==1 and key in '0123456789':
					raise RuntimeError(key)
				t = typeof( ob[key] )
				if t=='object' and instanceof(ob[key], Array) and ob[key].length and typeof(ob[key][0])=='number':
					struct_type.push( 'ARY_'+key )
					arrays.push(key)
				elif t=='number':
					struct_type.push( 'NUM_'+key)
					floats.push(key)
				elif instanceof(ob[key], Int16Array):
					struct_type.push( 'INT_'+key)
					if ob[key].length == 1:
						integers.push(key)
					else:
						pass  ## TODO int16array
				elif t=='object' and ob[key].__struct_name__:
					struct_type.push( 'S_'+key)
					structs.push( key )
					if ob[key].__struct_name__ not in self.struct_types:
						if ob[key].__struct_name__ in self.glsltypes:
							pass
						else:
							self.define_structure( ob[key] )

			if struct_name is None:
				#print('DEGUG: new struct name', ob.__struct_name__)
				#print(ob)
				struct_name = ''.join( struct_type )
				ob.__struct_name__ = struct_name

			if struct_name not in self.struct_types:
				member_list = []
				for key in integers:
					member_list.append('int '+key+';')
				for key in floats:
					member_list.append('float '+key+';')
				for key in arrays:
					arr = ob[key]
					member_list.append('float '+key+'['+arr.length+'];')
				for key in structs:
					subtype = ob[key].__struct_name__
					member_list.append( subtype+' '+key+';')

				if len(member_list)==0:
					raise RuntimeError(struct_name)

				members = ''.join(member_list)
				code = 'struct ' +struct_name+ ' {' +members+ '};'
				#print('-------struct glsl code-------')
				#print(code)
				#print('------------------------------')
				self.struct_types[ struct_name ] = {
					'arrays' : arrays,
					'floats' : floats,
					'integers': integers,
					'structs' : structs,
					'code'   : code
				}
			return struct_name

		def structure(self, ob, name):
			wrapper = None
			if instanceof(ob, Object):
				pass
			elif ob.__class__ is dict:
				wrapper = ob
				ob = ob[...]

			sname = self.define_structure(ob)
			if wrapper:
				wrapper.__struct_name__ = sname

			args = []
			stype = self.struct_types[ sname ]

			# if stype is None:  ## TODO fix me
			if sname not in self.struct_types:
				if sname in self.glsltypes:
					if sname == 'mat4':
						if ob.__struct_data__:
							o = ob[ ob.__struct_data__ ]
						else:
							o = ob

						for i in range(o.length):
							value = o[i] +''
							if '.' not in value: value += '.0'
							args.push( value )

				else:
					raise RuntimeError('no method to pack structure: ' +sname)

			has_arrays = False
			if stype:
				if stype['arrays'].length > 0:
					has_arrays = True

				for key in stype['integers']:
					args.push( ob[key][0]+'' )

				for key in stype['floats']:
					value = ob[key] + ''
					if '.' not in value:
						value += '.0'
					args.push( value )

				for key in stype['arrays']:
					#args.push( '{'+ob[key].toString()+ '}')  ## this will not work
					## arrays need to be assigned to a local variable before passing
					## it to the struct constructor.
					aname = '_'+key+name
					self.array(ob[key], aname)
					args.push( aname )

				for key in stype['structs']:
					aname = '_'+key+name
					self.structure(ob[key], aname)
					args.push( aname )

			args = ','.join(args)
			if has_arrays:
				self.shader.push( sname + ' ' +name+ '=' +sname+ '(' +args+ ');' )
			else:
				self.header.push( 'const ' + sname + ' ' +name+ '=' +sname+ '(' +args+ ');' )
			return stype

		def int16array(self, ob, name):
			a = ['int ' + name + '[' + ob.length + ']']
			i = 0
			while i < ob.length:
				a.push(';'+name+'['+i+']='+ob[i])
				i += 1

			self.shader.push( ''.join(a) )

		def array(self, ob, name):
			if instanceof(ob[0], Array):
				a = [] #'float ' + name + '[' + ob.length + ']']
				i = 0
				while i < ob.length:
					subarr = ob[i]
					subname = '%s_%s'%(name,i)
					if a.length==0:
						a.append('float ' + subname + '[' + subarr.length + ']')
					else:
						a.append(';float ' + subname + '[' + subarr.length + ']')
					j = 0
					while j < subarr.length:
						v = subarr[j] + ''
						if '.' not in v:
							v += '.0'
						a.push(';'+subname+'['+j+']='+v)
						j += 1

					i += 1

				self.shader.push( ''.join(a) )

			elif instanceof(ob[0], Object) or ob[0].__class__ is dict:
				i = 0
				while i < ob.length:
					self.structure( ob[i], name+'_'+i)
					i += 1

			else:
				a = ['float ' + name + '[' + ob.length + '];']
				i = 0
				while i < ob.length:
					a.push(name+'['+i+']='+ob[i] + ';')
					i += 1

				self.shader.push( ''.join(a) )

		def object(self, ob, name):
			for p in self.object_packagers:
				cls, func = p
				if instanceof(ob, cls):
					return func(ob)

		def unpack_array2d(self, arr, dims):
			if typeof(dims)=='number':
				return arr

			w,h = dims
			row = []
			rows = [row]
			for value in arr:
				row.append(value)
				if row.length >= w:
					row = []
					rows.append(row)
			rows.pop()
			if rows.length != h:
				print('ERROR: __unpack_array2d, invalid height.')
			return rows

		def unpack_vec4(self, arr, dims):
			if typeof(dims)=='number':
				w = dims
				h = 1
			else:
				w,h = dims
			rows = []
			i=0
			for y in range(h):
				row = []
				rows.append( row )
				for x in range(w):
					vec = []
					for j in range(4):
						vec.append( arr[i])
						i += 1
					row.append( vec )

			if rows.length != h:
				print('ERROR: __unpack_vec4, invalid height.')
			return rows

		def unpack_mat4(self, arr):
			i = 0
			for mat in self.matrices:
				for j in range(16):
					mat[j] = arr[i]
					i += 1
			return self.matrices