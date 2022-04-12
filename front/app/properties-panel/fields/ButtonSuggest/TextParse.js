export function getCurrentLineNumber(content, cursor) {
    let currentLine = 1
    let curretPos = 1

    while (true) {
        let targetPos = content.indexOf("\n", curretPos)
        if (cursor <= targetPos - 1 || targetPos == -1) {
            return currentLine
        }

        currentLine += 1

        curretPos += targetPos

        // for safety
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