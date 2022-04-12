
import React from 'react';
import { is } from 'bpmn-js/lib/util/ModelUtil';
//import Suggest from './Suggest/Suggest';
export let textData = {}

export function ElementProperties(props) {

    let {
        element,
        modeler
    } = props;

    if (element.labelTarget) {
        element = element.labelTarget;
    }

    textData.content = element.businessObject.name

    function updateName(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        textData.content = name
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
                    onChange={(event) => { updateName(event.target.value) }}
                    onKeyDown={(e) => { textData.cursor = e.target.selectionStart }}
                    onClick={(e) => { textData.cursor = e.target.selectionStart }}
                />

            </fieldset>

            <button onClick={addSuggestion}>{textData.content + String(textData.cursor)}</button>

        </div>
    );
}

