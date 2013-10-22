# Google Blockly wrapper for PythonJS
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

BlocklyBlockGenerators = dict()  ## Blocks share a single namespace in Blockly
_blockly_selected_block = None   ## for triggering on_click_callback

def initialize_blockly( blockly_id='blocklyDiv', toolbox_id='toolbox', on_changed_callback=None ):
	print 'initialize_blockly'
	if len( BlocklyBlockGenerators.keys() ):
		toolbox = document.getElementById( toolbox_id )
		cat = document.createElement('category')
		cat.setAttribute('name', 'Callbacks')
		toolbox.appendChild( cat )
		for block_name in BlocklyBlockGenerators.keys():
			e = document.createElement('block')
			e.setAttribute('type', block_name)
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
				if _blockly_selected_block and _blockly_selected_block.on_selected_callback:
					print 'BLOCKLY - new block selected:', _blockly_selected_block
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
	def __init__(self, name, title=None, color=None):
		self.setup( name, title=title, color=color )

	def setup(self, name, title=None, color=None):
		if name in BlocklyBlockGenerators: raise TypeError
		BlocklyBlockGenerators[ name ] = self
		self.name = name
		self.title = title
		self.color = color
		self.input_values = []
		self.input_statements = []
		self.output = None
		self.stackable = False
		self.stack_input = False
		self.stack_output = False
		self.is_statement = False
		self.external_function = None
		self.on_click_callback = None

	def callback(self, jsfunc):  ## decorator
		self.set_external_function( jsfunc.NAME )
		return jsfunc

	def set_on_click_callback(self, callback):
		self.on_click_callback = callback

	def set_external_function(self, func_name):
		self.external_function = func_name
		if self.title:
			self.title = self.title + ':  ' + func_name

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

	def add_input_value(self, name=None, type=None, title=None):
		if name is None: raise TypeError
		elif type == 'Number': pass
		elif type == 'String': pass
		elif type == 'Array': pass
		else: raise TypeError
		self.input_values.append(
			{'name':name, 'type':type, 'title':title}
		)

	def add_input_statement(self, name=None, title=None):
		if name is None: raise TypeError
		self.input_statements.append(
			{'name':name, 'title':title}
		)


	def bind_block(self):
		block_name = self.name
		stack_input = self.stack_input
		stack_output = self.stack_output
		output = self.output
		if stack_input or stack_output:
			if output:
				raise TypeError

		title = self.title
		input_values = self.input_values
		input_statements = self.input_statements
		color = self.color

		with javascript:
			def init():
				if color:
					this.setColour( color )

				if title:
					this.appendDummyInput().appendTitle(title)

				if stack_input:
					this.setPreviousStatement( True )
				if stack_output:
					this.setNextStatement( True )

				for input in input_values: # input[...]['name'] for a dict becomes: input.__dict__.js_object['name']
					this.appendValueInput( input['name'] ).setCheck( input['type'] ).appendTitle( input['title'] )

				for input in input_statements:
					this.appendStatementInput( input['name'] ).appendTitle( input['title'] )

				if output == '*':
					this.setOutput( True, null )  ## allows output of any type
				elif output:
					this.setOutput( True, output )

			print 'binding block:', block_name
			Blockly.Blocks[ block_name ] = {'init':init}  ## register the block type with Blockly

	def bind_generator(self):
		block_name = self.name
		external_function = self.external_function
		input_values = self.input_values
		input_statements = self.input_statements
		is_statement = self.is_statement

		with javascript:
			def generator(block):
				code = ''

				args = []
				for input in input_values:
					a = Blockly.Python.valueToCode(block, input['name'], Blockly.Python.ORDER_NONE)
					args.push( a )

				for input in input_statements:
					a = Blockly.Python.statementToCode(block, input['name'])
					args.push( a )

				if external_function:
					code += external_function + '(' + ','.join(args) + ')'
				else:  ## this should be a simple series of statements?
					for a in args:
						code += a + ';'

				if is_statement:
					return code  ## statements can directly return
				else:
					return [ code, Blockly.Python.ORDER_NONE ]  ## return Array

			print 'bindings block generator:', block_name
			Blockly.Python[ block_name ] = generator



class StatementBlock( BlocklyBlock ):
	'''
	A statement-block has a previous and/or next statement notch: stack_input and/or stack_output
	'''
	def __init__(self, name, title=None, stack_input=False, stack_output=False, color=150):
		self.setup( name, title=title, color=color )
		self.make_statement( stack_input=stack_input, stack_output=stack_output)


class ValueBlock( BlocklyBlock ):
	def __init__(self, name, title=None, output=None, color=120):
		if output is None: raise TypeError
		self.setup( name, title=title, color=color )
		self.set_output( output )





