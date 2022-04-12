
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getCurrentLineNumber, getCurrentLineText } from './ButtonSuggest/TextParse';
import { useState, setState } from 'react';
import { host_ip } from "../../network/api"

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
    } = props;


    const [cursor, setCursor] = useState(0)
    const [currentLineText, setCurrentLineText] = useState("")
    const [currentLineNumber, setcurrentLineNumber] = useState(0)
    //const [replaceText, setReplaceText] = useState("")
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

        fetch(host_ip + "graph/dump-lines")
            .then(res => res.json())
            .then(json => {
                setSuggestions(json)
            });

    }

    function updateCurrentLineInfo() {
        setcurrentLineNumber(getCurrentLineNumber(content, cursor))
        setCurrentLineText(getCurrentLineText(content, cursor))
    }

    function addSuggestion(replaceText) {
        let textLines = content.split("\n")
        textLines[currentLineNumber - 1] = replaceText
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
                //  list.push(<li>{suggestions[i].name}</li>);
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
                        setCursor(e.target.selectionStart)
                        updateCurrentLineInfo()
                    }}
                    onClick={(e) => {
                        setCursor(e.target.selectionStart)
                        updateCurrentLineInfo()
                    }}
                />
            </fieldset>
            <SuggestButtons />
        </div>
    );
}

