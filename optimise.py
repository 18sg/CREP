import itertools

def optimise_transfers(values, person=lambda v: v[0], ammount=lambda v: v[1]):
	transfers = list(_optimise_transfers(values, person, ammount))
	for p in values:
		assert((sum(t[2] for t in transfers if t[1] == p) 
		        - sum(t[2]
		              for t in transfers if t[0] == p))
		       == ammount(p))
	return transfers


def canonicalise_transfer(transfer):
	if transfer[2] >= 0:
		return transfer
	else:
		return (transfer[1], transfer[0], -transfer[2])


def find_simple_transfers(group, ammount):
	for p, rest in ((group[i], group[:i]+group[i+1:]) for i in range(len(group))):
		if ammount(p) == -sum(map(ammount, rest)):
			return map(canonicalise_transfer, ((p, r, ammount(r))
			                                   for r in rest))
	else:
		return None


def _optimise_transfers(values, person, ammount):
	for group in find_transfer_groups(values, ammount):
		transfers = find_simple_transfers(group, ammount)
		if transfers is not None:
			for t in transfers:
				yield t
		else:
			sorted_group = (sorted((v for v in group if ammount(v) <= 0), 
			                       key=lambda x: -ammount(x))
			                + sorted((v for v in group if ammount(v) > 0), 
			                         key=lambda x: -ammount(x)))
			last_transfer = 0.0
			for sender, recipient in zip(sorted_group[:-1], sorted_group[1:]):
				transfer = (-ammount(sender)) + last_transfer
				yield (sender, recipient, transfer)
				last_transfer = transfer



def find_transfer_groups(values, ammount):
	groups = []
	for seq_len in range(1, len(values) + 1):
		for combination in itertools.combinations(values, seq_len):
			value_used = any(any(v in group for group in groups) for v in combination)
			if (not value_used) and sum(map(ammount, combination)) == 0:
				groups.append(combination)
	assert(sum(map(len, groups)) == len(values))
	return groups
