from filter import alldgiter
from common import DependencyGraph

alldg = [dg for dg in alldgiter('conll/*/*.dp')]

import random
done = False
while not done:
	i = random.randint(0, len(alldg) -1)

	print str(alldg[i])
	print
	print str(DependencyGraph.filteredcopy(alldg[i]))
	print "-"*10
	while True:
		inpt = raw_input('Continue[y/n] ').upper()
		if inpt in ('Y','N'):
			if inpt == 'N':
				done = True
			break
			
