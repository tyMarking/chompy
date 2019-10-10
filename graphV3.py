# TODO:

"""
-graph object
	-dict of nodes
	-store start and end nodes
		-or their keys

	-functions for graph:
		-navigate/traverse
		-calc numbers (DFS?)
			stack of nodes
			add start to queue
			while stack has items
				curr = stack.pop


-node object
	-value
		-the matrix representing a board state
	-number
		-the "ideal" number of moves away from the end node
		-likely initialized at -1 or infinity or something like that
	-children
		-the nodes (or keys to nodes) that can be accessed with one move from this node
	-parents
		-the nodes (or keys to nodes) that have this node as a child

	-functions for node:
		-add child
			-given another node, add that node to children,
			-add this node to that node's parents

"""
