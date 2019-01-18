import math
import cmath

class ComplexPolynomial:
	def __init__(self, degree, *coefficients):
		self.degree = degree
		self.coeffs = [coefficients[i] if i < len(coefficients) else 0 for i in range(self.degree)]

	def __add__(self, other):
		smallest = self if self.degree < other.degree else other
		largest = self if self.degree >= other.degree else other

		coeffs = []
		for i in range(0, smallest.degree):
			coeffs.append(self.coeffs[i] + other.coeffs[i])
		for i in range(smallest.degree, largest.degree):
			coeffs.append(largest.coeffs[i])

		return ComplexPolynomial(largest.degree, *coeffs)

	def __radd__(self, other):
		if isinstance(other, ComplexPolynomial):
			return self + other
		else:
			return self + ComplexPolynomial(1, *[other])

	def __sub__(self, other):
		return self + ComplexPolynomial(other.degree, *[-1 * coeff for coeff in other.coeffs])

	def __mul__(self, other):
		coeffs = [0 for _ in range(max(self.degree, other.degree))]

		for i in range(self.degree):
			for j in range(other.degree):
				coeffs[(i+j) % len(coeffs)] += self.coeffs[i] * other.coeffs[j]

		return ComplexPolynomial(len(coeffs), *coeffs)

	def __pow__(self, power):
		result = ComplexPolynomial(self.degree, *[1])

		for _ in range(power):
			result = result * self

		return result

	def __str__(self):
		terms = []
		for i in range(self.degree):
			if i == 0:
				terms.append(str(self.coeffs[0]))
			else:
				terms.append(str(self.coeffs[i]) + 'w^' + str(i))
		return ' + '.join(terms)

	# Returns a floating point approximation of the value of the polynomial
	def num(self, omega):
		return sum([self.coeffs[i] * omega**i for i in range(self.degree)])

	# Returns a string representation of the current polynomial where 
	# each coefficient is divided by a given divisor
	def scaled(self, divisor):
		terms = []
		for i in range(self.degree):
			if i == 0:
				if self.coeffs[i] == 0:
					terms.append('0')
				else:
					terms.append(str(self.coeffs[i]) + '/' + str(divisor))
			else:
				if self.coeffs[i] == 0:
					terms.append(str(self.coeffs[i]) + 'w^' + str(i))
				else:
					terms.append(str(self.coeffs[i]) + '/' + str(divisor) + 'w^' + str(i))

		return ' + '.join(terms)

	# Returns a string representation of the exact phase.  To be more precise,
	# it first uses euler to transform the polynomial into a real and an imaginy part.
	# This is useful as we can see the imaginary part as the opposide side of the tri-angle 
	# and the real part as the adiacent side.  Knowing this, we can express the phase as
	# tan^-1(opposide / adiacent)
	def phase(self, parts_per_rotation):
		e = self.simplify().euler(parts_per_rotation)

		return 'arctan(({0}) / ({1}))'.format(' + '.join(e[1]), ' + '.join(e[0]))

	# Repeatedly applies Euler’s formula which states that e^ix = cos(x) + isin(x) to the polynomial,
	# resulting in a string representation of the polynomial in terms of cos, sin, π, p and i where
	# real and imaginary parts are clearly seperated
	def euler(self, parts_per_rotation):
		real = []
		imag = []

		for i in range(self.degree):
			if self.coeffs[i] == 0:
				continue
			if i == 0:
				real.append(str(self.coeffs[0]))
			else:
				if self.coeffs[i] == 1:
					real.append('cos({0}pi/{1})'.format(2*i, parts_per_rotation))
					imag.append('sin({0}pi/{1})'.format(2*i, parts_per_rotation))
				else:
					real.append(str(self.coeffs[i]) + 'cos({0}pi/{1})'.format(2*i, parts_per_rotation))
					imag.append(str(self.coeffs[i]) + 'sin({0}pi/{1})'.format(2*i, parts_per_rotation))

		return real, imag

	# Returns a floating-point value of r and θ that together constitute
	# the polar coordinates of the polynomial. It achieves this by using
	# other utility function to compute the required values.
	def polar_approx(self, omega):
		return self.magnitude_approx(omega), self.phase_approx(omega) / (2*cmath.pi) * 360

	# Returns a floating-point value of the phase.
	# It does this by calling num and then using the phase function from the cmath library.
	def phase_approx(self, omega):
		return cmath.phase(self.num(omega))
	
	# Uses that the powers of ω are in modulus p. This means that the inverse
	# of ω^n is ω^p-n as ω^n * ω^p-n = ω^p = ω^0 = 1. It returns the conjugate
	# of the polynomial and does so simply by inverting the order of all 
	# but the first of the coefficients
	def conjugate(self):
		return ComplexPolynomial(self.degree, *([self.coeffs[0]] + self.coeffs[::-1][:-1]))

	# Uses euler and the Pythagorean theorem to return a string representation
	# of the exact magnitude of the polynomial
	def magnitude(self, parts_per_rotation):
		e = self.simplify().euler(parts_per_rotation)

		return '(({0})^2 + ({1})^2)^0.5'.format(' + '.join(e[0]), ' + '.join(e[1]))

	# Returns the magnitude of the polynomial squared.
	# This is done by first computing ||z||^2 = z * z^-
	# The resulting value is transformed into a sum of cosines using the euler
	# function. Then we leverage symmetry and that cos(ω^n) = cos(ω^p-n) to
	# further simplify the result
	def magnitude_squared(self, parts_per_rotation):
		squared = (self * self.conjugate()).simplify()
		r, _ = squared.euler(parts_per_rotation)

		res = []
		for el in r[:math.ceil(len(r)/2)]:
			if 'cos' not in el:
				res.append(el)
			else:
				parts = el.split('cos')
				num = 2 if parts[0] == '' else 2 * int(parts[0])
				res.append(str(num) + 'cos' + ''.join(parts[1:]))

		return ' + '.join(res)

	# Uses num and the Pythagorean theorem to return a floating-
	# point value of the magnitude
	def magnitude_approx(self, omega):
		v = self.num(omega)
		return (v.real * v.real + v.imag * v.imag) ** 0.5

	# Uses the fact that ω^0 + ω^1 + ... + w^p-1 = 1.
	# This means we can add or substract 1 to/from each of the coefficients
	# and the result will stay the same. It looks for the coefficient closest to 0
	# and then repeatedly adds or substracts to make that one 0.
	def simplify(self):
		if all([coeff == 0 for coeff in self.coeffs]):
			return ComplexPolynomial(self.degree, *self.coeffs)

		min_index = 0
		for i in range(0, len(self.coeffs)):
			if abs(self.coeffs[i]) < abs(self.coeffs[min_index]):
				min_index = i

		return ComplexPolynomial(self.degree, *[coeff - self.coeffs[min_index] for coeff in self.coeffs])