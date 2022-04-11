import React from "react";
import Autosuggest from 'react-autosuggest';
import { host_ip } from "../../../network/api";
export let inputtedText = ""


const languages = [
    {
        name: 'C',
    },
    {
        name: 'C#',
    },
];

//let languages = []

const escapeRegexCharacters = str => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const getSuggestions = value => {
    const escapedValue = escapeRegexCharacters(value.trim());

    if (escapedValue === '') {
        return [];
    }


    //regex type seach
    const regex = new RegExp('^' + escapedValue, 'i');
    let suggestions = languages.filter(language => regex.test(language.name));

    // include-type search
    const suggestions2 = languages.filter(language => language.name.includes(escapedValue));
    suggestions = suggestions.concat(suggestions2)
    console.log(suggestions)

    if (suggestions.length === 0) {
        return [
            { isAddNew: true }
        ];
    }

    return suggestions;
}

class Suggest extends React.Component {
    constructor() {
        super();

        this.state = {
            value: '',
            suggestions: [],
            title: "",
        };

        this.onChange = this.onChange.bind(this)
        this.onSuggestionsFetchRequested = this.onSuggestionsFetchRequested.bind(this)
        this.renderSuggestion = this.renderSuggestion.bind(this)
    }

    onChange(event, { newValue, method }) {
        this.setState({
            value: newValue
        });
        inputtedText = newValue
    };

    getSuggestionValue(suggestion) {
        if (suggestion.isAddNew) {
            return this.state.value;
        }
        return suggestion.name;
    };

    renderSuggestion(suggestion) {
        if (suggestion.isAddNew) {
            return (
                <span>
                    [+] Add new: <strong>{this.state.value}</strong>
                </span>
            );
        }

        return suggestion.name;
    };

    onSuggestionsFetchRequested({ value }) {
        //console.log(languages)
        this.setState({
            suggestions: getSuggestions(value)
        });
    };

    onSuggestionsClearRequested() {
        this.setState({
            suggestions: []
        });
    };

    onSuggestionSelected(event, { suggestion }) {
        if (suggestion.isAddNew) {
            //console.log('Add new:', this.state.value);
        }
    };

    handleKeyDown(e) {
        if (e.key === 'Enter') {
            //    this.clearInputField()
        }
    };

    clearInputField() {
        this.setState({ value: "" })
        inputtedText = ""
        //console.log("clearinput")
        //console.log(this.state.value)
    }

    // fetch line data 
    componentDidMount() {

        fetch(host_ip + "graph/dump-lines")
            .then(res => res.json())
            .then(json => {
                //console.log(json);
                this.setState({
                    //isLoaded: true,
                    items: json
                });
            });

    }

    render() {
        //var { items, isLoaded } = this.state;
        var { items } = this.state;
        //console.log("render:",items);
        //languages = items

        const { value, suggestions } = this.state;
        const inputProps = {
            placeholder: "Input values to be added. Then double click a target node",
            value,
            onChange: this.onChange,
            onKeyDown: this.handleKeyDown
        };

        return (
            <>
                <br></br>
                <br></br>
                <br></br>
                <br></br>
                <Autosuggest
                    suggestions={suggestions}
                    onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
                    onSuggestionsClearRequested={this.onSuggestionsClearRequested}
                    getSuggestionValue={this.getSuggestionValue}
                    renderSuggestion={this.renderSuggestion}
                    onSuggestionSelected={this.onSuggestionSelected}
                    inputProps={inputProps}
                />
            </>
        );
    }
}
export default Suggest
export { Suggest }