# Google Blockly wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

Blockly.SCALE = 1.0
BlocklyImageHack = None
BlocklyBlockGenerators = dict()  ## Blocks share a single namespace in Blockly
BlocklyClasses = dict()

with javascript: BlocklyBlockInstances = {}   ## block-uid : block instance
_blockly_instances_uid = 0

with javascript:
	NEW_LINE = String.fromCharCode(10)

def bind_blockly_event( element, name, callback ):
	Blockly.bindEvent_( element, name, None, callback )


def __blockinstance( result, block_uid ):
	with javascript:
		BlocklyBlockInstances[ block_uid ].pythonjs_object = result
	return result

with javascript:
	def on_mouse_wheel(e):
		delta = 0
		if e.wheelDelta:  ## WebKit, Opera, IE9
			delta = e.wheelDelta
		elif e.detail:   ## firefox
			delta = -e.detail

		e.preventDefault()
		e.stopPropagation()
		if Blockly.SCALE >= 0.25 and Blockly.SCALE <= 1.0:
			Blockly.SCALE += delta * 0.001

		if Blockly.SCALE < 0.25:
			Blockly.SCALE = 0.25
		elif Blockly.SCALE > 1.0:
			Blockly.SCALE = 1.0

		#Blockly.fireUiEvent(window, 'resize')  ## this will not fire if blockly is inside a div with absolute height and width
		Blockly.mainWorkspace.setMetrics()  ## forces a direct redraw

def init_node_blockly( blockly_id ):
	document.getElementById( blockly_id ).addEventListener( 'mousewheel', on_mouse_wheel, False );
	document.getElementById( blockly_id ).addEventListener( 'DOMMouseScroll', on_mouse_wheel, False ); ## firefox

	## special node block ##
	_node_block = StatementBlock('node_input', color=0, title='<node>', category='HIDDEN')


	with javascript:
		
		## fully override Blockly.onMouseMove_
		def func(e):  ## bypass scroll bars
			drag = True
			if Blockly.on_mouse_move_workspace:
				drag = Blockly.on_mouse_move_workspace(e)

			if Blockly.mainWorkspace.dragMode and drag:
				dx = e.clientX - Blockly.mainWorkspace.startDragMouseX
				dy = e.clientY - Blockly.mainWorkspace.startDragMouseY
				x = Blockly.mainWorkspace.startScrollX + dx
				y = Blockly.mainWorkspace.startScrollY + dy
				Blockly.mainWorkspace.scrollX = x
				Blockly.mainWorkspace.scrollY = y
				Blockly.fireUiEvent(window, 'resize')
		Blockly.onMouseMove_ = func

		Blockly.__onMouseDown__ = Blockly.onMouseDown_
		def func(e):
			if Blockly.on_mouse_down_workspace:
				Blockly.on_mouse_down_workspace( e )
			Blockly.__onMouseDown__( e )
		Blockly.onMouseDown_ = func

		Blockly.__getMainWorkspaceMetrics__ = Blockly.getMainWorkspaceMetrics_
		def func():
			m = Blockly.__getMainWorkspaceMetrics__()
			m['scale'] = Blockly.SCALE
			return m
		Blockly.getMainWorkspaceMetrics_ = func

		## fully override Blockly.setMainWorkspaceMetrics_
		def func( xyRatio ):
			metrics = Blockly.getMainWorkspaceMetrics_();

			## TODO fix scroll bars
			#if goog.isNumber(xyRatio.x):
			#	Blockly.mainWorkspace.scrollX = -metrics.contentWidth * xyRatio.x - metrics.contentLeft
			#if goog.isNumber(xyRatio.y):
			#	Blockly.mainWorkspace.scrollY = -metrics.contentHeight * xyRatio.y - metrics.contentTop

			x = Blockly.mainWorkspace.scrollX + metrics.absoluteLeft
			y = Blockly.mainWorkspace.scrollY + metrics.absoluteTop
			trans = 'translate(' + x + ',' + y + ')'
			trans = trans + ',' + 'scale(' + metrics.scale + ',' + metrics.scale + ')'
			Blockly.mainWorkspace.getCanvas().setAttribute('transform', trans)
			Blockly.mainWorkspace.getBubbleCanvas().setAttribute('transform', trans)
		Blockly.setMainWorkspaceMetrics_ = func

		############################ override prototypes #########################

		## override BlockSvg init so that we can create the node link lines ##
		Blockly.BlockSvg.prototype.__init__ = Blockly.BlockSvg.prototype.init
		@Blockly.BlockSvg.prototype.init
		def func():
			this.__init__()
			this.svgLinks = Blockly.createSvgElement(
				'path',
				{}, 
				null
			)
			this.svgLinks.setAttribute('stroke','#000000')
			#this.svgLinks.setAttribute('style','stroke-width:2px;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:0.5')
			this.svgLinks.setAttribute('style','stroke-width:3px;stroke-linecap:round;stroke-linejoin:miter;stroke-opacity:0.5;stroke-dasharray:44, 22')

		@Blockly.BlockSvg.prototype.renderSvgLinks
		def func():
			if this.block_.nodeOutputBlocks != None and this.block_.nodeOutputBlocks.length:
				pt = this.block_.getRelativeToSurfaceXY()
				pt.y += 10
				d = []
				for block in this.block_.nodeOutputBlocks:
					xy = block.getRelativeToSurfaceXY()
					hw = block.getHeightWidth()
					x = xy.x + hw.width
					y = xy.y + 10
					d.push( 'M' )
					d.push( pt.x + ',' + pt.y )
					d.push( x + ',' + y )
				this.svgLinks.setAttribute('d', ' '.join(d) )

		Blockly.BlockSvg.prototype.__render__ = Blockly.BlockSvg.prototype.render
		@Blockly.BlockSvg.prototype.render
		def func():
			this.renderSvgLinks()
			this.__render__()

		Blockly.Block.prototype.__initSvg__ = Blockly.Block.prototype.initSvg
		@Blockly.Block.prototype.initSvg
		def func():
			this.__initSvg__()
			this.workspace.getCanvas().appendChild(this.svg_.svgLinks)


