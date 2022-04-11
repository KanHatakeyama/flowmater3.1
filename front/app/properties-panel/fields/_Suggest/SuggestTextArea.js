import React from "react";
import ReactTextareaAutocomplete from "@webscopeio/react-textarea-autocomplete";

import "@webscopeio/react-textarea-autocomplete/style.css";

const Item = ({ entity: { name, char } }) => <div>{`${name}: ${char}`}</div>;
const Loading = ({ data }) => <div>Loading</div>;

export const SuggestTextArea = () => (
    <div>
        <ReactTextareaAutocomplete
            className="my-textarea"
            loadingComponent={Loading}
            style={{
                fontSize: "15px",
                lineHeight: "20px",
                padding: 5
            }}
            containerStyle={{
                marginTop: 20,
                width: 400,
                height: 100,
                margin: "20px auto"
            }}
            minChar={0}
            trigger={{
                ":": {
                    dataProvider: token => {
                        return [
                            { name: "smile", char: "🙂" },
                            { name: "heart", char: "❤️" }
                        ];
                    },
                    component: Item,
                    output: (item, trigger) => item.char
                }
            }}
        />
    </div>
);

