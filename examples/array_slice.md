array slice syntax
------------------

note: below the untyped literal `[1,2,3,4,5]`  is used to initalize `a`, this is a simple case and the transpiler can infer that you want a shared reference to a `std::vector<int>`.

```rusthon
#backend:c++

def somefunc():
	a = [1,2,3,4,5]
	print('a addr:', a)
	print('len a:', len(a))
	b = a[1:]
	print('b addr (should not be `a` above):', b)
	print('len b  (should be 4):', len(b))

	c = a[:]
	print('c addr (should not be `a` or `b` above):', c)
	print('len c:', len(c))
	c.append(6)
	print('len c - after append:', len(c))
	print('len a:', len(a))

	print('end slice test')

	d = a[:2]
	print('len d:', len(d))
	print d[0]
	print d[1]

	print('len a:', len(a))
	e = a[::1]
	print('len e should be same as a:', len(e))
	for i in e: print i

	f = a[::2]
	print('len f:', len(f))
	for i in f: print i

	g = a[::-1]
	print('len g:', len(g))
	for i in g: print i

	h = a[2::-1]
	print('len h:', len(h))
	for i in h: print i

	print('---slice assignment---')
	h.append(1000)
	h.append(1000)
	a[:2] = h
	for i in a: print i
	print('len a:', len(a))

	print('somefunc done')

def main():
	print('calling somefunc')
	somefunc()
	print('OK')

```