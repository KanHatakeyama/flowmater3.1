
import React from 'react';
//import Suggest from './Suggest/Suggest';
import { getLineData } from './ButtonSuggest/TextParse';
import { host_ip } from "../../network/api"
let currentTextField = { content: "*", text: "*", upperText: "" }
let oldTextField = {}
let suggest = {}

export function ElementProperties(props) {

    let {
        element,
        modeler,
        content,
    } = props;



    if (element.labelTarget) {
        element = element.labelTarget;
    }

    content = element.businessObject.name

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
            //fetch suggestion data every 1000 ms
            this.intervalId = setInterval(() => {
                //console.log("aa")
                this.setState({
                    suggest: suggest
                });
            }, 1000);
        }
        componentWillUnmount() {
            clearInterval(this.intervalId);
        }

        render() {

            let list = [];
            for (var i in suggest) {
                list.push(<SuggestButton value={suggest[i].name} />)
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
                <button onClick={(e) => {
                    addSuggestion(this.props.value)
                }
                }> {this.props.value}</button >
            )
        }
    }

    const intervalMs = 1000;

    React.useEffect(() => {

        const intervalId = setInterval(() => {
            fetchSuggestions();
        }, intervalMs);
        return () => {
            clearInterval(intervalId)
        };

    }, []);



    return (
        <div className="element-properties" key={element.id}>

            <fieldset>
                <textarea value={element.businessObject.name || ''} id="textarea"
                    onChange={(e) => {
                        updateField(e.target.value)
                        //fetchSuggestions()
                    }}

                />
            </fieldset>
            <SuggestButtons />
        </div>
    );
}

