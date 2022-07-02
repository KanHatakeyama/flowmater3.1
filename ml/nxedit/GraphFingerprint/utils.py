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


def get_fp_key(fp_g: nx.DiGraph, node_id: str):
    val = fp_g.nodes[node_id]["node_name"]

    # in_node_names = sorted([node_id_to_name[i]
    #                        for i in list(fp_g.predecessors(node_id))])
    in_node_names = sorted([fp_g.nodes[i]["node_name"]
                            for i in list(fp_g.predecessors(node_id))])

    # out_node_names = sorted([node_id_to_name[i]
    #                         for i in list(fp_g.successors(node_id))])
    out_node_names = sorted([fp_g.nodes[i]["node_name"]
                             for i in list(fp_g.successors(node_id))])

    fp_key = val
    if len(in_node_names) > 0:
        fp_key += "-i-["+":".join(in_node_names)+"]"
    if len(out_node_names) > 0:
        fp_key += "-o-["+":".join(out_node_names)+"]"

    return fp_key


def get_node_id_with_fp_key(g: nx.DiGraph, target_fp_key: str):
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
        fp_key = get_fp_key(fp_g, node_id)
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
