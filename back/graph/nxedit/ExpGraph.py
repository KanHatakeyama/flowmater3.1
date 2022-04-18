import networkx as nx
import numpy as np
from .basic_utils import get_node_contents, get_node_ids, search_target_word_re
from .graph_checker.analyze_tips import search_start_end_nodes
import copy


class ExpGraph:
    def __init__(self, g: nx.DiGraph):
        self.g = copy.deepcopy(g)
        self._update_contents()
        self._initial_check()
        self.update_info()

    def _update_contents(self):
        self.content_array = np.array(get_node_contents(self.g))
        self.node_array = np.array(get_node_ids(self.g))

    def _initial_check(self):

        # check if all nodes are connected
        if not nx.is_tree(self.g):
            raise ValueError("all nodes must be connected in a graph")

        # check start and end nodes
        self.start_node, self.end_node = search_start_end_nodes(
            self.g, self.node_array, self.content_array)

    def update_info(self):
        self._update_contents()
        # search "load" labels
        self.load_node_nums = search_target_word_re(
            self.content_array, "^load")
        self.load_nodes = [self.node_array[n] for n in self.load_node_nums]

        self.load_commands = [self.content_array[n]
                              for n in self.load_node_nums]
