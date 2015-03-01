C++ Translator
-------------

subclass'es from the rust generator

```python

#import pythonjs_to_rust

JVM_HEADER = '''
#include <jni.h>

JavaVM* __create_javavm__() {
	JavaVM* jvm = new JavaVM();
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];
	args.version = JNI_VERSION_1_4;
	args.nOptions = 2;
	options[0].optionString = const_cast<char*>("-Djava.class.path=.%s");
	options[1].optionString = const_cast<char*>("-Xcheck:jni");
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;
	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

static JavaVM* __javavm__ = __create_javavm__();
'''
def gen_jvm_header( jars ):
	if jars:
		a = ':' + ':'.join(jars)
		return JVM_HEADER %a
	else:
		return JVM_HEADER %''


NIM_HEADER = '''
extern "C" {
	void PreMain();
	void NimMain();
}

'''

def gen_nim_header():
	return NIM_HEADER

class CppGenerator( RustGenerator ):
	def _visit_call_helper_new(self, node):
		'''
		low level `new` for interfacing with external c++.
		Also used for code that is blocked with `with pointers:`
		to create a class without having to create a temp variable,
		`f( new(MyClass(x,y)) )`, directly calls the constructor,
		if MyClass is a Rusthon class then __init__ will be called.
		TODO fix mixing with std::shared_ptr by keeping a weak_ptr
		in each object that __init__ returns (also fixes the _ref_hacks)
		'''
		if isinstance(node.args[0], ast.BinOp): # makes an array or map
			a = self.visit(node.args[0])
			if type(a) is not tuple:
				raise SyntaxError(self.format_error('TODO some extended type'))

			atype, avalue = a
			if atype.endswith('*'): atype = atype[:-1]
			else: pass  ## this should never happen
			return '(new %s %s)' %(atype, avalue)

		## Rusthon class ##
		elif isinstance(node.args[0], ast.Call) and isinstance(node.args[0].func, ast.Name) and node.args[0].func.id in self._classes:
			classname = node.args[0].func.id
			args = [self.visit(arg) for arg in node.args[0].args ]
			if self._classes[classname]._requires_init:
				return '(new %s)->__init__(%s)' %(classname, ','.join(args))
			else:
				if args:
					raise SyntaxError('class %s: takes no init args' %classname)
				return '(new %s)' %classname

		## external c++ class ##
		else:
			return '(new %s)' %self.visit(node.args[0])

	def __init__(self, source=None, requirejs=False, insert_runtime=False):
		RustGenerator.__init__(self, source=source, requirejs=False, insert_runtime=False)
		self._cpp = True
		self._rust = False  ## can not be true at the same time self._cpp is true, conflicts in switch/match hack.
		self._shared_pointers = True
		self._noexcept = False
		self._polymorphic = False  ## by default do not use polymorphic classes (virtual methods)
		self._has_jvm = False
		self._jvm_classes = dict()
		self._has_nim = False

	def visit_Delete(self, node):
		targets = [self.visit(t) for t in node.targets]
		if len(targets)==0:
			raise RuntimeError('no delete targets')
		r = []
		if self._shared_pointers:
			for t in targets:
				## shared_ptr.reset only releases if no there are no other references,
				## is there a way to force the delete on all shared pointers to something?
				#r.append('delete %s;' %t)  ## only works on pointers
				r.append('%s.reset();' %t)
		else:
			for t in targets:
				if t in self._known_arrays:
					r.append('delete[] %s;')
				else:
					r.append('delete %s;')

		return '\n'.join(r)

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		return 'std::string("%s")' % s

	def visit_Print(self, node):
		r = []
		for e in node.values:
			s = self.visit(e)
			if isinstance(e, ast.List) or isinstance(e, ast.Tuple):
				for sube in e.elts:
					r.append('std::cout << %s;' %self.visit(sube))
				if r:
					r[-1] += 'std::cout << std::endl;'
				else:
					r.append('std::cout << std::endl;')
			else:
				r.append('std::cout << %s << std::endl;' %s)
		return '\n'.join(r)


	def visit_TryExcept(self, node, finallybody=None):
		out = []

		out.append( 'try {' )
		self.push()
		for b in node.body:
			out.append( self.indent()+self.visit(b) )

		self.pull()
		out.append( self.indent() + '} catch (const std::exception& e) {' )
		self.push()
		for h in node.handlers:
			out.append(self.indent()+self.visit(h))
		self.pull()

		if finallybody:
			## wrap in another try that is silent, always throw e
			out.append('try {		// finally block')
			for b in finallybody:
				out.append(self.visit(b))

			out.append('} throw e;')

		out.append( '}' )

		out.append( self.indent() + 'catch (const std::overflow_error& e) { std::cout << "OVERFLOW ERROR" << std::endl; }' )
		out.append( self.indent() + 'catch (const std::runtime_error& e) { std::cout << "RUNTIME ERROR" << std::endl; }' )
		out.append( self.indent() + 'catch (...) { std::cout << "UNKNOWN ERROR" << std::endl; }' )

		return '\n'.join( out )

	def visit_Import(self, node):
		r = [alias.name.replace('__SLASH__', '/') for alias in node.names]
		includes = []
		if r:
			for name in r:
				if name == 'jvm':
					self._has_jvm = True
				elif name == 'nim':
					self._has_nim = True
				else:
					includes.append('#include <%s>' %name)
		return '\n'.join(includes)

	def visit_Module(self, node):
		header = [
			'#include <cmath>',
			'#include <memory>',
			'#include <vector>',
			'#include <array>',
			'#include <iostream>',
			'#include <fstream>',
			'#include <string>',
			'#include <map>',
			'#include <algorithm>', ## c++11
			'#include <functional>', ## c++11
			#'#include <sstream>',  ## c++11
			'#include <thread>', ## c++11
			'#include <chrono>', ## c++11
		]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line is not None:
				for sub in line.splitlines():
					if sub==';':
						#raise SyntaxError('bad semicolon')
						pass
					else:
						lines.append( sub )
			else:
				if isinstance(b, ast.Import):
					header.append( self.visit(b) )
				else:
					raise SyntaxError(b)

		if self._has_channels:
			## https://github.com/ahorn/cpp-channel
			#header.append('#include <channel>')
			## instead of including, just directly inline cpp-channel source
			dirname = os.path.dirname(os.path.abspath(__file__))
			header.append(
				open( os.path.join(dirname, 'runtime/c++/cpp-channel.h') ).read()
			)

		if self._has_jvm:
			header.append( gen_jvm_header(self._java_classpaths) )

		if self._has_nim:
			header.append( gen_nim_header() )

		## forward declare all classes
		for classname in self._classes:
			header.append('class %s;' %classname)

		if len(self._kwargs_type_.keys()):
			impl = []
			header.append('class _KwArgs_;')  ## forward declare
			header.append('class _KwArgs_ {')
			header.append('	public:')

			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				header.append( '  %s _%s_;' %(type,name))
				header.append( '  bool __use__%s;' %name)

			for name in self._kwargs_type_:
				type = self._kwargs_type_[name]
				header.append( '  _KwArgs_*  %s(%s %s);' %(name, type, name))

				impl.append( '  _KwArgs_*   _KwArgs_::%s(%s %s) {' %(name, type, name))
				impl.append( '		this->__use__%s = true;' %name)
				impl.append( '		this->_%s_ = %s;' %(name, name))
				impl.append( '		return this;')
				impl.append('};')
			header.append('};')
			header.extend( impl )

		self.output_pak = pak = {'c_header':'', 'cpp_header':'', 'main':''}
		cheader = None
		cppheader = None
		if len(self._cheader):
			cheader = []
			cppheader = ['extern "C" {']
			for line in self._cheader:
				cheader.append(line)
				cppheader.append('\t'+line)
			cppheader.append('}')

		if cheader:
			pak['header.c'] = '\n'.join( cheader )
		if cppheader:
			pak['header.cpp'] = '\n'.join( cppheader )

		if 'int main() {' in lines:
			main_index = lines.index('int main() {')
			for idef in self._cpp_class_impl:
				lines.insert(main_index,idef)
		else:
			## might want to warn user there is no main
			pass

		lines = header + list(self._imports) + lines
		pak['main'] = '\n'.join( lines )
		return pak['main']


def translate_to_cpp(script, insert_runtime=True):
	#raise SyntaxError(script)
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'cpp_builtins.py') ).read()
		script = runtime + '\n' + script

	try:
		tree = ast.parse(script)
	except SyntaxError as err:
		e = ['%s:	%s'%(i+1, line) for i,line in enumerate(script.splitlines())]
		sys.stderr.write('\n'.join(e))
		raise err

	g = CppGenerator( source=script )
	g.visit(tree) # first pass gathers classes
	pass2 = g.visit(tree)
	g.reset()
	pass3 = g.visit(tree)
	#open('/tmp/pass3.cpp', 'wb').write( pass3 )
	return g.output_pak

```