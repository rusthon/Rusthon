
```python

USE_UNICODE_VARS = '--literate-unicode' in sys.argv
OBFUSCATE_UNICODE = '--obfuscate' in sys.argv

ObfuscationMap = {}  ## unichar : random string

MathematicalAlphabet = {
	u'𝐀' : 'A',
	u'𝐁' : 'B',
	u'𝐂' : 'C',
	u'𝐃' : 'D',
	u'𝐄' : 'E',
	u'𝐅' : 'F',
	u'𝐆' : 'G',
	u'𝐇' : 'H',
	u'𝐈' : 'I',
	u'𝐉' : 'J',
	u'𝐊' : 'K',
	u'𝐋' : 'L',
	u'𝐌' : 'M',
	u'𝐍' : 'N',
	u'𝐎' : 'O',
	u'𝐏' : 'P',
	u'𝐐' : 'Q',
	u'𝐑' : 'R',
	u'𝐒' : 'S',
	u'𝐓' : 'T',
	u'𝐔' : 'U',
	u'𝐕' : 'V',
	u'𝐖' : 'W',
	u'𝐗' : 'X',
	u'𝐘' : 'Y',
	u'𝐙' : 'Z',
	u'𝐚' : 'a',
	u'𝐛' : 'b',
	u'𝐜' : 'c',
	u'𝐝' : 'd',
	u'𝐞' : 'e',
	u'𝐟' : 'f',
	u'𝐠' : 'g',
	u'𝐡' : 'h',
	u'𝐢' : 'i',
	u'𝐣' : 'j',
	u'𝐤' : 'k',
	u'𝐥' : 'l',
	u'𝐦' : 'm',
	u'𝐧' : 'n',
	u'𝐨' : 'o',
	u'𝐩' : 'p',
	u'𝐪' : 'q',
	u'𝐫' : 'r',
	u'𝐬' : 's',
	u'𝐭' : 't',
	u'𝐮' : 'u',
	u'𝐯' : 'v',
	u'𝐰' : 'w',
	u'𝐱' : 'x',
	u'𝐲' : 'y',
	u'𝐳' : 'z',
	u'𝐴' : 'A',
	u'𝐵' : 'B',
	u'𝐶' : 'C',
	u'𝐷' : 'D',
	u'𝐸' : 'E',
	u'𝐹' : 'F',
	u'𝐺' : 'G',
	u'𝐻' : 'H',
	u'𝐼' : 'I',
	u'𝐽' : 'J',
	u'𝐾' : 'K',
	u'𝐿' : 'L',
	u'𝑀' : 'M',
	u'𝑁' : 'N',
	u'𝑂' : 'O',
	u'𝑃' : 'P',
	u'𝑄' : 'Q',
	u'𝑅' : 'R',
	u'𝑆' : 'S',
	u'𝑇' : 'T',
	u'𝑈' : 'U',
	u'𝑉' : 'V',
	u'𝑊' : 'W',
	u'𝑋' : 'X',
	u'𝑌' : 'Y',
	u'𝑍' : 'Z',
	u'𝑎' : 'a',
	u'𝑏' : 'b',
	u'𝑐' : 'c',
	u'𝑑' : 'd',
	u'𝑒' : 'e',
	u'𝑓' : 'f',
	u'𝑔' : 'g',
	u'𝑖' : 'i',
	u'𝑗' : 'j',
	u'𝑘' : 'k',
	u'𝑙' : 'l',
	u'𝑚' : 'm',
	u'𝑛' : 'n',
	u'𝑜' : 'o',
	u'𝑝' : 'p',
	u'𝑞' : 'q',
	u'𝑟' : 'r',
	u'𝑠' : 's',
	u'𝑡' : 't',
	u'𝑢' : 'u',
	u'𝑣' : 'v',
	u'𝑤' : 'w',
	u'𝑥' : 'x',
	u'𝑦' : 'y',
	u'𝑧' : 'z',
	u'𝑨' : 'A',
	u'𝑩' : 'B',
	u'𝑪' : 'C',
	u'𝑫' : 'D',
	u'𝑬' : 'E',
	u'𝑭' : 'F',
	u'𝑮' : 'G',
	u'𝑯' : 'H',
	u'𝑰' : 'I',
	u'𝑱' : 'J',
	u'𝑲' : 'K',
	u'𝑳' : 'L',
	u'𝑴' : 'M',
	u'𝑵' : 'N',
	u'𝑶' : 'O',
	u'𝑷' : 'P',
	u'𝑸' : 'Q',
	u'𝑹' : 'R',
	u'𝑺' : 'S',
	u'𝑻' : 'T',
	u'𝑼' : 'U',
	u'𝑽' : 'V',
	u'𝑾' : 'W',
	u'𝑿' : 'X',
	u'𝒀' : 'Y',
	u'𝒁' : 'Z',
	u'𝒂' : 'a',
	u'𝒃' : 'b',
	u'𝒄' : 'c',
	u'𝒅' : 'd',
	u'𝒆' : 'e',
	u'𝒇' : 'f',
	u'𝒈' : 'g',
	u'𝒉' : 'h',
	u'𝒊' : 'i',
	u'𝒋' : 'j',
	u'𝒌' : 'k',
	u'𝒍' : 'l',
	u'𝒎' : 'm',
	u'𝒏' : 'n',
	u'𝒐' : 'o',
	u'𝒑' : 'p',
	u'𝒒' : 'q',
	u'𝒓' : 'r',
	u'𝒔' : 's',
	u'𝒕' : 't',
	u'𝒖' : 'u',
	u'𝒗' : 'v',
	u'𝒘' : 'w',
	u'𝒙' : 'x',
	u'𝒚' : 'y',
	u'𝒛' : 'z',
	u'𝒜' : 'A',
	u'𝒞' : 'C',
	u'𝒟' : 'D',
	u'𝒢' : 'G',
	u'𝒥' : 'J',
	u'𝒦' : 'K',
	u'𝒩' : 'N',
	u'𝒪' : 'O',
	u'𝒫' : 'P',
	u'𝒬' : 'Q',
	u'𝒮' : 'S',
	u'𝒯' : 'T',
	u'𝒰' : 'U',
	u'𝒱' : 'V',
	u'𝒲' : 'W',
	u'𝒳' : 'X',
	u'𝒴' : 'Y',
	u'𝒵' : 'Z',
	u'𝒶' : 'a',
	u'𝒷' : 'b',
	u'𝒸' : 'c',
	u'𝒹' : 'd',
	u'𝒻' : 'f',
	u'𝒻𝒽' : 'h',
	u'𝒾' : 'i',
	u'𝒿' : 'j',
	u'𝓀' : 'k',
	u'𝓁' : 'l',
	u'𝓂' : 'm',
	u'𝓃' : 'n',
	u'𝓅' : 'p',
	u'𝓆' : 'q',
	u'𝓇' : 'r',
	u'𝓈' : 's',
	u'𝓉' : 't',
	u'𝓊' : 'u',
	u'𝓋' : 'v',
	u'𝓌' : 'w',
	u'𝓍' : 'x',
	u'𝓎' : 'y',
	u'𝓏' : 'z',
	u'𝓐' : 'A',
	u'𝓑' : 'B',
	u'𝓒' : 'C',
	u'𝓓' : 'D',
	u'𝓔' : 'E',
	u'𝓕' : 'F',
	u'𝓖' : 'G',
	u'𝓗' : 'H',
	u'𝓘' : 'I',
	u'𝓙' : 'J',
	u'𝓚' : 'K',
	u'𝓛' : 'L',
	u'𝓜' : 'M',
	u'𝓝' : 'N',
	u'𝓞' : 'O',
	u'𝓟' : 'P',
	u'𝓠' : 'Q',
	u'𝓡' : 'R',
	u'𝓢' : 'S',
	u'𝓣' : 'T',
	u'𝓤' : 'U',
	u'𝓥' : 'V',
	u'𝓦' : 'W',
	u'𝓧' : 'X',
	u'𝓨' : 'Y',
	u'𝓩' : 'Z',
	u'𝓪' : 'a',
	u'𝓫' : 'b',
	u'𝓬' : 'c',
	u'𝓭' : 'd',
	u'𝓮' : 'e',
	u'𝓯' : 'f',
	u'𝓰' : 'g',
	u'𝓱' : 'h',
	u'𝓲' : 'i',
	u'𝓳' : 'j',
	u'𝓴' : 'k',
	u'𝓵' : 'l',
	u'𝓶' : 'm',
	u'𝓷' : 'n',
	u'𝓸' : 'o',
	u'𝓹' : 'p',
	u'𝓺' : 'q',
	u'𝓻' : 'r',
	u'𝓼' : 's',
	u'𝓽' : 't',
	u'𝓾' : 'u',
	u'𝓿' : 'v',
	u'𝔀' : 'w',
	u'𝔁' : 'x',
	u'𝔂' : 'y',
	u'𝔃' : 'z',
	u'𝔄' : 'A',
	u'𝔅' : 'B',
	u'𝔇' : 'D',
	u'𝔈' : 'E',
	u'𝔉' : 'F',
	u'𝔊' : 'G',
	u'𝔍' : 'J',
	u'𝔎' : 'K',
	u'𝔏' : 'L',
	u'𝔐' : 'W',
	u'𝔛' : 'X',
	u'𝔜' : 'Y',
	u'𝔞' : 'a',
	u'𝔟' : 'b',
	u'𝔠' : 'c',
	u'𝔡' : 'd',
	u'𝔢' : 'e',
	u'𝔣' : 'f',
	u'𝔤' : 'g',
	u'𝔥' : 'h',
	u'𝔦' : 'i',
	u'𝔧' : 'j',
	u'𝔨' : 'k',
	u'𝔩' : 'l',
	u'𝔪' : 'm',
	u'𝔫' : 'n',
	u'𝔬' : 'o',
	u'𝔭' : 'p',
	u'𝔮' : 'q',
	u'𝔯' : 'r',
	u'𝔰' : 's',
	u'𝔱' : 't',
	u'𝔲' : 'u',
	u'𝔳' : 'v',
	u'𝔴' : 'w',
	u'𝔵' : 'x',
	u'𝔶' : 'y',
	u'𝔷' : 'z',
	u'𝔸' : 'A',
	u'𝔹' : 'B',
	u'𝔻' : 'D',
	u'𝔼' : 'E',
	u'𝔽' : 'F',
	u'𝔾' : 'G',
	u'𝕀' : 'I',
	u'𝕁' : 'J',
	u'𝕂' : 'K',
	u'𝕃' : 'L',
	u'𝕄' : 'M',
	u'𝕆' : 'O',
	u'𝕊' : 'S',
	u'𝕋' : 'T',
	u'𝕌' : 'U',
	u'𝕍' : 'V',
	u'𝕎' : 'W',
	u'𝕏' : 'X',
	u'𝕐' : 'Y',
	u'𝕒' : 'a',
	u'𝕓' : 'b',
	u'𝕔' : 'c',
	u'𝕕' : 'd',
	u'𝕖' : 'e',
	u'𝕗' : 'f',
	u'𝕘' : 'g',
	u'𝕙' : 'h',
	u'𝕚' : 'i',
	u'𝕛' : 'j',
	u'𝕜' : 'k',
	u'𝕝' : 'l',
	u'𝕞' : 'm',
	u'𝕟' : 'n',
	u'𝕠' : 'o',
	u'𝕡' : 'p',
	u'𝕢' : 'q',
	u'𝕣' : 'r',
	u'𝕤' : 's',
	u'𝕥' : 't',
	u'𝕦' : 'u',
	u'𝕧' : 'v',
	u'𝕨' : 'w',
	u'𝕩' : 'x',
	u'𝕪' : 'y',
	u'𝕫' : 'z',
	u'𝕬' : 'A',
	u'𝕭' : 'B',
	u'𝕮' : 'C',
	u'𝕯' : 'D',
	u'𝕰' : 'E',
	u'𝕱' : 'F',
	u'𝕲' : 'G',
	u'𝕳' : 'H',
	u'𝕳' : 'I',
	u'𝕵' : 'J',
	u'𝕶' : 'K',
	u'𝕷' : 'L',
	u'𝕸' : 'M',
	u'𝕹' : 'N',
	u'𝕺' : 'O',
	u'𝕻' : 'P',
	u'𝕼' : 'Q',
	u'𝕽' : 'R',
	u'𝕾' : 'S',
	u'𝕿' : 'T',
	u'𝖀' : 'U',
	u'𝖁' : 'V',
	u'𝖂' : 'W',
	u'𝖃' : 'X',
	u'𝖄' : 'Y',
	u'𝖅' : 'E',
	u'𝖆' : 'a',
	u'𝖇' : 'b',
	u'𝖈' : 'c',
	u'𝖉' : 'd',
	u'𝖊' : 'e',
	u'𝖋' : 'f',
	u'𝖌' : 'g',
	u'𝖍' : 'h',
	u'𝖎' : 'i',
	u'𝖏' : 'j',
	u'𝖐' : 'k',
	u'𝖑' : 'l',
	u'𝖒' : 'm',
	u'𝖓' : 'n',
	u'𝖔' : 'o',
	u'𝖕' : 'p',
	u'𝖖' : 'q',
	u'𝖗' : 'r',
	u'𝖘' : 's',
	u'𝖙' : 't',
	u'𝖚' : 'u',
	u'𝖛' : 'v',
	u'𝖜' : 'w',
	u'𝖝' : 'x',
	u'𝖞' : 'y',
	u'𝖟' : 'z',
}

UnicodeEscapeMap = {}  ## number : unichar

def _gen_random_id(size=16):
	import random, string
	chars = string.ascii_uppercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))

class typedpython:
	unicode_vars = USE_UNICODE_VARS
	types = ['string', 'str', 'list', 'dict', 'bool']
	native_number_types = ['int', 'float', 'double']  ## float and double are the same
	simd_types = ['float32x4', 'int32x4']  ## dart
	vector_types = ['float32vec']
	vector_types.extend( simd_types )
	number_types = ['long']  ## requires https://github.com/dcodeIO/Long.js
	number_types.extend( native_number_types )
	types.extend( number_types)
	types.extend( vector_types )

	__whitespace = [' ', '\t']

	GO_SPECIAL_CALLS = {
		'go'         : '__go__',
		'spawn'      : '__go__',
		'channel'    : '__go_make_chan__',
		'go.channel' : '__go_make_chan__',
		'go.array'   : '__go__array__',
		'go.make'    : '__go_make__',
		'go.addr'    : '__go__addr__',
		'go.func'    : '__go__func__',
	}

	@classmethod
	def needs_escape(cls,txt):
		return '__x0s0x__' in txt

	@classmethod
	def escape_text(cls,txt):
		escape_hack_start = '__x0s0x__'
		escape_hack_end = '__x0e0x__'
		parts = []
		chunks = txt.split(escape_hack_start)
		if len(chunks)==1:
			raise RuntimeError('invalid sequence')

		for p in chunks:
			if escape_hack_end in p:
				#if p.endswith( escape_hack_end ):
				id = int(p.split(escape_hack_end)[0].strip())
				assert id in UnicodeEscapeMap.keys()
				uchar = UnicodeEscapeMap[ id ]
				#if '__x0' in uchar:
				#	print UnicodeEscapeMap
				#	raise RuntimeError('bad:'+uchar)
				parts.append(uchar)
				parts.append(p.split(escape_hack_end)[1])
			else:
				#if '__x0' in p:
				#	raise RuntimeError('bad escape:'+p)
				if not p:
					continue
					print chunks
				parts.append(p)

		res = ''.join(parts)
		return res.encode('utf-8')


	@classmethod
	def get_indent(cls, s):
		indent = []
		for char in s:
			if char in cls.__whitespace:
				indent.append( char )
			else:
				break
		return ''.join(indent)

	@classmethod
	def transform_source(cls, source, strip=False, allow_tabs_and_spaces=True ):
		output = []
		output_post = None
		asm_block = False
		asm_block_indent = 0
		indent_unit = '' # indent sensitive

		for line in source.splitlines():
			if line.strip().startswith('#'):
				continue

			if asm_block:
				dent = cls.get_indent(line)
				if asm_block==True:
					asm_block = 'OK'
					asm_block_indent = len(dent)

				if len(dent) < asm_block_indent:
					asm_block = False
					asm_block_indent = 0
				elif len(dent) > asm_block_indent:
					raise SyntaxError('invalid asm indentation level')
				else:
					assert len(dent)==asm_block_indent
					if line.strip():
						output.append( '%s"%s"' %(dent,line.strip()) )
					else:
						asm_block = False
						asm_block_indent = 0
					continue

			a = []
			hit_go_typedef = False
			hit_go_funcdef = False
			gotype = None
			isindef = False
			isinlet = False
			inline_wrap = False
			inline_ptr = False
			prevchar = None

			for i,char in enumerate(line):

				if isindef is False and len(a) and ''.join(a).strip().startswith('def '):
					isindef = True
				if isinlet is False and len(a) and ''.join(a).strip().startswith('let '):
					isinlet = True

				nextchar = None
				j = i+1
				while j < len(line):
					nextchar = line[j]
					if nextchar.strip(): break
					j += 1

				if char in MathematicalAlphabet.keys():
					if USE_UNICODE_VARS or OBFUSCATE_UNICODE:
						## note with unicode characters they can not
						## be restored wth chr(ord(char))
						if OBFUSCATE_UNICODE:
							if char not in ObfuscationMap:
								ObfuscationMap[ char ] = _gen_random_id()
							ucord = ObfuscationMap[ char ]
						else:
							ucord = ord(char)

						if ucord not in UnicodeEscapeMap:
							UnicodeEscapeMap[ ucord ] = char

						## escape syntax ##
						char = '__x0s0x__%s__x0e0x__' % ucord
					else:
						char = MathematicalAlphabet[ char ]

				elif ord(char) > 255:
					if OBFUSCATE_UNICODE:
						if char not in ObfuscationMap:
							ObfuscationMap[ char ] = _gen_random_id()
						ucord = ObfuscationMap[ char ]
					else:
						ucord = ord(char)
					if ucord not in UnicodeEscapeMap:
						UnicodeEscapeMap[ ucord ] = char
					char = '__x0s0x__%s__x0e0x__' % ucord

				##################################

				if prevchar=='=' and char in '&*~':
					inline_ptr = True
					a.append('__inline__["' + char)
				elif inline_ptr and char not in '&*~':
					inline_ptr = False
					a.append('"] << ')
					a.append( char )

				#elif char == '(' and nextchar in ('&','@'):  ## DEPRECATED
				#	inline_wrap = True
				#	a.append('(inline("')
				elif char in '),' and inline_wrap:
					inline_wrap = False
					for u,_ in enumerate(a):
						if _=='@':
							a[u] = 'ref '
					if char == ')':
						a.append('"))')
					else:
						a.append('"),')

				## go array and map syntax ##
				#elif (not isindef and not isinlet) and len(a) and char==']' and j==i+1 and nextchar!=None and nextchar in '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
				elif not isindef and len(a) and char==']' and j==i+1 and nextchar!=None and nextchar in '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
					assert '[' in a
					hit_go_typedef = True

					gotype = []
					restore = list(a)
					b = a.pop()
					while b != '[':
						gotype.append(b)
						b = a.pop()
					gotype.reverse()
					gotype = ''.join(gotype).strip()  ## fixes spaces inside brackets `[ 1 ]string()`
					if not gotype:
						if nextchar=='[':
							a.append('__go__array__<<')
						else:
							a.append('__go__array__(')
					elif gotype.isdigit():
						p = ''.join(a).split()[-1].strip()
						if p.startswith('[') or p.startswith('='):
							a.append('__go__arrayfixed__(%s,' %gotype)
						else:
							hit_go_typedef = False
							restore.append(char)
							a = restore

					elif ''.join(a[-3:])=='map' and gotype != 'func' and a[-4] in cls.__whitespace+['=']:
						a.pop(); a.pop(); a.pop()
						a.append('__go__map__(%s,' %gotype)
					else:
						hit_go_typedef = False
						restore.append(char)
						a = restore

				elif hit_go_funcdef and char==')' and ')' in ''.join(a).split('func(')[-1] and not ''.join(a).strip().startswith('def '):
					hit_go_funcdef = False
					a.append('))<<')
				elif hit_go_typedef and char=='(':
					if ''.join(a).endswith('func'):
						hit_go_funcdef = True
						a.append( '(' )
					else:
						a.append(')<<(')
					hit_go_typedef = False
				elif hit_go_typedef and char=='{':
					a.append(')<<{')
					hit_go_typedef = False
				elif hit_go_typedef and char==',':
					#a.append(', type=True),')  ## this breaks function annotations that splits on ','
					a.append('<<typedef),')
					hit_go_typedef = False
				elif hit_go_typedef and char in (' ', '\t'):
					hit_go_typedef = False
					if isinlet:
						a.append(')')
					else:
						aa = []
						for xx in a:
							if xx == '__go__array__(':
								aa.append('__go__array__[')
							else:
								aa.append( xx )
						a = aa
						a.append(']=\t\t\t\t')


				elif a and char in cls.__whitespace:
					b = ''.join(a)
					b = b.strip()
					is_class_type = b.startswith('class:') and len(b.split(':'))==2
					is_pointer = b.startswith('*')
					is_func = b.startswith('func(') and not ''.join(a).strip().startswith('func(')
					if (b in cls.types or is_class_type or is_pointer or is_func) and nextchar != '=':
						if strip:
							a = a[ : -len(b) ]
						elif is_class_type:
							cls = b.split(':')[-1]
							a = a[ : -len('class:')-len(cls)]
							a.append('__go__class__[%s]=\t\t\t\t' %cls)

						elif is_pointer:
							cls = b.split('*')[-1]
							a = a[ : -len('*')-len(cls)]
							a.append('__go__pointer__[%s]=\t\t\t\t' %cls)
						elif is_func:
							u = ''.join(a)
							u = u.replace('func(', '__go__func__["func(')
							u += '"]=\t\t\t\t'
							raise RuntimeError(u)
							a = [w for w in u]

						else:
							#if a[-1]=='*':
							#	a.pop()
							#	a.append('POINTER')
							#a.append('=\t\t\t\t')
							a.append( char )

					else:
						a.append( char )
				else:
					a.append( char )

				if char.strip():
					prevchar = char


			c = ''.join(a)
			cs = c.strip()

			if cs.startswith('//'):
				continue
			elif cs.startswith('inline(') or cs.startswith('JS('):
				output.append(c)
				continue


			if cs.startswith('var '):
				c = c.replace('var ', '')

			if cs.startswith('let '):
				mut = False
				if cs.startswith('let mut '):
					c = c.replace('let mut ', '__let__(')
					mut = True
				else:
					c = c.replace('let ', '__let__(')

				if ':' in c:  ## `let x:T`
					assert c.count(':')==1
					## type must be quoted if its external style (rust or c++)
					## like: `Vec<T>` or `std::something<T>`
					ct = c.split(':')[-1]
					if ('<' in ct and '>' in ct) or '::' in ct:
						c = c.replace(':', ',"')
						if '=' in c:
							c = c.replace('=', '", ')
						else:
							c += '"'
					else:
						c = c.replace(':', ',')
						if '=' in c:
							c = c.replace('=', ',')

				if mut:
					c += ',mutable=True)'
				else:
					c += ')'

			## this conflicts with inline javascript and lua,
			## TODO make the parser smarter, and skip quoted strings
			#if '= function(' in c:
			#	k = '= function('
			#	a,b = c.split(k)
			#	output.append( '@expression(%s)' %a.strip())
			#	c = 'def __NAMELESS__(' + b

			indent = []
			for char in c:
				if char in cls.__whitespace:
					indent.append( char )
				else:
					break
			indent = ''.join(indent)


			if ' except ' in c and ':' in c:  ## PEP 463 - exception expressions
				s = c.split(' except ')
				if len(s) == 2 and '=' in s[0] and ':' in s[1]:
					s0 = s[0].strip()
					output.append('%stry: %s' %(indent, s0) )
					exception, default = s[1].split(':')
					output.append('%sexcept %s: %s=%s' %(indent, exception, s0.split('=')[0], default) )
					c = ''

			if not allow_tabs_and_spaces:  ## TODO fixme, this is not safe now because we do not skip quoted text
				indent = len(c) - len(c.lstrip())
				if indent_unit == '' and indent:
					indent_unit = c[0]
				elif c:
					if indent and c[0] != indent_unit:
						raise TabError('inconsistent use of tabs and spaces in indentation in line:', str(i+1) + '\n'+ c)
					indent = indent_unit*indent

			if ' def(' in c or ' def (' in c:
				if ' def(' in c:
					a,b = c.split(' def(')
				else:
					a,b = c.split(' def (')

				if '=' in a:
					output.append( indent + '@expression(%s)' %a.split('=')[0])
					c = indent + 'def __NAMELESS__(' + b 



			if c.strip().startswith('def ') and '->' in c:  ## python3 syntax
				c, rtype = c.split('->')
				c += ':'
				rtype = rtype.strip()[:-1].strip()
				if rtype.endswith('*') or rtype.endswith('&'):
					rtype = '"%s"' %rtype
				elif rtype.startswith('['):
					rtype = '"%s"' %rtype

				if not strip:
					output.append( indent + '@returns(%s)' %rtype)

			if c.startswith('import '):
				if '-' in c:
					c = c.replace('-', '__DASH__')
				if '/' in c:
					c = c.replace('/', '__SLASH__')
				if '"' in c:
					c = c.replace('"', '')


			if ' new ' in c:
				c = c.replace(' new ', ' __new__>>')
			if '\tnew ' in c:
				c = c.replace('\tnew ', ' __new__>>')


			## golang

			if c.strip().startswith('switch '):
				c = c.replace('switch ', 'with __switch__(').replace(':', '):')

			if c.strip().startswith('default:'):
				c = c.replace('default:', 'with __default__:')

			if c.strip().startswith('select:'):
				c = c.replace('select:', 'with __select__:')

			if c.strip().startswith('case ') and c.strip().endswith(':'):
				c = c.replace('case ', 'with __case__(').replace(':', '):')

			if '<-' in c:
				if '=' in c and c.index('=') < c.index('<-'):
					c = c.replace('<-', '__go__receive__<<')
				else:
					## keeping `=` allows for compatible transform to stacklessPython API,
					## this is not used now because it is not required by the Go backend.
					c = c.replace('<-', '= __go__send__<<')
					#c = c.replace('<-', '<<__go__send__<<')


			## c++/libpython `->` gets translated to a CPython C-API call. 
			## TODO: could also be specialized or other backends, or by user  `with syntax('->', USER_MACRO):` ##
			if '->' in c:
				#a,b = c.split('->')
				#this_name = a.split()[-1].split('=')[-1].split(':')[-1].split(',')[-1]
				#method_name = b.split()[0].split('(')[0]
				#c = c.replace('->'+method_name, '.__right_arrow__<<'+method_name)

				c = c.replace('->(', '.__right_arrow__(')
				c = c.replace('->[', '.__right_arrow__[')
				c = c.replace('->', '.__right_arrow__.')


			## python3 annotations
			if 'def ' in c and c.count(':') > 1:
				#head, tail = c.split('(')
				head = c[ : c.index('(') ]
				tail = c[ c.index('(')+1 : ]
				args = []
				#tail, tailend = tail.split(')')
				tailend = tail[ tail.rindex(')')+1 : ]
				tail = tail[ : tail.rindex(')') ]


				for x in tail.split(','):
					y = x
					if ':' in y:
						kw = None
						if '=' in y:
							y, kw = y.split('=')
						#arg, typedef = y.split(':')
						arg = y[ : y.index(':') ]
						typedef = y[ y.index(':')+1 : ]
						typedef = typedef.strip()

						chan = False
						T = False
						if len(typedef.strip().split()) >= 2 and not typedef.startswith('func('):
							parts = typedef.strip().split()
							if 'chan' in parts:  ## go syntax
								chan = True
							else:                ## rust or c++ syntax
								T = ' '.join(parts[:-1])

							#typedef = typedef.strip().split()[-1]
							typedef = parts[-1]

						if '*' in arg:
							arg_name = arg.split('*')[-1]
						else:
							arg_name = arg

						if typedef.startswith('[]'):
							typedef = '__arg_array__("%s")' %typedef.strip()  ## this parses the go syntax and converts it for each backend

						elif typedef.startswith('map['):
							typedef = '__arg_map__("%s")' %typedef.strip()  ## this parses the go syntax and converts it for each backend

						elif typedef.endswith('*'):
							typedef = '"%s"' %typedef.strip()
						elif typedef.endswith('&'):
							typedef = '"%s"' %typedef.strip()
						elif typedef.startswith('func('):
							typedef = '"%s"' %typedef.strip()
							if ' ' in typedef or '\t' in typedef:
								## TODO deprecate this old pipe-sep hack
								typedef = '|'.join(typedef.split())

						elif typedef.startswith('lambda('):
							typedef = '"%s"' %typedef.strip()
						elif '::' in typedef:
							typedef = '"%s"' %typedef.strip()
						elif '<' in typedef and '>' in typedef: ## rust and c++ template/generics syntax
							typedef = '"%s"' %typedef.strip()
						elif ':' in typedef and typedef.strip().startswith('[') and typedef.strip().endswith(']'): ## verilog [bit:index] syntax
							typedef = '"%s"' %typedef.strip()

						if not strip:
							if T:  ## rust or c++ syntax
								output.append('%s@__typedef__(%s, %s, "%s")' %(indent, arg_name, typedef, T))
							elif chan:
								output.append('%s@typedef_chan(%s=%s)' %(indent, arg_name, typedef))
							else:
								output.append('%s@typedef(%s=%s)' %(indent, arg_name, typedef))

						if kw:
							arg += '=' + kw
						args.append(arg)
					else:
						args.append(x)
				c = head +'(' + ','.join(args) + ')'+tailend  ## restores to python2 syntax

			#elif '::' in c or ('<' in c and '>' in c and c.count('<')==c.count('>')):  ## c++ syntax `('std::bla<T>')(foo)`
			#	##  could auto quote here so `(std::<T>)` becomes `('std::<T>')
			#	left = c.index('::')
			#	while c[left]!='`':
			#		left -= 1
			#	if ">`" in c:
			#		c = c.replace(">`", ">')<<")
			#	elif c.endswith('`'):
			#		c = c[:-1] + "')"
			#	c = c[ :left-1 ] + " inline('" + c[left+1:]

			if '::' in c:
				c = c.replace('::', '.__doublecolon__.')
				## this easily breaks - example: "myarray[ ::x]"
				ugly = '[.__doublecolon__.'
				if ugly in c: c = c.replace(ugly, '[::')
				ugly = '.__doublecolon__.]'
				if ugly in c: c = c.replace(ugly, '::]')
				for n in range(-9, 9):
					nasty = '.__doublecolon__.%s]' %n
					if nasty in c:
						c = c.replace(nasty, '::%s]'%n)

			if c.strip().startswith('with ') and ' as ' in c and c.endswith(':'):
				x,y = c.split(' as ')
				if "'" in y or '"' in y:
					y = y[:-1] + '[MACRO]:'
					c = ' as '.join([x,y])
			elif not c.startswith('except ') and ' as ' in c:
				if (c.strip().startswith('return ') or '(' in c or ')' in c or '=' in c or c.strip().startswith('print')):
					c = c.replace(' as ', '<<__as__<<')
				elif c.strip().startswith('for '):
					c = c.replace('for ', 'for (').replace(' in ', ') in ').replace(' as ', ',__as__,')


			## jquery ##
			## TODO ensure this is not inside quoted text
			#if '$(' in c:
			#	c = c.replace('$(', '__DOLLAR__(')
			#if '$' in c and 'def ' in c:  ## $ as function parameter
			#	c = c.replace('$', '__DOLLAR__')
			#if '$.' in c:
			#	c = c.replace('$.', '__DOLLAR__.')
			if '$' in c:
				c = c.replace('$', '__DOLLAR__')

			if c.strip().startswith('nonlocal '):  ## Python3 syntax
				c = c.replace('nonlocal ', 'global ')  ## fake nonlocal with global

			if c.strip().startswith('with asm('):
				asm_block = True

			if strip and c.strip().startswith('with ('):
				c = c.split('with (')[0] + 'if True:'

			## regular output
			output.append( c )


		r = '\n'.join(output)

		try:
			ast.parse(r)
		except SyntaxError as e:
			print '-'*80
			print 'Syntax Error on this line:'
			eline = output[e.lineno-1]
			if eline.strip().startswith('def '):
				funcname = eline.strip().split('(')[0].split('def ')[-1]
				print 'SyntaxError in function definition: "%s"' % funcname
				for i,eln in enumerate(source.splitlines()):
					if 'def '+funcname in eln:
						print 'line number: %s' %(i+1)
						print eln
						if 'func(' or 'lambda(' in eln:
							if ')(' in eline:
								print 'note: the syntax for typed callback functions is "func(arg1 arg2)(return_type)"'
								print 'the arguments are space separated, not comma separated.'
								print 'example: "func(int int)()" is a callback that takes two ints and returns nothing.'
								sys.exit(1)
			else:
				print eline
			print '-'*80

			raise e

		return r

