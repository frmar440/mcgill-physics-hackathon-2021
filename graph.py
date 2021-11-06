import networkx as nx
import matplotlib.pyplot as plt


def graph(recursive_depth=0, binary_label=""):
    G = nx.DiGraph()
    print(f"Current position in tree: {recursive_depth}{binary_label}")
    component = input("Component to add: ")

    if component == "A":
        recursive_depth_next = recursive_depth + 1

        G.add_node(f"{recursive_depth}{binary_label}")

        binary_label_up = binary_label + "1"
        H_up = graph(recursive_depth_next, binary_label_up)
        G.add_nodes_from(H_up)
        G.add_edges_from(H_up.edges)
        G.add_edge(f"{recursive_depth}{binary_label}", f"{recursive_depth_next}{binary_label_up}")

        binary_label_down = binary_label + "0"
        H_down = graph(recursive_depth_next, binary_label_down)
        G.add_nodes_from(H_down)
        G.add_edges_from(H_down.edges)
        G.add_edge(f"{recursive_depth}{binary_label}", f"{recursive_depth_next}{binary_label_down}")

    if component == "D":

        G.add_node(f"{recursive_depth}{binary_label}")

    return G