def override_blockly_prototypes():

	with javascript:

		## returns class instance attached to this Block,
		## see bind_class for details
		@Blockly.Block.prototype.getPythonObject
		def func():
			return this.pythonjs_object


		Blockly.Block.prototype.__duplicate__ = Blockly.Block.prototype.duplicate_
		@Blockly.Block.prototype.duplicate_
		def func():
			block = this.__duplicate__()
			print 'NEW BLOCKKKKKKK', block
			return block

		Blockly.Block.prototype.__onMouseDown__ = Blockly.Block.prototype.onMouseDown_
		@Blockly.Block.prototype.onMouseDown_
		def func(e):
			if e.button == 1: ## middle click
				x = e.clientX * 1.0 / Blockly.SCALE
				y = e.clientY * 1.0 / Blockly.SCALE
				b = e.button
				ee = {clientX:x, clientY:y, button:b}
				ee.stopPropagation = lambda : e.stopPropagation()
				this.__onMouseDown__(ee)
			elif e.button == 0: ## left click
				x = e.clientX * 1.0 / Blockly.SCALE
				y = e.clientY * 1.0 / Blockly.SCALE
				b = e.button
				ee = {clientX:x, clientY:y, button:b}
				ee.stopPropagation = lambda : e.stopPropagation()
				this.__onMouseDown__(ee)
			else:
				this.__onMouseDown__(e)

		Blockly.Block.prototype.__onMouseUp__ = Blockly.Block.prototype.onMouseUp_
		@Blockly.Block.prototype.onMouseUp_
		def func(e):
			parent = this.getParent()
			connection = Blockly.highlightedConnection_
			this.__onMouseUp__(e)

			if this.__dragging:
				print 'drag done', this.svg_.getRootElement().getAttribute('transform')
				this.__dragging = False

			if parent is null and this.getParent():
				print 'plugged:', this
				parent = this.getParent()

				if this.__on_plugged:
					this.__on_plugged( this.pythonjs_object, parent.pythonjs_object, this, parent )

				if parent.on_child_plugged:
					parent.on_child_plugged( this )

				if this.nodeOutputBlocks != None and e.button == 1:  ## middle click

					this.setParent(null)
					this.moveTo( this.startDragX, this.startDragY )

					if parent.nodeInputBlocks.indexOf( this ) == -1:
						parent.nodeInputBlocks.push( this )

					dom = document.createElement('block')
					dom.setAttribute('type', 'node_input')
					node = Blockly.Xml.domToBlock_( this.workspace, dom )
					node.previousConnection.targetConnection = connection
					connection.targetConnection = node.previousConnection
					node.setParent( parent )
					parent.render()  ## rerendering moves the node block

					node.nodeInputBlocks.push( this )  ## temp just for proper rendering

					this.nodeOutputBlocks.push( node )

					this.render()

		Blockly.Block.prototype.__onMouseMove__ = Blockly.Block.prototype.onMouseMove_
		@Blockly.Block.prototype.onMouseMove_
		def func(e):

			if this.svg_.renderSvgLinks != None:
				this.svg_.renderSvgLinks()  ## render output node links
			## also need to call renderSvgLinks on our inputs
			if this.nodeInputBlocks != None and this.nodeInputBlocks.length:
				for block in this.nodeInputBlocks:
					block.svg_.renderSvgLinks()



			parent = this.getParent()
			x = e.clientX * 1.0 / Blockly.SCALE
			y = e.clientY * 1.0 / Blockly.SCALE
			b = e.button
			ee = {clientX:x, clientY:y, button:b}
			ee.stopPropagation = lambda : e.stopPropagation()

			this.__onMouseMove__(ee)
			this.__dragging = True
			if parent and this.getParent() is null:
				print 'unplugged:', this
				if this.__on_unplugged:
					this.__on_unplugged( this.pythonjs_object, parent.pythonjs_object, this, parent )


		Blockly.FieldTextInput.prototype.__onHtmlInputChange__ = Blockly.FieldTextInput.prototype.onHtmlInputChange_
		@Blockly.FieldTextInput.prototype.onHtmlInputChange_
		def func(e):
			this.__onHtmlInputChange__( e )
			if e.keyCode == 13: ## enter
				print 'ENTER KEY'
				value = this.getText()
				if this.name == 'NUM':
					if value.indexOf('.') != -1:
						value = parseFloat( value )
					else:
						value = parseInt( value )

				if this.on_enter_callback:
					print 'on_enter_callback:', value
					this.on_enter_callback( value )
				else:
					print 'WARNING: field has no on_enter_callback', this

			elif this.on_key_callback:
					this.on_key_callback( this.getText() )

		Blockly.FieldCheckbox.prototype.__showEditor__ = Blockly.FieldCheckbox.prototype.showEditor_
		@Blockly.FieldCheckbox.prototype.showEditor_
		def func():
			state = this.getValue() ## returns "TRUE" or "FALSE", (this.state_ is the raw bool)
			this.__showEditor__()
			if state != this.getValue():
				print 'check box changed'

		Blockly.FieldColour.prototype.__setValue__ = Blockly.FieldColour.prototype.setValue
		@Blockly.FieldColour.prototype.setValue
		def func( color ):
			this.__setValue__(color)
			if this.sourceBlock_ and this.sourceBlock_.rendered:
				print 'color changed', color

		Blockly.FieldDropdown.prototype.__setValue__ = Blockly.FieldDropdown.prototype.setValue
		@Blockly.FieldDropdown.prototype.setValue
		def func( value ):
			this.__setValue__(value)
			if this.sourceBlock_ and this.sourceBlock_.rendered:
				print 'dropdown changed', value
				if this.on_changed_callback:
					if value == 'FALSE' or value == 'false' or value is False:
						this.on_changed_callback( False )
					elif value == 'TRUE' or value == 'true' or value is True:
						this.on_changed_callback( True )
					else:
						this.on_changed_callback( value )




