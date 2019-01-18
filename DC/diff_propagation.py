from Util import *
from ThreeCircle import *
from Constants import *

import itertools

template = [rand(P) for _ in range(160)]

m_1 = []
for el in list(itertools.product(range(P), repeat=2)):
	m = template[:]
	m[0] = el[0]
	m[32] = el[1]
	m_1 += [to_state(m)]

m_2 = [tuple(from_state(round(m))) for m in m_1]
m_2_chi = [tuple(from_state(chi(round(m)))) for m in m_1]

for el in m_2:
	prints(el)