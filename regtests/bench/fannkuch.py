# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# contributed by Sokolov Yura
# modified by Tupteq
# modified by hartsantler 2014

from time import time

DEFAULT_ARG = 9

def main():
	if PYTHON=='PYTHONJS':
		pythonjs.configure( direct_operator='+' )
		pythonjs.configure( direct_keys=True )
		pass

	times = []
	for i in range(4):
		t0 = time()
		#res = fannkuch(DEFAULT_ARG)
		res = fannkuch(8)
		tk = time()
		times.append(tk - t0)
	avg = sum(times) / len(times)
	print(avg)

def fannkuch(n):
	count = range(1, n+1)
	max_flips = 0
	m = n-1
	r = n
	check = 0
	perm1 = range(n)
	perm = range(n)
	#perm1_ins = perm1.insert
	#perm1_pop = perm1.pop
	if PYTHON=='PYTHON3':
		count = list(count)
		perm1 = list(perm1)
		perm = list(perm)

	while True:
		if check < 30:
			check += 1

		while r != 1:
			count[r-1] = r
			r -= 1

		if perm1[0] != 0 and perm1[m] != m:
			perm = perm1[:]
			flips_count = 0
			k = perm[0]
			#while k:  ## TODO fix for dart
			while k != 0:
				perm[:k+1] = perm[k::-1]
				flips_count += 1
				k = perm[0]

			if flips_count > max_flips:
				max_flips = flips_count

		while r != n:
			#perm1_ins(r, perm1_pop(0))
			perm1.insert(r, perm1.pop(0))
			count[r] -= 1
			if count[r] > 0:
				break
			r += 1
		else:
			return max_flips


