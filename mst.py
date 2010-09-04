import pdb

def mst(nodes, edges):
	if not edges:
		return []
	no_nodes = len(nodes)
	nodes_not_in_tree = set(nodes)
	nodes_in_tree = set()
	edges_not_in_tree = set(edges)
	edges_in_tree = set()
	
	first_edge = min(edges_not_in_tree, key=lambda e: e[2])
	edges_in_tree.add(first_edge)
	nodes_in_tree.update(first_edge[:2])
	
	edges_not_in_tree.remove(first_edge)
	nodes_not_in_tree.remove(first_edge[0])
	nodes_not_in_tree.remove(first_edge[1])
	while len(nodes_in_tree) < no_nodes:
		edge = min((e for e in edges_not_in_tree if e[0] in nodes_in_tree and e[1] in nodes_not_in_tree),
		           key=lambda e: e[2])
		edges_in_tree.add(edge)
		nodes_in_tree.add(edge[1])
		
		edges_not_in_tree.remove(edge)
		nodes_not_in_tree.remove(edge[1])
	
	return edges_in_tree
