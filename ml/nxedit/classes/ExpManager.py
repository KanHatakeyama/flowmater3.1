import json
import bpmn_python.bpmn_diagram_rep as diagram
import io
from .ExpGraph import ExpGraph
from ..integrator.cut_and_connect import load_another_graph
from ..integrator.duplicator import check_splits
from ..graph_checker.protect_nodes import protect_node_characters
import copy

MAX_NEST_GRAPH = 4


class ExpManager:
    def __init__(self, dump_path="dump.json"):
        self.dump_path = dump_path
        self._initialize()

    def _initialize(self):
        # load dump json data
        with open(self.dump_path) as f:
            record_list = json.load(f)

        self.exp_dict = {}

        for record in record_list:
            data = {}
            data["title"] = record["title"]
            data["tags"] = record["tags"]

            # parse bpmn data
            bpmn_graph = diagram.BpmnDiagramGraph()
            try:
                bpmn_graph.load_diagram_from_xml_file(
                    io.StringIO(record["graph"]))
            except:
                print("error parsing bpmn ", record["title"])
                continue
            data["bpmn"] = bpmn_graph

            # initialize nx graph object
            try:
                exp = ExpGraph(bpmn_graph.diagram_graph)
            except Exception as e:
                print("error", e, record["title"])
                #print("error", e, record)
                continue
                #raise ValueError("error parsing ", record)
            data["exp"] = exp

            self.exp_dict[str(record["id"])] = data

        # replace "=" and "," of non-property lines with random characters
        self._protect_words(protect_mode=True)

        self._load_son_graphs()
        self._delete_memo_nodes()
        self._delete_file_nodes()
        self._attibute_val_nodes()
        self._duplicate_graphs_with_comma()

        self._protect_words(protect_mode=False)

    def _protect_words(self, protect_mode=True):
        for pk in list(self.exp_dict):
            g = self.exp_dict[pk]["exp"].g
            protect_node_characters(g, protect_mode=protect_mode)

    def _load_son_graphs(self):
        # load son graphs according to "load ****" command
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]

            for _ in range(MAX_NEST_GRAPH+1):
                # load
                while True:
                    load_commands = list(exp.load_commands)
                    if len(load_commands) == 0:
                        break

                    # for i in range(len(load_commands)):
                    #    load_another_graph(i, pk, exp, self)
                    try:
                        load_another_graph(0, pk, exp, self)
                    except Exception as e:
                        print("caution! error, parsing",
                              pk, exp, "error position: ", e, load_commands)
                        break
                    exp.update_info()

            if len(load_commands) > 0:
                print("caution! too many nesting over ", MAX_NEST_GRAPH, pk)
                break
                # raise ValueError(
                #    "Too many nesting of graphs! over ", MAX_NEST_GRAPH)

    def _delete_memo_nodes(self):
        self._delete_nodes_regex(target=".*\[Memo\]")

    def _delete_file_nodes(self):
        self._delete_nodes_regex(target="file .*")

    def _delete_nodes_regex(self, target: str):
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]
            exp.delete_nodes_regex(target)

    def _attibute_val_nodes(self):
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]
            exp.attribute_val_nodes()

    def _clean_nodes(self):
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]
            exp.clean_node_info()

    def _duplicate_graphs_with_comma(self):

        for pk in list(self.exp_dict):
            record = self.exp_dict[pk]
            exp = record["exp"]

            n_comma, comma_dict = check_splits(exp)

            #print(pk, n_comma, comma_dict)
            if n_comma == 0:
                # return
                continue

            # duplicate records
            for i in range(n_comma+1):
                dup_record = copy.deepcopy(record)
                for node_id in comma_dict:
                    dup_record["exp"].g.nodes[node_id]["node_name"] = comma_dict[node_id][i]

                dup_record["exp"].update_info()
                dup_record["title"] += f"_{i}"
                self.exp_dict[pk+f"_{i}"] = dup_record

            # delete original one
            self.exp_dict.pop(pk)
