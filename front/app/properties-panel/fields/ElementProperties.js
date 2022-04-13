
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getLineData } from './ButtonSuggest/TextParse';
import { useState } from 'react';
import { host_ip } from "../../network/api"

let currentTextField = {}
let suggest = {}

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
    } = props;



    if (element.labelTarget) {
        element = element.labelTarget;
    }

    content = element.businessObject.name

    function updateField(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        content = name
        currentTextField.content = name
    }

    function updateCurrentLineInfo() {
        currentTextField = getLineData(currentTextField.content, currentTextField.cursor)
        //console.log(currentTextField)
        fetch(host_ip + "graph/dump-lines?cl=" + currentTextField.text + "&ul=" + currentTextField.upperText)
            .then(res => res.json())
            .then(json => {
                suggest = json
            });
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

        render() {

            let target = ""
            if (suggest.length > 0) {
                target = suggest[0].name
            }

            let list = [];
            for (var i in suggest) {
                list.push(<SuggestButton value={suggest[i].name} />)
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
                    onChange={(e) => {
                        updateField(e.target.value)
                        updateCurrentLineInfo()
                    }}
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

