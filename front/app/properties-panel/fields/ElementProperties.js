
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getLineData } from './ButtonSuggest/TextParse';
import { host_ip } from "../../network/api"
let currentTextField = { content: "*", text: "*", upperText: "" }
let oldTextField = {}
let suggest = {}
import { renderOverlays } from './Overlays/parseGraphNodes';
import "./ButtonSuggest/suggest.css"
// interval (ms) to check inputted data and fetch suggestions from server
const suggestFetchIntervalMs = 100;

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
        rootElement,
        canvas,
        overlays,
    } = props;



    if (element.labelTarget) {
        element = element.labelTarget;
    }


    content = String(element.businessObject.name)

    // apply textarea change to graph object
    function updateField(name) {
        const modeling = modeler.get('modeling');
        modeling.updateLabel(element, name);
        content = name
        currentTextField.content = name
    }


    //get suggestion data from server
    function fetchSuggestions() {
        //check for update fields
        var target = document.getElementById('textarea');
        currentTextField.cursor = target.selectionStart
        currentTextField.content = target.value
        currentTextField = getLineData(currentTextField.content, currentTextField.cursor)

        if ((currentTextField.content !== oldTextField.content) ||
            (currentTextField.line !== oldTextField.line)) {

            Object.assign(oldTextField, JSON.parse(JSON.stringify(currentTextField)));

            fetch(host_ip + "graph/dump-lines?cl=" + currentTextField.text + "&ul=" + currentTextField.upperText)
                .then(res => res.json())
                .then(json => {
                    suggest = json
                });
        }
    }

    // apply suggestions to the graph object
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

        constructor(props) {
            super(props);
            this.state = {
                suggest: {}
            };
        }

        componentDidMount() {
            //check change of suggestion data at every 100 ms
            this.intervalId = setInterval(() => {
                // if suggestion has changed, change this.state (this induces re-rendering of buttons. this.state.suggest itself is not necessary)
                if (JSON.stringify(suggest) !== JSON.stringify(this.state.suggest)) {
                    this.setState({
                        suggest: suggest
                    });
                }
            }, 100);



        }
        componentWillUnmount() {
            clearInterval(this.intervalId);
        }

        render() {
            let list = [];
            for (var i in suggest) {
                if ((suggest[i].name !== "") && (suggest[i].name != currentTextField.text)) {
                    list.push(<SuggestButton value={suggest[i].name} />)
                }
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
                <button className="suggestButton" onClick={(e) => {
                    addSuggestion(this.props.value)
                }
                }> {this.props.value}</button >
            )
        }
    }


    //periorically check cursor position etc and fetch suggestions from server
    React.useEffect(() => {
        const intervalId = setInterval(() => {
            fetchSuggestions();
        }, suggestFetchIntervalMs);
        return () => {
            clearInterval(intervalId)
        };
    }, []);

    canvas = modeler.get('canvas');
    rootElement = canvas.getRootElement();
    overlays = modeler.get('overlays');
    renderOverlays(rootElement.children, overlays)

    // main rendering
    return (
        <div className="element-properties" key={element.id}>

            <fieldset>
                <textarea value={element.businessObject.name || ''} id="textarea"
                    onChange={(e) => {
                        updateField(e.target.value)
                    }}

                />
            </fieldset>
            <SuggestButtons />
        </div>
    );
}

