from xml.etree.ElementTree import Element, SubElement, ElementTree
from networkx.drawing.nx_agraph import graphviz_layout


def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))


def save_root_as_xml(root, file_path):
    _pretty_print(root)

    tree = ElementTree(root)

    with open(file_path, "wb") as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)


def calc_tree_pos(g,
                  SCALE=5*10**-2,
                  width=100,
                  height=80,
                  y_ratio=1.5,
                  ):

    # plt.figure(figsize=(10,15))
    original_pos = graphviz_layout(
        g, prog='dot', root=0, args='-Grankdir="LR" -Gnodesep=1 -Nshape="box" -Granksep=2 -Gsplines="ortho" ')

    # modify overlaps (nor perfect)
    modif_pos = {}
    for k, v in original_pos.items():
        modif_pos[k] = (((v[0]*SCALE)), ((v[1]*SCALE*1.5)))

    def get_pos(modif_pos, node_id):
        x = modif_pos[node_id][0]
        y = modif_pos[node_id][1]
        return x, y

    for node_id in g.nodes:
        x, y = get_pos(modif_pos, node_id)
        for target_node_id in g.nodes:
            if node_id == target_node_id:
                continue

            tx, ty = get_pos(modif_pos, target_node_id)
            # check collision
            if x+width > tx and x < tx+width:
                if y+height > ty and y < ty+height:
                    modif_pos[target_node_id] = (tx, ty-height*y_ratio)

    pos = {}
    for k, v in modif_pos.items():
        pos[k] = (str(int(v[0])), str(int(v[1])))

    return pos
