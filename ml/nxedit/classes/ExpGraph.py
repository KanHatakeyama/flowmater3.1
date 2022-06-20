import networkx as nx
import numpy as np
from ..basic_utils import get_node_contents, get_node_ids, search_target_word_re, random_name
from ..graph_checker.analyze_tips import search_start_end_nodes
from .. graph_checker.initializer import claify_compounds
from ..integrator.string_parser import parse_command, clean_line
from ..draw import save_graph_html
import copy


class ExpGraph:
    def __init__(self, g: nx.DiGraph):
        self.g = copy.deepcopy(g)
        claify_compounds(self.g)
        self._update_contents()
        self._initial_check()
        self.update_info()

    def _update_contents(self):
        self.content_array = np.array(get_node_contents(self.g))
        self.node_array = np.array(get_node_ids(self.g))

    def _initial_check(self):

        # check if all nodes are connected
        if not nx.is_weakly_connected(self.g):
            save_graph_html(self.g, save_path="error.html")
            raise ValueError("all nodes must be connected in a graph")

        if not nx.is_tree(self.g):
            save_graph_html(self.g, save_path="error.html")
            raise ValueError("graphs should not have cycles!")

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

    def relabel(self):
        """
        relabel node ids
        """
        original_node_ids = self.node_array
        modif_dict = {i: i+"_"+random_name() for i in original_node_ids}
        self.g = nx.relabel_nodes(self.g, modif_dict)

        self._update_contents()
        self._initial_check()
        self.update_info()

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

    def clean_node_info(self):
        g = self.g

        is_changed = False
        for node_id in g.nodes:
            content = g.nodes[node_id]["node_name"]

            clean_content = clean_line(content)
            if content != clean_content:
                g.nodes[node_id]["node_name"] = clean_content
                is_changed = True

        if is_changed:
            self.update_info()

    def attribute_val_nodes(self):
        #exception_lines = []
        # search for property nodes or smiles nodes (e.g., volume=10 mL)
        while True:
            node_num = search_target_word_re(
                self.content_array, ".*=", prompt_mode=True)
            # self.content_array, ".*=", prompt_mode=True)

            # smiles_node_num = search_target_word_re(
            #    self.content_array, "^SMILES ", prompt_mode=True)

            # if type(smiles_node_num)

            if type(node_num) is not int:
                break

            node_id = self.node_array[node_num]
            g = self.g

            target_node = node_id

            content_list = g.nodes[node_id]["node_name"].split("\n")
            content_list = [i for i in content_list if i not in [""]]

            non_colon_content_list = [
                #    i for i in content_list if (i.find("=") < 0 and not i.startswith("SMILES "))]
                i for i in content_list if i.find("=") < 0]

            # smiles can be a single node
            # if len(content_list) == 1:
            #    if content_list[0].startswith("SMILES "):
            #        non_colon_content_list = content_list
            #        exception_lines.append(content_list[0])

            if len(non_colon_content_list) == 0:
                target_node = list(g.successors(node_id))[0]

            # print("c", content_list, "non",
            #      non_colon_content_list, "target", target_node)
            # add nodes and edges to express numeric variables
            for content in list(content_list):
                continue_flag = False
                # if content.find("=") < 0 and not content.startswith("SMILES "):
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
