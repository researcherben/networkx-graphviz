#!/usr/bin/env python3
"""
query a graphviz dot file

python3 search_graphviz_dot.py --help

python3 search_graphviz_dot.py example_flat_graph.dot --list_all_nodes

python3 search_graphviz_dot.py example_flat_graph.dot --list_all_neighbors a1 1


"""
# https://realpython.com/python-logging-source-code/
import argparse  # https://docs.python.org/3.3/library/argparse.html


import networkx as nx


def recursive_predecessors(
    G, suffix_str: str, parent_node_name: str, max_depth: int, counter: int
) -> None:
    """
    recursively print parent nodes
    """
    for this_node in G.predecessors(parent_node_name):
        print(str(counter) + ": " + this_node + " -> " + parent_node_name + suffix_str)
        max_depth -= 1
        if max_depth > 0:
            counter += 1
            suffix_str += " -> " + parent_node_name
            recursive_predecessors(G, suffix_str, this_node, max_depth, counter)
    return


def recursive_successors(
    G, prefix_str: str, parent_node_name: str, max_depth: int, counter: int
) -> None:
    """
    recursively print child nodes
    """
    for this_node in G.successors(parent_node_name):
        print(str(counter) + ": " + prefix_str + parent_node_name + " -> " + this_node)
        max_depth -= 1
        if max_depth > 0:
            counter += 1
            prefix_str += parent_node_name + " -> "
            recursive_successors(G, prefix_str, this_node, max_depth, counter)

    return


def args() -> None:
    """
    command-line arguments
    """
    theparser = argparse.ArgumentParser(
        description="query grpahviz dot file", allow_abbrev=False
    )

    # required positional argument
    theparser.add_argument(
        "dotfilename",
        # metavar="dot_file_name",
        type=str,
        help="file name of graphviz dot",
    )

    # optional argument
    theparser.add_argument(
        "--list_all_nodes",
        action="store_true",  # https://stackoverflow.com/a/5271692/1164295
        help="list all nodes",
    )

    # optional argument
    theparser.add_argument(
        "--list_all_neighbors",
        nargs=2,  # https://stackoverflow.com/a/43381946/1164295
        metavar=(
            "node_name",
            "depth_integer",
        ),  # https://stackoverflow.com/a/43660050/1164295
        help="list all neighbors",
    )

    # optional argument
    theparser.add_argument(
        "--list_upstream",
        nargs=2,
        metavar=(
            "node_name",
            "depth_integer",
        ),  # https://stackoverflow.com/a/43660050/1164295
        help="list upstream nodes",
    )

    # optional argument
    theparser.add_argument(
        "--list_downstream",
        nargs=2,
        metavar=(
            "node_name",
            "depth_integer",
        ),  # https://stackoverflow.com/a/43660050/1164295
        help="list downstream nodes",
    )

    # optional argument
    theparser.add_argument(
        "--list_start_nodes",
        action="store_true",  # https://stackoverflow.com/a/5271692/1164295
        help="list nodes that have only outbound edges",
    )

    # optional argument
    theparser.add_argument(
        "--list_end_nodes",
        action="store_true",  # https://stackoverflow.com/a/5271692/1164295
        help="list nodes that have only inbound edges",
    )

    # optional argument
    theparser.add_argument(
        "--list_unconnected_nodes",
        action="store_true",  # https://stackoverflow.com/a/5271692/1164295
        help="list nodes that have no edges",
    )

    # optional argument
    theparser.add_argument(
        "--shortest_path",
        nargs=2,
        metavar=(
            "start_node_name",
            "end_node_name",
        ),  # https://stackoverflow.com/a/43660050/1164295
        help="shortest path between two nodes",
    )

    arguments = theparser.parse_args()

    return arguments


