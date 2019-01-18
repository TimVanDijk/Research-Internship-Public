from sympy.logic import SOPform
from sympy import symbols
from sympy.combinatorics import GrayCode

import math

#This function counts and prints the number of occurances of AND, OR and NEG operations in the solution
def evaluate(solution):
	solution = str(solution)
	ands = solution.count('&')
	ors = solution.count('|')
	negs = solution.count('~')

	print("{}\n&: {}\t|: {}\t~: {}\n".format(solution, ands, ors, negs))

# Generates a list of inputs whose output we don't care about.
def generate_dontcares(num_bits, mod):
	dontcares = []
	for a in GrayCode(num_bits).generate_gray():
		for b in GrayCode(num_bits).generate_gray():
			if int(a, 2) >= mod or int(b, 2) >= mod:
				dontcares += [b + a]
	return dontcares

# Modular addition of a and b where a and b are bitstrings
def mod_add(a, b, mod):
	res = (int(a, 2) + int(b, 2)) % mod
	num_bits = str(math.ceil(math.log(mod, 2)))
	return ('{:0' + num_bits + 'b}').format(res)

# Modular addition of a and b where a and b are bitstrings
def mod_mult(a, b, mod):
	res = (int(a, 2) * int(b, 2)) % mod
	num_bits = str(math.ceil(math.log(mod, 2)))
	return ('{:0' + num_bits + 'b}').format(res)

def main():
	mod = 3
	operation = mod_mult
	#operation = mod_add

	num_bits = math.ceil(math.log(mod, 2))

	dontcares = generate_dontcares(num_bits, mod)

	for index in range(0, num_bits):
		print("Minimized Sum of Products (SOP) boolean expression for c" + str(index))
		
		# Create a list of inputs where the output is 1
		minterms = []
		for a in GrayCode(num_bits).generate_gray():
			for b in GrayCode(num_bits).generate_gray():
				if b + a in dontcares:
					continue
				if operation(a, b, mod)[-(index + 1)] == '1':
					minterms += [b + a]

		# Transform dontcares and minterms into format required by SOPform
		transformed_dontcares = [[int(c) for c in el] for el in dontcares]
		transformed_minterms = [[int(c) for c in el] for el in minterms]

		#Prepare a symbol string e.g. 'b2, b1, b0, a2, a1, a0'
		symbol_string = ', '.join([c + str(i) for c in ['a', 'b'] for i in range(num_bits)][::-1])

		solution = SOPform(symbols(symbol_string), transformed_minterms, transformed_dontcares)
		evaluate(solution)

if __name__ == "__main__":
	main()