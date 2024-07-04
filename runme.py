#!/usr/bin/env python3
"""
query a graphviz dot file
"""
# https://realpython.com/python-logging-source-code/
import argparse  # https://docs.python.org/3.3/library/argparse.html


import networkx as nx

def args():
	"""
	"""
	theparser = argparse.ArgumentParser(
		description="query grpahviz dot file", allow_abbrev=False
	)

	# required positional argument
	theparser.add_argument(
		"dotfilename",
		#metavar="dot_file_name",
		type=str,
		help="file name of graphviz dot",
	)

	# optional argument
	theparser.add_argument(
		"--list_all_nodes",
		action='store_true', # https://stackoverflow.com/a/5271692/1164295
		help="list all nodes")

	# optional argument
	theparser.add_argument(
		"--list_all_neighbors",
		nargs=2, # https://stackoverflow.com/a/43381946/1164295
		metavar=('node_name', 'depth_integer'), # https://stackoverflow.com/a/43660050/1164295
		help="list all neighbors")

	# optional argument
	theparser.add_argument(
		"--list_upstream",
		nargs=2,
		metavar=('node_name', 'depth_integer'), # https://stackoverflow.com/a/43660050/1164295
		help="list upstream nodes")

	# optional argument
	theparser.add_argument(
		"--list_downstream",
		nargs=2,
		metavar=('node_name', 'depth_integer'), # https://stackoverflow.com/a/43660050/1164295
		help="list downstream nodes")

	# optional argument
	theparser.add_argument(
		"--shortest_path",
		nargs=2,
		metavar=('start_node_name', 'end_node_name'), # https://stackoverflow.com/a/43660050/1164295
		help="shortest path between two nodes")

	arguments = theparser.parse_args()

	return arguments

if __name__ == "__main__":

	arguments = args()
	#print("filename=",arguments.dotfilename)

	# https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pydot.read_dot.html
	G = nx.Graph(nx.nx_pydot.read_dot(arguments.dotfilename))

	if arguments.list_all_nodes:
		print("all nodes:")
		print(G.nodes)
		# ['start', 'end', 'a0', 'b0', 'a1', 'b3', 'b2', 'a3']

	if arguments.list_all_neighbors:
		print("neighbors of "+arguments.list_all_neighbors[0]+" to depth "+arguments.list_all_neighbors[1]+":")
		print(list(nx.all_neighbors(G, arguments.list_all_neighbors[0])))

	# https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.predecessors.html
	if arguments.list_upstream:
		print("upstream neighbors of "+arguments.list_upstream[0]+" to depth "+arguments.list_upstream[1]+":")
		print(list(nx.predecessors(G, arguments.list_upstream[0])))

	# https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.successors.html#networkx.DiGraph.successors
	if arguments.list_downstream:
		print("down neighbors of "+arguments.list_downstream[0]+" to depth "+arguments.list_downstream[1]+":")
		print(list(nx.successors(G, arguments.list_downstream[0])))

	if arguments.shortest_path:
		path = nx.shortest_path(G, arguments.shortest_path[0], arguments.shortest_path[1])
		print(path)


	#print([n for n in G.predecessors('a1')])