```

Simple Syntax Test
------------------


```python

__test_typedpython__ = u'''

if True:
	d = a[ 'somekey' ] except KeyError: 'mydefault'

## <- becomes __go__send__<<a
g <- a
## = <- becomes __go__receive__<<b
g = <- b

def call_method( cb:func(int)(int) ) ->int:
	return cb(3)

def wrapper(a:int, c:chan int):
	result = longCalculation(a)
	c <- result

switch a.f():
	case 1:
		print(x)
	case 2:
		print(y)
	default:
		break

select:
	case x = <- a:
		y += x
	case x = <- b:
		y += x



def f(a:int, b:int, c:int) ->int:
	return a+b+c

def f(a:int=100, b:int=100) ->int:
	return a+b

def f(*args:int, **kwargs:int) ->int:
	return a+b

a = []int(x for x in range(3))

y = go.make([]float64, 1000)

def plot(id:string, latency:[]float64, xlabel:string, title:string ):
	pass

def f( x:*ABC ) -> *XXX:
	pass

def listpass( a:[]int ):
	pass

def mappass( a:map[string]int ):
	return ConvertDataUnits[unit_type][unit][1][0]

m = map[int]string{ a:'xxx' for a in range(10)}


functions = map[string]func(int)(int){}
[]int a = go( f() for f in funtions )

## in go becomes: map[string]int{x,y,z}
## becomes: __go__map__(string, int) << {'x':x, 'y':y, 'z':z}
a = map[string]int{
	"x":x, 
	"y":y, 
	"z":z
}

def f():
    return [[0]]
print f()[0][0]

## in go becomes: []string{x,y,z}
## becomes: __go__array__(string) << (x,y,z)
a = []string(x,y,z)

## in go becomes: [3]int{x,y,z}
## becomes: __go__arrayfixed__(3, string) << (x,y,z)
a = [ 3 ]int(x,y,z)

## Rust - DEPRECATED (replaced by minimacro with syntax)
## f(inline('&mut *x'))
#f(&mut *x)
## f(inline('ref mut *x'), y.z())
#f(@mut *x, y.z())


## f(x << __as__ << uint)
f(x as uint)

## __let__[x :" Vec<(uint, Y<int>)> "]= range(0,1).map().collect()
let x : Vec<(uint, Y<int>)> = range(0,1).map().collect()
let i
i = &**x

def f(a:&mut int) ->int:
	return a

def f():
	with asm( outputs=b, inputs=a, volatile=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return x

let mut x : int = 1
let x : int
def __init__():
	let self.x : int = x
	let mut self.y : int = y


def call_method( cb:lambda(int)(int) ) ->int:
	return cb(3)

if self.__map[r][c] in (WALL,PERM_WALL): pass

## allow func to be used as a function name, because it is pretty commom and allowed by most backends.
def func(x=None, callback=None):
	func( callback=xxx )
	x.func( xx=yy )

let mut x = 0

def templated( x : Type<T> ):
	pass
def templated( x : namespace::Type<T> ):
	pass

c.x[0] = def(xx,yy) ->int:
	return xx+yy

mdarray = [][]int()
def F() ->[][]int:
	pass

def f():
	return A as B

print `std::chrono::duration_cast<std::chrono::microseconds>`clock().count()

with (some, stuff):
	pass
def f():
	let x : map[string]int = {}

'''

def test_typedpython():
	out = typedpython.transform_source(__test_typedpython__)
	print(out)
	import ast
	print( ast.parse(out) )

```