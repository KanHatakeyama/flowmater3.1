export function renderOverlays(children, overlays) {

    for (var i in children) {
        let node = children[i]
        let nodeID = node.id
        let content = node.businessObject.name
        console.log(nodeID, content)
        parseText(nodeID, content, overlays)
    }


}


function parseText(nodeID, content, overlays) {
    // attach an overlay to a node

    if (content === "start") {
        overlays.add(nodeID, {
            position: {
                top: 0,
                right: -50
            },
            //   html: '<div>Mixed up the labels?</div>'
            html: '<img class="fit-picture" src="https://cdn-bst.freetls.fastly.net/prod-gixo/assets/img/header/head_logo.png">'
        });
    }

}