import numpy as np

from ThreeCircle import theta
from Util import *

inp = np.identity(160)
out = np.apply_along_axis(lambda x: from_state(theta(to_state(x))), axis=1, arr=inp)

inv = Matrix(IntegerModRing(3), out).inverse()

for el in list(inv):
	print(el)