from pyvis.network import Network
import networkx as nx


def save_graph_html(g: nx.DiGraph, save_path="flowchart.html"):
    pyvis_g = Network(directed=True)
    for i in g.nodes:
        pyvis_g.add_node(i, label=g.nodes[i]["node_name"])

    for i, j in list(g.edges):
        pyvis_g.add_edge(i, j)

    pyvis_g.save_graph(save_path)
