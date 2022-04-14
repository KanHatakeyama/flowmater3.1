import { parseLine } from "./tagGenerator"

export function renderOverlays(children, overlays) {
    overlays.clear();
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

    // if (content.indexOf("load") >= 0) {
    // }



    //if (content === "start") {
    if (tag !== "") {
        overlays.add(nodeID, {
            position: {
                bottom: 0,
                left: 0
            },
            //   html: '<div>Mixed up the labels?</div>'
            //html: '<img class="fit-picture" src="https://cdn-bst.freetls.fastly.net/prod-gixo/assets/img/header/head_logo.png">'
            html: String(tag)
        });
    }

}