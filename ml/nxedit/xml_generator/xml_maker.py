
from xml.etree.ElementTree import Element, SubElement, ElementTree


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
