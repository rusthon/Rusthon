# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# contributed by Sokolov Yura
# modified by Tupteq
# modified by hartsantler 2014

from time import clock
from runtime import *

DEFAULT_ARG = 9

def main():
	times = []
	for i in range(4):
		t0 = clock()
		res = fannkuch(DEFAULT_ARG)
		tk = clock()
		times.append(tk - t0)
	avg = sum(times) / len(times)
	print(avg)

def fannkuch(n):
	count = list(range(1, n+1))
	perm1 = list(range(n))
	perm = list(range(n))
	max_flips = 0
	m = n-1
	r = n
	check = 0

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

		do_return = True
		while r != n:
			perm1.insert(r, perm1.pop(0))
			count[r] -= 1
			if count[r] > 0:
				do_return = False
				break
			r += 1

		if do_return:
			return max_flips


main()