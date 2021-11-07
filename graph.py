import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt
from physics import spinor, analyzer
from itertools import chain


class dict_add(dict):
    def __add__(self, other):
        dico = {}
        for key, val in chain(self.items(), other.items()):
            dico[key] = val
        return dict_add(dico)


def graph(recursive_depth=0, binary_label=""):
    G = nx.DiGraph()
    dico = dict_add({})
    print(f"current position in tree: {recursive_depth}{binary_label}")
    component = input("Component to add: ")

    node_id = f"{recursive_depth}{binary_label}"

    if component == "A":
        theta = float(input("theta (as a fraction of pi): "))*np.pi
        phi = float(input("phi (as a fraction of pi): "))*np.pi
        orientation = (theta, phi)
        recursive_depth_next = recursive_depth + 1

        G.add_node(node_id)
        dico[node_id] = orientation

        binary_label_up = binary_label + "1"
        H_up, dico_up = graph(recursive_depth_next, binary_label_up)
        G.add_nodes_from(H_up)
        G.add_edges_from(H_up.edges)
        G.add_edge(node_id, f"{recursive_depth_next}{binary_label_up}")
        dico += dico_up

        binary_label_down = binary_label + "0"
        H_down, dico_down = graph(recursive_depth_next, binary_label_down)
        G.add_nodes_from(H_down)
        G.add_edges_from(H_down.edges)
        G.add_edge(node_id, f"{recursive_depth_next}{binary_label_down}")
        dico += dico_down

    if component == "D":

        G.add_node(node_id)

    return G, dico


def local_computation(spinor, P_in, G, dico_orientation, node_id="0"):
    dico_probability = dict_add({})
    orientation = dico_orientation.get(node_id)

    if not orientation:
        dico_probability[node_id] = P_in

    for node_id in G.succ[node_id]:
        output = analyzer(spinor, orientation, P_in)
        if node_id[-1] == "1":
            dico_probability += local_computation(*output["up"], G, dico_orientation, node_id)
        if node_id[-1] == "0":
            dico_probability += local_computation(*output["down"], G, dico_orientation, node_id)

    return dico_probability


def build_json(spinor=(1,0)):
    G, dico_orientation = graph()
    dico_probability = local_computation(spinor, 1, G, dico_orientation)
    data = dico_orientation + dico_probability
    for n in G:
        G.nodes[n]["display"] = str(data[n])
        if isinstance(data[n], tuple):
            G.nodes[n]["type"] = "A"
        elif isinstance(data[n], float):
            G.nodes[n]["type"] = "D"
    # write json formatted data
    d = nx.json_graph.node_link_data(G)  # node-link format to serialize
    # write json
    json.dump(d, open("force/force.json", "w"))