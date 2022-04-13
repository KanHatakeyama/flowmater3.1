export function getCurrentLineNumber(content, cursor) {
    let currentLine = 1
    let curretPos = 1

    while (true) {
        let targetPos = content.indexOf("\n", curretPos)
        if (cursor <= targetPos || targetPos == -1) {
            return currentLine
        }

        currentLine += 1

        curretPos += targetPos

        // for safety (avoid infinite loop by bug)
        if (currentLine > 10) {
            return -1
        }

    }
}

export function getCurrentLineText(content, cursor) {
    const currentLine = getCurrentLineNumber(content, cursor)
    const lines = content.split("\n")
    return lines[currentLine - 1]

}

export function getLineData(content, cursor) {
    const currentLine = getCurrentLineNumber(content, cursor)
    const lines = content.split("\n")
    const currentText = lines[currentLine - 1]

    let upperText = ""
    if (currentLine >= 2) {
        upperText = lines[currentLine - 2]
    }

    return {
        "cursor": cursor,
        "line": currentLine,
        "text": currentText,
        "upperText": upperText
    }



}