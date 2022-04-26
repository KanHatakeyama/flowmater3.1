import { parseLine } from "./tagGenerator"

export function renderOverlays(children, overlays) {
    //console.log(overlays)
    //overlays.clear();
    for (var i in children) {
        let node = children[i]
        let nodeID = node.id
        let content = String(node.businessObject.name)

        parseText(nodeID, content, overlays)
    }


}


function parseText(nodeID, content, overlays) {
    let tag = ""
    // attach an overlay to a node
    var split_text = (content.split("\n"))
    for (var i in split_text) {
        var line = split_text[i]
        tag += (parseLine(line))
    }


    if (tag !== "") {
        overlays.add(nodeID, {
            position: {
                bottom: 0,
                left: 0
            },
            html: String(tag),
            type: "manual"
        });
    }

}