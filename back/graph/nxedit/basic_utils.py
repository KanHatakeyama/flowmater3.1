import numpy as np
import re


def get_node_ids(g):
    return list(g.nodes)


def get_node_contents(g):
    return [g.nodes[name]["node_name"] for name in get_node_ids(g)]


def search_target_word(content_array, search_word):
    found_nums = np.where(content_array == search_word)[0]
    return found_nums


def search_target_word_re(content_array, search_word):
    id_list = []
    for num, content in enumerate(content_array):
        res = re.match(search_word, content)
        if res is not None:
            id_list.append(num)

    return np.array(id_list)