def initialize_blockly( blockly_id='blocklyDiv', toolbox_id='toolbox', on_changed_callback=None, node_blockly=False ):
	print 'initialize_blockly'

	override_blockly_prototypes()
	if node_blockly:
		init_node_blockly( blockly_id )


	if len( BlocklyBlockGenerators.keys() ):
		toolbox = document.getElementById( toolbox_id )
		defaults = []
		cats = {}
		for block_name in BlocklyBlockGenerators.keys():
			b = BlocklyBlockGenerators[ block_name ]
			e = document.createElement('block')
			e.setAttribute('type', block_name)

			if b.category == 'HIDDEN':
				pass

			elif b.category:
				if b.category in cats:
					cats[ b.category ].appendChild( e )
				else:
					cat = document.createElement('category')
					cat.setAttribute('name', b.category)
					cat.appendChild( e )
					toolbox.appendChild( cat )
					cats[ b.category ] = cat

			else:
				defaults.append( e )

			i = 0
			#for i in range(len(b.input_values)):  ## TODO check why this got broken
			while i < len(b.input_values):
				input = b.input_values[i]
				v = document.createElement('value')
				v.setAttribute('name', input['name'])
				e.appendChild(v)
				nb = document.createElement('block')
				if input['default_value'] is not None:
					default_value = input['default_value']
					if typeof(default_value) == 'boolean':
						nb.setAttribute('type', 'logic_boolean')
						t = document.createElement('title')
						t.setAttribute('name', 'BOOL')
						## Blockly is picky about these keywords, passing "True" or "true" will show 'true' in the UI but give you False for the actual value!
						if default_value:
							t.appendChild( document.createTextNode('TRUE') )
						else:
							t.appendChild( document.createTextNode('FALSE') )
						nb.appendChild(t)

					else:
						nb.setAttribute('type', 'math_number')  ## TODO support other types
						t = document.createElement('title')
						t.setAttribute('name', 'NUM')
						t.appendChild( document.createTextNode(default_value) )
						nb.appendChild(t)

				elif input['name'].startswith('color'):  ## this is hackish, but it works
					nb.setAttribute('type', 'colour_picker')

				else:
					nb.setAttribute('type', 'logic_null')
				v.appendChild(nb)
				i += 1


		if len(defaults):
			cat = document.createElement('category')
			cat.setAttribute('name', 'Callbacks')
			toolbox.appendChild( cat )
			for e in defaults:
				cat.appendChild( e )

	with javascript:
		Blockly.inject(
			document.getElementById( blockly_id ),
			{path : './', toolbox : document.getElementById(toolbox_id)}
		)


	if on_changed_callback:
		Blockly.addChangeListener( on_changed_callback )

	for block_name in BlocklyBlockGenerators.keys():
		b = BlocklyBlockGenerators[ block_name ]
		b.bind_block()
		b.bind_generator()


	bind_blockly_event(
		Blockly.getMainWorkspace().getCanvas(),
		'blocklySelectChange',
		on_select_changed
	)


