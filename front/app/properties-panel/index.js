import ReactDOM from 'react-dom';
import React from 'react';

import PropertiesView from './PropertiesView';


export default class PropertiesPanel {

  constructor(options) {

    const {
      modeler,
      container,
      original_record,
    } = options;

    //console.log(original_record)

    ReactDOM.render(
      <PropertiesView modeler={modeler} />,
      container
    );
  }
}


