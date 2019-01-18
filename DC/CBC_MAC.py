import random

#from ThreeCircle import threecircle, round
from ThreeCircle import *
from Util import *
from Constants import *

rand = lambda x : random.randint(0, x-1)

def n_round_threecircle(a, n):
	a = to_state(a)
	for _ in range(n):
		a = chi(a)
		a = theta(a)
		a = pi(a)
		a = iota(a)
		a = rho(a)
	return from_state(a)

class ThreeCircleMAC:

	def __init__(self, key=None):
		self.key = key if key != None else [rand(P) for _ in range(LANES * DIGITS_PER_LANE)]

	def CBC(self, messages, n=2):
		mac = self.key[:]

		for message in messages[:-1]:
			a = digitwise_addition(mac, message)
			mac = n_round_threecircle(a, n)

		mac = digitwise_addition(mac, messages[-1])
		mac = from_state(threecircle(to_state(mac)))

		mac = digitwise_addition(mac, self.key)

		return mac
