from ..basic_utils import search_target_word_re
from ..classes.ExpGraph import ExpGraph


def check_commas(exp: ExpGraph):
    """
    search for comma split nodes, indicating multiple experiments (e.g., 10,20,30)

    Parameters
    ----------
    exp: ExpGraph
        Experiment

    Returns
    -------
    n_comma: int
        number of commas in nodes in a graph
    comma_dict: dict
        node id and its content split by comma
        e.g., {'zDxBlSOaemBcEb6_prop': ['10', '20', '60'], 'CWOtmNOzi7KtOwe_prop': ['90', '60', '70']}    
    """

    comma_nodes_nums = search_target_word_re(exp.content_array, ".*,")

    n_comma_list = []
    comma_dict = {}
    for node_num in comma_nodes_nums:
        content = exp.content_array[node_num]
        n_comma = content.count(",")
        n_comma_list.append(n_comma)
        comma_dict[exp.node_array[node_num]] = content.split(",")

    # if number of commas are different in a graph, raise error
    if len(list(set(n_comma_list))) != 1 and len(n_comma_list) != 0:
        raise ValueError(
            "number of commas (,) in nodes must be the same in a graph!", comma_dict)

    if len(n_comma_list) == 0:
        n_comma = 0
        return (n_comma, None)

    return (n_comma, comma_dict)
