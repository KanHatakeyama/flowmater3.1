import { is } from 'bpmn-js/lib/util/ModelUtil';
import React, { Component } from 'react';
import './PropertiesView.css';
import { updateGraph, newGraph } from '../network/api';
import { CustomTags } from './fields/CustomTags';
import { FileForm } from './fields/DropZone';

export let currentGraph = {}

export default class PropertiesView extends Component {

  constructor(props) {
    super(props);

    // funcs
    this.saveData = this.saveData.bind(this);
    this.saveNewData = this.saveNewData.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);

    this.state = {
      selectedElements: [],
      element: null,
      title: this.props.original_record.title,
    };


    currentGraph = {
      "title": this.props.original_record.title,
      "graph": this.props.original_record.graph,
      "pk": this.props.original_record.pk,
      "tags": this.props.original_record.tags.split(","),    // split string with comma
    }
  }
  //---------- exporting funcs------------------
  saveData() {
    const {
      modeler, original_record
    } = this.props;

    modeler.saveXML({ format: true }, function (err, xml) {
      updateGraph(original_record.pk, { "graph": xml })
    });
  }
  saveNewData() {
    const {
      modeler, original_record
    } = this.props;

    modeler.saveXML({ format: true }, function (err, xml) {
      // TODO, save other data (e.g., title)
      newGraph({ "graph": xml })
      window.alert("saved as a new graph");
    });
  }

  // ------- title editing ----------
  //save title change
  handleTitleChange(event) {
    currentGraph.title = event.target.value
    this.setState({ title: currentGraph.title });
    updateGraph(currentGraph.pk, { "title": currentGraph.title })
  };


  componentDidMount() {
    const {
      modeler
    } = this.props;

    //---------- diagram editing-----
    modeler.on('selection.changed', (e) => {

      const {
        element
      } = this.state;

      this.setState({
        selectedElements: e.newSelection,
        element: e.newSelection[0]
      });
      this.saveData()
    });


    modeler.on('element.changed', (e) => {

      const {
        element
      } = e;

      const {
        element: currentElement
      } = this.state;

      if (!currentElement) {
        return;
      }

      // update panel, if currently selected element changed
      if (element.id === currentElement.id) {
        this.setState({
          element
        });
      }

      this.saveData()
      //console.log("saved")

    });
  }

  // --------- rendering-------------
  render() {

    const {
      modeler
    } = this.props;

    const {
      selectedElements,
      element
    } = this.state;

    return (
      //Rendering
      <div>
        <div>
          <h5>Title: {currentGraph.pk}_</h5>
          <input type="title" value={this.state.title} onChange={this.handleTitleChange} style={{ width: "30%" }} />
          <h5 style={{ padding: "0px 10px" }}>Tags: </h5><CustomTags></CustomTags>
        </div>

        <div>
          <button onClick={this.saveNewData} modeler={modeler}>Save as New</button>
        </div>
        {
          selectedElements.length === 1
          && <ElementProperties modeler={modeler} element={element} />
        }

        {
          selectedElements.length === 0
          && <span>Please select an element.</span>
        }

        {
          selectedElements.length > 1
          && <span>Please select a single element.</span>
        }

        <div>
          <FileForm></FileForm>
        </div>
      </div>

    );
  }

}


function ElementProperties(props) {

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
        <input value={element.businessObject.name || ''} onChange={(event) => {
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