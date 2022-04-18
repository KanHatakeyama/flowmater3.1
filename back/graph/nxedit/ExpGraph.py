import networkx as nx
import numpy as np
from .basic_utils import get_node_contents, get_node_ids
from .graph_checker.analyze_tips import search_start_end_nodes


class ExpGraph:
    def __init__(self, g: nx.DiGraph):
        self.g = g

        self.content_array = np.array(get_node_contents(g))
        self.node_array = np.array(get_node_ids(g))

        self._initialize()

    def _initialize(self):

        # check if all nodes are connected
        if not nx.is_tree(self.g):
            raise ValueError("all nodes must be connected in a graph")

        # check start and end nodes
        self.start_node, self.end_node = search_start_end_nodes(
            self.g, self.node_array, self.content_array)