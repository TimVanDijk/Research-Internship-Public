from Constants import *

import random
rand = lambda x : random.randint(0, x-1)

def to_state(m):
	return [m[i*DIGITS_PER_LANE:(i+1)*DIGITS_PER_LANE] for i in range(5)]

def from_state(a):
	return [digit for lane in a for digit in lane]

def digitwise_addition(x, y):
	if (len(x) != len(y)):
		raise ValueError('Error: x and y must have same length.')

	return [(x[i] + y[i]) % P for i in range(len(x))]

def digitwise_substraction(x, y):
	if (len(x) != len(y)):
		raise ValueError('Error: x and y must have same length.')

	return [(x[i] - y[i]) % P for i in range(len(x))]

def hamming_weight(value):
	return len([digit for digit in value if digit != 0])

def probability(b):
	return 1/P**hamming_weight(b)

def difference(x, y):
	if (len(x) != len(y)):
		raise ValueError('Error: x and y must have same length.')

	return [(y[i] - x[i]) % P for i in range(len(x))]

def prints(state):
	if len(state) != LANES:
		state = to_state(state)
	for lane in state:
		s = ' '.join(['.' if digit == 0 else str(digit) for digit in lane])
		print(s)
	print()

def invmodp(a, p):
    for d in range(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def rowtate(delta, i):
	return from_state([row[-i:] + row[:-i] for row in to_state(delta)])

def coltate(delta, i):
	return from_state(to_state(delta)[-i:] + to_state(delta)[:-i])