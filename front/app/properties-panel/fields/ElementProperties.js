
import React from 'react';
//import Suggest from './Suggest/Suggest';

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
        cursor,
    } = props;

    if (element.labelTarget) {
        element = element.labelTarget;
    }

    content = element.businessObject.name

    function updateField(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        content = name

        console.log(content, cursor)
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

            <button onClick={addSuggestion}>{content + String(cursor)}</button>

        </div>
    );
}

