import numpy as np
import re
import random
import string


def random_name(n=15):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return ''.join(randlst)


def get_node_ids(g):
    return list(g.nodes)


def get_node_contents(g):
    return [g.nodes[name]["node_name"] for name in get_node_ids(g)]


def search_target_word(content_array, search_word):
    found_nums = np.where(content_array == search_word)[0]
    return found_nums


def search_target_word_re(content_array, search_word, prompt_mode=False):
    id_list = []
    for num, content in enumerate(content_array):
        for lines in content.split("\n"):
            res = re.match(search_word, lines)
            if res is not None:
                if prompt_mode:
                    return num
                id_list.append(num)
                break

    return np.array(id_list)
