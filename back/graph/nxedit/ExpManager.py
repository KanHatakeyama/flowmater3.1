import json
import bpmn_python.bpmn_diagram_rep as diagram
import io
from .ExpGraph import ExpGraph


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
            #data["bpmn"] = record["graph"]

            # parse bpmn data
            bpmn_graph = diagram.BpmnDiagramGraph()
            bpmn_graph.load_diagram_from_xml_file(io.StringIO(record["graph"]))
            data["bpmn"] = bpmn_graph
            exp = ExpGraph(bpmn_graph.diagram_graph)
            data["exp"] = exp

            self.exp_dict[record["id"]] = data
