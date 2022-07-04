import networkx as nx
import copy
NUM_CHAR = "*NUM"


def fill_numbers(fp_g: nx.DiGraph):
    for node_id in fp_g.nodes:
        val = fp_g.nodes[node_id]["node_name"]

        # convert numbers into "number"
        try:
            val = float(val)
            val = NUM_CHAR
        except:
            pass

        fp_g.nodes[node_id]["node_name"] = val.replace("\n", "+")


def get_fp_key_pre_suc(fp_g: nx.digraph, node_id: str):
    """
    calc fp key according to the "node_name" of the target node and neighboring nodes
    """
    val = fp_g.nodes[node_id]["node_name"]

    in_node_names = sorted([fp_g.nodes[i]["node_name"]
                            for i in list(fp_g.predecessors(node_id))])

    out_node_names = sorted([fp_g.nodes[i]["node_name"]
                             for i in list(fp_g.successors(node_id))])

    fp_key = val
    if len(in_node_names) > 0:
        fp_key += "-i-["+":".join(in_node_names)+"]"
    if len(out_node_names) > 0:
        fp_key += "-o-["+":".join(out_node_names)+"]"

    return fp_key


def get_fp_key_pre_suc_k(fp_g: nx.digraph, node_id: str, k=3):
    """
    calc fp key according to the "node_name" of the target node and neighboring nodes (K=2)
    """
    val = fp_g.nodes[node_id]["node_name"]
    current_node_id = node_id

    for f, d in zip([fp_g.predecessors, fp_g.successors], ("b", "f")):

        #TODO: recursion
        for n_node in list(f(current_node_id)):
            val += f" 1{d}:"+fp_g.nodes[n_node]["node_name"]

            if k >= 2:
                for n_n_node in list(f(n_node)):
                    val += f" 2{d}:"+fp_g.nodes[n_n_node]["node_name"]

                    if k >= 3:
                        for n_n_n_node in list(f(n_n_node)):
                            val += f" 3{d}:" + \
                                fp_g.nodes[n_n_n_node]["node_name"]

    return val


# calc fp key according to K-neighbor node info
"""
def get_fp_key_K_neighbor(fp_g: nx.digraph, node_id: str, K=2):
    #very

    val = fp_g.nodes[node_id]["node_name"]+"|"
    name_dict = {}

    #r_fp_g = fp_g.reverse()
    # search for K-neighboring nodes
    for k in range(1, K + 1):
        # for g, d in zip([fp_g, r_fp_g], ("f", "r")):
        for g, d in zip([fp_g.to_undirected()], ("")):

            neighbor_ids = nx.single_source_shortest_path_length(
                g, node_id, cutoff=k)
            neighbor_ids = [n for (n, v) in neighbor_ids.items() if v == k]

            if len(neighbor_ids) > 0:
                add_keys = sorted([g.nodes[i]["node_name"]
                                   for i in neighbor_ids])
                add_keys = "-".join(add_keys)
            else:
                add_keys = "-"

            name_dict[f"{d}{k}"] = add_keys

    for k, v in name_dict.items():
        val += f" {k}: {v}"

    return val
"""


def get_node_id_with_fp_key(g: nx.DiGraph, target_fp_key: str, fp_class):
    """
    get node id having a specific fp_key. return a node which is nearest to the "end" node
    """

    fp_g = copy.deepcopy(g)
    fill_numbers(fp_g)

    end_node_id = search_for_target_node_name_id(g, node_name="end")

    final_node_id = None
    final_dist = 10**5

    #node_id_list = []
    for node_id in fp_g.nodes:
        fp_key = fp_class.fp_key_algorithm(fp_g, node_id)
        if fp_key == target_fp_key:
            # node_id_list.append(node_id)
            distance = len(nx.shortest_path(
                g, source=node_id, target=end_node_id))

            if distance < final_dist:
                final_node_id = node_id
                final_dist = distance
    return final_node_id
    # return node_id_list


def search_for_target_node_name_id(g: nx.DiGraph, node_name="end"):
    for k in g.nodes:
        if g.nodes[k]["node_name"] == node_name:
            return k

    raise ValueError(f"{node_name} not found in {g}")
