from Util import *
from ThreeCircle import *
from CBC_MAC import ThreeCircleMAC
import json

def linear(a):
	a = theta(a)
	a = pi(a)
	a = iota(a)
	a = rho(a)
	return a

# Only use the key for testing and initializing the MACer!!!
KEY = 	[0, 0, 1, 1, 2, 1, 1, 2, 1, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1] + \
		[2, 0, 0, 0, 2, 0, 2, 1, 2, 1, 2, 2, 2, 1, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2] + \
		[2, 2, 2, 0, 1, 1, 1, 0, 1, 2, 0, 2, 0, 0, 2, 1, 2, 2, 0, 2, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0] + \
		[2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 1, 2, 0, 2, 0, 2, 1, 2] + \
		[0, 1, 2, 2, 2, 2, 2, 0, 2, 1, 1, 2, 0, 2, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 2, 0, 2, 1, 0, 2, 1, 0]


def trails_2r():
	MAC = ThreeCircleMAC(KEY)

	SEED_IN = 	[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	collision_data = []

	for colshift in range(LANES):
		for rowshift in range(DIGITS_PER_LANE):
			print("Progress: ", colshift*DIGITS_PER_LANE + rowshift, '/', LANES*DIGITS_PER_LANE)
			# Shift columns and find corresponding delta_out by assuming first round chi and theta are identity
			delta_in = coltate(SEED_IN, colshift)
			delta_out = from_state(linear(chi(rho(pi(to_state(delta_in))))))

			# Shift rows
			delta_in = rowtate(delta_in, rowshift)
			delta_out = rowtate(delta_out, rowshift)

			# Find a collision for given differential
			while True:
				X = [[rand(P) for _ in range(160)] for _ in range(2)]
				Y = [digitwise_addition(X[0], delta_in), digitwise_substraction(X[1], delta_out)]
			
				macX = MAC.CBC(X, 2)
				macY = MAC.CBC(Y, 2)

				if macX == macY:
					break

			# If we made it here, we found a collision and the variables are still set
			collision = {'colshift': colshift, 'rowshift': rowshift, \
			'message': X, 'delta_in': delta_in, 'delta_out': delta_out}

			collision_data.append(collision)

	# Save collision data to disk
	with open('collision_data_2r.json', 'w') as fp:
		json.dump(collision_data, fp)
	print("Saved collision data to collision_data_2r.json")

if __name__ == "__main__":
	trails_2r ()
