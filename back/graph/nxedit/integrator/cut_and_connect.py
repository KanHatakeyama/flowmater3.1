import copy
import networkx as nx
from ..ExpGraph import ExpGraph
from .. ExpManager import ExpManager


def load_another_graph(command_id: int, pk: int, exp: ExpGraph,  manager: ExpManager):

    load_command = exp.load_commands[command_id]

    # load command must be in the first line
    load_pk = int(load_command[5:].split("_")[0])

    if load_pk == pk:
        raise ValueError("self-referencing the graph! pk: ", pk)

    # another commands (2nd lines~)
    additional_commands = load_command.split("\n")[1:]

    # load son experiment
    son_exp = manager.exp_dict[load_pk]["exp"]

    # get sun graph to be connected (w/o "start" and "end" nodes)
    son_g, son_start_node, son_end_node = cut_son_graphs(son_exp)

    # get connections from/to the "load" node
    parent_g = exp.g
    parent_load_node = exp.load_nodes[command_id]
    parent_load_starts = list(parent_g.predecessors(parent_load_node))
    parent_load_ends = list(parent_g.successors(parent_load_node))

    # integrate son_graph
    integ_g = copy.deepcopy(nx.compose(parent_g, son_g))

    # connect graphs
    for parent_load_start in parent_load_starts:
        integ_g.add_edge(parent_load_start, son_start_node)

    for parent_load_end in parent_load_ends:
        integ_g.add_edge(son_end_node, parent_load_end)

    # remove "load" node
    integ_g.remove_node(parent_load_node)

    # write other commands in the original load node
    son_commands = integ_g.nodes[son_start_node]["node_name"].split("\n")
    son_commands.extend(additional_commands)
    integ_g.nodes[son_start_node]["node_name"] = "\n".join(son_commands)

    exp.g = integ_g


def cut_son_graphs(son_exp: ExpGraph):
    son_g = copy.deepcopy(son_exp.g)

    # end of son node (excluding the actural "end" node)
    son_end_node = list(son_g.predecessors(son_exp.end_node))[0]
    # start of son
    son_start_node = list(son_g.successors(son_exp.start_node))[0]

    # delete "start" and "end" nodes in the son
    son_g.remove_node(son_exp.end_node)
    son_g.remove_node(son_exp.start_node)

    return son_g, son_start_node, son_end_node
