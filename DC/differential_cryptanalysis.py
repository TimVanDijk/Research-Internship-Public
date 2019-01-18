import itertools
import random
from copy import deepcopy

from CBC_MAC import *
from ThreeCircle import *
from Util import *
from Constants import *

rand = lambda x : random.randint(0, x-1)

def linear(a):
	a = theta(a)
	a = pi(a)
	a = iota(a)
	a = rho(a)
	return a

def inv_linear(a):
	a = inv_rho(a)
	a = inv_iota(a)
	a = inv_pi(a)
	a = inv_theta(a)
	return a

def coll_1r_old():
	MAC = ThreeCircleMAC()

	a = [[rand(P) for _ in range(LANES * DIGITS_PER_LANE)] for _ in range(2)]
	mac_a = MAC.CBC(a, 1) 

	# Set b[0] to be a with with input difference [1, 0, 0, ..., 0]
	b = [a[0][:], None]
	b[0][0] = (b[0][0] + 1) % P

	# After chi(b[0]), the difference is either
	# [1, 0, 0, ..., 0], [1, 0, 0, ..., 0] or [1, 0, 0, ..., 2]
	# For each of the possible outcomes, compute the difference after the first round.
	for i in range(3):
		# Compute possible outcome
		b_after_chi = chi(to_state(a[0]))
		b_after_chi[0][0] = (b_after_chi[0][0] + 1) % P
		b_after_chi[4][-1] = (b_after_chi[4][-1] + i) % P

		# Compute value after first round for that outcome
		out = theta(b_after_chi)
		out = pi(out)
		out = iota(out)
		out = rho(out)

		# Now, we must pick b[1] such that out + b[1] = a[0]_after_first_round + a[1]
		# ==> b[1] = a[0]_after_first_round + a[1] - out
		b[1] = digitwise_substraction(digitwise_addition(from_state(round(to_state(a[0]))), a[1]), from_state(out))
		
		# Compute MAC of b and check if same as MAC of a
		mac_b = MAC.CBC(b, 1)
		print("MAC of b_" + str(i) + ":")
		for el in to_state(mac_b):
			print(el)
		print("Same? ", "yes" if mac_a == mac_b else "no")
		print()

def coll_1r():
	i = 1
	delta_in = 	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	delta_out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

	MAC = ThreeCircleMAC()

	while True:
		X = [[rand(P) for _ in range(160)] for _ in range(2)]
		Y = [digitwise_addition(X[0], delta_in), digitwise_substraction(X[1], delta_out)]

		macX = MAC.CBC(X, 1)
		macY = MAC.CBC(Y, 1)

		# Check if we found a collision.
		if macX == macY:
			print(i)

			for el in to_state(X[0]):
				print(el)
			print()
			for el in to_state(X[1]):
				print(el)
			break

		i += 1

def coll_2r():
	i = 1
	delta_in = 	[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	delta_out = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] + \
				[1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

	MAC = ThreeCircleMAC()

	prints(delta_in)
	prints(delta_out)
	while True:
		X = [[rand(P) for _ in range(160)] for _ in range(2)]
		Y = [digitwise_addition(X[0], delta_in), digitwise_substraction(X[1], delta_out)]
	
		macX = MAC.CBC(X, 2)
		macY = MAC.CBC(Y, 2)

		# Check if we found a collision.
		if macX == macY:
			print(i)
			break

		i += 1

def coll_3r():
	i = 1
	while True:
		if (i % 1000) == 0:
			print(i)

		i += 1

		X = [[rand(P) for _ in range(160)] for _ in range(2)]
		Y = [X[0][:], X[1][:]]
		Y[0][96] = (Y[0][96] + 2) % P
		Y[0][128] = (Y[0][128] + 1) % P

		#l2X = from_state(round(round(to_state(X[0]))))
		#l2Y = from_state(round(round(to_state(Y[0]))))

		sX = to_state(X[0])
		sY = to_state(Y[0])

		# Begin round 1
		sX = round(sX)
		sY = round(sY)
		# End round 1

		# Begin round 2
		sX = round(sX)
		sY = round(sY)
		# End round 2

		diff = from_state([	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
							[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
							[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
							[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]])

		actual = difference(from_state(sX), from_state(sY))
		if diff == actual:
			pass
			#print("Correct difference at start of round 3 at attempt:", i)
		else:
			continue
		# Now, we must pick Y[1] such that it compensates for the differential after round 2
		# ==> 
		# Y[1] = X[1] - diff

		Y[1] = digitwise_substraction(X[1], diff) 
		
		# Compute MACs for X and Y.

		MAC = ThreeCircleMAC()
		macX = MAC.CBC(X, 3)
		macY = MAC.CBC(Y, 3)

		# Check if we found a collision.
		if macX == macY:
			print("Collision found!!!")
			print(X)
			print(Y)
			print(i)
			break

		i += 1

if __name__ == "__main__":
	#coll_1r()
	coll_2r()

	if False:
		delta_in = 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
					[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		for i in range(1000000):
			X = [rand(P) for _ in range(160)]
			Y = to_state(digitwise_addition(X, delta_in))
			X = to_state(X)

			l2X = round(round(X))
			l2Y = round(round(Y))

			if hamming_weight(difference(from_state(l2X), from_state(l2Y))) == 12:
				c3X = from_state(chi(l2X))
				c3Y = from_state(chi(l2Y))
				print(difference(c3X, c3Y))
				prints(difference(c3X, c3Y))
				break