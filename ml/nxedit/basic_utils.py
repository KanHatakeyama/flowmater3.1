import numpy as np
import re
import random
import string
import networkx as nx


def random_name(n: int = 15, prefix: str = "TASK_"):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return prefix+''.join(randlst)


def get_node_ids(g: nx.DiGraph):
    return list(g.nodes)


def get_node_contents(g: nx.DiGraph):
    return [g.nodes[name]["node_name"] for name in get_node_ids(g)]


def search_target_word(content_array: np.array, search_word: str):
    found_nums = np.where(content_array == search_word)[0]
    return found_nums


def search_target_word_re(content_array: np.array, search_word: str,
                          prompt_mode=False,
                          exception_lines=[""]):
    id_list = []
    for num, content in enumerate(content_array):
        for line in content.split("\n"):
            if line in exception_lines:
                continue

            res = re.match(search_word, line)

            if res is not None:

                # return only one
                if prompt_mode:
                    return num

                id_list.append(num)
                break

    return np.array(id_list)
