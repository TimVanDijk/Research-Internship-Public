import itertools
import cmath
import math
import sys

from ComplexPolynomial import ComplexPolynomial

p = 5
n = math.ceil(math.log(p, 2))

# Number of output values of func
m = 2

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

# Some example function used for testing. It maps 3 input values into 2 output value in range [0, p)
def func0(a2, a1, a0):
	return (a2*a1 + a0) % p, (a2*a0 + a1) % p

# Uses an example function to generate an input.
# Then performs forward FWHT and backward FWHT on that input.
# This results once again in the input we started with.
def main():
	# Compute h
	h = [(inp, func0(*inp)) for inp in list(itertools.product(range(p), repeat=n))]
	print("h:", h, '\n')

	# Compute h^
	h_hat = [1 if func0(*x) == y else 0 for x in itertools.product(range(p), repeat=n) for y in itertools.product(range(p), repeat=m)]
	print("h^:", h_hat, '\n')

	# Convert h^ into polynomials such that we can apply the transformation
	h_hat_poly = list(map(hatter, h_hat))

	# Compute C from h^_poly
	C = fwht(h_hat_poly[:], forward=True)
	print("C(h^): ")
	for el in C:
		num = el.num(inprecise_omega())
		print(el, ' || ', el.simplify(), ' || ', '%0.2f + %0.2fi' % (num.real, num.imag), ' || ', el.phase(p))
	print()

	# Scale C
	print("C(h^) scaled: ")
	for el in C:
		print(el.simplify().scaled(p**n))
	print()

	# Compute h^_poly from C
	h_hat_poly_reconstructed = [el.simplify() for el in fwht(C[:], forward=False)]

	# Compute h^ from h^_poly
	h_hat_reconstructed = list(map(unhatter, h_hat_poly_reconstructed))
	print("h^ reconstructed:", h_hat_reconstructed, '\n')

	print("h^ is still the same?", h_hat_reconstructed == h_hat)
	# We cannot reconstruct h using the information we have

if __name__ == "__main__":
	main()