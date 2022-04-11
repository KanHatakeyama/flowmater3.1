import React, { Component } from 'react';
import './PropertiesView.css';
import { updateGraph, newGraph } from '../network/api';
import { CustomTags } from './fields/CustomTags';
import { FileForm } from './fields/DropZone';
import { ElementProperties } from './fields/ElementProperties';
import Menu from './fields/Menu/Menu';

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
      newGraph({ "graph": xml, "title": currentGraph.title, "tags": currentGraph.tags })
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
        {
          selectedElements.length === 1
          && <ElementProperties modeler={modeler} element={element} />
        }

        {
          selectedElements.length === 0
          && <span>

            <Menu right width={250} />
            <div style={{ whiteSpace: "nowrap" }}>
              <p style={{ display: "inline-flex", whiteSpace: "nowrap", padding: "3px 30px" }}>
                <h5>Title: {currentGraph.pk}_</h5>
                <input type="title" value={this.state.title} onChange={this.handleTitleChange} style={{ width: "30%" }} />
                <h5 style={{ padding: "0px 10px" }}>Tags: </h5><CustomTags></CustomTags>
                <button onClick={this.saveNewData} modeler={modeler}>Save as New</button>
              </p>
              <FileForm></FileForm>
            </div>


          </span>
        }

        {
          selectedElements.length > 1
          && <span>Please select a single element.</span>
        }


      </div>

    );
  }

}
