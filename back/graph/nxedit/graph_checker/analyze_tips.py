from ..basic_utils import random_name, search_target_word
import networkx as nx
from ..basic_utils random_name


def search_start_end_nodes(g: nx.DiGraph, node_array, content_array):
    """
    search start and end nodes in a graph
    """

    start_num, end_num = search_tips(content_array)
    start_node = node_array[start_num]

    # if end node is not defined clearly, add  it
    if end_num == -1:
        # search for the tip node in the directed graph
        tip_node = [x for x in g.nodes() if g.out_degree(x) == 0]

        if len(tip_node) != 1:
            raise ValueError("you should clarify the end node")

        end_node = "end_"+random_name(15)
        g.add_node(end_node, node_name='end')
        g.add_edge(tip_node[0], end_node)

    return start_node, end_node


def search_tips(content_array):
    """
    manually search "start" and "end" nodes
    """

    # raise error if there are multiple starts or no start
    startnums = search_target_word(content_array, "start")
    if startnums.shape[0] != 1:
        raise ValueError("'start' should be only one")

    startnum = startnums[0]

    # raise error if there are more than two ends
    endnums = search_target_word(content_array, "end")
    if endnums.shape[0] >= 2:
        raise ValueError("'end' should be only one")

    # in a graph, "end" node can be abbreviated. if so, the endnum will be -1
    if endnums.shape[0] == 0:
        endnum = -1
    else:
        endnum = endnums[0]

    return startnum, endnum
