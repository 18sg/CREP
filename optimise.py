import itertools
from mst import mst
from pprint import pprint
import lp

def optimise_transfers(values, person=lambda v: v[0], ammount=lambda v: v[1]):
	assert(sum(map(ammount, values)) == 0)
	transfers = list(_optimise_transfers(values, person, ammount))
	for p in values:
		assert((sum(t[2] for t in transfers if t[1] == person(p)) 
		        - sum(t[2]
		              for t in transfers if t[0] == person(p)))
		       == ammount(p))
	return transfers


def canonicalise_transfer(transfer):
	if transfer[2] >= 0:
		return transfer
	else:
		return (transfer[1], transfer[0], -transfer[2])


def find_simple_transfers(group, person, ammount):
	for p, rest in ((group[i], group[:i]+group[i+1:]) for i in range(len(group))):
		if ammount(p) == -sum(map(ammount, rest)):
			yield map(canonicalise_transfer, ((person(p), person(r), ammount(r))
			                                  for r in rest))


def make_transfers(ordered_group, person, ammount):
	last_transfer = 0
	for sender, recipient in zip(ordered_group[:-1], ordered_group[1:]):
		transfer = (-ammount(sender)) + last_transfer
		yield canonicalise_transfer((person(sender), person(recipient), transfer))
		last_transfer = transfer


def cost(transfers):
	return sum(abs(t[2]) for t in transfers)


def find_transfers(nodes, edges, start_node=None, already_visited=None):
	start_node = start_node or nodes[0]
	already_visited = (already_visited or []) + [start_node]
	next_nodes = ([e[1] for e in edges if e[0] == start_node and e[1] not in already_visited] + 
	              [e[0] for e in edges if e[1] == start_node and e[0] not in already_visited])
	if not next_nodes:
		return (start_node[1], [])
	
	total_value = 0
	all_transfers = []
	for next_node in next_nodes:
		value, transfers = find_transfers(nodes, edges, next_node, already_visited)
		total_value += value
		all_transfers.extend(transfers)
		all_transfers.append(canonicalise_transfer((start_node, next_node, value)))
	total_value += start_node[1]
	return (total_value, all_transfers)

def find_optimal_transfer(values, person, ammount):
	nodes = [(person(v), ammount(v)) for v in values]
	edges = [(a, b, abs(a[1] + b[1])) for (a, b) in itertools.permutations(nodes, 2)]
	assert(value == 0)
	return [(t[0][0], t[1][0], t[2]) for t in transfers]

def _optimise_transfers(values, person, ammount):
	for group in find_transfer_groups(values, ammount):
		# all_transfers = []
		# all_transfers.extend(find_simple_transfers(group, person, ammount))
		# all_transfers.extend(list(make_transfers(g, person, ammount))
		#                      for g in itertools.permutations(group))
		# all_transfers.append(find_optimal_transfer(group, person, ammount))
		# transfers = min(all_transfers, key=cost)
		transfers = lp.solve(group)
		for transfer in transfers:
			yield transfer



def find_transfer_groups(values, ammount):
	groups = []
	for seq_len in range(1, len(values) + 1):
		for combination in itertools.combinations(values, seq_len):
			value_used = any(any(v in group for group in groups) for v in combination)
			if (not value_used) and sum(map(ammount, combination)) == 0:
				groups.append(combination)
	assert(sum(map(len, groups)) == len(values))
	return groups
