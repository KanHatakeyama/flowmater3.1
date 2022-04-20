import networkx as nx

ESCAPE_EQUAL = "ue3dV8eO3NG45hiU"
ESCAPE_COMMA = "0iC565y7Ixpnh6PB"


def protect_node_characters(g: nx.DiGraph, protect_mode=True, exception_list=["SMILES=", "file "]):

    for node_id in g.nodes:
        content = g.nodes[node_id]["node_name"]
        modif_lines = []
        for line in content.split("\n"):

            # protect
            for exception_word in exception_list:
                if protect_mode:
                    if line.startswith(exception_word):
                        line = line[:len(exception_word)] + \
                            line[len(exception_word):].replace(
                                "=", ESCAPE_EQUAL)

                        break

            # deprotect
            if not protect_mode:
                line = line.replace(ESCAPE_EQUAL, "=")

            # protect comma
            if line.find("=") < 0:
                if protect_mode:
                    line = line.replace(",", ESCAPE_COMMA)
                else:
                    line = line.replace(ESCAPE_COMMA, ",")

            modif_lines.append(line)

        g.nodes[node_id]["node_name"] = "\n".join(modif_lines)
