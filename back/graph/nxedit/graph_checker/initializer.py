import networkx as nx


def claify_compounds(g: nx.DiGraph):
    for node in g.nodes:
        g.nodes[node]["node_name"] = g.nodes[node]["node_name"].replace(
            "SMILES=", "Compound\nSMILES=")
