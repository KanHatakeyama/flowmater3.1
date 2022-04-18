import numpy as np


def get_node_ids(g):
    return list(g.nodes)


def get_node_contents(g):
    return [g.nodes[name]["node_name"] for name in get_node_ids(g)]


def search_target_word(content_array, search_word="start"):
    found_ids = np.where(content_array == search_word)[0]
    return found_ids
