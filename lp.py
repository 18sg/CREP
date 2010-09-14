import pulp
import operator
import itertools

def solve(values):
	if len(values) <= 1:
		return []
	all_pairs = list(itertools.combinations(values, 2))
	all_transfers = ([((a, b), pulp.LpVariable(str(a[0])+'_'+str(b[0]), 0, cat=int)) 
	                  for a, b 
	                  in all_pairs] + 
	                 [((a, b), pulp.LpVariable(str(a[0])+'_'+str(b[0]), 0, cat=int)) 
	                  for b, a 
	                  in all_pairs])
	
	prob = pulp.LpProblem("myProblem", pulp.LpMinimize)
	
	# prob += reduce(operator.add, [t[1] for t in all_transfers])
	prob += pulp.lpSum([t[1] for t in all_transfers])
	
	
	for v in values:
		prob += (sum([t[1] for t in all_transfers if t[0][1] == v]) - 
		         sum([t[1] for t in all_transfers if t[0][0] == v])) == v[1]
	# prob.writeLP("test.lp")
	status = prob.solve()
	return [(t[0][0], t[1][0], int(pulp.value(v))) for t, v in all_transfers if int(pulp.value(v)) != 0]


if __name__ == "__main__":
	from pprint import pprint
	v = [('james', -322), ('matt', 485 + 322), ('jonny', -(521 + 485)), ('tom', 521)]
	# v = [('tom', -674), ('matt', 674 + 452), ('james', -452)]
	import random
	v = []
	for i in xrange(29):
		v.append((chr(ord('a') + i), random.randrange(-1000, 1000)))
	v.append(("rest", -sum(x[1] for x in v)))
	pprint(solve(v))

