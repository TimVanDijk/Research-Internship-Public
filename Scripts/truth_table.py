import itertools
import math

# A list of the fields we want to create truth tables of operations for.
mods = [3, 5, 7]

def main():
	# Build a truth table for +, * and ^ for GF(3), GF(5) and GF(7).
	for mod in mods:
		# Compute the number of bits required to store a digit in mod.
		num_bits = math.ceil(math.log(mod, 2))

		# Generate and set the header for our three csv files.
		header = ','.join([letter + str(i) for letter in ['b', 'a', 'c'] for i in range(num_bits)[::-1]]).replace(',c', ',,c', 1) + '\n'
		add_truthtable = mult_truthtable = sqr_truthtable = header

		# Generate the left-hand side of the truth table containing all possible combinations of inputs.
		table = list(itertools.product([0, 1], repeat=num_bits*2))

		# For each row of input in the table.
		for inputs in table:
			# Format the inputs nicely in the required format.
			left = ','.join([str(el) for el in inputs]) + ',,'

			#Compute B and A: the values that the input is the binary representation of.
			A = B = 0
			for i in range(num_bits):
				A += inputs[len(inputs)//2  - 1 - i] << i
				B += inputs[len(inputs) - 1 - i] << i

			# If either A or B is too large to be a member of the group we are in, set the output value to "don't care".
			if A >= mod or B >= mod:
				line = left + ','.join(['X' for _ in range(num_bits)]) + '\n'
				add_truthtable += line
				mult_truthtable += line
				sqr_truthtable += line
			else:
				# Compute the desired outcome for all operations. Then format it to be a valid right-hand side of the table.
				# Then append the truth table with a line consisting of right-hand side concatenated to the left-hand side.
				add_truthtable += left + ','.join(format((A + B) % mod, '0' + str(num_bits) + 'b')) + '\n' 
				mult_truthtable += left + ','.join(format((A * B) % mod, '0' + str(num_bits) + 'b')) + '\n' 
				
				# Squaring is a special case and we only care about the outcome when the input values are same.
				if A == B:
					sqr_truthtable += left + ','.join(format((A * A) % mod, '0' + str(num_bits) + 'b')) + '\n'
				else:
					sqr_truthtable += left + ','.join(['X' for _ in range(num_bits)]) + '\n'

		# Store truth tables to disk in LogicFriday (.csv) format.
		with open('../LogicFriday/TruthTables/F_'+str(mod)+'_add.csv', 'w') as f:
			f.write(add_truthtable)

		with open('../LogicFriday/TruthTables/F_'+str(mod)+'_mult.csv', 'w') as f:
			f.write(mult_truthtable)

		with open('../LogicFriday/TruthTables/F_'+str(mod)+'_sqr.csv', 'w') as f:
			f.write(sqr_truthtable)	

if __name__ == "__main__":
	main()