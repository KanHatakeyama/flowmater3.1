import json
import bpmn_python.bpmn_diagram_rep as diagram
import io
from .ExpGraph import ExpGraph
from ..integrator.cut_and_connect import load_another_graph
from ..integrator.duplicator import check_commas
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
            bpmn_graph.load_diagram_from_xml_file(io.StringIO(record["graph"]))
            data["bpmn"] = bpmn_graph

            # initialize nx graph object
            exp = ExpGraph(bpmn_graph.diagram_graph)
            data["exp"] = exp

            self.exp_dict[str(record["id"])] = data

        self._load_son_graphs()
        self._delete_memo_nodes()
        self._delete_file_nodes()
        self._attibute_val_nodes()
        self._duplicate_graphs_with_comma()

    def _load_son_graphs(self):
        # load son graphs according to "load ****" command
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]

            for _ in range(MAX_NEST_GRAPH+1):
                # load
                load_commands = list(exp.load_commands)
                if load_commands == 0:
                    break

                for i in range(len(load_commands)):
                    load_another_graph(i, pk, exp, self)
                exp.update_info()

            if len(load_commands) > 0:
                raise ValueError(
                    "Too many nesting of graphs! over ", MAX_NEST_GRAPH)

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

    def _duplicate_graphs_with_comma(self):

        for pk in list(self.exp_dict):
            record = self.exp_dict[pk]
            exp = record["exp"]

            n_comma, comma_dict = check_commas(exp)

            if n_comma == 0:
                return

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
