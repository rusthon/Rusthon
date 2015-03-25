

```python

def convert_to_markdown_project(path, rust=True, python=True, asm=True, c=True, cpp=True, java=True, java2rusthon=False, giws=False, file_metadata=False):
	files = []
	exts = []
	if rust: exts.append('.rs')
	if python: exts.append('.py')
	if asm: exts.append('.s')
	if c:   exts.append('.c')
	if cpp: exts.append('.cpp')
	if java: exts.append('.java')
	exts = tuple(exts)

	if os.path.isfile(path):
		files.append( path )

	elif os.path.isdir(path):
		for name in os.listdir(path):
			if name.endswith( exts ):
				files.append(os.path.join(path,name))

	project = []
	for file in files:
		print('reading: ', file)

		data = open(file, 'rb').read()
		header = []
		if file_metadata:
			header.extend([
			'#' + os.path.split(file)[-1],
			'* file: ' + file,
			'* md5sum   : %s' %hashlib.md5(data).hexdigest(),
			'* changed  : %s' %os.stat(file).st_mtime,
			''
			])
		lang = ''
		if file.endswith('.rs'):
			lang = 'rust'
		elif file.endswith('.py'):
			lang = 'python'
		elif file.endswith('.s'):
			lang = 'asm'
		elif file.endswith('.c'):
			lang = 'c'
		elif file.endswith('.cpp'):
			lang = 'c++'
		elif file.endswith('.java'):
			if java2rusthon:
				## pre converts into rusthon in markdown, for hand editing ##
				lang = 'rusthon'
				data = java_to_rusthon(data)
			else:
				## this still trigers java2rusthon at final compile time ##
				lang = 'java'

		impls = []
		pub_funcs = []
		pri_funcs = []
		pub_structs = []
		pri_structs = []
		pub_enums = []
		pri_enums = []

		code = [
			os.path.split(file)[-1],
			'-----------',
			'\n', 
			'@%s'%os.path.split(file)[-1],
		]
		code.append('```%s' %lang)  ## begin fence
		fence = True
		comment_block = False
		for line in data.splitlines():
			if not line.strip(): continue
			if True:
				if line.strip().startswith('//'):
					if fence:
						code.append('```\n')  ## end fence
						fence = False
					code.append('>'+line)

				elif line.strip().startswith('/*'):
					if fence:
						code.append('```\n')  ## end fence
						fence = False

					if '*/' in line:
						code.append('%s' %line.replace('/*', '').replace('*/','').strip() )
						code.append('\n```%s' %lang)  ## begin fence
						fence = True
					else:
						comment_block = True

				elif '*/' in line and comment_block:
					comment_block = False
					a = line.replace('*/', '').strip()
					if a: code.append('>'+a)
					code.append('\n```%s' %lang)  ## begin fence
					fence = True

				elif comment_block:
					line = line.strip()
					if line.startswith('*'): line = line[1:]
					code.append(line)
				else:

					code.append(line)

			else:  ## DEPRECATED
				if not fence:
					code.append('\n```%s' %lang)  ## begin fence
					fence = True

				if lang=='rust':
					a = line ##.strip()
					if a.startswith('pub fn '):
						pub_funcs.append( a.split('pub fn ')[-1].split('(')[0] )
					elif a.startswith('fn '):
						pub_funcs.append( a.split('fn ')[-1].split('(')[0] )
					elif a.startswith('pub struct '):
						pub_structs.append( a.split('pub struct ')[-1].split('{')[0] )
					elif a.startswith('struct '):
						pri_structs.append( a.split('struct ')[-1].split('{')[0] )
					elif a.startswith('pub enum '):
						pub_enums.append( a.split('pub enum ')[-1].split('{')[0] )
					elif a.startswith('enum '):
						pri_enums.append( a.split('enum ')[-1].split('{')[0] )
					elif a.startswith('impl '):
						impls.append( a.split('impl ')[-1].split('{')[0] )

				code.append( line )
		if fence:
			code.append('```')

		if impls:
			header.append('###implementations:')
			for a in impls:
				header.append('* '+a)
			header.append('')

		if pub_funcs:
			header.append('###public functions:')
			for a in pub_funcs:
				header.append('* '+a)
			header.append('')
		if pub_structs:
			header.append('###public structs:')
			for a in pub_structs:
				header.append('* '+a)
			header.append('')

		if pub_enums:
			header.append('###public enums:')
			for a in pub_enums:
				header.append('* '+a)
			header.append('')

		if pri_funcs:
			header.append('###private functions:')
			for a in pri_funcs:
				header.append('* '+a)
			header.append('')
		if pri_structs:
			header.append('###private structs:')
			for a in pri_structs:
				header.append('* '+a)
			header.append('')

		if pri_enums:
			header.append('###private enums:')
			for a in pri_enums:
				header.append('* '+a)
			header.append('')

		code.append('___')

		md = '\n'.join(header+code)
		project.append({'name':os.path.split(file)[-1], 'path':file, 'markdown':md})

	return project

```