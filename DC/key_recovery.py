from Util import *
from ThreeCircle import *
from CBC_MAC import *
from differential_cryptanalysis import inv_linear

import itertools
import json

# Only use the key for testing!!!
KEY = 	[0, 0, 1, 1, 2, 1, 1, 2, 1, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1] + \
		[2, 0, 0, 0, 2, 0, 2, 1, 2, 1, 2, 2, 2, 1, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2] + \
		[2, 2, 2, 0, 1, 1, 1, 0, 1, 2, 0, 2, 0, 0, 2, 1, 2, 2, 0, 2, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0] + \
		[2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 1, 2, 0, 2, 0, 2, 1, 2] + \
		[0, 1, 2, 2, 2, 2, 2, 0, 2, 1, 1, 2, 0, 2, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 2, 0, 2, 1, 0, 2, 1, 0]

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

def main():
	#Load collision data from disk
	with open('collision_data_2r.json', 'r') as fp:
		collision_data = json.load(fp)
	
	key_guess = [[None for _ in range(DIGITS_PER_LANE)] for _ in range(LANES)]

	for entry in collision_data:
		delta_in, delta_out = to_state(entry['delta_in']), to_state(entry['delta_out'])
		message = to_state(entry['message'][0])
		c, r = entry['colshift'], entry['rowshift']

		b_i_prime = inv_linear(inv_round(delta_out))[c-1][r-1]
		a_i_prime = delta_in[c-1][r-1]
		a_j_prime = delta_in[c][r]

		# Use the fact that a_j = b_i' - a_i' -a_j'^2 / (2aj')
		a_j = ((b_i_prime - a_i_prime - a_j_prime**2) * 2 * invmodp(a_j_prime, P)) % P

		#We know a_j is the sum of the input value and the key => derive the key
		key_guess[c][r] = (a_j - message[c][r]) % P

	for i in range(LANES):
		print("Key:  ", to_state(KEY)[i])
		print("Guess:", key_guess[i])
		print("Same? ", to_state(KEY)[i] == key_guess[i])
		print()
	print("Full match on the key?", key_guess == to_state(KEY))
		

if __name__ == "__main__":
	main()
