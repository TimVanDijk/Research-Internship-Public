import itertools
import cmath
import math
import sys

p = 3
n = math.ceil(math.log(p, 2))

def omega():
	return cmath.exp(2 * cmath.pi * 1j / p)

def cformat(l):
	return '[' + ', '.join(['%0.2f + %0.2fi' % (el.real, el.imag) for el in l]) + ']'

def hatter(val):
	return omega() ** (val % p)

def fwht(arr, forward=True):
	w = omega() if forward else omega().conjugate()
	
	h = 1
	while h < len(arr):
		for i in range(0, len(arr), h * p):
			for j in range(i, i + h):
				temp = [arr[j + k*h] for k in range(p)]

				for k in range(p):
					arr[j + k*h] = sum([w**(k*l) * temp[l] for l in range(p)])

		h *= p
	return arr

def func0(a1, a0):
	return (a1 + a1*a0) % p

def func1(a3, a2, a1, a0):
	return (a3 * a2 * a1 + a2 * a1 + a3 + a2 + a0) % p

def main():
	# Compute f
	f = [func0(*inp) for inp in list(itertools.product(range(p), repeat=n))]
	print("f: ", f, '\n')

	# Compute f^
	f_hat = list(map(hatter, f))
	print("f^: " + cformat(f_hat) + '\n')

	# Compute F from f^
	F = fwht(f_hat[:], forward=True)
	print("F(f^): " + cformat(F) + '\n')

	# Scale F
	scaled = [el / p**n for el in F]
	print("scaled: " + cformat(scaled) + '\n')

	# Compute f^ from scaled F
	twice  = fwht(scaled[:], forward=False)
	print("F(F(f^)): " + cformat(twice) + '\n')

	print("fwht(hwft(x)) == x?", all([cmath.isclose(twice[i], f_hat[i], abs_tol=0.0001) for i in range(len(twice))]))

if __name__ == "__main__":
	main()
