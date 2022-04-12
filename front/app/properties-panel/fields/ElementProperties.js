
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getCurrentLineNumber, getCurrentLineText } from './ButtonSuggest/TextParse';

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
        cursor,
        currentLineText,
        currentLineNumber,
    } = props;

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
        currentLineNumber = (getCurrentLineNumber(content, cursor))
        currentLineText = (getCurrentLineText(content, cursor))
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
                    onChange={(event) => { updateField(event.target.value) }}
                    onKeyDown={(e) => { cursor = e.target.selectionStart }}
                    onClick={(e) => { cursor = e.target.selectionStart }}
                />

            </fieldset>

            <button onClick={addSuggestion}>{content + currentLineText}</button>

        </div>
    );
}

