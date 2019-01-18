import itertools
import cmath
import math
import sys

from ComplexPolynomial import ComplexPolynomial

p = 3
n = math.ceil(math.log(p, 2))

# Creates a polynomial that equals 1*w^1
def omega():
	return ComplexPolynomial(p, *[1 if i == 1 else 0 for i in range(p)])

# Returns the floating point value of omega
def inprecise_omega():
	return cmath.exp(2 * cmath.pi * 1j / p)

# Pretty prints a list of complex numbers
def cformat(l):
	return '[' + ', '.join(['%0.2f + %0.2fi' % (el.real, el.imag) for el in l]) + ']'

# Turns a number n into a polynomial equal to omega^n
def hatter(val):
	return ComplexPolynomial(p, *[1 if val == i else 0 for i in range(p)])

# Turns a polynomial that equals omega^n into a number n
def unhatter(hatted):
	for i, el in enumerate(hatted.coeffs):
		if el != 0:
			return i
	raise ValueError("Polynomial cannot be unhatted: " + str(hatted))

# Performs a forward or backward Walsh-Hadamard transform on GF(p)
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

# Some example function used for testing. It maps 2 input values into 1 output value in range [0, p)
def func0(a1, a0):
	return (a1 + a1*a0) % p

# Some example function used for testing. It maps 3 input values into 1 output value in range [0, p)
def func1(a2, a1, a0):
	return (a2 * a1 + a2 * a1 + a2 + a0) % p

# Uses an example function to generate an input.
# Then performs forward FWHT and backward FWHT on that input.
# This results once again in the input we started with.
def main():
	# Compute f
	f = [func1(*inp) for inp in list(itertools.product(range(p), repeat=3))]
	print("f: ", f, '\n')

	# Compute f^
	f_hat = list(map(hatter, f))
	print("f^: ")
	for el in f_hat:
		print(el)
	print()

	# Compute F from f^
	F = fwht(f_hat[:], forward=True)
	print("F(f^): ")
	for el in F:
		num = el.num(inprecise_omega())
		print(el, ' || ', el.simplify(), ' || ', '%0.2f + %0.2fi' % (num.real, num.imag), ' || ', el.phase(p))
	print()

	# Scale F
	print("F(f^) scaled: ")
	for el in F:
		print(el.simplify().scaled(p**n))
	print()

	# Compute f^ from F
	f_hat_reconstructed  = fwht(F[:], forward=False)
	print("f^ reconstructed: ")
	for el in f_hat_reconstructed:
		print(el.simplify().scaled(p**n))
	print()

	# Compute f from f^
	f_reconstructed = list(map(unhatter, f_hat_reconstructed))
	print("f reconstructed:", f_reconstructed, '\n')

if __name__ == "__main__":
	main()