from xml.etree.ElementTree import Element, SubElement, ElementTree


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
