
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getLineData } from './ButtonSuggest/TextParse';
import { useState } from 'react';
import { host_ip } from "../../network/api"

let currentTextField = {}

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
    } = props;


    //const [cursor, setCursor] = useState(0)
    //const [currentLineText, setCurrentLineText] = useState("")
    //const [upperLineText, setUpperlineText] = useState("")
    //const [currentLineNumber, setcurrentLineNumber] = useState(0)
    const [suggestions, setSuggestions] = useState({})



    if (element.labelTarget) {
        element = element.labelTarget;
    }

    content = element.businessObject.name

    function updateField(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        content = name
        updateCurrentLineInfo()

        fetch(host_ip + "graph/dump-lines?cl=" + currentTextField.text + "&ul=" + currentTextField.upperText)
            .then(res => res.json())
            .then(json => {
                setSuggestions(json)
            });

    }

    function updateCurrentLineInfo() {
        currentTextField = getLineData(content, currentTextField.cursor)
        console.log(currentTextField)

    }

    function addSuggestion(replaceText) {
        let textLines = content.split("\n")
        textLines[currentTextField.line - 1] = replaceText
        const newContent = textLines.join("\n")
        element.businessObject.name = newContent
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, element.businessObject.name);
    }

    // Suggestion components
    class SuggestButtons extends React.Component {
        // download suggestion data

        render() {

            let target = ""
            if (suggestions.length > 0) {
                target = suggestions[0].name
            }

            let list = [];
            for (var i in suggestions) {
                list.push(<SuggestButton value={suggestions[i].name} />)
            }

            return (
                <>
                    {list}
                </>

            )
        }
    }

    class SuggestButton extends React.Component {
        render() {
            return (
                <button onClick={(e) => {
                    addSuggestion(this.props.value)
                }
                }> {this.props.value}</button >
            )
        }
    }


    return (
        <div className="element-properties" key={element.id}>

            <fieldset>
                <textarea value={element.businessObject.name || ''}
                    onChange={(e) => { updateField(e.target.value) }}
                    onKeyDown={(e) => {
                        currentTextField.cursor = e.target.selectionStart
                        updateCurrentLineInfo()
                    }}
                    onClick={(e) => {
                        currentTextField.cursor = e.target.selectionStart
                        updateCurrentLineInfo()
                    }}
                />
            </fieldset>
            <SuggestButtons />
        </div>
    );
}

