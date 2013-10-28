# Google Blockly wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"


BlocklyBlockGenerators = dict()  ## Blocks share a single namespace in Blockly
_blockly_selected_block = None   ## for triggering on_click_callback

with javascript: BlocklyBlockInstances = {}   ## block-uid : block instance
_blockly_instances_uid = 0

with javascript:
	NEW_LINE = String.fromCharCode(10)

def __blockinstance( result, block_uid ):
	with javascript:
		BlocklyBlockInstances[ block_uid ].pythonjs_object = result
	return result

def initialize_blockly( blockly_id='blocklyDiv', toolbox_id='toolbox', on_changed_callback=None ):
	print 'initialize_blockly'
	if len( BlocklyBlockGenerators.keys() ):
		toolbox = document.getElementById( toolbox_id )
		defaults = []
		cats = {}
		for block_name in BlocklyBlockGenerators.keys():
			b = BlocklyBlockGenerators[ block_name ]
			e = document.createElement('block')
			e.setAttribute('type', block_name)

			if b.category:
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

		def on_changed():
			global _blockly_selected_block
			if Blockly.selected != _blockly_selected_block:
				_blockly_selected_block = Blockly.selected
				if _blockly_selected_block:
					print 'BLOCKLY - new block selected:', _blockly_selected_block
					if _blockly_selected_block.on_selected_callback:
						print 'BLOCKLY - doing on select block callback'
						_blockly_selected_block.on_selected_callback()

			if on_changed_callback:  ## this gets triggered for any change, even moving a block in the workspace.
				on_changed_callback()

		Blockly.addChangeListener( on_changed )

	for block_name in BlocklyBlockGenerators.keys():
		b = BlocklyBlockGenerators[ block_name ]
		b.bind_block()
		b.bind_generator()

class BlocklyBlock:
	'''
	Instead of using this class directly, you should use StatementBlock or ValueBlock subclasses below.
	notes:
		. a block is not allowed to have previous or next statement notches and have an output.
		. a bare block can have no inputs or output, and no previous or next statement notches.

	'''
	def __init__(self, block_name=None, title=None, color=None, category=None):
		self.setup( block_name=block_name, title=title, color=color, category=None )

	def setup(self, block_name=None, title=None, color=None, category=None):
		if block_name is None: block_name = '_generated_block' + str(len(BlocklyBlockGenerators.keys()))
		if block_name in BlocklyBlockGenerators: raise TypeError
		BlocklyBlockGenerators[ block_name ] = self
		self.name = block_name
		self.title = title
		self.color = color
		self.category = category
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
		self.on_removed = None  ## when a block is removed from its parent block
		self.on_plugged = None
		self.pythonjs_object = None

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

	def add_input_statement(self, name=None, title=None, callback=None):
		if name is None: raise TypeError
		if title is None: title = name
		if callback:
			self.input_statements.append(
				{'name':name, 'title':title, 'callback':callback}
			)
		else:
			self.input_slots.append(
				{'name':name, 'title':title }
			)

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
		input_values = self.input_values.js_object
		input_statements = self.input_statements.js_object
		input_slots = self.input_slots.js_object
		external_function = self.external_function
		external_javascript_function = self.external_javascript_function
		is_statement = self.is_statement
		on_unplugged = self.on_unplugged
		on_plugged = self.on_plugged

		with javascript:
			def init():
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

				this.__previous_child_blocks = []	## this is a hackish way to check for when a block is removed

				if color:
					this.setColour( color )

				if title:
					this.appendDummyInput().appendTitle(title)

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
			def generator(block):

				## TODO - hook into Blockly event system to catch when a block is removed ##
				if block.__previous_child_blocks.length != block.childBlocks_.length:
					if block.__previous_child_blocks.length > block.childBlocks_.length:
						for child in block.__previous_child_blocks:
							#if child not in block.childBlocks_:  ## TODO fix me
							if block.childBlocks_.indexOf( child ) == -1:
								print 'UNPLUGGED:', child
								if child.__on_unplugged:
									child.__on_unplugged( child.pythonjs_object, block.pythonjs_object, child, block )
								break
					else:
						for child in block.childBlocks_:
							if block.__previous_child_blocks.indexOf( child ) == -1:
								print 'PLUGGED:', child
								if child.__on_plugged:
									child.__on_plugged( child.pythonjs_object, block.pythonjs_object, child, block )
								break


				block.__previous_child_blocks = block.childBlocks_.slice()


				input_values = block.__input_values
				input_statements = block.__input_statements
				input_slots = block.__input_slots
				external_function = block.__external_function
				external_javascript_function = block.__external_javascript_function
				is_statement = block.__is_statement

				#dynamic = input_statements.length
				#dynamic = True  ## for now make everything dynamic - TODO check if external_function returns something - this will not work!
				#dynamic = not external_javascript_function  ## TODO fix "not" in 'with javascript:'
				dynamic = True
				if external_javascript_function:
					dynamic = False

				code = ''
				input = null  ## TODO fix local scope generator in python_to_pythonjs.py - need to traverse whileloops - the bug pops up here because this is recursive?
				args = []

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
							js = Blockly.JavaScript.statementToCode(block, input['name'])
							print('block.pythonjs_object - update-dynamic: code to eval')
							print(js)
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
					if is_statement and block.parentBlock_:  ## TODO request Blockly API change: "parentBlock_" to "parentBlock"
						print 'is_statement with parent block - OK'
						code += external_javascript_function + '( [' + ','.join(args) + '], {} )'  ## calling from js a pyjs function
						print code

					elif block.parentBlock_:  ## TODO request Blockly API change: "parentBlock_" to "parentBlock"
						print 'with parent block - OK'
						code += external_javascript_function + '( [' + ','.join(args) + '], {} )'  ## calling from js a pyjs function
						print code

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
	def __init__(self, block_name=None, title=None, stack_input=True, stack_output=False, color=170, category=None):
		self.setup( block_name=block_name, title=title, color=color, category=category )
		self.make_statement( stack_input=stack_input, stack_output=stack_output)


class ValueBlock( BlocklyBlock ):
	def __init__(self, block_name=None, title=None, output='*', color=100, category=None):
		if output is None: raise TypeError
		self.setup( block_name=block_name, title=title, color=color, category=category )
		self.set_output( output )





