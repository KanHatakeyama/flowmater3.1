from turtle import color
from pyvis.network import Network
import networkx as nx


def save_graph_html(g: nx.DiGraph, save_path="flowchart.html", color_dict={}):
    pyvis_g = Network(directed=True, notebook=True)
    for i in g.nodes:
        if i in color_dict:
            color = color_dict[i]
        else:
            color = None
        pyvis_g.add_node(i, label=g.nodes[i]["node_name"], color=color)

    for i, j in list(g.edges):
        pyvis_g.add_edge(i, j)

    return pyvis_g.save_graph(save_path)
