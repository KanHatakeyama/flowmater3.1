import json
import bpmn_python.bpmn_diagram_rep as diagram
import io
from .ExpGraph import ExpGraph
from .integrator.cut_and_connect import load_another_graph

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

            self.exp_dict[int(record["id"])] = data

        self._load_son_graphs()

    def _load_son_graphs(self):
        # load son graphs according to "load ****" command
        for pk in list(self.exp_dict):
            exp = self.exp_dict[pk]["exp"]

            for nest_count in range(MAX_NEST_GRAPH+1):
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
