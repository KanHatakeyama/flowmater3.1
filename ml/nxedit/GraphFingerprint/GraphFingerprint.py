import networkx as nx
import copy
from .utils import fill_numbers, get_fp_key, NUM_CHAR


class GraphFingerprint:
    def __init__(self, g_list: list):
        self.key_list = []
        self.g_list = g_list

        self.add_keys()
        self.key_list = sorted(self.key_list)
        self._init_fp_template()

    def add_keys(self):
        for g in self.g_list:
            fp_g = copy.deepcopy(g)
            fill_numbers(fp_g)
            for node_id in fp_g.nodes:
                fp_key = get_fp_key(fp_g, node_id)

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
        fp_g = copy.deepcopy(g)
        fill_numbers(fp_g)
        fp = copy.deepcopy(self._fp_template)

        for node_id in fp_g.nodes:
            fp_key = get_fp_key(fp_g, node_id)

            node_val = fp_g.nodes[node_id]["node_name"]

            if node_val == NUM_CHAR:
                fp[fp_key] = float(g.nodes[node_id]["node_name"])

            else:
                fp[fp_key] = 1

        sorted_fp_as_list = sorted(fp.items())
        out_fp = [i[1] for i in sorted_fp_as_list]

        return out_fp
