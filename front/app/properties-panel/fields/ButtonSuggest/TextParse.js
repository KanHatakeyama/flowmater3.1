export function getCurrentLineNumber(content, cursor) {
    let str = content.substring(0, cursor) + "a";
    let lines = str.split("\n");
    return lines.length


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
        "upperText": upperText,
        "content": content,
    }



}