import glpk
import itertools


# 'values' is a list of pairs of (name, ammount_owed).
def solve(values):
	if len(values) <= 1:
		return []
	
	# Start a new minimisation problem.
	lp = glpk.LPX()
	lp.obj.maximize = False
	
	# The set of transfers between any two people.
	transfers = list(itertools.permutations(values, 2))
	
	# Add a constraint for each person so that they recieve the ammount they are owed.
	lp.rows.add(len(values))
	for r, (name, ammount) in zip(lp.rows, values):
		r.bounds = ammount
	
	# Each col is a potential transfer between two people.
	lp.cols.add(len(transfers))
	for c in lp.cols:
		c.bounds = 0, None
	
	# Weight the value of all transfers equally.
	lp.obj[:] = [1] * len(transfers)
	
	# Set up the problem matrix.  Each row in the matrix represents a sum of the
	# ammounts that each person sends or recieves, and each column represents a
	# particular transfer, so each cell is 1 if the person recieves from a
	# transfer, -1 if they are the senser, or 0 if they are not affected.
	matrix = []
	for name, ammount in values:
		for (sender_name, sender_ammount), (recipient_name, recipient_ammount) in transfers:
			if name == recipient_name:
				matrix.append(1)
			elif name == sender_name:
				matrix.append(-1)
			else:
				matrix.append(0)
	lp.matrix = matrix
	
	# Run the solver.
	lp.simplex()
	
	# Return a list of (sender, recipient, ammount) for all non-zero transfers.
	return [(transfer[0][0], transfer[1][0], int(value.primal))
	        for transfer, value in zip(transfers, lp.cols)
	        if int(value.primal) != 0]


# Check a problem and solution for consistency, returnin the total ammount transfered.
def check(prob, soln):
	value = sum(s[2] for s in soln)
	for name, owed in prob:
		actual = sum(s[2] for s in soln if s[1] == name) - sum(s[2] for s in soln if s[0] == name)
		if actual != owed:
			print (name, owed, actual)
	return value


if __name__ == "__main__":
	from pprint import pprint
	v = [('james', -322), ('matt', 485 + 322), ('jonny', -(521 + 485)), ('tom', 521)]
	# v = [('tom', -674), ('matt', 674 + 452), ('james', -452)]
	# import random
	# v = []
	# for i in xrange(29):
	# 	v.append((chr(ord('a') + i), random.randrange(-1000, 1000)))
	# v.append(("rest", -sum(x[1] for x in v)))
	s2 = solve(v)
	print check(v, s2)

