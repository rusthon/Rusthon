import os, sys, subprocess

passed = {}
ignore = ()

TODO_FIX = (
	'ffi_hello.py',  ## libc is unstable as of Rust1.2
	'pointer_syntax.py',
	'rust_select.py',
	'try.py',
)

files = os.listdir('./rust')
files.sort()

for md in files:
	if md in TODO_FIX:
		print 'skip test: %s (TODO fix later)' %md
		continue
	elif not md.endswith('.py'):
		continue

	print md
	if md.startswith( ignore ):
		continue
	subprocess.check_call([
		'python',
		'../rusthon.py',
		'--rust',
		os.path.join('./rust', md)
	])
	passed[ md ] = open('/tmp/rusthon-build.rs').read().split('/*end-builtins*/')[-1]

report = [
	'Rust Backend Regression Tests',
	'-----------------------------',
	'the following tests compiled, and the binary executed without any errors',
]
print 'TESTS PASSED:'
for md in passed:
	print md
	report.append('* [%s](rust/%s)' %(md,md))
	report.append('')
	report.append('input:')
	report.append('------')
	report.append('```python')
	report.extend( open('./rust/'+md, 'rb').read().splitlines() )
	report.append('```')
	report.append('output:')
	report.append('------')
	report.append('```rust')
	report.extend( passed[md].splitlines() )
	report.append('```')

open('regtest-report-rust.md', 'wb').write('\n'.join(report))
