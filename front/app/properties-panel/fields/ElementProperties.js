
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getCurrentLineNumber, getCurrentLineText } from './ButtonSuggest/TextParse';
import { useState } from 'react';

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
    } = props;


    const [cursor, setCursor] = useState(0)
    const [currentLineText, setCurrentLineText] = useState("")
    const [currentLineNumber, setcurrentLineNumber] = useState(0)



    if (element.labelTarget) {
        element = element.labelTarget;
    }

    content = element.businessObject.name

    function updateField(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        content = name
        updateCurrentLineInfo()
    }

    function updateCurrentLineInfo() {
        setcurrentLineNumber(getCurrentLineNumber(content, cursor))
        setCurrentLineText(getCurrentLineText(content, cursor))
    }

    function addSuggestion() {
        element.businessObject.name = "aa"
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, element.businessObject.name);
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

            <button onClick={addSuggestion}>{currentLineText}</button>
        </div>
    );
}

