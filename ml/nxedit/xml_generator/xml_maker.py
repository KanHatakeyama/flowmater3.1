
from .utils import save_root_as_xml
from xml.etree.ElementTree import Element, SubElement, ElementTree


def graph_to_xml(g, pos, save_path):

    # header
    root = prepare_header()

    # main nodes
    process = Element("bpmn:process")

    # content
    root.append(process)
    process.set("id", "Process_1")
    process.set("isExecutable", "false")

    # view
    diagram = Element("bpmndi:BPMNDiagram")
    root.append(diagram)
    diagram.set("id", "BPMNDiagram_1")
    plane = Element("bpmndi:BPMNPlane")
    diagram.append(plane)
    plane.set("id", "BPMNPlane_1")
    plane.set("bpmnElement", "Process_1")

    for node_id in g.nodes:
        # node content
        content = g.nodes[node_id]["node_name"]

        task = Element("bpmn:task")
        process.append(task)
        task.set("id", node_id)
        task.set("name", content)

        from_nodes = list(g.predecessors(node_id))
        to_nodes = list(g.successors(node_id))

        # edge
        for from_node in from_nodes:
            # connect
            flow = Element("bpmn:sequenceFlow")
            process.append(flow)
            income = Element("bpmn:incoming")
            task.append(income)
            income.text = f"SequenceFlow-{from_node}:{node_id}"

            flow.set("id", f"SequenceFlow-{from_node}:{node_id}")
            flow.set("sourceRef", from_node)
            flow.set("targetRef", node_id)

            # view
            vedge = Element("bpmndi:BPMNEdge")
            plane.append(vedge)
            vedge.set("id", f"SequenceFlow-{from_node}:{node_id}_di")
            vedge.set("bpmnElement", f"SequenceFlow-{from_node}:{node_id}")
            way = Element("di:waypoint")
            vedge.append(way)
            way.set("x", pos[node_id][0])
            way.set("y", pos[node_id][1])

        for to_node in to_nodes:
            # connect
            flow = Element("bpmn:sequenceFlow")
            process.append(flow)
            outgo = Element("bpmn:outgoing")
            task.append(outgo)
            outgo.text = f"SequenceFlow-{node_id}:{to_node}"

            flow.set("id", f"SequenceFlow-{node_id}:{to_node}")
            flow.set("sourceRef", node_id)
            flow.set("targetRef", to_node)

            # view
            vedge = Element("bpmndi:BPMNEdge")
            plane.append(vedge)
            vedge.set("id", f"SequenceFlow-{node_id}:{to_node}_di")
            vedge.set("bpmnElement", f"SequenceFlow-{node_id}:{to_node}")
            way = Element("di:waypoint")
            vedge.append(way)
            way.set("x", pos[node_id][0])
            way.set("y", pos[node_id][1])

    # view
    for node_id in g.nodes:
        content = g.nodes[node_id]["node_name"]
        shape = Element("bpmndi:BPMNShape")
        plane.append(shape)
        shape.set("id", node_id+"_di")
        shape.set("bpmnElement", node_id)

        bounds = Element("dc:Bounds")
        shape.append(bounds)
        bounds.set("x", pos[node_id][0])
        bounds.set("y", pos[node_id][1])
        bounds.set("height", "80")
        bounds.set("width", "100")

    save_root_as_xml(root, save_path)


def prepare_header():

    root = Element("bpmn:definitions")

    # bpmn header
    header_dict = {
        "xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        "xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
        "xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:di": "http://www.omg.org/spec/DD/20100524/DI",
        "id": "Definitions_1",
        "targetNamespace": "http://bpmn.io/schema/bpmn", }

    for k, v in header_dict.items():
        root.set(k, v)

    return root
