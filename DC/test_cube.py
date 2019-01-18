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

	return Mi_1, Mi_2, MAC.CBC([Mi_1, Mi_2], n=2)

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

M0_1 = [0 for _ in range(160)]
M0_2 = [0 for _ in range(160)]

DIM = 9
print("Nodes:", 2**DIM)
print("Edges:", DIM * 2**(DIM-1))
MAC = ThreeCircleMAC()

def check_shifts():
	for j in range(1, 32):
			i = 0
			while True:
				d_in = rowtate(delta_in, j)
				d_out = rowtate(delta_out, j)

				A = [rand(P) for _ in range(160)]
				B = digitwise_addition(A, d_in)

				X = from_state(round(round(to_state(A))))
				Y = from_state(round(round(to_state(B))))

				if difference(X, Y) == d_out:
					print("It worked for", j ,"in", i, "tries")
					break

				i += 1
				if i > 800:
					print(j, "failed")
					break

def main():
	print("M0_1:")
	prints(M0_1)

	print("M0_2:")
	prints(M0_2)

	print("[!] Initializing hypercube")
	hc = [None for _ in range(2**DIM)]
	print("[+] Completed initializing hypercube")

	print("[!] Building hypercube...")
	hc = parmap.map(functools.partial(build_node, hc=hc), range(len(hc)), pm_pbar=True, pm_processes=8, pm_chunksize=100)

	#hc = [build_node(i, hc) for i in range(len(hc))]
	print("[+] Completed building hypercube")
	
	for i, node in enumerate(hc):
		Mi_1, Mi_2, MAC_i = node
		for x, neighbor in [(x, i ^ (1 << x)) for x in range(DIM)]:
			if i > neighbor:
				continue

			Mj_1, Mj_2, MAC_j = hc[neighbor]
			
			if MAC_i == MAC_j:
				print("Collision between nodes", (i, neighbor), "over an edge through dimension", x+1)
	
	print("[!] Checking for full collisions...")
	# Counts elements in O(n)
	D = defaultdict(list)
	for idx, item in enumerate(hc):
		D[tuple(item[2])].append(idx)
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
	#check_shifts()