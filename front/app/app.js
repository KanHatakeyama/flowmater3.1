
import Modeler from 'bpmn-js/lib/Modeler';
import PropertiesPanel from './properties-panel';
import customModdleExtension from './moddle/custom.json';
import { getTargetGraph } from './network/api';
import { AuthForm } from './properties-panel/auth';
import BpmnColorPickerModule from 'bpmn-js-color-picker';

const $modelerContainer = document.querySelector('#modeler-container');
const $propertiesContainer = document.querySelector('#properties-container');

const modeler = new Modeler({
  container: $modelerContainer,
  moddleExtensions: {
    custom: customModdleExtension
  },
  keyboard: {
    bindTo: document.body
  },
  additionalModules: [
    BpmnColorPickerModule
  ]
});



// load json data of the record and launch editor
getTargetGraph().then((original_record) => {
  const propertiesPanel = new PropertiesPanel({
    container: $propertiesContainer,
    modeler,
    original_record
  });

  const diagramXML = original_record.graph
  modeler.importXML(diagramXML);
}).catch(err => {
  AuthForm()
}
)


