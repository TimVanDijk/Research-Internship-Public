import numpy as np
import random
import pickle

from Constants import *
from Util import *

rand = lambda x : random.randint(0, x-1)
transpose = lambda l : list(map(list, zip(*l)))

NUM_TESTS = 10

THETA_INV_MATRIX = pickle.load(open('theta_inv_matrix.dat', 'rb'))

RC = [0 for _ in range(DIGITS_PER_LANE)]

def chi(a):
	b = [[None for _ in range(DIGITS_PER_LANE)] for _ in range(LANES)]
	for j in range(LANES * DIGITS_PER_LANE):
		cur_y = j % LANES; next_y = (j+1) % LANES
		cur_x = j % DIGITS_PER_LANE; next_x = (j+1) % DIGITS_PER_LANE
		b[cur_y][cur_x] = (a[cur_y][cur_x] + a[next_y][next_x]*a[next_y][next_x]) % P
	return b 

def inv_chi(b):
	a = [[None for _ in range(DIGITS_PER_LANE)] for _ in range(LANES)]
	
	for v in range(P):
		a[LANES-1][DIGITS_PER_LANE-1] = v
		for j in range(LANES * DIGITS_PER_LANE - 1)[::-1]:
			cur_y = j % LANES; next_y = (j+1) % LANES
			cur_x = j % DIGITS_PER_LANE; next_x = (j+1) % DIGITS_PER_LANE
			a[cur_y][cur_x] = (b[cur_y][cur_x] - a[next_y][next_x]**2) % P
		# check if no contradiction
		if (a[LANES-1][DIGITS_PER_LANE-1] + a[0][0]**2) % P == b[LANES-1][DIGITS_PER_LANE-1]:
			return a

	raise(ValueError('b has no preimage'))
	

def theta(a):
	p = [sum([a[y][x] for y in range(LANES)]) % P for x in range(DIGITS_PER_LANE)]
	e = [(p[(x+12) % DIGITS_PER_LANE] + p[(x+17) % DIGITS_PER_LANE]) % P for x in range(DIGITS_PER_LANE)]
	return [[(a[y][x] + e[(x+y) % DIGITS_PER_LANE]) % P for x in range(DIGITS_PER_LANE)] for y in range(LANES)]

def inv_theta(a):
	a = np.matmul(np.array(from_state(a)), THETA_INV_MATRIX) % P
	return to_state(list(a))


def pi(a):
	return [a[(y+1) % LANES] for y in range(LANES)]

def inv_pi(a):
	return [a[(y-1) % LANES] for y in range(LANES)]


def iota(a):
	return [[(a[0][z] + RC[z]) % P for z in range(DIGITS_PER_LANE)]] + a[1:]

def inv_iota(a):
	return [[(a[0][z] - RC[z]) % P for z in range(DIGITS_PER_LANE)]] + a[1:]


def rho(a):
	r = [0, 2, 6, 11, 19]
	return [[a[y][(z+r[y]) % DIGITS_PER_LANE] for z in range(DIGITS_PER_LANE)] for y in range(LANES)]

def inv_rho(a):
	r = [0, 2, 6, 11, 19]
	return [[a[y][(z-r[y]) % DIGITS_PER_LANE] for z in range(DIGITS_PER_LANE)] for y in range(LANES)]


def round(a, nr=0):
	a = chi(a)
	a = theta(a)
	a = pi(a)
	a = iota(a)
	a = rho(a)
	return a

def inv_round(a, nr=0):
	a = inv_rho(a)
	a = inv_iota(a)
	a = inv_pi(a)
	a = inv_theta(a)
	a = inv_chi(a)
	return a
	

def threecircle(a):
	for nr in range(-11, 0+1):
		a = round(a, nr)
	return a

def inv_threecircle(a):
	for nr in range(0, -11-1, -1):
		a = inv_round(a, nr)
	return a
		

def main():
	a = [[rand(P) for _ in range(DIGITS_PER_LANE)] for _ in range(LANES)]
	print('Input')
	prints(a)

	result = threecircle(a)
	print('Result')
	prints(a)

def test():
	for n in range(NUM_TESTS):
		print("Test #" + str(n))
		a = [[rand(P) for _ in range(DIGITS_PER_LANE)] for _ in range(LANES)]

		print("Chi inverse test        ", ("ok" if chi(a) == chi(inv_chi(chi(a))) else 'fail'))
		print("Theta inverse test      ", ("ok" if a == inv_theta(theta(a)) else 'fail'))
		print("Pi inverse test         ", ("ok" if a == inv_pi(pi(a)) else 'fail'))
		print("Iota inverse test       ", ("ok" if a == inv_iota(iota(a)) else 'fail'))
		print("Rho inverse test        ", ("ok" if a == inv_rho(rho(a)) else 'fail'))
		print("Round inverse test      ", ("ok" if round(a) == round(inv_round(round(a))) else 'fail'))
		print("ThreeCircle inverse test", ("ok" if threecircle(a) == threecircle(inv_threecircle(threecircle(a))) else 'fail'))
		print()

if __name__ == "__main__":
	#main()
	test()
