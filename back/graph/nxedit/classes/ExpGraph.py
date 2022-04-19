import networkx as nx
import numpy as np
from ..basic_utils import get_node_contents, get_node_ids, search_target_word_re, random_name
from ..graph_checker.analyze_tips import search_start_end_nodes
from ..integrator.string_parser import parse_command
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

    def delete_memo_nodes(self):
        self.delete_nodes_regex(target=".*\[Memo\]")

    def delete_file_nodes(self):
        self.delete_nodes_regex(target="file .*")

    def delete_nodes_regex(self, target: str):

        del_flag = False
        # search for target nodes, which should be deleted for ML
        memo_node_nums = search_target_word_re(
            self.content_array, target)

        for target_num in memo_node_nums:
            self.g.remove_node(self.node_array[target_num])
            del_flag = True

        if del_flag:
            self.update_info()

    def attribute_val_nodes(self):

        # search for property nodes (e.g., volume=10 mL)
        while True:
            node_num = search_target_word_re(self.content_array, ".*=", True)
            if type(node_num) is not int:
                break
            node_id = self.node_array[node_num]
            g = self.g

            target_node = node_id

            content_list = g.nodes[node_id]["node_name"].split("\n")

            for exception_word in ["SMILES", "file"]:
                for content in list(content_list):
                    if content.startswith(exception_word):
                        content_list.remove(content)

            non_colon_content_list = [
                i for i in content_list if i.find("=") < 0]

            if len(non_colon_content_list) == 0:
                target_node = list(g.successors(node_id))[0]

            # add nodes and edges to express numeric variables
            for content in list(content_list):
                continue_flag = False
                if content.find("=") < 0:
                    continue_flag = True

                if continue_flag:
                    continue

                content_list.remove(content)

                # parse line
                title, prop, unit = parse_command(content)

                # add new nodes
                title_node = random_name()+"_title"
                prop_node = random_name()+"_prop"
                unit_node = random_name()+"_unit"

                g.add_node(title_node, node_name=title)
                g.add_edge(title_node, target_node)

                g.add_node(prop_node, node_name=prop)
                g.add_edge(prop_node, title_node)

                if unit != "":
                    g.add_node(unit_node, node_name=unit)
                    g.add_edge(unit_node, prop_node)

            if len(content_list) == 0:
                g.remove_node(node_id)
            else:
                g.nodes[node_id]["node_name"] = "\n".join(content_list)

            self.update_info()
