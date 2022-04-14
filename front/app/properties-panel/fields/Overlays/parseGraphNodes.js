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
                right: -10
            },
            //   html: '<div>Mixed up the labels?</div>'
            html: '<img class="fit-picture" src="https://bst-image.imgix.net/prod-gixo/content/uploads/2020/12/test.png?auto=compress%2Cformat&fit=scale&h=881&ixlib=php-3.3.0&w=1536&wpsize=1536x1536">'
        });
    }

}