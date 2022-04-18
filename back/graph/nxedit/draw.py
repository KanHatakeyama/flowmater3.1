from pyvis.network import Network


def save_graph_html(fc_g, save_path="flowchart.html"):
    pyvis_g = Network(directed=True)
    for i in fc_g.nodes:
        pyvis_g.add_node(i, label=fc_g.nodes[i]["node_name"])

    for i, j in list(fc_g.edges):
        pyvis_g.add_edge(i, j)
