from Util import *
from CBC_MAC import ThreeCircleMAC
from ThreeCircle import *

import math
import functools
import parmap
from collections import defaultdict, Counter

def rowtate(delta, i):
	return from_state([row[-i:] + row[:-i] for row in to_state(delta)])

def rotate(delta, i):
	return delta[-i:] + delta[:-i]

def build_node(i, hc):
	Mi_1 = M0_1[:]
	Mi_2 = M0_2[:]

	for idx, val in enumerate(list(format(i, '032b')[::-1])):
		if val == '1':
			Mi_1 = digitwise_addition(Mi_1, rowtate(delta_in, idx))
			Mi_2 = digitwise_substraction(Mi_2, rowtate(delta_out, idx))

	return MAC.CBC([Mi_1, Mi_2], n=2)

delta_in = 	[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
			[1,	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

delta_out = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0] + \
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0] + \
			[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] + \
			[1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + \
			[0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

M0_1 = [rand(P) for _ in range(160)]
M0_2 = [rand(P) for _ in range(160)]

DIM = 9
print("Nodes:", 2**DIM)
print("Edges:", DIM * 2**(DIM-1))
MAC = ThreeCircleMAC()

def main():
	# Print M0 such that you are able to reconstruct the messages used at any node
	print("M0_1:")
	prints(M0_1)

	print("M0_2:")
	prints(M0_2)

	# Make room for 2^n nodes
	print("[!] Initializing hypercube")
	hc = [None for _ in range(2**DIM)]
	print("[+] Completed initializing hypercube")

	# Compute the MAC of each node in parallel and show a progress bar
	print("[!] Building hypercube...")
	hc = parmap.map(functools.partial(build_node, hc=hc), range(len(hc)), pm_pbar=True, pm_processes=8, pm_chunksize=100)
	print("[+] Completed building hypercube")	

	# Check for collisions in O(n)
	print("[!] Checking for full collisions...")
	D = defaultdict(list)
	for idx, mac in enumerate(hc):
		D[tuple(mac)].append(idx)
	D = {k: v for k, v in D.items() if len(v) > 1}

	if len(D.items()) == 0:
		print("[-] No collisions found")
	else:
		print("[+] Collisions found")
		for k, v in D.items():
			print("Nodes", v, "share the following MAC:")
			prints(k)

if __name__ == "__main__":
	main()