if __name__ == "__main__":

    arguments = args()
    # print("filename=",arguments.dotfilename)

    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pydot.read_dot.html
    G = nx.DiGraph(nx.nx_pydot.read_dot(arguments.dotfilename))

    if arguments.list_all_nodes:
        # print("all nodes:")
        for this_node in G.nodes:
            print(this_node)

    if arguments.list_start_nodes:
        for this_node in G.nodes:
            list_of_predecessors = G.predecessors(this_node)
            list_of_successors = G.successors(this_node)
            if ((len(list_of_predecessors)==0) and (len(list_of_successors)>0)):
                print(this_node)

    if arguments.list_end_nodes:
        for this_node in G.nodes:
            list_of_predecessors = G.predecessors(this_node)
            list_of_successors = G.successors(this_node)
            if ((len(list_of_predecessors)>0) and (len(list_of_successors)==0)):
                print(this_node)

    if arguments.list_unconnected_nodes:
        for this_node in G.nodes:
            list_of_predecessors = G.predecessors(this_node)
            list_of_successors = G.successors(this_node)
            if ((len(list_of_predecessors)==0) and (len(list_of_successors)==0)):
                print(this_node)

    if arguments.list_all_neighbors:
        print(
            "neighbors of "
            + arguments.list_all_neighbors[0]
            + " to depth "
            + arguments.list_all_neighbors[1]
            + ":"
        )
        # print(list(nx.all_neighbors(G, arguments.list_all_neighbors[0])))
        # for this_node in G.predecessors(arguments.list_all_neighbors[0]):
        # 	print(this_node+" -> "+arguments.list_all_neighbors[0])
        # for this_node in G.successors(arguments.list_all_neighbors[0]):
        # 	print(arguments.list_all_neighbors[0]+" -> "+this_node)
        recursive_predecessors(
            G,
            "",
            arguments.list_all_neighbors[0],
            int(arguments.list_all_neighbors[1]),
            1,
        )
        recursive_successors(
            G,
            "",
            arguments.list_all_neighbors[0],
            int(arguments.list_all_neighbors[1]),
            1,
        )

    # https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.predecessors.html
    if arguments.list_upstream:
        print(
            "upstream neighbors of "
            + arguments.list_upstream[0]
            + " to depth "
            + arguments.list_upstream[1]
            + ":"
        )
        # print(list(G.predecessors(arguments.list_upstream[0])))
        # for this_node in G.predecessors(arguments.list_upstream[0]):
        # 	print(this_node+" -> "+arguments.list_upstream[0])
        recursive_predecessors(
            G, "", arguments.list_upstream[0], int(arguments.list_upstream[1]), 1
        )

    # https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.successors.html#networkx.DiGraph.successors
    if arguments.list_downstream:
        print(
            "downstream neighbors of "
            + arguments.list_downstream[0]
            + " to depth "
            + arguments.list_downstream[1]
            + ":"
        )
        # not recursive:
        # print(list(G.successors(arguments.list_downstream[0])))

        # brute force
        # for nearest_node in G.successors(arguments.list_downstream[0]):
        # 	print("depth=1: "+arguments.list_downstream[0]+" -> "+nearest_node)
        # 	if arguments.list_downstream[1]>2:
        # 		for next_nearest_node in G.successors(nearest_node):
        # 			print("depth=2: "+arguments.list_downstream[0]+" -> "+nearest_node+" -> "+next_nearest_node)
        # 			if arguments.list_downstream[1]>3:
        # 				for next_next_nearest_node in G.successors(next_nearest_node):
        # 					print("depth=3: "+arguments.list_downstream[0]+" -> "+nearest_node+" -> "+next_nearest_node+" -> "+next_next_nearest_node)

        recursive_successors(
            G, "", arguments.list_downstream[0], int(arguments.list_downstream[1]), 1
        )

    if arguments.shortest_path:
        try:
            path = nx.shortest_path(
                G, arguments.shortest_path[0], arguments.shortest_path[1]
            )
            print(path)
        except nx.exception.NetworkXNoPath as e:
            print("\n")
            print(e)
            print("Try reversing the order of the nodes. Directionality matters.")

    # print([n for n in G.predecessors('a1')])