def on_select_changed():
	if Blockly.selected:
		print 'new selection', Blockly.selected
		if Blockly.selected.on_selected_callback:
			Blockly.selected.on_selected_callback()


class BlocklyBlock:
	'''
	Instead of using this class directly, you should use StatementBlock or ValueBlock subclasses below.
	notes:
		. a block is not allowed to have previous or next statement notches and have an output.
		. a bare block can have no inputs or output, and no previous or next statement notches.

	'''
	def __init__(self, block_name=None, title=None, color=None, category=None, inputs_inline=False):
		self.setup( block_name=block_name, title=title, color=color, category=None, inputs_inline=inputs_inline )

	def setup(self, block_name=None, title=None, color=None, category=None, inputs_inline=False):
		if block_name is None: block_name = '_generated_block' + str(len(BlocklyBlockGenerators.keys()))
		if block_name in BlocklyBlockGenerators: raise TypeError
		BlocklyBlockGenerators[ block_name ] = self
		self.name = block_name
		self.title = title
		self.color = color
		self.category = category
		self.inputs_inline = inputs_inline
		self.input_values = []
		self.input_statements = []
		self.input_slots = []
		self.output = None
		self.stackable = False
		self.stack_input = False
		self.stack_output = False
		self.is_statement = False
		self.external_function = None
		self.external_javascript_function = None
		self.on_click_callback = None
		self.on_unplugged = None  ## when a block is removed from its parent block
		self.on_plugged = None
		self.on_child_plugged = None
		self.pythonjs_object = None  ## this is not correct, it goes on the block instance

		self.input_class_slots = []
		self._class = None
		self._class_name = None
		self._class_setters = []

		self.dropdowns = []

	def get_class(self):
		return self._class



	def _on_class_init(self, instance):
		name = self.name
		with javascript:
			block = new( Blockly.Block( Blockly.getMainWorkspace(), name ) )
			block.initSvg()
			block.render()

			## an infinite loop is avoided because we directly update the
			## low level wrapped javascript object: instance[...]
			## this.property_name is set below on the field object
			def sync_low_level(val):
				if Object.hasOwnProperty.call( instance[...], this.property_name ):
					instance[...][this.property_name] = val
				else:
					with python:
						setattr( instance, this.property_name, val, property=True )

			def sync_high_level(val):
				with python:
					prev = getattr( instance, this.property_name, property=True )
					if prev != val:
						setattr( instance, this.property_name, val, property=True )

		instance.block = block
		block.pythonjs_object = instance
		fields = {}

		#for input in self.input_values:  ## TODO - check how this got broken.
		i = 0
		while i < len(self.input_values):
			input = self.input_values[ i ]
			name = input['name']
			print 'input name', name

			default_value = getattr(instance, name)

			btype = 'text'
			if typeof( default_value ) == 'number':
				btype = 'math_number'
			elif typeof( default_value ) == 'boolean':
				btype = 'logic_boolean'

			with javascript:
				sub = new( Blockly.Block( Blockly.getMainWorkspace(), btype ) )
				print btype, sub
				sub.initSvg()
				sub.render()
				con = block.getInput( name ).connection
				con.connect( sub.outputConnection )

				if btype == 'math_number':
					field = sub.inputList[0].titleRow[0]
					field.setValue(''+default_value)
					field.on_enter_callback = sync_low_level

				elif btype == 'logic_boolean':
					field = sub.inputList[0].titleRow[0]
					field.setValue(''+default_value)
					field.on_changed_callback = sync_high_level

				elif btype == 'text':
					field = sub.inputList[0].titleRow[1]
					field.setValue(''+default_value)
					field.on_enter_callback = sync_high_level
					field.on_key_callback = sync_high_level

				field.property_name = name

			fields[ name ] = field

			i += 1

		#func = lambda n,val,inst: fields[n].setValue(''+val)  ## TODO - check why this got broken
		def func(n, val, inst):
			fields[n].setValue(''+val)

		## not all setters will have fields, only input-values,
		## not input-class-slots.
		#for name in self._class_setters:
		for name in fields:
			instance.property_callbacks[ name ] = func


		for input in self.input_class_slots:
			name = input['name']
			sinst = getattr(instance, name)
			## if sinst is None that means a subclass has defined a setter,
			## but did not initialize it, this is normal if the instance is
			## created "factory-style", and gets set afterward,
			## the factory maker or the setter, just needs to make sure it 
			## connects the block like below and calls self.block.render()
			if sinst:
				sblock = sinst.block
				con = block.getInput( name ).connection
				con.connect( sblock.previousConnection )
				instance.block.render()

	def bind_class(self, cls):  ## can be used as a decorator
		self._class = cls
		class_init_cb = self._on_class_init
		with javascript:
			class_name = cls.__name__

			if cls.init_callbacks is None:
				print 'ERROR: class needs to be decorated with: @pythonjs.init_callbacks'
			cls.init_callbacks.push( class_init_cb )

			with python:
				self._generate_from_properties( cls )

		self.title = class_name
		self._class_name = class_name
		BlocklyClasses[ class_name ] = self

		return cls

	def _generate_from_properties(self, cls):
		with javascript:
			for key in cls.__properties__:
				prop = cls.__properties__[ key ]
				return_type = prop['get'].return_type

				if prop['set'] != None:

					with python:
						self._class_setters.append( key )
						if return_type == 'float':
							self.add_input_value( name=key )
						elif return_type == 'int':
							self.add_input_value( name=key )
						elif return_type == 'bool':
							self.add_input_value( name=key)
						elif return_type == 'str':
							self.add_input_value( name=key)
						elif return_type in BlocklyClasses:
							klass = BlocklyClasses[return_type].get_class()
							self.add_input_statement(name=key, class_type=klass)

						else:
							self.add_input_statement(name=key)
				else:
					with python:
						if return_type in BlocklyClasses:
							klass = BlocklyClasses[return_type].get_class()
							self.add_input_statement(name=key, class_type=klass)


			if cls.__bases__.length:
				for base in cls.__bases__:
					with python:
						self._generate_from_properties( base )


	def javascript_callback(self, jsfunc):  ## decorator
		self.set_external_function( jsfunc.NAME, javascript=True )
		with javascript:
			arr = jsfunc.args_signature
			defs = jsfunc.kwargs_signature
		for i in range(arr.length):
			name = arr[i]
			if defs[name] is null:  ## special case: null creates a non-dynamic "slot" input statement
				self.add_input_statement( name )
			else:
				self.add_input_value( name, default_value=defs[name] )
		return jsfunc

	def callback(self, jsfunc):  ## decorator
		self.set_external_function( jsfunc.NAME )
		with javascript:
			arr = jsfunc.args_signature
			defs = jsfunc.kwargs_signature
		for i in range(arr.length):
			name = arr[i]
			if defs[name] is null:  ## special case: null creates a non-dynamic "slot" input statement
				self.add_input_statement( name )
			else:
				self.add_input_value( name, default_value=defs[name] )
		return jsfunc

	def slot_callback(self, jsfunc):  ## decorator
		self.set_external_function( jsfunc.NAME )
		with javascript:
			arr = jsfunc.args_signature
		for i in range(arr.length):
			name = arr[i]
			self.add_input_statement( name )
		return jsfunc


	def set_on_click_callback(self, callback):
		self.on_click_callback = callback

	def set_external_function(self, func_name, javascript=False):
		print 'setting external function:', func_name
		if javascript: self.external_javascript_function = func_name
		else: self.external_function = func_name
		if not self.title: self.title = func_name

	def set_output(self, output):
		if self.stack_input: raise TypeError
		elif self.stack_output: raise TypeError
		elif output == 'Number': pass
		elif output == 'String': pass
		elif output == 'Array': pass
		elif output == '*': pass
		else: raise TypeError
		self.output = output

	def make_statement(self, stack_input=None, stack_output=None):
		if self.output: raise TypeError
		elif stack_input: pass
		elif stack_output: pass
		else: raise TypeError
		self.stack_input = stack_input
		self.stack_output = stack_output
		self.is_statement = True

	def add_input_value(self, name=None, type=None, title=None, default_value=None):
		if name is None: raise TypeError
		elif type == 'Number': pass
		elif type == 'String': pass
		elif type == 'Array': pass
		#else: raise TypeError
		if title is None: title = name
		self.input_values.append(
			{'name':name, 'type':type, 'title':title, 'default_value':default_value}
		)

	def add_input_statement(self, name=None, title=None, callback=None, class_type=None):
		if name is None: raise TypeError
		if title is None: title = name
		if class_type:
			self.input_class_slots.append(
				{'name':name, 'title':title, 'class_type':class_type}
			)
		elif callback:
			self.input_statements.append(
				{'name':name, 'title':title, 'callback':callback}
			)
		else:
			self.input_slots.append(
				{'name':name, 'title':title }
			)

	def add_dropdown(self, name=None, items=None, callback=None):
		with javascript:
			jsob = []
			for item in items[...]:
				jsob.push( [item, item] )

		self.dropdowns.append( {'name':name, 'items':jsob, 'callback':callback} )

	def bind_block(self):
		global _blockly_instances_uid

		block_name = self.name
		stack_input = self.stack_input
		stack_output = self.stack_output
		output = self.output
		if stack_input or stack_output:
			if output:
				raise TypeError

		title = self.title
		color = self.color
		inputs_inline = self.inputs_inline

		input_values = self.input_values[...]
		input_statements = self.input_statements[...]
		input_slots = self.input_slots[...]
		input_class_slots = self.input_class_slots[...]

		external_function = self.external_function
		external_javascript_function = self.external_javascript_function
		is_statement = self.is_statement
		on_unplugged = self.on_unplugged
		on_plugged = self.on_plugged
		on_child_plugged = self.on_child_plugged

		dropdowns = self.dropdowns[...]

		with javascript:
			def init():
				global BlocklyImageHack

				input = null
				block_uid = _blockly_instances_uid
				_blockly_instances_uid += 1
				BlocklyBlockInstances[ block_uid ] = this
				this.uid = block_uid  ## note that blockly has its own id called: this.id

				this.__input_values = input_values
				this.__input_statements = input_statements
				this.__input_slots = input_slots
				this.__external_function = external_function
				this.__external_javascript_function = external_javascript_function
				this.__is_statement = is_statement
				this.__on_unplugged = on_unplugged
				this.__on_plugged = on_plugged
				this.on_child_plugged = on_child_plugged

				if inputs_inline:
					this.setInputsInline( True )

				this.nodeOutputBlocks = []
				this.nodeInputBlocks = []

				if color:
					this.setColour( color )

				if title:
					header = this.appendDummyInput()
					if BlocklyImageHack:  ## TODO - find a better way to do this
						img = new( Blockly.FieldImage(BlocklyImageHack, 64, 64) )
						header.appendTitle( img )
						BlocklyImageHack = null
					header.appendTitle(title)

				if dropdowns.length:
					row = header
					i = 0
					while i < dropdowns.length:
						a = dropdowns[i][...]
						if a['title']:
							row = this.appendDummyInput()
							row.appendTitle( a['title'] )

						field = new( Blockly.FieldDropdown(a['items']) )
						field.on_changed_callback = a['callback']
						field.property_name = a['name']
						field.block = this
						row.appendTitle( field )
						i += 1


				if stack_input:
					this.setPreviousStatement( True )
				if stack_output:
					this.setNextStatement( True )


				i = 0
				while i < input_values.length:
					input = input_values[i][...]
					if input['type']:
						this.appendValueInput(input['name'] ).setCheck( input['type'] ).appendTitle( '<'+input['type']+'> '+input['title'] ).setAlign(Blockly.ALIGN_RIGHT)
					else:
						this.appendValueInput(input['name'] ).appendTitle( input['title'] ).setAlign(Blockly.ALIGN_RIGHT)
					i += 1

				i = 0
				while i < input_class_slots.length:
					input = input_class_slots[i][...]
					this.appendStatementInput( input['name'] ).appendTitle( input['title']+':' )
					i += 1


				i = 0
				while i < input_slots.length:
					input = input_slots[i][...]
					this.appendStatementInput( input['name'] ).appendTitle( input['title'] )
					i += 1

				i = 0
				while i < input_statements.length:
					input = input_statements[i][...]
					this.appendStatementInput( input['name'] ).appendTitle( '{' + input['title'] + '}' )
					i += 1


				if output == '*':
					this.setOutput( True, null )  ## allows output of any type
				elif output:
					this.setOutput( True, output )

			Blockly.Blocks[ block_name ] = {'init':init}  ## register the block type with Blockly

	def bind_generator(self):
		block_name = self.name

		## this is not safe with recursive functions? or this was due to the bad local scope bug below? (see input=null)
		#external_function = self.external_function
		#external_javascript_function = self.external_javascript_function
		#is_statement = self.is_statement
		#input_values = self.input_values.js_object
		#input_statements = self.input_statements.js_object

		with javascript:
			def generator(block, from_node):

				if block.nodeOutputBlocks.length and from_node is None:
					return ''


				input_values = block.__input_values
				input_statements = block.__input_statements
				input_slots = block.__input_slots
				external_function = block.__external_function
				external_javascript_function = block.__external_javascript_function
				is_statement = block.__is_statement

				code = ''
				input = null  ## TODO fix local scope generator in python_to_pythonjs.py - need to traverse whileloops - the bug pops up here because this is recursive?
				args = []

				dynamic = True
				if external_javascript_function:
					dynamic = False
				if this.type == 'node_input':
					dynamic = False
					link = this.nodeInputBlocks[0]  ## node_input only has a single input
					code = Blockly.Python[ link.type ]( link, this )  ## from_node


				i = 0
				while i < input_values.length:
					input = input_values[i][...]
					if external_javascript_function:
						a = Blockly.JavaScript.valueToCode(block, input['name'], Blockly.JavaScript.ORDER_NONE)
					else:
						a = Blockly.Python.valueToCode(block, input['name'], Blockly.Python.ORDER_NONE)
					if a is not null:  ## blockly API not correct? is says this will return null when nothing is connected.
						args.push( a )
					i += 1

				
				if block.pythonjs_object: ## input statements are used for dynamic updates
					wrapper = block.pythonjs_object[...]
					print 'block.pythonjs_object.wrapper', wrapper
					i = 0
					while i < input_statements.length:
						input = input_statements[i][...]
						attr = wrapper[ input['name'] ]
						if attr:
							#js = Blockly.JavaScript.statementToCode(block, input['name'])
							target_block = block.getInput( input['name'] ).connection.targetBlock()
							if target_block:
								if target_block.type == 'node_input':
									target_block = target_block.nodeInputBlocks[0]
								js = Blockly.JavaScript[ target_block.type ]( target_block, True )
								if js.length:
									if input['callback']:
										print 'callback', input['callback'].NAME
										input['callback']( wrapper, attr, eval(js) )
									else:
										print 'ERROR - input is missing callback', input
						i += 1

				if external_javascript_function:
					i = 0
					while i < input_slots.length:
						input = input_slots[i][...]
						a = Blockly.JavaScript.statementToCode(block, input['name'])
						if a.length:
							args.push( a )
						else:
							args.push( "null" )
						i += 1
				else:
					i = 0
					while i < input_slots.length:
						input = input_slots[i][...]
						a = Blockly.Python.statementToCode(block, input['name'])
						if a.length:
							args.push(input['name'] + '=' +a)
						i += 1

				if external_function:
					code += external_function + '(' + ','.join(args) + ')'
				elif external_javascript_function:
					## TODO what about pure javascript functions?
					#if is_statement and block.parentBlock_:  ## TODO request Blockly API change: "parentBlock_" to "parentBlock"
					#	print 'is_statement with parent block - OK'
					#	code += external_javascript_function + '( [' + ','.join(args) + '], {} )'  ## calling from js a pyjs function
					#	print code
					#elif block.parentBlock_:  ## TODO request Blockly API change: "parentBlock_" to "parentBlock"
					#	print 'with parent block - OK'
					#	code += external_javascript_function + '( [' + ','.join(args) + '], {} )'  ## calling from js a pyjs function
					#	print code

					code += external_javascript_function + '( [' + ','.join(args) + '], {} )'  ## calling from js a pyjs function


				else:  ## TODO this should be a simple series of statements?
					for a in args:
						code += a + ';'


				if dynamic:
					code = '__blockinstance(  ' + code + '  ,' + block.uid + ')'


				if is_statement: ## statements can directly return
					if block.getSurroundParent():
						return code
					else:
						return code + NEW_LINE
				else:
					return [ code, Blockly.Python.ORDER_NONE ]  ## return Array

			if Blockly.Python:
				Blockly.Python[ block_name ] = generator
			else:
				print 'WARNING - Blockly.Python has not been loaded'

			if Blockly.JavaScript:
				Blockly.JavaScript[ block_name ] = generator
			else:
				print 'WARNING - Blockly.JavaScript has not been loaded'

			if Blockly.Python is None and Blockly.JavaScript is None:
				print 'ERROR - no blockly languages have been loaded.'

class StatementBlock( BlocklyBlock ):
	'''
	A statement-block has a previous and/or next statement notch: stack_input and/or stack_output
	'''
	def __init__(self, block_name=None, title=None, stack_input=True, stack_output=False, color=170, category=None, inputs_inline=False):
		self.setup( block_name=block_name, title=title, color=color, category=category, inputs_inline=inputs_inline )
		self.make_statement( stack_input=stack_input, stack_output=stack_output)


class ValueBlock( BlocklyBlock ):
	def __init__(self, block_name=None, title=None, output='*', color=100, category=None, inputs_inline=True):
		if output is None: raise TypeError
		self.setup( block_name=block_name, title=title, color=color, category=category, inputs_inline=inputs_inline )
		self.set_output( output )





