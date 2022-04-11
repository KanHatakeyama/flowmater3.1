
import React from 'react';
import { is } from 'bpmn-js/lib/util/ModelUtil';

export function ElementProperties(props) {

    let {
        element,
        modeler
    } = props;

    if (element.labelTarget) {
        element = element.labelTarget;
    }

    function updateName(name) {
        const modeling = modeler.get('modeling');

        modeling.updateLabel(element, name);


    }

    function updateTopic(topic) {
        const modeling = modeler.get('modeling');

        modeling.updateProperties(element, {
            'custom:topic': topic
        });
    }

    function makeMessageEvent() {

        const bpmnReplace = modeler.get('bpmnReplace');

        bpmnReplace.replaceElement(element, {
            type: element.businessObject.$type,
            eventDefinitionType: 'bpmn:MessageEventDefinition'
        });
    }

    function makeServiceTask(name) {
        const bpmnReplace = modeler.get('bpmnReplace');

        bpmnReplace.replaceElement(element, {
            type: 'bpmn:ServiceTask'
        });
    }



    function attachTimeout() {
        const modeling = modeler.get('modeling');
        const autoPlace = modeler.get('autoPlace');
        const selection = modeler.get('selection');

        const attrs = {
            type: 'bpmn:BoundaryEvent',
            eventDefinitionType: 'bpmn:TimerEventDefinition'
        };

        const position = {
            x: element.x + element.width,
            y: element.y + element.height
        };

        const boundaryEvent = modeling.createShape(attrs, position, element, { attach: true });

        const taskShape = append(boundaryEvent, {
            type: 'bpmn:Task'
        });

        selection.select(taskShape);
    }

    function isTimeoutConfigured(element) {
        const attachers = element.attachers || [];

        return attachers.some(e => hasDefinition(e, 'bpmn:TimerEventDefinition'));
    }

    function append(element, attrs) {

        const autoPlace = modeler.get('autoPlace');
        const elementFactory = modeler.get('elementFactory');

        var shape = elementFactory.createShape(attrs);

        return autoPlace.append(element, shape);
    };

    return (
        <div className="element-properties" key={element.id}>

            <fieldset>
                <label>name</label>
                <textarea value={element.businessObject.name || ''} onChange={(event) => {
                    updateName(event.target.value)
                }} />
            </fieldset>

            <fieldset>
                <label>actions</label>
                {
                    is(element, 'bpmn:Task') && !is(element, 'bpmn:ServiceTask') &&
                    <button onClick={makeServiceTask}>Make Service Task</button>
                }

                {
                    is(element, 'bpmn:Event') && !hasDefinition(element, 'bpmn:MessageEventDefinition') &&
                    <button onClick={makeMessageEvent}>Make Message Event</button>
                }

                {
                    is(element, 'bpmn:Task') && !isTimeoutConfigured(element) &&
                    <button onClick={attachTimeout}>Attach Timeout</button>
                }
            </fieldset>
        </div>
    );
}


// helpers ///////////////////

function hasDefinition(event, definitionType) {

    const definitions = event.businessObject.eventDefinitions || [];

    return definitions.some(d => is(d, definitionType));
}