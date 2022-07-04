import networkx as nx
import copy
from .utils import fill_numbers,  NUM_CHAR, search_for_target_node_name_id
from .utils import get_fp_key_pre_suc, get_fp_key_pre_suc_k
from tqdm import tqdm


class GraphFingerprint:
    def __init__(self, g_list: list, fp_key_algorithm=get_fp_key_pre_suc_k):
        self.key_list = []
        self.g_list = g_list
        self.fp_key_algorithm = fp_key_algorithm

        self.add_keys()
        self.key_list = sorted(self.key_list)
        self._init_fp_template()

    def add_keys(self):
        for g in (self.g_list):
            fp_g = copy.deepcopy(g)
            fill_numbers(fp_g)
            for node_id in (fp_g.nodes):
                fp_key = self.fp_key_algorithm(fp_g, node_id)

                if fp_key not in self.key_list:
                    self.key_list.append(fp_key)

    def _init_fp_template(self):
        fp = {}
        for key in self.key_list:
            if key.startswith(NUM_CHAR):
                fp[key] = None
            else:
                fp[key] = 0

        self._fp_template = fp

    def __call__(self, g: nx.DiGraph):
        return self.calc_fingerprint(g)

    def calc_fingerprint(self, g: nx.DiGraph):
        """
        calc FP
        if multiple nodes are available with numeric vals, use the one which is the closest to the "end" node
        """

        fp_g = copy.deepcopy(g)
        fill_numbers(fp_g)
        fp = copy.deepcopy(self._fp_template)

        # check for duplicates
        dup_dict = {}

        end_node_id = search_for_target_node_name_id(g, node_name="end")

        for node_id in fp_g.nodes:
            fp_key = self.fp_key_algorithm(fp_g, node_id)
            node_val = fp_g.nodes[node_id]["node_name"]

            if node_val == NUM_CHAR:
                val = float(g.nodes[node_id]["node_name"])

                # calc distance between the node and "end" node
                distance = len(nx.shortest_path(
                    g, source=node_id, target=end_node_id))

                # check for duplicated fps
                if fp_key in dup_dict:
                    #print("dup", fp_key, distance)
                    # use the node val with smaller distance to the "end" node
                    if distance < dup_dict[fp_key]:
                        dup_dict[fp_key] = distance
                        fp[fp_key] = val
                        # print("updated")

                else:
                    # first occurence
                    fp[fp_key] = val
                    dup_dict[fp_key] = distance

            else:
                fp[fp_key] = 1

        sorted_fp_as_list = sorted(fp.items())
        out_fp = [i[1] for i in sorted_fp_as_list]

        return out_fp
